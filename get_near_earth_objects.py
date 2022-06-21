import json
import logging

import httpx
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from near_earth_data import get_near_earth_object_from_dict
from utils import check_dates_format, check_nasa_response, config

app = FastAPI()


def custom_openapi():
    with open("openapi.json", "r") as openapi:
        return json.load(openapi)


app.openapi = custom_openapi
API_KEY = config["API_KEY"]

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


class NeoWsItem(BaseModel):
    start_date: str = config['DEFAULT_START_DATE']
    end_date: str = config['DEFAULT_END_DATE']


NASA_URL = config['URL']


@app.get('/')
def index():
    return {'message': 'GETS NEAR EARTH OBJECTS'}


'''
### returns near earth objects between start and end time sorted by closing distance.
'''


@app.post("/get_near_earth_objects/")
def get_near_earth_objects(item: NeoWsItem):
    is_dates_correct, msg = check_dates_format(item.start_date, item.end_date)
    if not is_dates_correct:
        return {'result': msg}
    params = {
        "start_date": item.start_date,
        "end_date": item.end_date,
        "api_key": API_KEY}

    try:
        client = httpx.Client(timeout=None)
        response = client.get(NASA_URL, params=params)
        response_json = json.loads(response.text)
        response_not_empty, response_msg = check_nasa_response(response_json)
        if not response_not_empty:
            return {'result': response_msg}
        else:
            response = response_json['near_earth_objects']
            near_earth_object_list = []

            for day, objects in response.items():
                near_earth_object_list.extend([get_near_earth_object_from_dict(x) for x in objects])

            near_earth_object_list.sort(key=lambda x: x.estimated_size[
                config['ESTIMATED_SIZE_TYPE']][config['SIZE_COMPARE_VAL']])
            logging.warning('Successfully returns near earth objects')

            return {'NearEarthObjectList': near_earth_object_list}

    except Exception as err:
        logging.error({'error_message': err})
        return {'result': err}


if __name__ == '__main__':
    uvicorn.run(app, host=config['HOST'], port=config['PORT'])
