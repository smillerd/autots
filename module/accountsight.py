#

import pandas as pd
import urllib


class AccountSightInterface:
    def __init__(self):
        pass

    def login(self, username, password):
        """
        method used for logging into the AccountSight website

        :param username:
        :param password:
        :return:
        """
        pass

    def submit_hours(self, report):
        """
        method used for submitting the report to accountsight

        :param report: pandas.DataFrame
        :return:
        """
        pass
