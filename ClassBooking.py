import datetime as dt
import sqlite3
from AirbnbParent import UpdateTable

conn = sqlite3.connect("airbnb.db")
c = conn.cursor()

# ********************************************************************************************************************#
# ********************************Uses Inheritance method from AirbnbParent module************************************#
# ********************************************************************************************************************#

# Class Booking: SQL wrapper for SQL operation update Bookings.
# Allows booking only if entered number of days is > minimum number of days
class Booking(UpdateTable):

    @staticmethod
    # Function to book stays takes booking name, number of people, number of days, stay id to book as positional
    # arguments returns nothing
    def add_bookings(booking_name, number_of_people, number_of_days, id):

        # Check if entered id is available in stays table
        c.execute("SELECT COUNT(*) FROM stays WHERE id=:id", {'id': id})
        a = c.fetchall()[0]

        if a[0] > 0:
            # Check minimum nights condition satisfies for the stay to book
            c.execute("SELECT minimum_nights FROM stays WHERE id=:id", {'id': id})
            x = c.fetchall()[0]

            x = list(x)
            if number_of_days > x[0]:

                # book the stay if minimum nights condition passes
                c.execute("""SELECT a.id+1 bookingid, a.id, a.name name, :booking_name, :number_of_members, 
                                :booking_date, :booked_for_days
                             FROM stays a WHERE a.id=:id""",
                          {'booking_name': booking_name, 'number_of_members': number_of_people,
                           'booking_date': dt.date.today(), 'booked_for_days': number_of_days, 'id': id})
                details = c.fetchall()
                # Invoke insert_table function from AirbnbParent
                # Inherited method from AirbnbParent
                UpdateTable.insert_table('bookings', ' VALUES(?, ?, ?, ?, ?, ?, ? )', details[0])
                conn.commit()

            else:
                # print if entered no of days to book is less than allowed number of nights.
                print("You have to book for minimum ", x[0], "nights in this stay, please book for more nights or book "
                                                             "other stays")
        else:
            print("Enter correct stay id")
        return


conn.commit()
