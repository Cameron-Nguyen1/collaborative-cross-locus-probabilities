import requests, re
from bs4 import BeautifulSoup

def assemble_cc_locus_report(dicto,entries,cc,tag):
    legend={1:'A/J', 2:'C57BL/6J', 3:'129S1/SvlmJ', 4:'NOD/ShiLtJ', 
        5:'NZO/HILtJ', 6:'CAST/EiJ', 7:'PWK/PhJ', 8:'WSB/EiJ'}
    legend2={
        'AB': 'A/J+C57BL/6J', 'AC': 'A/J+129S1/SvlmJ', 'AD': 'A/J+NOD/ShiLtJ', 
        'AE': 'A/J+NZO/HILtJ', 'AF': 'A/J+CAST/EiJ', 'AG': 'A/J+PWK/PhJ', 
        'AH': 'A/J+WSB/EiJ', 'BC': 'C57BL/6J+129S1/SvlmJ', 'BD': 'C57BL/6J+NOD/ShiLtJ', 
        'BE': 'C57BL/6J+NZO/HILtJ', 'BF': 'C57BL/6J+CAST/EiJ', 'BG': 'C57BL/6J+PWK/PhJ', 
        'BH': 'C57BL/6J+WSB/EiJ', 'CD': '129S1/SvlmJ+NOD/ShiLtJ', 'CE': '129S1/SvlmJ+NZO/HILtJ', 
        'CF': '129S1/SvlmJ+CAST/EiJ', 'CG': '129S1/SvlmJ+PWK/PhJ', 'CH': '129S1/SvlmJ+WSB/EiJ', 
        'DE': 'NOD/ShiLtJ+NZO/HILtJ', 'DF': 'NOD/ShiLtJ+CAST/EiJ', 'DG': 'NOD/ShiLtJ+PWK/PhJ', 
        'DH': 'NOD/ShiLtJ+WSB/EiJ', 'EF': 'NZO/HILtJ+CAST/EiJ', 'EG': 'NZO/HILtJ+PWK/PhJ', 
        'EH': 'NZO/HILtJ+WSB/EiJ', 'FG': 'CAST/EiJ+PWK/PhJ', 'FH': 'CAST/EiJ+WSB/EiJ', 
        'GH': 'PWK/PhJ+WSB/EiJ'
    }
    dicto_s = {}
    myl = []
    col = 0
    for value in entries:
        col += 1
        if col < 9:
            if value.text == "" or value.text == " 0.00" or value == None:
                continue
            else:
                value = value.text.strip()
                myl.append(f'{legend[col]}|{value}')
                continue
        else:
            if not "background-image" in str(value):
                continue
            else:
                sk = re.search("bkgnd([A-Za-z]{2})\.png",str(value))
                if sk.group(1)[0] == sk.group(1)[1]:
                    continue
                myl.append(f'{legend2[sk.group(1)]}|{value.text}')
    if tag in dicto_s.keys():
        dicto_s[tag].extend(myl)
    else:
        dicto_s[tag] = myl
    if cc in dicto.keys():
        dicto[cc].update(dicto_s)
    else:
        dicto[cc] = dicto_s
    return(dicto)

def submit_search(gid):
    url = "https://csbio.unc.edu/CCstatus/index.py?run=locus"
    payload = {"build":"b38","region":str(gid),"submit":"Submit","target":"locus.process"}
    response = requests.post(url,payload)
    soup = BeautifulSoup(response.text)
    tables_l1 = soup.find_all('table')
    tables_l2 = tables_l1[2].find_all('tr')
    dicto = {}
    init = 0
    for row in tables_l2:
        init+=1
        if init < 3 or len(row) < 2:
            continue
        if row.find_all('td',{'align':'left'}):
            meta = row.find_all('td',{'align':'left'}) #Two items
            cc,tag = meta[0].text, meta[1].text #CC + Tag
        else:
            hold = row.find_all('td',{'align':'right', 'colspan':'2'}) #Next tag
            tag = re.search('colspan="2">([\S]+)<\\/td>',str(hold)).group(1)
        entries = row.find_all('td',{'align':'right','width':'36px'}) #Table Cell Values
        dicto = assemble_cc_locus_report(dicto,entries,cc,tag)
    return(dicto)

