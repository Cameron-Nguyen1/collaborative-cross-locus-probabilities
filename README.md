# Collaborative Cross Locus Probabilities
![alt text](https://i.imgur.com/h8cmemI.png)
-------------------------------------------------------------------------------------------------------------------------------------
## Description:
Queries the University of North Carolina's Collaborative Cross genetics site for founder contribution probabilities at a given locus.
This application is using Python 3.10 Runtime.
This application is particularly useful for QTL analysis (also available in my public repo) where collaborative cross mice are used.

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
