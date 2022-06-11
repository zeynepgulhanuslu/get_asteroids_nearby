import logging
from datetime import datetime

import yaml

with open("config.yaml", "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logging.error(exc)

DATE_LIMIT = 7
DATE_FORMAT_MESSAGE = config['DATE_FORMAT_MESSAGE']

'''
### Check dates are not exceed day limit
'''


def check_dates_format(start_time, end_time):
    logging.warning(f'start time: {start_time} end time: {end_time}')
    try:
        start_time_obj = datetime.fromisoformat(start_time)
        end_time_obj = datetime.fromisoformat(end_time)
        day_limit = abs(end_time_obj.day - start_time_obj.day)
        month_limit = abs(end_time_obj.month - start_time_obj.month)
        year_limit = abs(end_time_obj.year - start_time_obj.year)
        logging.warning(f'start time: {start_time_obj} end time: {end_time_obj} date limit : {day_limit}')

        if day_limit > DATE_LIMIT:
            error_msg = f'The Feed date limit is only {DATE_LIMIT} Days. Please give another date. ' \
                        f'Given year difference: {year_limit}' \
                        f' month difference: {month_limit} day difference : {day_limit}'
            logging.error(error_msg)
            return False, error_msg
        elif month_limit != 0 or year_limit != 0:
            error_msg = f'The Feed date limit is only {DATE_LIMIT} Days. Please give another date. ' \
                        f'Given year limit: {year_limit} month limit: {month_limit} day limit : {day_limit}'
            logging.error(error_msg)
            return False, error_msg
        else:
            msg = 'dates are correct format.'
            logging.warning(msg)
            return True, msg

    except Exception as err:
        logging.error(err)
        return False, DATE_FORMAT_MESSAGE


'''
### Check if nasa server returns near earth objects successfully.
'''


def check_nasa_response(response):
    if not bool(response):
        msg = config['NASA_SERVER_NOT_RESPOND']
        logging.error(msg)
        return False, msg
    elif 'near_earth_objects' not in response.keys():
        msg = config['NEAR_OBJECTS_NOT_EXIST']
        logging.error(msg)
        return False, msg
    elif len(response['near_earth_objects']) == 0:
        msg = config['NEAR_OBJECTS_EMPTY']
        logging.error(msg)
        return False, msg
    else:
        msg = config['NASA_SERVER_SUCCESS']
        logging.warning(msg)
        return True, msg
