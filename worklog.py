import sys
import os
import datetime

from collections import OrderedDict
from tasks import Tasks


t = Tasks()
t.initialise()


def main_menu(status='WORK LOG\nWhat would you like to do?'):
    '''Return to main menu'''

    clear_screen()
    # display main menu header
    print(status)
    # display menu options
    for option, desc in main_menu_options.items():
        print('{}) {}'.format(option, desc.__doc__))
    # prompt for user to select from the main menu
    choice = input('> ').lower().strip()
    # check selection is valid ...
    if valid_main_menu_choice(choice):
        clear_screen()
        # ... and initiate choice ...
        main_menu(status=main_menu_options[choice]())
    else:
        # ... prompt user to select from menu again if choice is invalid
        main_menu(status='Invalid choice. Please select again.\n')


def valid_main_menu_choice(choice):
    # check user selection from main menu is valid
    return True if choice in main_menu_options.keys() else False


def add_entry():
    '''Add an entry to the database'''

    # gather entry details ...
    entry = {'name': get_name(),
             'date': get_date(),
             'title': get_title(),
             'time_spent': get_time_spent(),
             'notes': get_notes()
             }
    # ... and add to database ...
    t.add_entry(entry)
    # ... returning to main menu, confirming addition has been completed
    return 'The entry has been added...\nWhat would you like to do?'


def get_name():
    '''Enter a name'''
    # gather employee name details from user...
    name = input(get_name.__doc__ + '\n> ').rstrip()
    # ... validating that a name has been input -
    # name has to be at least one character long
    return name if validate_length(name, 'name') else get_name()


def get_date(status=''):
    '''Enter a date (DD/MM/YYYY)'''
    # gather date of work from user...
    getting_date = True
    while getting_date:
        try:
            date = datetime.datetime.strptime(
                input(status + get_date.__doc__ + '\n> ').strip(), '%d/%m/%Y')
        except ValueError:
            # ... prompting the user to input the date again if invalid
            input('Invalid input. [Enter] to try again.\n')
            continue
        else:
            date = datetime.datetime.strftime(date, '%d/%m/%Y')
            getting_date = False
    return date


def get_title():
    '''Enter a title'''

    # gather title of work from user...
    title = input(get_title.__doc__ + '\n> ').rstrip()
    # ... validating that a title has been input -
    # title has to be at least one character long
    return title if validate_length(title, 'title') else get_title()


def get_time_spent():
    '''Enter time spent, rounded to nearest minute.'''
    # gather the time spent working from user ...
    getting_time_spent = True
    while getting_time_spent:
        try:
            minutes = int(input(get_time_spent.__doc__ + '\n> '))
        except ValueError:
            # ... prompting the user to input time spent again
            # if not expressed as int.
            input('Invalid input. [Enter] to try again.\n')
            continue
        else:
            time_spent = minutes
            getting_time_spent = False
    return time_spent


def get_notes():
    '''Enter notes, optional - leave blank as required.'''
    # gather worklog notes from user ...
    notes = (input(get_notes.__doc__ + '\n> ').rstrip())
    # ... completing them as 'None' if no notes supplied
    return notes + 'None' if len(notes) == 0 else notes


def validate_length(s, desc):
    ''' Ensures that a worklog name or title are provided '''
    # check a valid name or title has been supplied
    return True if len(s) > 0 else print('No {} entered. Please try again.'.
                                         format(desc))


def search_menu(status='\nHow do you want to search?'):
    '''Search Entries'''
    # if there are existing work logs ...
    if entries():
        clear_screen()
        # ... print search menu header ...
        print(status)
        # ... display search menu options ...
        for option, desc in search_menu_options.items():
            print('{}) {}'.format(option, desc.__doc__))
        # ... prompt user to select way of searching work logs.
        choice = input('> ').lower().strip()
        # if user choice is valid ...
        if valid_search_menu_choice(choice):
            clear_screen()
            # ... initiate their choice, returning to search menu
            # once user is ready for next search ...
            search_menu(status=search_menu_options[choice]())
        else:
            # ...otherwise, prompt them to select again.
            search_menu(status='Invalid selection, please try again...\n'
                               'How do you want to search?')
    else:
        # ...Return to the main menu if database is empty.
        main_menu(status='There are no work logs recorded.\n'
                         'What would you like to do?')


