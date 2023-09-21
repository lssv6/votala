from email.mime.text import MIMEText
from smtplib import SMTP_SSL

import pika

VOTALA_EMAIL = "votalapoolingsystem@gmail.com"
VOTALA_EMAIL_PASSWORD = "CxkjVsiTz3sVciZ"
print("trying to connect to gmail")
smtp = SMTP_SSL("smtp.gmail.com", 456)
print("connected to gmail")
print("Trying to login")
smtp.login(VOTALA_EMAIL, VOTALA_EMAIL_PASSWORD)
print("logged")


def handle_new_user_request(new_user_email):
    global smtp

    sender = VOTALA_EMAIL

    subject = "ACTIVATION FOR VOTALA.COM"

    link = "google.com"
    body = f"""
    <html>
        <h>Thanks for creating a account in votala.com.br.</h>
        <p>Clck in the link bellow for activate your account: </p>
        <p>Link --> {link}</p>
        <br>
        <p>If you can't enter, then paste the following url into your address bar:</p>
        <p>{link}</p>

        <h2>Regards. VOTALA polling system team ¯\\_(ツ)_/¯ </h2>
    </html>
    """

    html_message = MIMEText(body, "html")
    html_message["Subject"] = subject
    html_message["From"] = sender
    html_message["To"] = new_user_email
    smtp.sendmail(sender, new_user_email, html_message.as_string())
    smtp.quit()


def on_message(channel, method_frame, _, body):
    email = str(body, encoding="utf-8")
    handle_new_user_request(email)
    print(f"sending email to {email}")
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


# Configure the handler
params = pika.URLParameters("ampq://guest:guest@10.0.0.109:5672")
print("creating blocking connection.")
connection = pika.BlockingConnection(params)  # Only one email at time :)
print("created connection")
channel = connection.channel()

channel.queue_declare(
    "new_user_request",
    # arguments={"x-message-ttl":3600000} # Setting the argument message-ttl as an hour
)
channel.basic_qos(prefetch_count=1)
channel.basic_consume("new_user_request", on_message_callback=handle_new_user_request)

try:
    channel.start_consuming()

except KeyboardInterrupt:
    channel.stop_consuming()

connection.close()
