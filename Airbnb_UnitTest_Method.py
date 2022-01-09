import sqlite3

conn = sqlite3.connect("airbnb.db")
conn.execute("PRAGMA foreign_keys = 1")
c = conn.cursor()


# Unit Testing function to Test add_bookings function, takes test id as arguments
# returns test results
def unit_testing(test_id):
    # Check if entered id is available in stays table
    c.execute("SELECT COUNT(*) FROM stays WHERE id=:id", {'id': test_id})
    a = c.fetchall()[0]
    if a[0] > 0:
        # Check if the entered id is successfully added to bookings table
        c.execute("SELECT COUNT(*) FROM bookings WHERE booking_id=:id", {'id': test_id + 1})
        a = c.fetchall()[0]
        if a[0] > 0:
            # Check if the booking id auto created matching with manually created id as per the logic
            c.execute("SELECT booking_id FROM bookings WHERE booking_id=:id", {'id': test_id + 1})
            x = c.fetchall()[0]
            if x[0] == test_id + 1:
                # print pass if actual booking id matches with expected booking id
                print('Test Passed')
                print('____________')
            else:
                # print fail if actual booking id does not match with expected booking id
                print('Test Failed')
                print('____________')
        else:
            # print fail if actual booking id does not match with expected booking id
            print('Test Failed')
            print('____________')
    else:
        # print fail if entered id is not available in stay table
        print('Test Failed')
        print('____________')