def write_report(dicto,csv):
    legend = {'A/J': 1,'C57BL/6J': 2,'129S1/SvlmJ': 3,'NOD/ShiLtJ': 4,'NZO/HILtJ': 5,'CAST/EiJ': 6,'PWK/PhJ': 7,'WSB/EiJ': 8}
    sents = []
    sents.append(f'Strain,Old-ID,{",".join([strain for strain in legend.keys()])},Hetero_Combination')
    for k,v in dicto.items():
        for k2,v2 in v.items():
            if v2 == []:
                series = [0]*8
                sents.append(f'{k},{k2},{",".join(map(str,series))}')
                continue
            het = any("+" in ele for ele in v2)
            if het == True and len(v2) == 1:
                het_s = [ele for ele in v2 if "+" in ele]
                series = [0]*8
                sents.append(f'{k},{k2},{",".join(map(str,series))},{",".join(het_s)}')
                continue
            elif het == True and len(v2) > 1:
                het_s = [ele for ele in v2 if "+" in ele]
                nhet_list = [ele for ele in v2 if not "+" in ele]
                series = [0]*8
                for v3 in nhet_list:
                    ind = legend[v3.split("|")[0]]-1
                    series[ind] = v3.split("|")[1]
                sents.append(f'{k},{k2},{",".join(map(str,series))},{"~".join(het_s)}')
                continue
            else:
                het_s = ""
            if len(v2) > 1:
                v_list = []
                series = [0]*8
                for v3 in v2:
                    ind = legend[v3.split("|")[0]]-1
                    series[ind] = v3.split("|")[1]
                sents.append(f'{k},{k2},{",".join(map(str,series))},{",".join(het_s)}')
                continue
            else:  
                series = [0]*8
                ind = v2[0].split("|")[0]
                series[(legend[ind])-1] = v2[0].split("|")[1]
                sents.append(f'{k},{k2},{",".join(map(str,series))},{",".join(het_s)}')
                continue
    #with open(csv,'w') as hout:
    #    for line in sents:
    #        hout.write(line+"\n")
    return(sents)

def fetch_aa_seqs(gene_symbol,strain):
    base_url = "https://rest.ensembl.org"
    endpoint = "/sequence/id/"
    headers = {"Content-Type": "application/json"}
    #gene_symbol = "Ybx1"
    #strain = "WSB/EiJ"
    species = "mus_musculus"
    ens_legend = {
        'A/J': 'mus_musculus_aj', 'C57BL/6J': 'mus_musculus_c57bl6nj', '129S1/SvlmJ': 'mus_musculus_129s1svimj', 
        'NOD/ShiLtJ': 'mus_musculus_nodshiltj', 'NZO/HILtJ': 'mus_musculus_nzohlltj', 'CAST/EiJ': 'mus_musculus_casteij', 
        'PWK/PhJ': 'mus_musculus_pwkphj', 'WSB/EiJ': 'mus_musculus_wsbeij'
        }
    species = ens_legend[strain]
    lookup_url = f"{base_url}/xrefs/symbol/{species}/{gene_symbol}?"
    response = requests.get(lookup_url, headers=headers)
    
    if response.ok:
        gene_info = response.json()
        if gene_info:
            ensembl_gene_id = gene_info[0]['id']
            
            sequence_url = f"{base_url}{endpoint}{ensembl_gene_id}?type=protein;multiple_sequences=True"
            sequence_response = requests.get(sequence_url, headers=headers)
            
            if sequence_response.ok:
                sequence_data = sequence_response.json()
                protein_sequence = sequence_data[0]['seq']
                return(protein_sequence)
            else:
                print("Error retrieving protein sequence.")
        else:
            print("Gene symbol not found.")
    else:
        print("Error retrieving gene information.")
        
def generate_modular_html_table(data):
    modular_html = "<table border='1'>\n"
    # Add header row
    modular_html += "  <tr>\n"
    for header in data[0].split(","):
        modular_html += f"    <th>{header}</th>\n"
    modular_html += "  </tr>\n"
    
    # Add data rows
    for row in data[1:]:
        row = row.split(",")
        modular_html += "  <tr>\n"
        for cell in row:
            modular_html += f"    <td>{cell}</td>\n"
        modular_html += "  </tr>\n"
    
    modular_html += "</table>\n"
    return modular_html
    
def generate_csv_download_button(data,gid):
    csv_content = "\n".join(data)
    
    button_html = f"""
    <button onclick="downloadCSV()">Download CSV</button>
    <script>
    function downloadCSV() {{
        var csvContent = `{csv_content}`;
        var blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
        var link = document.createElement("a");
        if (link.download !== undefined) {{
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", "{gid}_CC_Probabilities.csv");
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }}
    }}
    </script>
    """
    
    return button_html

def generate_fasta_download_button(txt_content,gid):    
    button_html = f"""
    <button onclick="downloadTXT()">Download FASTA</button>
    <script>
    function downloadTXT() {{
        var txtContent = `{txt_content}`;
        var blob = new Blob([txtContent], {{ type: 'text/plain;charset=utf-8;' }});
        var link = document.createElement("a");
        if (link.download !== undefined) {{
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", "{gid}.fasta");
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }}
    }}
    </script>
    """
    
    return button_html