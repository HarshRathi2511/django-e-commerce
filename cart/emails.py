# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
# import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail


# def send_email(from_email,to_email):
#     message = Mail(
#         from_email='f20200794@pilani.bits-pilani.ac.in',
#         to_emails='rathiharsh2002@gmail.com',
#         subject='Sending with Twilio SendGrid is Fun',
#         html_content='<strong>and easy to do anywhere, even with Python</strong>')
            
#     try:
#         sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#         response = sg.send(message)
#         print(response.status_code)
#         print(response.body)
#         print(response.headers)
#     except Exception as e:
#          print(e.message)