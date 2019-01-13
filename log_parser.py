import config

import boto3
import botocore

import re
import pandas as pd
from ua_parser import user_agent_parser

from pandas.io.json import json_normalize

import maxminddb


maxminddb_reader = maxminddb.open_database('data/GeoLite2-City.mmdb')


import sqlalchemy

print("Good till here")

LOCAL_FILE_NAME = 'mylocalacess.log'

def get_log_file():
    s3 = boto3.resource(
        's3',
        region_name=config.REGION,
        aws_access_key_id = config.ACCESS_KEY,
        aws_secret_access_key = config.SECRET_KEY)

    try:
        s3.Bucket(config.BUCKET).download_file(config.KEY, LOCAL_FILE_NAME)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


def extract_user_agent(x):
    """
    Extracts user agent.

    """
    return x[1:-1]

def user_agent_parsing(ua):
    try:
        return user_agent_parser.Parse(ua) if ua else ''
    except:
        pass

def parse_content(ua, root_key, desired_key, deep_key=None):
    try:
        if ua[root_key][desired_key] and not deep_key:
            return ua[root_key][desired_key]
        elif ua[root_key][desired_key][deep_key]:
            return ua[root_key][desired_key][deep_key]
    except:
        pass

def create_geo_info_from_ip(ip):
    if not ip:
        return None
    try:
        return maxminddb_reader.get(ip)
    except:
        pass



def overwrite_log_data(dataframe):
    database_connection = \
        sqlalchemy.create_engine(
            'mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(
                config.database_username,
                config.database_password,
                config.database_ip,
                config.database_name
            )
        )
    dataframe.to_sql(con=database_connection, name='access_log_details', if_exists='replace')



def create_pandas_df():
    ### Read the log file and parse the content into a Dataframe.
    data = pd.read_csv(
        LOCAL_FILE_NAME,
        sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
        engine='python',
        na_values='-',
        header=None,
        usecols=[0, 8],
        names=['ip', 'user_agent'],
        converters={'user_agent': extract_user_agent})

    ### Parse the Contents and derive the user agent information.
    data['parsed_agent'] = data['user_agent'].apply(user_agent_parsing)
    data['device_brand'] = data['parsed_agent'].apply(parse_content, root_key = 'device', desired_key = 'brand')
    data['device_model'] = data['parsed_agent'].apply(parse_content, root_key = 'device', desired_key = 'model')
    data['os_family'] = data['parsed_agent'].apply(parse_content, root_key = 'os', desired_key = 'family')
    data['user_agent_family'] = data['parsed_agent'].apply(parse_content, root_key = 'user_agent', desired_key = 'family')
    pd.set_option('display.max_columns', None)

    ### using the IP identify the geo location info using maxmind.

    data['geo_json'] = data['ip'].apply(create_geo_info_from_ip)

    data['latitude'] = data['geo_json'].apply(parse_content, root_key = 'location', desired_key = 'latitude')
    data['longitude'] = data['geo_json'].apply(parse_content, root_key = 'location', desired_key = 'longitude')
    data['country'] = data['geo_json'].apply(parse_content, root_key = 'country', desired_key = 'names', deep_key = 'en')

    data = data.drop(columns=['parsed_agent','geo_json'])

    pd.set_option('display.max_columns', None)


    print(data.head())
    return data



get_log_file()
dataframe = create_pandas_df()
overwrite_log_data(dataframe)


