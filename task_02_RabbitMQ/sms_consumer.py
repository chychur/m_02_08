import sys

import pika
from mongoengine import connect

from models import Contact

connect(
    db='web138hw_part2',  # DB name
    host='mongodb+srv://chychur:VuMoT5JYjeOMrgyk@clusterb.sffzgqf.mongodb.net/?retryWrites=true&w=majority',
    alias='default',
    ssl=True
)


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='sms_route')

    def send_sms_(contact_id):

        print(f"Sending sms to contact with ID: {contact_id}")
        return True

    def callback(ch, method, properties, body):
        contact_id = body.decode('utf-8')
        contact = Contact.objects(id=contact_id).first()

        if contact:
            if not contact.send_status:
                if send_sms_(contact_id):
                    contact.send_status = True
                    contact.save()
                    print(f'The sms was successfully sent to the "{contact.full_name}" on the phone number "{contact.phone_number}"')
            else:
                print(f'The sms had already sent to the "{contact.full_name}"')
        else:
            print(f"The contact with ID {contact_id} not found")

    channel.basic_consume(queue='sms_route', on_message_callback=callback, auto_ack=True)

    print("SMS Consumer is waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
