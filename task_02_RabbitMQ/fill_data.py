from random import choice

import faker
from mongoengine import connect

from models import Contact

fake = faker.Faker('en_US')
NUMBER_CONTACTS = 10

connect(
    db='web138hw_part2',  # DB name
    host='mongodb+srv://chychur:VuMoT5JYjeOMrgyk@clusterb.sffzgqf.mongodb.net/?retryWrites=true&w=majority',
    alias='default',
    ssl=True
)


def create_contacts(contacts: int | int = 5):
    for _ in range(contacts):
        full_name = f'{fake.first_name()} {fake.last_name()}'
        email = fake.email()
        phone_number = fake.phone_number()
        send_method = choice(["email", "sms"])
        #send_method = "email"
        contact = Contact(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            send_method=send_method,
            send_status=False
        )
        contact.save()


if __name__ == '__main__':
    create_contacts(NUMBER_CONTACTS)
