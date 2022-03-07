import json

with open("data.json", "r") as f:
    data = json.load(f)


def price(x):
    """Returns price of an object in a list, if the object has a price. Otherwise, returns false."""
    if not input_check(x, 'price'):
        return False
    else:
        return x['price']


def input_check(x, string):
    """Verifies whether an item in a list contains a string. Can be used to ensure a list contains a specific field."""

    if string in x:
        return True
    else:
        return False


def parse_inventory(inventory):
    """Parse an inventory list into a dictionary with each distinct item type as key. Only items with a 'type' field
    will be added to the dictionary."""

    my_dictionary = {}

    for x in inventory:
        if not input_check(x, 'type'):
            continue

        elif x['type'] not in my_dictionary.keys():
            my_dictionary[x['type']] = [x]
        else:
            my_dictionary[x['type']].append(x)

    return my_dictionary


def top_5_in_category(inventory):
    """Accepts a list as an argument, parses it into a dictionary, then prints out the five most expensive items in each
     category."""

    parsed_inventory = parse_inventory(inventory)

    for x in parsed_inventory.keys():
        parsed_inventory[x].sort(reverse=True, key=price)
        parsed_inventory[x] = parsed_inventory[x][0:5]
        print("Type: " + x)
        print(*parsed_inventory[x], sep='\n')

    return parsed_inventory


def running_time(inventory, target=3600):
    """Accepts a list as first argument and a target run time (in seconds).
    Returns a list containing all CD's in inventory with run time > target.
    Target is time in seconds and default target is 1 hour (3600 seconds)."""
    
    over_target = []
    
    for x in inventory:
        if not input_check(x, 'type'):
            continue

        if x['type'] == 'cd':
            total_run_time = 0
            if not input_check(x, 'tracks'):
                continue
            for i in x['tracks']:
                if not input_check(i, 'seconds'):
                    continue
                total_run_time += i['seconds']
            if total_run_time > target:
                over_target.append(x)
    return over_target


def cd_and_book(inventory):
    """Accepts an inventory list. Returns new list containing author names who have released both a book and CD."""

    book_authors = []
    both = []

    for x in inventory:
        if not input_check(x, 'type'):
            continue
        elif x['type'] == 'book':
            if not input_check(x, 'author'):
                continue
            else:
                book_authors.append(x['author'])

    for x in inventory:
        if not input_check(x, 'type'):
            continue
        if x['type'] == 'cd':
            for i in book_authors:
                if not input_check(x, 'author'):
                    continue
                if x['author'] == i:
                    both.append(x['author'])
                    break
    return both


def string_contains_year(string, digits=4):
    """Checks the inputted string to see whether it contains a year. A year is considered to be any sequence of exactly
    four numbers with no spaces between. Can change number of sequential digits with 'digits' argument, default is 4."""

    count = 0
    length = len(string)

    for x in range(length):
        if string[x].isdigit():
            count += 1
        elif not string[x].isdigit():
            count = 0
            continue
        if count == digits:
            if x == (length-1):
                return True
            elif not string[x+1].isdigit():
                return True
            else:
                continue
    return False


def contains_year(inventory):
    """Accepts an inventory list. Parses list to see which items contain a year in either it's title, chapters or
    tracks. Returns list of all items that meet this criteria."""

    contain_year = []

    for x in inventory:
        if not input_check(x, 'type'):
            continue
        if x['type'] == 'book':
            if not input_check(x, 'title'):
                continue
            if string_contains_year(x['title']):
                contain_year.append(x)
            else:
                if not input_check(x, 'chapters'):
                    continue
                if string_contains_year(x['chapters']):
                    contain_year.append(x)

        elif x['type'] == 'dvd':
            if not input_check(x, 'title'):
                continue
            if string_contains_year(x['title']):
                contain_year.append(x)

        elif x['type'] == 'cd':
            if not input_check(x, 'title'):
                continue
            if string_contains_year(x['title']):
                contain_year.append(x)
            else:
                if not input_check(x, 'tracks'):
                    continue
                for i in x['tracks']:
                    if string_contains_year(i['name']):
                        contain_year.append(x)
                        continue
    return contain_year


print("\n Top 5 most expensive items in price per category:")
dictionary = top_5_in_category(data)

print("\n CD's with run time longer than 60 minutes:")
over_an_hour = running_time(data)
print(*over_an_hour, sep="\n")

print("\nAuthors that have also released CDs:")
cd_and_book = cd_and_book(data)
print(*cd_and_book, sep="\n")

print("\nItems with titles, tracks, or chapters that contain a year:")
has_year = contains_year(data)
print(*has_year, sep="\n")
