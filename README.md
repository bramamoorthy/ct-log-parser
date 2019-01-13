# ct-log-parser

##The Apache Access Log Parser - Enricher

This repository contains the code that will consume Apache Access log parser/enricher that that fetches an access log from s3, maps IP address to geodata, maps user-agent to device info and store the results in a database.

For the purpose of this exercise we are going to use the following public APIS:

### boto 
enables the script to communicate to AWS S3 to grab the files.

### apache-log-parser
A library that can Parse log lines from an apache log file in (almost) any format possible

### maxminddb
A maxmind local DB that provides the meta data detail for a given IP.


The objective of this script is very simple as stated below.

1. Use boto library grab the access log files intot local disk / memory
2. Using apache-log-parser library parse the log file line items.
3. For each line item grab the IP and use maxmind API to get the IP details.
4. The details would inclue 
   IP Address and 
    - Latitude
    - Longitude
    - Country
    - State
    - City
    - Zip code
    
    User Agent and 
    - Browser
    - Device type (desktop, mobile, table, robot)
    - Operating system  
5. Once the details are available in a list / dataframe persist it to MysqlDB.

