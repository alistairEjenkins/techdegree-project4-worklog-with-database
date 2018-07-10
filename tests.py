import unittest
import string
import worklog

from unittest.mock import patch

from models import Entry
from tasks import Tasks


# test data
test1 = {'name': 'test name1',
         'date': '12/12/1212',
         'title': 'test title1',
         'time_spent': 12,
         'notes': 'test notes1'}

test2 = {'name': 'test name2',
         'date': '13/12/1212',
         'title': 'test title1',
         'time_spent': 12,
         'notes': 'test notes1'}

test3 = {'name': 'test name2',
         'date': '13/12/1212',
         'title': 'test qqq',
         'time_spent': 12,
         'notes': 'test qqq'}

test4 = {'name': 'test name3',
         'date': '14/12/1212',
         'title': 'test qqq',
         'time_spent': 45,
         'notes': 'None'}

test5 = {'name': 'test name3',
         'date': '15/12/1212',
         'title': 'test title2',
         'time_spent': 45,
         'notes': 'test notes2'}

test6 = {'name': 'test name3',
         'date': '15/12/1212',
         'title': 'test title2',
         'time_spent': 45,
         'notes': 'test notes2'}

test7 = {'name': 'test name4',
         'date': '15/12/1212',
         'title': 'test title2',
         'time_spent': 45,
         'notes': 'test notes2'}

tests = [test1, test2, test3, test4, test5, test6, test7]

t = Tasks()


