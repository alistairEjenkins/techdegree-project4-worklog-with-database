import sys
import os
import datetime

from collections import OrderedDict
from tasks import Tasks


t = Tasks()
t.initialise()

class Worklog():

    def __init__(self):

        self.main_menu_options = OrderedDict([
            ('a', self.add_entry),
            ('b', self.search_menu),
            ('c', self.quit_program)
        ])

        self.search_menu_options = OrderedDict([
            ('a', self.find_from_list_of_names),
            ('b', self.find_by_name),
            ('c', self.find_from_list_of_dates),
            ('d', self.find_from_range_of_dates),
            ('e', self.find_by_time_spent),
            ('f', self.find_from_term),
            ('g', self.main_menu)
        ])

        self.edit_menu_options = OrderedDict([
            ('a', self.get_date),
            ('b', self.get_title),
            ('c', self.get_time_spent),
            ('d', self.get_notes)
        ])


    def main_menu(self):
        '''Main menu'''

        self.clear_screen()
        print('WORK LOG\nWhat would you like to do?')
        for option, desc in self.main_menu_options.items():
            print('{}) {}'.format(option, desc.__doc__))
        choice = input('> ').lower().strip()
        if self.valid_main_menu_choice(choice):
            self.main_menu_options[choice]()
        else:
            self.main_menu()

    def valid_main_menu_choice(self, choice):

        return True if choice in self.main_menu_options.keys() else False

    def add_entry(self):
        '''Add an entry to the database'''

        t.add_entry({'name': self.get_name(),
                     'date': self.get_date(),
                     'title': self.get_title(),
                     'time_spent': self.get_time_spent(),
                     'notes': self.get_notes()})
        input('The entry has been added. [Enter] to return to the menu.')
        self.main_menu()

    def get_name(self):
        '''Enter a name'''
        print(self.get_name.__doc__)
        name = input('> ').rstrip()
        return name if self.validate_length(name, 'name') else self.get_name()

    def get_date(self):
        '''Enter a date (DD/MM/YYYY)'''
        print(self.get_date.__doc__)
        date = input('> ').strip()
        try:
            datetime.datetime.strptime(date, '%d/%m/%Y')
        except ValueError:
            self.get_date()
        else:
            return date

    def get_title(self):
        '''Enter a title'''
        print(self.get_title.__doc__)
        title = input('> ').rstrip()
        return title if self.validate_length(title, 'title') else \
            self.get_title()

    def get_time_spent(self):
        '''Enter time spent, rounded to nearest minute.'''
        print(self.get_time_spent.__doc__)
        try:
            time_spent = int(input('> '))
        except ValueError:
            self.get_time_spent()
        else:
            return time_spent

    def get_notes(self):
        '''Enter notes, optional - leave blank as required.'''
        print(self.get_notes.__doc__)
        notes = input('> ').rstrip()
        return notes + 'None' if len(notes) == 0 else notes

    def validate_length(self, s, desc):

        return True if len(s) > 0 else print('No {} entered. Please try '
                                             'again.'.format(desc))

    def search_menu(self):
        '''Search Entries'''
        self.clear_screen()
        print('How do you want to search?')
        for option, desc in self.search_menu_options.items():
            print('{}) {}'.format(option, desc.__doc__))
        choice = input('> ').lower().strip()
        self.search_menu_options[choice]() if self.valid_search_menu_choice(
                choice) else self.search_menu()

    def valid_search_menu_choice(self, choice):

        return True if choice in self.search_menu_options.keys() else False

    def find_from_list_of_names(self):
        '''from the list of Employees with worklogs'''
        self.choose_from_unique_field_values([entry.name for entry in t.employees()], 'name')

    def find_by_name(self):
        '''by employee name, including partial matches'''
        self.choose_from_unique_field_values([entry.name for entry in
                                              t.employees_contains(self.get_name())], 'name')

    def find_from_list_of_dates(self):
        '''from a list of unique log dates'''
        self.choose_from_unique_field_values([entry.date for entry in t.dates()], 'date')

    def find_from_range_of_dates(self):
        '''from a range of dates.'''
        self.clear_screen()
        print('Start date - ',end='')
        start_date = self.get_date()
        print('End date - ',end='')
        end_date = self.get_date()
        self.find_from_range_of_dates() if start_date >= end_date else \
            self.choose_from_unique_field_values([entry.date for entry in
                                                  t.range_of_dates(start_date, end_date)], 'date')

    def find_by_time_spent(self):
        '''from time spent'''
        self.page_worklogs(
            t.entry_by_time_spent(self.get_time_spent()))

    def find_from_term(self):
        '''from a term in worklog title or notes.'''
        print('Please enter the term you wish to search by.')
        self.page_worklogs(t.entry_by_term(input('> ')))

    def choose_from_unique_field_values(self, values, field):

        if len(values) == 0:
            input('There are no entries. [enter] to return to main menu')
            self.main_menu()

        self.clear_screen()
        print('Below is a list of {}s to choose from:\n'.format(field))
        for entry in values:
            print(entry)
        if input('\n[Enter] to input your chosen date, [r]eturn to search '
                     'menu.').lower().strip() == 'r':
            self.search_menu()
        choice = self.get_name() if field == 'name' else self.get_date()
        if choice not in values: self.choose_from_unique_field_values(values,
                                                                     field)
        self.page_worklogs(t.entry_by_name(choice)) if field == 'name' else \
            self.page_worklogs(t.entry_by_date(choice))

    def page_worklogs(self, matches, index=0):

        if not self.match_exists(matches):
            input('There are no matches. [enter] to return to search options.')
            self.search_menu()

        self.clear_screen()
        self.display_entry(matches[index])
        page_menu_options = self.page_menu(matches, index)
        choice = input('> ')
        if choice not in page_menu_options: self.page_worklogs(matches, index)

        page_menu_selection = {'n': lambda : self.page_worklogs(matches,
                                                               index+1),
                    'p': lambda : self.page_worklogs(matches, index-1),
                    'e': lambda : self.edit_entry(matches[index]),
                    'd': lambda : self.delete_entry(matches[index]),
                    'r': lambda : self.search_menu()}
        page_menu_selection[choice]()

    def match_exists(self, matches):

        return False if not matches.exists() else True

    def page_menu(self, matches, index):

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
        print(page_options.format(**options))
        return page_options.replace('{','').replace('}','')

    def display_entry(self, match):

        print('Name: {}\nDate : {}\nTitle : {}\nTime Spent : {}\nNotes: {}'.
              format(match.name, match.date, match.title,match.time_spent,
                     match.notes))

    def edit_entry(self, match):

        self.clear_screen()
        self.display_entry(match)

        print('Select which field you wish to update.')
        for option, desc in self.edit_menu_options.items():
            print('{}) {}'.format(option, desc.__doc__))
        choice = input('> ')
        if self.valid_edit_menu_choice(choice):
            t.edit_table(match, choice, self.edit_menu_options[choice]())
            self.clear_screen()
            print('Edit made ...\n')
            self.display_entry(match)
        else:
            self.edit_entry(match)

        self.search_menu() if input('\nDo you wish to edit the entry further? [y/N]')!= 'y'.lower().strip() else self.edit_entry(match)

    def valid_edit_menu_choice(self, choice):

        return True if choice in self.edit_menu_options.keys() else False

    def delete_entry(self, match):
        '''Allows user to delete task entry'''
        if input('Confirm deletion [y/N]') == 'y'.lower().strip():
            t.delete(match)
            print('Worklog entry deleted')
        else:
            print("Deletion cancelled")
        self.search_menu()

    def clear_screen(self):
        '''Clears the screen'''
        os.system('cls' if os.name == 'nt' else 'clear')

    def quit_program(self):
        '''Quit the program'''
        sys.exit()


def main():
    wl = Worklog()
    wl.main_menu()


if __name__ == '__main__': main()
