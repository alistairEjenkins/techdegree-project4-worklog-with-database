import unittest
import re
import string
import datetime


from unittest.mock import patch
from models import Entry

from worklog import Worklog
from tasks import Tasks

test1 = {'name' : 'test name1',
	'date' : '12/12/1212',
	'title' : 'test title1',
	'time_spent' : 12,
	'notes' : 'test notes1'}

test2 = {'name' : 'test name2',
	'date' : '13/12/1212',
	'title' : 'test title1',
	'time_spent' : 12,
	'notes' : 'test notes1'}

test3 = {'name' : 'test name2',
	'date' : '13/12/1212',
	'title' : 'test qqq',
	'time_spent' : 12,
	'notes' : 'test qqq'}

test4 = {'name' : 'test name3',
	'date' : '14/12/1212',
	'title' : 'test qqq',
	'time_spent' : 45,
	'notes' : 'None'}

test5 = {'name' : 'test name3',
	'date' : '15/12/1212',
	'title' : 'test title2',
	'time_spent' : 45,
	'notes' : 'test notes2'}

test6 = {'name' : 'test name3',
	'date' : '15/12/1212',
	'title' : 'test title2',
	'time_spent' : 45,
	'notes' : 'test notes2'}

test7 = {'name' : 'zzzzz',
	'date' : '10/10/1010',
	'title' : 'zzzzz',
	'time_spent' : 100,
	'notes' : 'zzzzz'}

tests = [test1, test2, test3, test4, test5, test6]

wl = Worklog()
t = Tasks()

