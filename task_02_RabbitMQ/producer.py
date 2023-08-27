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
    channel.queue_declare(queue='email_route')

    contacts = Contact.objects
    for contact in contacts:
        if contact.send_method == 'sms':
            channel.basic_publish(exchange='', routing_key='sms_route', body=str(contact.id).encode())
        elif contact.send_method == 'email':
            channel.basic_publish(exchange='', routing_key='email_route', body=str(contact.id).encode())

    print(' [x] Sent messages to email_queue and sms_queue')
    connection.close()


if __name__ == '__main__':
    main()
