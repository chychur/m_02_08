# MongoDB & RabbitMQ


## MongoDB connection 
A database consist of two collections:
- Author
```commandline
{
  "_id": {
    "$oid": "64e8e68bc512f8bf3920dff7"
  },
  "full_name": "Albert Einstein",
  "born_date": "March 14, 1879",
  "born_location": "in Ulm, Germany",
  "description": "In 1879, Albert Einstein was born in Ulm, Germany...
}
```

- Quote ()
```commandline
{
  "_id": {
    "$oid": "64e8e68bc512f8bf3920dff9"
  },
  "tags": [
    "change",
    "deep-thoughts",
    "thinking",
    "world"
  ],
  "author": {
    "$oid": "64e8e68bc512f8bf3920dff7"
  },
  "quote": "“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”"
}
```
Also was created a script-file for uploading `json` files to a cloud database and a script for searching quotes by `tag`, by the author's `name`, or by a set of `tags`.
The script executes in an infinite loop and accepts commands in the following format command: value using the usual input operator. Example:

`name: Steve Martin` — find and return a list of all quotes by the author Steve Martin;

`tag:life` — find and return a list of quotes for the tag life;

`tags:life,live` — find and return a list of quotes with life or live tags (note: no spaces between life, live tags);

`exit` — end the execution of the script;

## RabbitMQ queues 
WWith the help of queues in RabbitMQ, the simulation of sending email and SMS is implemented.

Using Mongoengine's ODM, a contact model is created. The model necessarily includes fields: full name, email and a logical field that has a value of `False` by default.
It means that the message to the contact has not been sent and should become `True` when sent.

When the f`ill_data.py` script is run, it generates a certain number of fake contacts and writes them to the database.

When the `producer.py` script runs, it puts a message on the RabbitMQ queue that contains the ObjectID of the generated contact, and so on for all generated contacts.

The `sms_consumer.py` and `email_consumer.py` scripts receive messages from the RabbitMQ queue, process them and simulate sending messages by email and sms with a stub function. After the message is sent, the logical field for the contact is set to True. The script works constantly while waiting for messages from RabbitMQ.D