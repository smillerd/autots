import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime


class EmailInterface:

    def __init__(self, sender, recipient, attachment,
                 subject_str="FYI NAR Timesheet - SMillerd ",
                 body_text=(f"Attached is the timesheet that has been specially prepared for rapid "
                            f"upload to AccountSight.\n\n\n\n This project is available OpenSource "
                            f"at https://github.com/smillerd/autots. This email was sent with Amazon SES using the AWS "
                            f"SDK for Python (Boto). Many thanks to pandas and requests. Built on the shoulders of "
                            f"giants."
                            ),
                 aws_region="us-east-1"):
        """
        When initialized, format message and attachment, send email to recipient from sender. NOT YET TESTED.

        :param sender:
        :param recipient:
        :param attachment:
        :param subject_str:
        :param body_text:
        :param aws_region:
        """

        # The subject line for the email. Added date to end of subject line to be polite
        subject_str = subject_str
        subject_str = subject_str + " " + datetime.today().strftime("%m/%d/%Y") + " (automated)"

        # Create a new SES resource and specify a region.
        client = boto3.client('ses', region_name=aws_region)
        msg = self.make_message(sender, recipient, subject_str, body_text, attachment)
        # send email
        self.send_email(client, sender, recipient, msg)

    @staticmethod
    def make_message(sender, recipient, subject, body_text, attachment):
        # setup the parameters of the message
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject

        # add in the message body
        msg.attach(MIMEText(body_text, 'plain'))

        # Define the attachment part and encode it using MIMEApplication.
        att = MIMEApplication(open(attachment, 'rb').read())

        # Add a header to tell the email client to treat this part as an attachment,
        # and to give the attachment a name.
        att.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
        # Add the attachment to the parent container.
        msg.attach(att)
        return msg

    @staticmethod
    def send_email(client, sender, recipient, msg):
        # Try to send the email.
        try:
            # Provide the contents of the email.
            response = client.send_raw_email(
                Source=sender,
                Destinations=[
                    recipient
                ],
                RawMessage={
                    'Data': msg.as_string(),
                },
                #         ConfigurationSetName=CONFIGURATION_SET
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