class WorklogTests(unittest.TestCase):
	
	def setUp(self):
	
		for test in tests:
			t.add_entry(test)
	
	def test_validate_main_menu_choice(self):
	
		for choice in string.ascii_letters:
			if choice in ['a','b','c']:
				self.assertTrue(wl.valid_main_menu_choice(choice))
			else:
				self.assertFalse(wl.valid_main_menu_choice(choice))
	
	def test_validate_search_menu_choice(self):
	
		for choice in string.ascii_letters:
			if choice in ['a','b','c','d','e','f','g']:
				self.assertTrue(wl.valid_search_menu_choice(choice))
			else:
				self.assertFalse(wl.valid_search_menu_choice(choice))
	
	def test_validate_edit_menu_choice(self):
	
		for choice in string.ascii_letters:
			if choice in ['a','b','c','d']:
				self.assertTrue(wl.valid_edit_menu_choice(choice))
			else:
				self.assertFalse(wl.valid_edit_menu_choice(choice))
	
	def test_get_name(self):
		with unittest.mock.patch('builtins.input', side_effect=['bob']):
			self.assertEqual(wl.get_name(), 'bob')
	
	def test_get_date(self):
		with unittest.mock.patch('builtins.input', side_effect=['12/12/1212']):
			self.assertEqual(wl.get_date(), '12/12/1212')
	
	def test_get_title(self):
		with unittest.mock.patch('builtins.input', side_effect=['test title']):
			self.assertEqual(wl.get_title(), 'test title')
	
	def test_get_time_spent(self):
		with unittest.mock.patch('builtins.input', side_effect=[12]):
			self.assertEqual(wl.get_time_spent(), 12)
	
	def test_get_notes(self):
		with unittest.mock.patch('builtins.input', side_effect=['notes']):
			self.assertEqual(wl.get_notes(), 'notes')
		with unittest.mock.patch('builtins.input', side_effect=['']):
			self.assertEqual(wl.get_notes(), 'None')
	
	def test_validate_length(self):
	
		self.assertTrue(wl.validate_length('test name', 'name'))
		self.assertFalse(wl.validate_length('', 'name'))
		self.assertTrue(wl.validate_length('test title', 'title'))
		self.assertFalse(wl.validate_length('', 'title'))
	
	def test_add_entry(self):
	
		self.assertEqual(Entry.select().count(), 6)
	
		t.add_entry(test7)
		self.assertEqual(Entry.select().count(), 7)
		test7_from_db = Entry.select().where(Entry.name == 'zzzzz')
		self.assertEqual(test7['name'],test7_from_db[0].name)
		self.assertEqual(test7['date'], test7_from_db[0].date)
		self.assertEqual(test7['title'], test7_from_db[0].title)
		self.assertEqual(test7['time_spent'], test7_from_db[0].time_spent)
		self.assertEqual(test7['notes'], test7_from_db[0].notes)
		test7_from_db[0].delete_instance()
		
	def test_employees(self):
	
		# generate a set of all names in test data
		names1 = set()
		for test in tests:
			names1.add(test['name'])
	
		# generate a list of unique employee names by searching the database
		names2 = []
		matches = t.employees()
		for match in matches:
			names2.append(match.name)
	
		names1 = list(names1)
	
		self.assertEqual(names1.sort(), names2.sort())
	
	def test_dates(self):
	
		# generate a set of all dates in test data
		dates1 = set()
		for test in tests:
			dates1.add(test['date'])
	
		# generate a list of unique worklog dates by searching the database
		dates2 = []
		matches = t.dates()
		for match in matches:
			dates2.append(match.date)
	
		dates1 = list(dates1)
	
		self.assertEqual(dates1.sort(), dates2.sort())
	
	def test_entry_by_name(self):
	
		name = 'test name1'
	
		entries1 = []
		for test in tests:
			if test['name'] == name:
				entries1.append([str(value) for value in test.values()])
	
		entries2 = []
		for entry in t.entry_by_name(name):
			entries2.append([entry.name,entry.date,entry.title,
							 entry.time_spent, entry.notes])
	
		self.assertEquals(entries1.sort(), entries2.sort())
	
	def test_entry_by_date(self):
	
		date = '12/12/1212'
	
		entries1 = []
		for test in tests:
			if test['date'] == date:
				entries1.append([str(value) for value in test.values()])
	
		entries2 = []
		for entry in t.entry_by_date(date):
			entries2.append([entry.name, entry.date, entry.title,
							 entry.time_spent, entry.notes])
	
		self.assertEqual(entries1.sort(), entries2.sort())
	
	def test_entry_by_time_spent(self):
	
		time_spent = '12'
	
		entries1 = []
		for test in tests:
			if test['time_spent'] == time_spent:
				entries1.append([str(value) for value in test.values()])
	
		entries2 = []
		for entry in t.entry_by_time_spent(time_spent):
			entries2.append([entry.name, entry.date, entry.title,
							 entry.time_spent, entry.notes])
	
		self.assertEquals(entries1.sort(), entries2.sort())
	
	def test_range_of_dates(self):
	
		start_date, end_date = '12/12/1212','14/12/1212'
	
		dates1 = set()
		for test in tests:
			for date in self.daterange(start_date, end_date):
				if test['date'] == date.strftime('%d/%m/%Y'):
					dates1.add(date)
	
		dates2 = []
		for entry in t.range_of_dates(start_date, end_date):
			dates2.append(entry.date)
	
		dates1 = list(dates1)
	
		self.assertEqual(dates1.sort(), dates2.sort())
	
	def daterange(self, start_date, end_date):
		# generator function, yielding a range of dates to be searched over.
		start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
		end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')
		for day in range(int((end_date - start_date).days + 1)):
			yield start_date + datetime.timedelta(day)
	
	def test_employees_contains(self):
	
		pattern = 'test'
		names1 = set(test['name'] for test in tests if re.search(pattern,
																 test['name']))
	
		names2 = [entry.name for entry in t.employees_contains(pattern)]
	
		names1 = list(names1)
	
		self.assertEqual(names1.sort(), names2.sort())
	
	
	def test_entry_by_term(self):
	
		pattern = 'test'
	
		entries1 = []
		for test in tests:
			if re.search(pattern, test['title']) or re.search(pattern,
															  test['notes']
															  ):
				entries1.append([str(value) for value in test.values()])
	
		entries2 = []
		for entry in t.entry_by_term(pattern):
			entries2.append([entry.name, entry.date, entry.title,
							 entry.time_spent, entry.notes])
	
		self.assertEquals(entries1.sort(), entries2.sort())
	
	
	def test_match_exists(self):

		self.assertTrue(wl.match_exists(t.entry_by_name('test '
														 'name1')))
		self.assertFalse(wl.match_exists(t.entry_by_name('error')))
	
	def test_page_menu(self):
	
		self.assertEqual(wl.page_menu(t.entry_by_name('test name1'), 0), 'edr')
		self.assertNotEqual(wl.page_menu(t.entry_by_name('test name1'), 0),
							'nedr')
		self.assertEqual(wl.page_menu(t.entry_by_name('test name2'), 0),
							'nedr')
		self.assertNotEqual(wl.page_menu(t.entry_by_name('test name2'), 1),
							'nedr')
		self.assertEqual(wl.page_menu(t.entry_by_name('test name3'), 0),
							'nedr')
		self.assertEqual(wl.page_menu(t.entry_by_name('test name3'), 1),
							'npedr')
		self.assertEqual(wl.page_menu(t.entry_by_name('test name3'), 2),
						 'pedr')
	
	def test_edit_table(self):
	
		entry = Entry.select().where(Entry.name == 'test name1')
		print(entry[0].name)
		updates = {'a' : '01/01/0101', 'b' : 'aaaaa', 'c': 1, 'd': 'aaaaa'}
		for selection, new_info in updates.items():
			t.edit_table(entry[0], selection, new_info)
	
		self.assertEqual(entry[0].date, updates['a'])
		self.assertEqual(entry[0].title, updates['b'])
		self.assertEqual(entry[0].time_spent, updates['c'])
		self.assertEqual(entry[0].notes, updates['d'])
	
	
	def test_delete(self):
	
		#t.add_entry(test7)
		entries = Entry.select()
		self.assertEqual(entries.count(), 6)
		entries[4].delete_instance()
		self.assertFalse(Entry.select().where(Entry.name == 'test '
															'name4').exists())
		self.assertEqual(entries.count(), 5)
	
	def tearDown(self):
	
		for test in Entry.select():
			test.delete_instance()
	
	
if __name__ == '__main__':
	unittest.main()