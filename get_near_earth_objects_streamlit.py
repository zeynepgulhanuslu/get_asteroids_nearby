import json
import logging

import pandas as pd
import requests
import streamlit as st
import yaml

with open('config.yaml', "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logging.error(exc)

backend = "http://" + config['HOST'] + ":" + str(config['PORT']) + "/get_near_earth_objects/"

st.title("Get Near Earth Object by Closest Distance")  # title for project

st.write(
    """  This streamlit example uses a Get Near Earth Object service as backend.""")  # description and instructions


# Convert datetime to string
def convert_datetime_to_str(date_time):
    return f'{date_time.year}-{str(date_time.month).zfill(2)}-{str(date_time.day).zfill(2)}'


start_date = convert_datetime_to_str(st.date_input('Start', value=pd.to_datetime('2020-06-10'))) # get dates from picker
end_date = convert_datetime_to_str(st.date_input('End', value=pd.to_datetime('2020-06-15')))


# this code send request to get near earth object server
def process(start_date, end_date, server_url: str):
    params = json.dumps({
        "start_date": start_date,
        "end_date": end_date})
    try:

        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", server_url, headers=headers, data=params)

        response_json = json.loads(response.text)
        return response_json
    except Exception as e:
        return e


if st.button('Get Near Earth Objects'):
    result = process(start_date, end_date, backend)
    st.success(st.json(result))
else:
    st.write("Press the above button..")
