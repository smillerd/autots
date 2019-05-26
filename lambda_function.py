#

import pandas as pd
import datetime
from secrets import hours_for_team_password
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
        # NOTE -- this requires the existence of a secrets.py that contains hours_for_team_password
        password = hours_for_team_password
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

        :param data:
        :return:
        """
        # change field names to AccountSight field names
        hoursforteams_accountsight_key = {"Client": "Customer",
                                          "Project": "Project",
                                          "Date": "Date",
                                          "Start": "Start Time",
                                          "End": "End Time",
                                          "Note": "Comments",
                                          "Duration": "Hours",
                                          "Person": "User ID/Email ID"
                                          }

        out_data = data.rename(hoursforteams_accountsight_key, axis=1)

        # aggregate data into appropriate level for Accountsight
        out_data = out_data.groupby(['Date', 'Customer', 'Project']).agg({'Hours': 'sum',
                                                                          # 'Comments': 'sum'
                                                                          })
        out_data.reset_index(level=[0, 1, 2], inplace=True)

        # transform date field into correct format for Accountsight
        out_data['Date'] = out_data.apply(
            lambda x: datetime.datetime.strptime(x['Date'], '%m/%d/%Y').strftime('%d-%b-%Y'),
            axis=1)

        # create null columns for blank fields in AccountSight upload
        out_data = pd.concat([out_data, pd.DataFrame(columns=['Task', 'Start Time', 'End Time', 'User ID/Email ID'])],
                             sort=False)
        return out_data

    @staticmethod
    def email_xl_report(sender='millerd2seth@gmail.com',
                        recipient='smillerd@aqnstrategies.com',
                        attachment='/tmp/ts.xlsx'):
        try:
            EmailInterface(sender, recipient, attachment)
        finally:
            pass


def main():
    """emails timesheet from previous 7 days to hardcoded recipients"""

    # get dates for reporting
    today = datetime.datetime.today()
    seven_days_ago = today - datetime.timedelta(days=7)
    start_date = datetime.datetime.strftime(seven_days_ago, '%Y-%m-%d')
    end_date = datetime.datetime.strftime(today, '%Y-%m-%d')

    # set the settings for hoursforteams_username and the list of recipients
    hoursforteams_username = 'millerd2seth@gmail.com'
    recipients = ['smillerd@aqnstrategies.com']

    ats = AutoTSApp(start_date, end_date, hoursforteams_username)
    data = ats.get_ts_from_hours()
    data_ready_for_email = ats.transform_and_agg_ts(data)
    # print(data_ready_for_email)

    # store as xlsx in tmp location
    data_ready_for_email.to_excel('/tmp/ts.xlsx')

    # send email with report attachment
    for recipient in recipients:
        ats.email_xl_report(recipient=recipient, attachment='/tmp/ts.xlsx')


if __name__ == "__main__":
    main()
