from mongoengine import Document, StringField, BooleanField


class Contact(Document):
    full_name = StringField(required=True, max_length=100)
    email = StringField(required=True, max_length=100, unique=True)

    phone_number = StringField(max_length=22)
    send_method = StringField(choices=["email", "sms"], required=True)
    send_status = BooleanField(default=False)

    meta = {'collection': 'contacts'}
