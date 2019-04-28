#

import pandas as pd
from io import StringIO
import requests
import json


class HoursInterface:
    """
    class used to wrap all functionality required for interacting with hoursforteams.com. When instantiated, it will
    start a requests session, though the session will not make any requests
    """

    def __init__(self, start_url='https://api2.hoursforteams.com/index.php/api/users/login'):
        """

        :param start_url: url used for submitting login
        """
        self.start_url = start_url

        # start requests session so that cookies can be captured
        self.session = requests.Session()

    @staticmethod
    def prepare_data_for_requests_post(username, password):
        """
        Create bytes of request string to be passed to a requests.session.post() method as data parameter.

        :param username: string that will be used to authenticate
        :param password: string that will be used as the password for the request
        :return: bytes data that can be used as data argument for requests.session.post() method
        """
        data = {"email": username,
                "password": password,
                "remember": True,
                "deviceID": "web:" + username,
                "devicename": "web:" + username}

        # format dictionary as JSON
        data = json.dumps(data)
        # Convert to String
        data = str(data)
        # Convert string to byte
        data = data.encode('utf-8')
        return data

    def login(self, username, password):
        """
        Creates self.session and attempts to login to start_url.

        :param username: string that will be used to authenticate
        :param password: string that will be used as the password for the request
        :return: Bool indicating success/failure of login attempt
        """
        data = self.prepare_data_for_requests_post(username, password)

        # post request using session created at instantiation
        r = self.session.post(self.start_url, data=data)

        return r.ok

    def download_summarized_report(self, start_timestamp, end_timestamp):
        """

        :param start_timestamp:
        :param end_timestamp:
        :return:
        """
        result = dict()

        data = {"startTimestamp": start_timestamp,
                "endTimestamp": end_timestamp,
                "type": "csv",
                "timeZoneName": "America/New_York",
                "client": None,
                "project": None,
                "task": None,
                "person": None,
                "team": None}

        # format dictionary as JSON
        data = json.dumps(data)
        # Convert to String
        data = str(data)
        # Convert string to byte
        data = data.encode('utf-8')

        url = "https://api2.hoursforteams.com/index.php/api/reports/export"

        r = self.session.post(url, data=data)
        result['fetch_export_url'] = r.ok

        if r.ok:
            next_url = r.json()['result']['file']
            next_r = self.session.get(next_url)
            result['download_csv'] = next_r.ok
            if next_r.ok:
                response_data = StringIO(next_r.text)
                df = pd.read_csv(response_data)
                result['data'] = df
        else:
            result['download_csv'] = False
            result['data'] = None

        return result
