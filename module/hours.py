#

import pandas as pd
import urllib


class HoursInterface:
    """
    class used to wrap all functionality required for interacting with hoursforteams.com
    """
    def __init__(self, start_url='https://www.hoursforteams.com/#/login/'):
        """

        :param start_url: url used for submitting login
        """
        self.start_url = start_url

    def login(self, username, password):
        """
        method used for logging into the Hours website

        :param username:
        :param password:
        :return:
        """
        pass

    def download_detailed_report(self, period):
        """

        :param period: string representing the period of the report to download (e.g. 'Daily', 'Weekly', etc.)
        :return:
        """
        pass

    def standardize_time_sheet(self):
        """
        Transform the time sheet so that it meets the standards required for later use by autots.

        :return:
        """
        pass
