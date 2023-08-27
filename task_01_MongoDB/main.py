from db.models import Author, Quote
import mongoengine


mongoengine.connect(
    db='web138hw',  # DB name
    host='mongodb+srv://chychur:VuMoT5JYjeOMrgyk@clusterb.sffzgqf.mongodb.net/?retryWrites=true&w=majority',
    alias='default',
    ssl=True
)


def help_():
    """

    """
    help_message = ''

    for key, value in HANDLERS.items():
        help_message += f'{key} | {value.__doc__}\n'
    return help_message


def exit_():
    return


def unknown_command():
    '''
    Default function
    :return: string 'unknown command'
    '''
    return "unknown command"


def find_quotes_by_name(arg: list):
    """
    This command find the all quotes of the specific author in the DateBase.
    :param arg: list of author name. But expect the one name. (Length of the list - 1.)
    :return: list[str]. The list of the quotes.
    """
    if len(arg) == 1:
        author_name = arg[0]
        authors = Author.objects(full_name__icontains=author_name)
        result = []

        if authors:
            for author in authors:
                quotes = Quote.objects(author=author)
                for quote in quotes:
                    result.append(quote.quote)
                    #print(quote.quote)
        else:
            result = f'There is no "{author_name}" in this data base.'
        return result


def find_quotes_by_tags(tags: list):
    """
    This command find the all quotes that has specific tag or tags in the DateBase.
    :param tags: list of the tags.
    :return: list[str]. The list of the quotes.
    """
    result = []
    quotes = Quote.objects(tags__in=tags)

    if quotes:
        for quote in quotes:
            result.append(quote.quote)
            # print(quote.quote)
    else:
        result = f'There is no "{tags}" in this data base.'
    return result


def parse_user_input(user_input):
    comm, *args = user_input.split(':')
    comm = comm.lstrip()
    arguments = []
    try:
        args = args[0].split(',')
        for arg in args:
            arguments.append(arg.strip())
    except IndexError:
        arguments = None

    try:
        command = HANDLERS[comm.lower()]
    except KeyError:
        command = unknown_command
    # print(command, arguments)
    return command, arguments


HANDLERS = {
    'help': help_,
    'name': find_quotes_by_name,
    'tag': find_quotes_by_tags,
    'tags': find_quotes_by_tags,
    'exit': exit_
}


def main():
    while True:
        user_input = str(input('Please enter command and args: '))
        command, arguments = parse_user_input(user_input)
        if arguments == None:
            result = command()
        else:
            result = command(arguments)

        if not result:
            print('Good bye!')
            break
        print(result)


if __name__ == "__main__":
    main()
