import sqlite3

conn = sqlite3.connect("airbnb.db")
conn.execute("PRAGMA foreign_keys = 1")
c = conn.cursor()


# ********************************************************************************************************************#
# ********************************Parent Method has insert_table method***********************************************#
# ********************************************************************************************************************#


# Reusable UpdateTable Class to do database operations has one class method.
class UpdateTable(object):

    @classmethod
    # insert_table method takes table name, columns and new records to insert as positional arguments # returns nothing
    def insert_table(cls, table, columns, new_records):
        x = 'INSERT INTO '
        y = table
        z = columns
        try:
            c.execute(x + y + z, new_records)
            conn.commit()
            print(f'New ', y, ' details ', new_records[1:2], ' has been added to the table; \n your ', y, ' id : ',
                  new_records[0:1])
        # capture KeyError
        except KeyError as e:
            print(e, 'KeyError occurred below results may not be valid')

    # Commit
    conn.commit()
