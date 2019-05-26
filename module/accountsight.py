#

import pandas as pd
import requests
import json


class AccountSightInterface:
    def __init__(self, start_url='https://aqn.accountsight.com/Login.do'):
        """

        :param start_url: url used for submitting login
        """
        self.start_url = start_url

        # start requests session so that cookies can be captured
        self.session = requests.Session()

    @staticmethod
    def prepare_data_for_requests_post(username, password, company_id_form="aqn.accountsight.com"):
        """
        Create bytes of request string to be passed to a requests.session.post() method as data parameter.

        :param username: string that will be used to authenticate
        :param password: string that will be used as the password for the request
        :param company_id_form: used to indicate the AccountSight account for which the request is related to
        :return: bytes data that can be used as data argument for requests.session.post() method
        """
        raise NotImplementedError
        # data = {"MIME Type": "application/x-www-form-urlencoded",
        #         "companyIdForm": company_id_form,
        #         "userName": username,
        #         "userPwd": password}
        #
        # # format dictionary as JSON
        # data = json.dumps(data)
        # # Convert to String
        # data = str(data)
        # # Convert string to byte
        # data = data.encode('utf-8')
        # return data

    def login(self, username, password):
        """
        Using self.session, attempt to login to start_url.

        :param username: string that will be used to authenticate
        :param password: string that will be used as the password for the request
        :return: Bool indicating success/failure of login attempt
        """
        raise NotImplementedError
        # data = self.prepare_data_for_requests_post(username, password)
        #
        # # post request using session created at instantiation
        # r = self.session.post(self.start_url, data=data)
        #
        # return r.ok

    def download_summarized_report(self):
        raise NotImplementedError

    def submit_hours(self, report):
        """
        method used for submitting the report to accountsight

        :param report: pandas.DataFrame
        :return:
        """
        raise NotImplementedError
