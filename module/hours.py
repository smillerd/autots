#

import pandas as pd
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
    def prepare_data_for_requests_post(useremail, userpassword):
        """
        Create bytes of request string to be passed to a requests.session.post() method as data parameter.

        :param useremail: string that will be used to authenticate
        :param userpassword: string that will be used as the password for the request
        :return: bytes data that can be used as data argument for requests.session.post() method
        """
        data = {"email": useremail,
                "password": userpassword,
                "remember": True,
                "deviceID": "web:" + useremail,
                "devicename": "web:" + useremail}

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

    def download_detailed_report(self, period):
        """

        :param period: string representing the period of the report to download (e.g. 'Daily', 'Weekly', etc.)
        :return:
        """
        pass

# TODO -- where should this actually live?
    def standardize_time_sheet(self):
        """
        Transform the time sheet so that it meets the standards required for later use by autots.

        :return:
        """
        pass
