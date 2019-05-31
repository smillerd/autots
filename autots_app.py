#

import pandas as pd
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

        print('Login Success!')

        # nasty bit of code that retries the report download up to 5 times. This is to handle the inconsistency
        retries = 5
        count = 0
        summarized_report_dict, summarized_report_df = dict(), pd.DataFrame()
        summarized_report_dict['fetch_export_url'] = False
        while count < retries:
            count += 1
            try:
                summarized_report_dict = hi.download_summarized_report(self.start_timestamp, self.end_timestamp)
                summarized_report_df = summarized_report_dict['data']
                if not summarized_report_dict['fetch_export_url']:
                    raise ValueError('Failed to obtain export_url')
                elif not summarized_report_dict['download_csv']:
                    raise ValueError('Failed to obtain download_csv')
                else:
                    break
            except ValueError:
                pass

        if not summarized_report_dict['fetch_export_url']:
            raise ValueError('Failed to obtain export_ur: max retries exceeded')

        return summarized_report_df

    @staticmethod
    def transform_and_agg_ts(data):
        """
        Note!!!! Assumes that the Project is just the 001 Customer

        :param data:
        :return:
        """
        # change field names to AccountSight field names
        hoursforteams_accountsight_key = {"Client": "Customer (*)",
                                          "Project": "Task (*)",
                                          "Date": "Date (*)",
                                          "Start": "Start Time",
                                          "End": "End Time",
                                          "Note": "Comments",
                                          "Duration": "Hours",
                                          "Person": "User ID/Email ID"
                                          }

        out_data = data.rename(hoursforteams_accountsight_key, axis=1)

        # aggregate data into appropriate level for Accountsight
        out_data = out_data.groupby(['Date (*)', 'Customer (*)', 'Task (*)']).agg({'Hours': 'sum',
                                                                                   # 'Comments': 'sum'
                                                                                   })
        out_data.reset_index(level=[0, 1, 2], inplace=True)

        # transform date field into correct format for Accountsight
        out_data['Date (*)'] = out_data.apply(
            lambda x: datetime.datetime.strptime(x['Date (*)'], '%m/%d/%Y').strftime('%d-%b-%Y'),
            axis=1)

        # create null columns for blank fields in AccountSight upload
        out_data = pd.concat([out_data, pd.DataFrame(columns=['Start Time', 'End Time', 'User ID/Email ID'])],
                             sort=False)

        # assume that Project is 001 Customer, unless Customer is AQN
        out_data['Project (*)'] = out_data.apply(
            lambda x: '001 ' + x['Customer (*)'] if x['Customer (*)'] != 'AQN' else 'Internal',
            axis=1
        )

        # set the comments
        out_data['Comments'] = 'Automatically uploaded via autots (https://github.com/smillerd/autots)'

        # reorder columns
        out_data = out_data[['Date (*)',
                             'Customer (*)',
                             'Project (*)',
                             'Task (*)',
                             'Start Time',
                             'End Time',
                             'Hours',
                             'Comments',
                             'User ID/Email ID'
                             ]]

        return out_data

    @staticmethod
    def email_xl_report(sender='millerd2seth@gmail.com',
                        recipient='smillerd@aqnstrategies.com',
                        attachment='/tmp/ts.xlsx'):
        try:
            EmailInterface(sender, recipient, attachment)
        finally:
            pass

    # def submit_ts_to_accountsight(self):
    #     pass


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
                        help='The email address associated with your hoursforteams.com account')
    parser.add_argument('report_recipient',
                        help='The email address that the summarized timesheet (\"report\") will be sent to')

    # parse the arguments from standard input
    args = parser.parse_args()

    ats = AutoTSApp(args.start_date, args.end_date, args.hoursforteams_username)
    data = ats.get_ts_from_hours()
    data_ready_for_email = ats.transform_and_agg_ts(data)
    # print(data_ready_for_email)

    # store as xlsx in tmp location
    data_ready_for_email.to_excel('/tmp/ts.xlsx', index=False)

    # send email with report attachment
    ats.email_xl_report(recipient=args.report_recipient, attachment='/tmp/ts.xlsx')


if __name__ == "__main__":
    main()