def entries():
    # check to see if database has any entries stored in it
    return True if t.has_entries() else False


def valid_search_menu_choice(choice):
    # validate user search menu choice
    return True if choice in search_menu_options.keys() else False


def find_from_list_of_names(status=''):
    '''from the list of Employees with work logs'''
    clear_screen()
    # display header
    print(status)
    # display list of unique employees, whom have recorded a work log, by name
    display_names(t.employees())
    # prompt the user to choose an employee
    choice = input('\nChoice:\n> ')
    # page work log for that employee if the user has made a valid selection,
    # prompt them to select again if invalid choice made.
    if t.entry_by_name(choice).exists():
        page_worklogs(t.entry_by_name(choice))
    else:
        find_from_list_of_names(status='Invalid selection. Please try again...')
    # return update to search menu header
    return 'Actions complete.'


def find_by_name(
        status='Please enter a name and choose from the list of names'):
    '''by employee name, including partial matches'''
    clear_screen()
    # print search header
    print(status)
    # prompt the user to input a name and display full and
    # partial matching results from database
    display_names(t.employees_contains(get_name()))
    # prompt user to select one of the matching results
    choice = input('\nChoice:\n> ')
    # page work logs for that employee if the user has made a valid selection,
    # prompt them to select again if invalid choice made.
    if t.entry_by_name(choice).exists():
        page_worklogs(t.entry_by_name(choice))
    else :
        find_by_name(status='Invalid selection. Please try again.')
    # return update to search menu header
    return 'Actions complete.'


def display_names(names):
    # display a list of work log authors
    print('Please choose from the following names\n')
    for entry in names:
        print(entry.name)


def find_from_list_of_dates(status=''):
    '''from a list of unique log dates'''
    clear_screen()
    print(status)
    display_dates(t.dates())
    choice = input('\nChoice\n> ')
    if t.entry_by_date(choice).exists():
        page_worklogs(t.entry_by_date(choice))
    else:
        find_from_list_of_dates(status='Invalid selection. Please try again.')
    return 'Actions complete.'


def find_from_range_of_dates(status='Please enter a start date followed by '
                                    'an end date, then make a selection'):
    '''from a range of dates.'''
    clear_screen()
    print(status)
    # display work logs according to a valid date range supplied by the user
    display_dates(dates=t.range_of_dates(*valid_date_range(get_date(),
                                                           get_date())))
    choice = input('\nChoice\n> ')
    if t.entry_by_date(choice).exists():
        page_worklogs(t.entry_by_date(choice))
    else:
        find_from_range_of_dates(status='Invalid selection. Please try again.')
    return 'Actions complete.'


def valid_date_range(start, end):
    # check range of dates input is valid - start date preceeds end date
    return (start, end) if start < end else find_from_range_of_dates(
        status='Invalid date range. Please input again.')


def display_dates(dates):
    clear_screen()
    # display the dates work logs were made
    print('Please choose from the following dates')
    for entry in dates:
        print(entry.date)


def find_by_time_spent():
    '''from time spent'''
    # prompt the user for the time spent completing a task,
    # paging all work log entries detailing that corresponding number of minutes
    page_worklogs(t.entry_by_time_spent(get_time_spent()))
    return 'Actions complete.'


def find_from_term():
    '''from a term in worklog title or notes.'''
    # prompt the user to input a term that may be found in the title or
    # notes of a work log, displaying any matching results as pages.
    page_worklogs(t.entry_by_term(input('Please enter the term you '
                                        'wish to search by > ')))
    return 'Actions complete.'


