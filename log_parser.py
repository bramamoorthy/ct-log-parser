import config

import boto3
import botocore

import re
import pandas as pd
from ua_parser import user_agent_parser

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
    parsed_value = user_agent_parser.Parse(ua)
    return parsed_value

def parse_content(ua, root_key, deired_key):
    if ua[root_key] and ua[root_key][deired_key]:
        return ua[root_key][deired_key]
    else:
        ''



def create_pandas_df():
    data = pd.read_csv(
        LOCAL_FILE_NAME,
        sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
        engine='python',
        na_values='-',
        header=None,
        usecols=[0, 8],
        names=['ip', 'user_agent'],
        converters={'user_agent': extract_user_agent})
    print(data.head())
    parsed_user_agent = data['user_agent'].apply(user_agent_parsing)


# get_log_file()
create_pandas_df()
