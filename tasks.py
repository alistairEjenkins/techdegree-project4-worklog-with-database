
from models import Entry, database


class Tasks():

    def initialise(self):

        database.connect()
        database.create_tables([Entry], safe=True)

    def add_entry(self, entry):

        worklog = Entry(**entry)
        worklog.save()

    def has_entries(self):

        entries = self.employees()
        return True if entries.count() >= 1 else False

    def employees(self):

        return Entry.select(Entry.name).distinct()

    def employees_contains(self, name):

        return Entry.select(Entry.name).where(Entry.name.contains(
            name)).distinct()

    def entry_by_name(self, name):

        return Entry.select().where(
            Entry.name == name)

    def dates(self):

        return Entry.select(Entry.date).distinct()

    def range_of_dates(self, first_date, last_date):

        return Entry.select(Entry.date).where(
            Entry.date.between(first_date, last_date)).distinct()

    def entry_by_date(self, date):

        return Entry.select().where(Entry.date == date)

    def entry_by_time_spent(self, time_spent):

        return Entry.select().where(Entry.time_spent == time_spent)

    def entry_by_term(self, term):

        return Entry.select().where(Entry.title.contains(term) |
                                    Entry.notes.contains(term))

    def edit_table(self, match, field, new_info):

        if field == 'a':
            match.date = new_info
        elif field == 'b':
            match.title = new_info
        elif field == 'c':
            match.time_spent = new_info
        else:
            match.notes = new_info
        match.save()

    def delete(self, match):

        match.delete_instance(recursive=True)