def page_worklogs(matches, index=0):
    ''' displays worklog entries according to a search criteria as
    pages.
    '''
    # return to search menu if there are no matches to search query
    if not match_exists(matches):
        search_menu(status='There are no matches. Search again?')

    clear_screen()
    # display a matching work log entry as a page
    print('Matching worklog entries')
    display_entry(matches[index])
    # confirm which number search is displayed out of total number of
    # matches.
    print('\nEntry {} / {}'.format(index + 1, matches.count()))
    # find paging options
    page_menu_options = page_menu(matches, index)
    # prompt user to select a page option ...
    choice = input('> ')
    # ... prompt them to choose again if invalid choice made
    if choice not in page_menu_options: page_worklogs(matches, index)

    page_menu_selection = {'n': lambda: page_worklogs(matches,
                                                      index + 1),
                           'p': lambda: page_worklogs(matches,
                                                      index - 1),
                           'e': lambda: edit_entry(matches[index]),
                           'd': lambda: delete_entry(matches[index]),
                           'r': lambda: search_menu(
                               status='Search Complete.\n'
                                      'How do you want to search?')}
    # initiate page option choice
    page_menu_selection[choice]()


def match_exists(matches):
    # check to see if matching entries exist according to search query
    return True if matches.exists() else False


def page_menu(matches, index):
    '''produces and prints correct paged work log navigation options,
    also options to edit, delete an entry and return to the search
    menu.
    '''

    options = {'n': '[N]ext, ', 'e': '[E]dit, ',
               'p': '[P]revious ', 'd': '[D]elete, ',
               'r': '[R]eturn to search menu'}
    if matches.count() == 1:
        page_options = '{e}{d}{r}'
    elif index == 0:
        page_options = '{n}{e}{d}{r}'
    elif index >= 1 and index < matches.count() - 1:
        page_options = '{n}{p}{e}{d}{r}'
    else:
        page_options = '{p}{e}{d}{r}'
    # print page options
    print(page_options.format(**options))
    return page_options.replace('{', '').replace('}', '')


def display_entry(match):
    # print work log entry details
    print('Name: {}\nDate : {}\nTitle : {}\nTime Spent : {}\nNotes: {}'.
          format(match.name, match.date, match.title, match.time_spent,
                 match.notes))


def edit_entry(match):
    ''' Allows a user to edit an entry by date, title, time spent and notes.'''

    clear_screen()
    display_entry(match)

    print('Select which field you wish to update.')
    # list editing options
    for option, desc in edit_menu_options.items():
        print('{}) {}'.format(option, desc.__doc__))
    # prompt user to selection an editing option
    choice = input('> ')
    # if a valid choice is entered
    if valid_edit_menu_choice(choice):
        # edit the work log using new appropriate information gathered.
        t.edit_table(match, choice, edit_menu_options[choice]())
        clear_screen()
        print('Edit made ...\n')
        # display edited work log entry - confirm edit completed.
        display_entry(match)
    else:
        edit_entry(match)

    # give the user an option to edit the work log again.
    if edit_further():
        edit_entry(match)


def valid_edit_menu_choice(choice):
    # check a chosen editing option is valid
    return True if choice in edit_menu_options.keys() else False


def edit_further():
    # confirm if further editing is required.
    if input('\nDo you wish to edit the entry further? [y/N]').lower().strip() \
            != 'y':
        return False
    else:
        True


def delete_entry(match):
    '''Allows user to delete task entry'''

    # delete an entry on confirmation
    if confirm_delete(input('Confirm deletion [y/N]')):
        t.delete(match)
        print('Worklog entry deleted')
    else:
        print("Deletion cancelled")


def confirm_delete(delete):
    # confirmation that an entry is to be deleted.
    return True if delete.lower().strip() == 'y' else False


def clear_screen():
    '''Clears the screen'''
    os.system('cls' if os.name == 'nt' else 'clear')


def quit_program():
    '''Quit the program'''
    sys.exit()


main_menu_options = OrderedDict([
    ('a', add_entry),
    ('b', search_menu),
    ('c', quit_program)
])

search_menu_options = OrderedDict([
    ('a', find_from_list_of_names),
    ('b', find_by_name),
    ('c', find_from_list_of_dates),
    ('d', find_from_range_of_dates),
    ('e', find_by_time_spent),
    ('f', find_from_term),
    ('g', main_menu)
])

edit_menu_options = OrderedDict([
    ('a', get_date),
    ('b', get_title),
    ('c', get_time_spent),
    ('d', get_notes)
])

if __name__ == '__main__': main_menu()

