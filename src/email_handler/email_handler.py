import pika
import pika.spec
#import smtplib
import threading

def get_amqp_connection():
    ampq_connection : None | pika.BlockingConnection = getattr(get_amqp_connection, "amqp_connection", None)
    if ampq_connection is None:
        setattr(get_amqp_connection, "amqp_connection", pika.BlockingConnection())
    return ampq_connection

class EmailWorker(threading.Thread):
    def __init__(self, connection: pika.BlockingConnection, which_email_to_send:str):
        self.connection = connection
        self.which_email_to_send = which_email_to_send

    def run(self):
        def send_email(channel: pika.BlockingChannel, method: pika.spec.Basic.Deliver, properties: pika.spec.BasicProperties, body: bytes):
            return body.decode("UTF-8")
        self.connection.basic_consume("new_user_request",callback=send_email)