class WorklogTests(unittest.TestCase):

    def setUp(self):
        # add test data to database
        for test in tests:
            t.add_entry(test)

    def test_main_menu_choices(self):
        self.assertTrue(worklog.valid_main_menu_choice('a'))
        self.assertTrue(worklog.valid_main_menu_choice('b'))
        self.assertTrue(worklog.valid_main_menu_choice('c'))
        self.assertFalse(worklog.valid_main_menu_choice('d'))

    def test_add_entry(self):
        with unittest.mock.patch('builtins.input',
                                 side_effect=['bob', '12/12/1212',
                                              'bobs title', 12,
                                              'bobs notes']):
            self.assertEqual(worklog.add_entry(),
                             'The entry has been added...''\nWhat would you '
                             'like to do?')

    def test_get_name(self):
        with unittest.mock.patch('builtins.input', side_effect=['bob']):
            self.assertTrue(worklog.get_name(), 'bob')

    def test_get_date(self):
        with unittest.mock.patch('builtins.input', side_effect=['12/12/1212']):
            self.assertTrue(worklog.get_date(), '12/12/1212')

    def test_get_title(self):
        with unittest.mock.patch('builtins.input', side_effect=['bobs log']):
            self.assertTrue(worklog.get_title(), 'bobs log')

    def test_get_time_spent(self):
        with unittest.mock.patch('builtins.input', side_effect=['1234']):
            self.assertTrue(worklog.get_time_spent(), 1234)

    def test_get_notes(self):
        with unittest.mock.patch('builtins.input', side_effect=['']):
            self.assertTrue(worklog.get_notes(), 'None')
        with unittest.mock.patch('builtins.input', side_effect=['bobs notes']):
            self.assertTrue(worklog.get_notes(), 'bobs notes')

    def test_validate_length(self):
        self.assertTrue(worklog.validate_length('sss', 'name'))

    def test_valid_search_menu_choice(self):
        self.assertTrue(worklog.valid_search_menu_choice('a'))
        self.assertTrue(worklog.valid_search_menu_choice('b'))
        self.assertTrue(worklog.valid_search_menu_choice('c'))
        self.assertTrue(worklog.valid_search_menu_choice('d'))
        self.assertTrue(worklog.valid_search_menu_choice('e'))
        self.assertTrue(worklog.valid_search_menu_choice('f'))
        self.assertTrue(worklog.valid_search_menu_choice('g'))
        self.assertFalse(worklog.valid_search_menu_choice('h'))

    def test_find_from_list_of_names(self):
        with unittest.mock.patch('builtins.input', side_effect=['test name1',
                                                                'd', 'n']):
            self.assertEqual(worklog.find_from_list_of_names(), 'Actions'
                                                                ' complete.')

    def test_find_from_name(self):
        with unittest.mock.patch('builtins.input', side_effect=['te', 'test '
                                                                'name1',
                                                                'd', 'n']):
            self.assertEqual(worklog.find_by_name(), 'Actions complete.')

    def test_find_from_list_of_dates(self):
        with unittest.mock.patch('builtins.input', side_effect=['15/12/1212',
                                                                'd', 'n']):
            self.assertEqual(worklog.find_from_list_of_dates(), 'Actions'
                                                                ' complete.')

    def test_find_from_range_of_dates(self):
        with unittest.mock.patch('builtins.input', side_effect=['12/12/1212',
                                                                '15/12/1212',
                                                                '13/12/1212',
                                                                'd', 'y']):
            self.assertEqual(worklog.find_from_range_of_dates(), 'Actions '
                                                                 'complete.')

    def test_valid_date_range(self):
        self.assertEqual(worklog.valid_date_range('12/12/1212', '14/12/1212'),
                                                 ('12/12/1212', '14/12/1212'))

    def test_find_by_time_spent(self):
        with unittest.mock.patch('builtins.input', side_effect=['12','e',
                                                                'c', '15',
                                                                'n']):
            self.assertEqual(worklog.find_by_time_spent(), 'Actions complete.')

    def test_find_from_term(self):
        with unittest.mock.patch('builtins.input', side_effect=['te',
                                                                'd', 'n']):
            self.assertEqual(worklog.find_from_term(), 'Actions complete.')

    def test_match_exists(self):
        self.assertTrue(worklog.match_exists(t.entry_by_name('test name1')))

    def test_page_menu(self):
        self.assertEqual(worklog.page_menu(t.entry_by_name('test name1'), 0),
                         'edr')
        self.assertNotEqual(worklog.page_menu(t.entry_by_name('test name1'), 0),
                            'nedr')
        self.assertEqual(worklog.page_menu(t.entry_by_name('test name2'), 0),
                         'nedr')
        self.assertNotEqual(worklog.page_menu(t.entry_by_name('test name2'), 1),
                            'nedr')
        self.assertEqual(worklog.page_menu(t.entry_by_name('test name3'), 0),
                     'nedr')
        self.assertEqual(worklog.page_menu(t.entry_by_name('test name3'), 1),
                         'npedr')
        self.assertEqual(worklog.page_menu(t.entry_by_name('test name3'), 2),
                         'pedr')

    def test_edit_entry(self):
        entry = t.entry_by_name('test name1')
        with unittest.mock.patch('builtins.input',
                                 side_effect=['b', 'edited title', 'n']):
            worklog.edit_entry(entry[0])
            self.assertEqual(entry[0].title, 'edited title')

    def test_validate_edit_menu_choice(self):
        for choice in string.ascii_letters:
            if choice in ['a', 'b', 'c', 'd']:
                self.assertTrue(worklog.valid_edit_menu_choice(choice))
            else:
                self.assertFalse(worklog.valid_edit_menu_choice(choice))

    def test_edit_further(self):
        with unittest.mock.patch('builtins.input', side_effect=['n']):
            self.assertFalse(worklog.edit_further())

    def test_delete_entry(self):
        entries = Entry.select()
        with unittest.mock.patch('builtins.input', side_effect=['y']):
            worklog.delete_entry(entries[6])
        self.assertFalse(worklog.match_exists(t.entry_by_name('test name4')))

    def test_confirm_delete(self):
        self.assertTrue(worklog.confirm_delete('y'))
        self.assertFalse(worklog.confirm_delete('n'))

    def tearDown(self):
        # delete all test data
        entries = t.employees_contains('test')
        for entry in entries:
            t.delete(entry)


if __name__ == '__main__':
    unittest.main()

