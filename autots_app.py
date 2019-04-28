#

import argparse
import datetime
import getpass
from module import *


class AutoTSApp:
    def __init__(self, start_date, end_date, hoursforteams_username):
        self.start_timestamp = self.get_timestamp_from_date_string(start_date)
        self.end_timestamp = self.get_timestamp_from_date_string(end_date)
        self.hoursforteams_username = hoursforteams_username

    @staticmethod
    def get_timestamp_from_date_string(datestring):
        """

        :param datestring: UTC string in YYYY-MM-DD form, aka '%Y-%m-%d'
        :return:
        """
        dt = datetime.datetime.strptime(datestring, '%Y-%m-%d')
        dt = dt.timestamp()
        return dt

    def get_ts_from_hours(self):
        """
        Login to hoursforteams.com and download timesheet for range from self.start_timestamp to self.end_timestamp

        :return:
        """
        hi = HoursInterface()
        password = getpass.getpass(prompt='Password for hoursforteams.com [{}]'.format(self.hoursforteams_username))
        if not hi.login(self.hoursforteams_username, password):
            raise ValueError("Unable to login, double check the password and try again")

        summarized_report_dict = hi.download_summarized_report(self.start_timestamp, self.end_timestamp)
        summarized_report_df = summarized_report_dict['data']
        return summarized_report_df

    def transform_and_agg_ts(self):
        pass

    def submit_ts_to_accountsight(self):
        pass


def main():
    # create parser object
    description = 'Use this app to submit your timesheet more efficiently. The app will download your time from ' \
                  'hoursforteams.com for the supplied date range and then reconcile the hours with AccountSight.com' \
                  '\n\n' \
                  ''

    parser = argparse.ArgumentParser(description=description)

    # add arguments
    parser.add_argument('start_date',
                        help='Start date (UTC timezone) string, in \"%%Y-%%d-%%m\" form, e.g. \'2017-01-30\'')
    parser.add_argument('end_date',
                        help='End date (UTC timezone) string, in \"%%Y-%%d-%%m\" form, e.g. \'2017-01-30\'')
    parser.add_argument('hoursforteams_username',
                        help='the email address associated with your hoursforteams.com account')

    # parse the arguments from standard input
    args = parser.parse_args()

    ats = AutoTSApp(args.start_date, args.end_date, args.hoursforteams_username)
    data = ats.get_ts_from_hours()
    # print(data)


if __name__ == "__main__":
    main()
