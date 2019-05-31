#

import datetime
from autots_app import AutoTSApp


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
    data = ats.get_ts_from_hours(secrets_file=True)
    data_ready_for_email = ats.transform_and_agg_ts(data)
    # print(data_ready_for_email)

    # store as xlsx in tmp location
    data_ready_for_email.to_excel('/tmp/ts.xlsx')

    # send email with report attachment
    for recipient in recipients:
        ats.email_xl_report(recipient=recipient, attachment='/tmp/ts.xlsx')


if __name__ == "__main__":
    main()
