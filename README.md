# ct-log-parser

## The Apache Access Log Parser - Enricher

This repository contains the code that will consume Apache Access log parser/enricher that that fetches an access log from s3, maps IP address to geodata, maps user-agent to device info and store the results in a database.

For the purpose of this exercise we are going to use the following public APIS:

### boto 
enables the script to communicate to AWS S3 to grab the files.

### apache-log-parser
A library that can Parse log lines from an apache log file in (almost) any format possible

**FYI:** 

The original idea was to consume the file via ```apache-log-parser``` api but using ```pandas```
was much better and easier in this case as the file can be treated as dataframe and 
parsing can be done on top of the parsed columns within the dataframe using lambdas.


### maxminddb
A maxmind local DB that provides the meta data detail for a given IP.

**FYI**

The version of the maxmind that i used didnt provide ```city , state, zip```. Following 
is an example of what maxmind included with this code base.

```{
     'continent': {
       'code': 'OC',
       'geoname_id': 6255151,
       'names': {
         'de': 'Ozeanien',
         'en': 'Oceania',
         'es': 'Oceanía',
         'fr': 'Océanie',
         'ja': 'オセアニア',
         'pt-BR': 'Oceania',
         'ru': 'Океания',
         'zh-CN': '大洋洲'
       }
     },
     'country': {
       'geoname_id': 2077456,
       'iso_code': 'AU',
       'names': {
         'de': 'Australien',
         'en': 'Australia',
         'es': 'Australia',
         'fr': 'Australie',
         'ja': 'オーストラリア',
         'pt-BR': 'Austrália',
         'ru': 'Австралия',
         'zh-CN': '澳大利亚'
       }
     },
     'location': {
       'accuracy_radius': 1000,
       'latitude': -33.494,
       'longitude': 143.2104
     },
     'registered_country': {
       'geoname_id': 2077456,
       'iso_code': 'AU',
       'names': {
         'de': 'Australien',
         'en': 'Australia',
         'es': 'Australia',
         'fr': 'Australie',
         'ja': 'オーストラリア',
         'pt-BR': 'Austrália',
         'ru': 'Австралия',
         'zh-CN': '澳大利亚'
       }
     }
   }
   ```


# HOW: 
## The objective of this script is very simple as stated below

1. Use boto library grab the access log files intot local disk / memory.

~~2. Using apache-log-parser library parse the log file line items~~
2. Using Pands create a dataframe that has the log info.
3. For each row grab the IP and use maxmind API to get the IP details using ```maxmind```.
4. Using ```ua_parser``` create the user agent info.
5. The details would inclue 
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
6. Once the details are available in a list / dataframe persist it to MysqlDB.


# Running the script
**prerequisite is Docker.**

### Approach 1

Once docker is installed the following command can be run to invoike the script

```docker-compose up```

### Approach 2
1. If there are any complication in setting up the localhost with docker mysql, with this approach
bring up the mysql docker separately to house the table with the following command.

```
docker-compose -f docker-compose-mysql.yml up
```

2. Once the ```ctlp_mysql``` is up and running on ```0.0.0.0:3306``` setup the 
```config.database_ip``` with that address(for SQL Achemy the default port is 3306. dont worry about it).

3. Run the following command to parse the logs and enrich it with both Geo info and 
user agent.
```
python3 log_parser.py
```


