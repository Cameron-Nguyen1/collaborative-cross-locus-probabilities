import requests, re, base64, logging
from requests_toolbelt import MultipartDecoder
from bs4 import BeautifulSoup
import cc_locus_search_lib as cc

logger = logging.getLogger()
logger.setLevel("INFO")

with open("cc_locus_search_DHTML.html",'r') as handle:
    html = handle.read()
    
def get_key(form_data):
    key = form_data.split(";")[1].split("=")[1].replace('"', '')
    return(key)

def lambda_handler(event, context):
    flag = 0
    try:
        z = event["requestContext"]["http"]["method"]
        flag = 1
    except:
        print("Event is irregular")
    finally:
        if flag == 1:
            if z == "POST":
                headers = event['headers']
                # decode the multipart/form-data request
                postdata = base64.b64decode(event['body'])
                request = {} # Save request here
                for part in MultipartDecoder(postdata, headers['content-type']).parts:
                    decoded_header = part.headers[b'Content-Disposition'].decode('utf-8')
                    key = get_key(decoded_header)
                    request[key] = part.content
                for k,v in request.items():
                    request[k] = v.decode("utf-8")
                query_gid = request["gid"].capitalize()
                logger.info(f'Query was: {query_gid}')
                result = cc.submit_search(query_gid)
                table = cc.write_report(result,None)
                modular_html = cc.generate_modular_html_table(table)
                download_button = cc.generate_csv_download_button(table,query_gid)
                legend = {'A/J': 1,'C57BL/6J': 2,'129S1/SvlmJ': 3,'NOD/ShiLtJ': 4,'NZO/HILtJ': 5,'CAST/EiJ': 6,'PWK/PhJ': 7,'WSB/EiJ': 8}
                zed = [cc.fetch_aa_seqs(query_gid,k) for k in legend.keys()]
                txt_content = "\n".join([f'>{header}\n{seq}' for header,seq in zip(legend.keys(),zed)])
                fasta_button = cc.generate_fasta_download_button(txt_content,query_gid)
                if modular_html:
                    rehtml = html.replace("{replaceme}",modular_html + download_button + fasta_button)
                else:
                    rehtml = html.replace('{replaceme}', "Something went wrong :^(")
                    
                response = {
                    "statusCode": 200,
                    "body": rehtml,
                    "headers": {
                        'Content-Type': 'text/html',
                    }
                }
            else:
                rehtml = html.replace('{replaceme}',z)
                response = {
                    "statusCode": 201,
                    "body": rehtml,
                    "headers": {
                        'Content-Type': 'text/html',
                    }
                }
        else:
            response = {
                "statusCode": 202,
                "body": html,
                "headers": {
                    'Content-Type': 'text/html',
                }
            }
        return(response)