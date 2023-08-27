import json
from models import Author, Quote

import mongoengine

# Connection to the  MongoDB
mongoengine.connect(
    db='web138hw',  # DB name
    host='mongodb+srv://chychur:VuMoT5JYjeOMrgyk@clusterb.sffzgqf.mongodb.net/?retryWrites=true&w=majority',
    alias='default',
    ssl=True
)


def load_authors(filename):
    with open(filename, 'r') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            existing_author = Author.objects(
                full_name=author_data['full_name']).first()
            if not existing_author:
                author = Author(**author_data)
                author.save()


def load_quotes(filename):
    with open(filename, 'r') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author = Author.objects(full_name=quote_data['author']).first()
            if author:
                quote_data['author'] = author
                quote = Quote(**quote_data)
                quote.save()


if __name__ == '__main__':
    load_authors('authors.json')
    load_quotes('quotes.json')
