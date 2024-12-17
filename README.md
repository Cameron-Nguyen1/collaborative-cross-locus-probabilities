# Collaborative Cross Locus Probabilities
![Figure 1](https://i.imgur.com/h8cmemI.png)
![Figure 2](https://github.com/user-attachments/assets/dd0cc2e6-7ce8-4ea6-bfaf-3e88c88d5a39)
![Figure 3](https://github.com/user-attachments/assets/ca359d92-ede2-47a8-a081-543c15678898)
![Figure 4](https://github.com/user-attachments/assets/17808e33-20dc-4bcc-ae1a-16d7d23aef8b)
![Figure 5](https://github.com/user-attachments/assets/6a06e8a3-ce5d-471d-9532-197d83d6bfaf)


-------------------------------------------------------------------------------------------------------------------------------------
## Description:
Queries the University of North Carolina's Collaborative Cross genetics site for founder contribution probabilities at a given locus.
This application is using Python 3.10 Runtime.
This application is particularly useful for QTL analysis (also available in my public repo) where collaborative cross mice are used.

Results are avaiable in 
- CSV (CC founder probabilities)
- FASTA (Ensembl protein sequences by strain, "None" if unable to retrieve for one reason or another)

## Dependencies:
requests
requests_toolbelt
beautifulsoup4

## How to use:
- This application is set up as a Lambda function on AWS that is interacted with through a simple dynamic HTML webform.
- Simply enter a gene symbol like "Sox9" or "Irf7" to retrieve the founder contribution probabilities for collaborative cross mice.

### You will need to: 
 - Create a lambda function in AWS Lambda with sufficient appropriate permissions. 
 - Copy Python and DHTML to function, source Python dependencies
