# Airbnb-Bookings

Description
An Airbnb dataset was provided, which contained details of Airbnb listings in Singapore. Expectation was to design classes and functions in Python and to design a relational database with normalized tables out of the given dataset. clean up the raw dataset and perform various functions using pandas, sqlite and object-oriented programming concepts.

History
initial Version Mar, 6;
Draft Version 1 Mar, 13;
final Version Mar, 15;
Installation
1. Import Sqlite3
2. Import pandas
Author
name: Srinivas Srinivasan Balasubramanian
Student no.: 40317448
How to use?
Run - Airbnb_main.py - ## to get complete output

There are nine python files available in the project folder.

i. Airbnb_main.py
    run this python file to get the complete output.
    Contains: - 
    * Function to establish the connectin with database using Sqlite3.
    * Airbnb parent class with four Child class for python implementation._using inheritance relationship_
        * contains a method to drop duplicates from raw data.
        Child Class
            * Accommodation
            * StaysReview
            * Landlord
            * Neighbourhood
ii AirbnbParent.py Defined class within other classes
    * Contains update table class
        * has insert table method
    Acts as a parent class for other modules.
iii ClassSelect.py
    * SQL wrapper class for SQL operations.
    * Select class - contains 3 methods for search operations.
iv ClassUpdate.py
    * SQL wrapper class for SQL operations.
    * Update class - contains 3 classes for insert operation.
    * Update Class uses a defined class from AirbnbParent.
V ClassBooking.py
    * SQL wrapper class for SQL operations.
    * Experimental clss uses other tables to join and generate bookings.
Vi ClassDelete.py
    * SQL wrapper class for SQL operations.
    * Delete class - contains 1 module for delete operations.
Vii. Airbnb_UnitTest_Method.py
    contains unit testing method & update table method.
Viii. CreateTablecommands.py
    * contains create table method
    * contains SQLs to create tables.
iX. drop_tables.py
    **only run if you want to drop all tables and redo from step one.** - drops all tables in the database.
Source Code
Airbnb_main.py
Run this file to integrate all modules.
Import library Functions
import sqlite3
from sqlite3 import Error
import pandas as pd
Import functions from other modules
from ClassBooking import Booking
from ClassSelect import Select
from ClassDelete import Delete
from ClassUpdate import UpdateStays
from ClassUpdate import UpdateHost
from ClassUpdate import UpdateCounty
from Airbnb_UnitTest_Method import unit_testing
from CreateTableCommands import create_table
from CreateTableCommands import create_county
from CreateTableCommands import create_acc
from CreateTableCommands import create_review
from CreateTableCommands import create_host
from CreateTableCommands import create_bookings
Database name
database = "airbnb.db"
************Creates Connection#
Function to Create Database connection takes database name as positional argument
returns conn element
def create_connection(airbnb):
    conn = None
    try:
        conn = sqlite3.connect(airbnb)
        conn.text_factory = str
        return conn
    except Error as e:
        print(e)
        return conn
Create database connection
conn = create_connection(database)
Set FOREIGN KEY constraint OFF
conn.execute("PRAGMA foreign_keys = 0")
open Cursor
c = conn.cursor()
***************#
*********Cleanses CSV & Loads Data#
Parent Class Airbnb has four child classes AND a method to remove duplicates.
class Airbnb(object):

    def __init__(self):
        # Import the dataset into the program as a data frame.
        self.read_data = pd.read_csv('listings.csv', header=0)

        # read portion of data from dataframe # Inherited attribute
        self.listings = self.read_data.loc[:, ["id", "name", "latitude", "longitude", "room_type", "price",
                                               "minimum_nights", "availability_365", "calculated_host_listings_count",
                                               "host_id", "neighbourhood"]]

        self.stays_review = self.read_data.loc[:, ["id", "number_of_reviews", "last_review", "reviews_per_month"]]

        self.landlord = self.read_data.loc[:, ["host_id", "host_name"]]

        self.neighbourhood = self.read_data.loc[:, ["neighbourhood", "neighbourhood_group"]]
    
    def drop_duplicates(self, duplicates):
        # Data cleansing - Drop duplicate records - pass data frame with duplicate records
        listings = duplicates.drop_duplicates(keep='first')
        return listings
Accommodation class inherited from Airbnb parent class has one method
class Accommodation(Airbnb):

    # stays method uses attributes from Airbnb class takes no arguments # returns nothing
    def stays(self):
        # Data cleansing - Drop duplicate records using method from parent class and load it to tables
        Airbnb.drop_duplicates(self, self.listings).to_sql("stays", conn, if_exists='append', index=False)
        # Export portion of data to csv
        Airbnb.drop_duplicates(self, self.listings).to_csv("stays.csv", index=False)
        return
StaysReview class inherited from Airbnb parent class has one method
class StaysReview(Airbnb):

    # review method uses attributes from Airbnb class takes no arguments # returns nothing
    def review(self):
        # Data cleansing - Drop duplicate records using method from parent class and load it to tables
        stays_review = Airbnb.drop_duplicates(self, self.stays_review)
        # Dropped unwanted data from the dataset
        stays_review = stays_review[stays_review.number_of_reviews > 0]
        # Populate portion of data to normalized table
        stays_review.to_sql("review", conn, if_exists='append', index=False)
        # Export portion of data to csv
        stays_review.to_csv("stays_review.csv", index=False)
        return
Landlord class inherited from Airbnb parent class has one method
class Landlord(Airbnb):

    # host method uses attributes from Airbnb class takes no arguments # returns nothing
    def host(self):
        # Data cleansing - Drop duplicate records using method from parent class and load it to tables
        Airbnb.drop_duplicates(self, self.landlord).to_sql("host", conn, if_exists='append', index=False)
        # Export portion of data to csv
        Airbnb.drop_duplicates(self, self.landlord).to_csv("stays_review.csv", index=False)
        return
Neighbourhood class inherited from Airbnb parent class has one method
class Neighbourhood(Airbnb):

    # county method uses attributes from Airbnb class takes no arguments # returns nothing
    def county(self):
        # Data cleansing - Drop duplicate records using method from parent class and load it to tables
        Airbnb.drop_duplicates(self, self.neighbourhood).to_sql("county", conn, if_exists='append', index=False)
        # Export portion of data to csv
        Airbnb.drop_duplicates(self, self.neighbourhood).to_csv("stays_review.csv", index=False)
        return
Commit
conn.commit()

stays = Accommodation()
review = StaysReview()
host = Landlord()
county = Neighbourhood()
Commit
conn.commit()
****************#
create accommodation tables
create_table(create_acc)
create review tables
create_table(create_review)
create host tables
create_table(create_host)
create county tables
create_table(create_county)
Create bookings tables
create_table(create_bookings)

conn.commit()
try:
    stays.stays()
    review.review()
    host.host()
    county.county()
    print("-------------------------------------------------------------------------------------------"
          "\\n     |||#*#*#*#*---------Data loaded into normalized tables!!!--------*#*#*#*#|||\\n"
          "-------------------------------------------------------------------------------------------")
except Error as e:

    print("-------------------------------------------------------------------------------------------"
          "\\n               |||#*#*#*#*---------Data loaded already!!!--------*#*#*#*#|||\\n"
          "|||#*#*#*#*---------Error message:", e, "!!!--------*#*#*#*#|||\\n"
          "-------------------------------------------------------------------------------------------")
****************#
search = Select()
remove = Delete()
update_stays = UpdateStays()
update_host = UpdateHost()
update_county = UpdateCounty()
booking = Booking()
Commit
conn.commit()
****************#
Test Data & Test Scripts*****#
**Class Select***#
Test Data to test budget stays method
county = ['Woodlands', 'River Valley', 'Sembawang']  # neighbourhood
budget_price = [10, 20, 30]
limit = 2
Test Script to test budget stays method
for i in range(len(budget_price)):
    print('____Test ', i + 1, ' budget stays____________')
    print('Test input:- county:', county[i], ',budget price', budget_price[i])
    try:
        # budget_stays_based_on_neighbourhood arguments: self, county_name, price:
        search.budget_stays_based_on_neighbourhood(county[i], budget_price[i], limit)
    except Error as e:
        print(e)
print('______________________________________________')
Test Data to test short vacation method
short_vaca_days = [2, 5, 20]
limit = 2
Test script to test short vacation method
for i in range(len(short_vaca_days)):
    print('____Test ', i + 1, ' short vacation____________')
    print('Test input:- days :', short_vaca_days[i])
    try:
        # stays_for_short_vacation arguments : days:
        search.stays_for_short_vacation(short_vaca_days[i], limit)
    except Error as e:
        print(e)
print('______________________________________________')
Test Data to test top stays method
Test Cases to check whether join between county and stays are working fine.
county = ['Woodlands', 'River Valley', 'Sembawang']  # neighbourhood
no_of_reviews = [200, 100, 150]
Test scripts to test top stays method
for i in range(len(no_of_reviews)):
    print('____Test ', i + 1, ' top stays____________')
    print('Test input:- county:', county[i], ',no of reviews:', no_of_reviews[i])
    try:
        # top_stays_in_neighbourhood county, no_of_reviews :
        search.top_stays_in_neighbourhood(county[i], no_of_reviews[i])
    except Error as e:
        print(e)
print('______________________________________________')
***Class Update**#
Test Data to test add stays method
l_id = [71907, 1111, 3333]
name = ['stay near lake', 'park view tower', 'stay with garden']
latitude = [100.76, 123.56, 111.02]
longitude = [12.9, 10.09, 11.19]
room_type = ['private', 'Entire house', 'private']
price = [12, 150, 200]
minimum_nights = [10, 15, 30]
availability_365 = [10, 365, 50]
calculated_host_listings_count = [2, 5, 30]
host_id = [11111, 1017645, 12367]
county = ['Woodlands', 'River Valley', 'Sembawang1']  # neighbourhood
Test scripts to test add stays method
for i in range(len(l_id)):
    print('____Test ', i + 1, ' add stays____________')
    print('Test input:- stayid:', l_id[i], ',name', name[i], ',latitude', latitude[i], ',longitude',
          longitude[i], ',room type', room_type[i], ',price', price[i], ',minimum nights', minimum_nights[i],
          ',availability', availability_365[i], ',host list cnt', calculated_host_listings_count[i], ',host id',
          host_id[i], ',county', county[i])
    try:
        # add_stays(self, l_id, name, latitude, longitude, room_type, price, minimum_nights, availability_365,calculated_host_listings_count,host_id, neighbourhood):
        update.add_stays(l_id[i], name[i], latitude[i], longitude[i], room_type[i], price[i], minimum_nights[i],
                         availability_365[i], calculated_host_listings_count[i], host_id[i], county[i])
    except Error as e:
        print(e)
print('______________________________________________')
Test Data to test add host method
host_id = [11111, 1017645, 22222]
host_name = ['qqqq', 'wwww', 'rrrr']
Test script to test add host method
for i in range(len(host_id)):
    print('____Test ', i + 1, ' add host____________')
    print('Test input:- host id:', host_id[i], ',host name:', host_name[i])
    try:
        update.add_host(host_id[i], host_name[i])
    except Error as e:
        print(e)
print('______________________________________________')
Test Data to test add county method
county = ['Woodlands', 'TEst1', 'TESt2']
county_group = ['GR1', 'GR2', 'GR3']
Test script to test add county method
for i in range(len(county)):
    print('____Test ', i + 1, ' add county____________')
    print('Test input:- county:', county[i], ', county group:', county_group[i])
    try:
        update.add_county(county[i], county_group[i])
    except Error as e:
        print(e)
print('______________________________________________')
Class Delete*************#
Test data to test delete review method
no_of_review = [1, 2, 3]
Test script to test delete review method
for i in range(len(no_of_review)):
    print('____Test ', i + 1, ' delete review____________')
    print('Test input:- number of reviews:', no_of_review[i])
    try:
        remove.delete_review(no_of_review[i])
    except Error as e:
        print(e)
print('______________________________________________')
Commit
conn.commit()
ClassBooking - Unit Test*****#
Unit Testing
Test Data to test add_bookings Functions
booking_name = ['Ann', 'Jack', 'Sam']
no_of_people = [2, 3, 4]
no_of_days = [92, 12, 10]
stayid = [38112762, 3811276, 49091]
Iterate the Test data
for i in range(len(no_of_people)):
    print('Test input :- Booking_name :', booking_name[i], ', no_of_people :', no_of_people[i], ', no_of_days :',
          no_of_days[i], ', Stay id :', stayid[i])
    try:
        # Invoke the add booking function to test
        booking.add_bookings(booking_name[i], no_of_people[i], no_of_days[i], stayid[i])
    # Catch exceptions
    except Error as e:
        print(e)
    # Call the unit testing function
    unit_testing(stayid[i])
CreateTableCommands.py
import sqlite3 from sqlite3 import Error

conn = sqlite3.connect("airbnb.db") c = conn.cursor()

*********Creates tables#
Reusable Function for table creation takes create table SQL as positional argument
returns nothing
def create_table(create_table_sql):
    try:
        c.execute(create_table_sql)
    except Error as e:
        print(e)

create_acc = """CREATE TABLE if NOT EXISTS stays (id int not null unique , name text, latitude real, longitude real, 
                    room_type text,price real, minimum_nights real, availability_365 real, 
                    calculated_host_listings_count real, host_id int not null,neighbourhood text,
                    PRIMARY KEY(id, host_id),
                    FOREIGN KEY(neighbourhood) REFERENCES county(neighbourhood)
                    FOREIGN KEY(host_id) REFERENCES host(host_id))"""

create_review = """CREATE TABLE if NOT EXISTS review(id int PRIMARY KEY , 
                        number_of_reviews int CHECK(number_of_reviews > 0), last_review date ,reviews_per_month real,
                        FOREIGN KEY(id) REFERENCES stays(id))"""

create_host = """CREATE TABLE if NOT EXISTS host(host_id int not null unique , host_name text,
                        PRIMARY KEY(host_id))"""

create_county = """CREATE TABLE if NOT EXISTS county (neighbourhood text, neighbourhood_group text,
                        PRIMARY KEY(neighbourhood))"""

create_bookings = """CREATE TABLE if NOT EXISTS bookings(booking_id int PRIMARY KEY, id int, name text, 
                         booking_name text , number_of_members int, booking_date date, booked_for_days int,
                         FOREIGN KEY(id) REFERENCES stays(id))"""


if __name__ == '__main__':

    print("-------------------------------------------------------------------------------------------"
          "\\n|#*#*#*#*------------Your database is created with necessary tables!!!------------*#*#*#*#|\\n"
          "-------------------------------------------------------------------------------------------")
****************#
AirbnbParent.py
import sqlite3

conn = sqlite3.connect("airbnb.db")
conn.execute("PRAGMA foreign_keys = 1")
c = conn.cursor()
****************#
Parent Method has insert_table method***************#
****************#
Reusable UpdateTable Class to do database operations has one class method.
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
            print(f'New ', y, ' details ', new_records[1:2], ' has been added to the table; \\n your ', y, ' id : ',
                  new_records[0:1])
        # capture KeyError
        except KeyError as e:
            print(e, 'KeyError occurred below results may not be valid')

    # Commit
    conn.commit()
Class Booking
    import datetime as dt
import sqlite3
from AirbnbParent import UpdateTable

conn = sqlite3.connect("airbnb.db")
c = conn.cursor()
****************#
Uses Inheritance method from AirbnbParent module****#
****************#
Class Booking: SQL wrapper for SQL operation update Bookings.
Allows booking only if entered number of days is > minimum number of days
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
Class Delete
import sqlite3

conn = sqlite3.connect("airbnb.db")
c = conn.cursor()
Class Delete: SQL wrapper for SQL operation delete has one static method
class Delete(object):

    # delete records from review table like delete negative review takes one positional argument
    @staticmethod
    def delete_review(no_of_review):

        # check for review from reviews table bases on condition
        c.execute("select count(*) from review where number_of_reviews<:no_of_review", {'no_of_review': no_of_review})
        if c.fetchone()[0] >= 1:

            c.execute("delete from review where number_of_reviews<:no_of_review", {'no_of_review': no_of_review})
            conn.commit()
            # print if removed successfully
            print(f'as per the request review with no_of_reviews less than (', str(no_of_review),
                  ') has been removed from review table')
        else:
            # return if nothing to remove
            return print("No reviews with less than ", str(no_of_review), " reviews available in review table")
Commit
conn.commit()
Class Select
import sqlite3

conn = sqlite3.connect("airbnb.db")
c = conn.cursor()
Class Select: SQL wrapper for SQL operation Select has three static method
class Select(object):

    @staticmethod
    # search budget stays take county name and price as positional arguments and limit as optional argument
    # returns search results
    def budget_stays_based_on_neighbourhood(county_name, price, limit=5):
        # Check if stays available for entered neighbourhood and price
        c.execute("""select count(*) from stays where price<:price and neighbourhood=:neighbourhood limit :limit""",
                  {'price': price, 'neighbourhood': county_name, 'limit': limit})
        if c.fetchone()[0] == 0:
            # print if no stays available for the input
            print("No Airbnb budget stays available in ", county_name)
        else:
            # print if stays found for the input
            print('Airbnb budget stays in ', county_name, ': limited to ', limit, ' results :')
            # return search result
            c.execute(
                """select * from stays where price<:price and neighbourhood=:neighbourhood 
                   order by price asc limit :limit""",
                {'price': price, 'neighbourhood': county_name, 'limit': limit})
            return print(c.fetchall())

    # search stays for short vacation takes days as positional argument and limit as optional argument
    # Returns search results
    @staticmethod
    def stays_for_short_vacation(days, limit=5):
        # check if stays available for entered condition
        c.execute("""select count(*) from stays where minimum_nights<:min_days limit :limit""",
                  {'min_days': days, 'limit': limit})
        if c.fetchone()[0] == 0:
            # print if search fails
            print("No Airbnb stays available with minimum booking days < ", str(days))
        else:
            # print if found stays for entered condition
            print("Airbnb stays for short vacation of ", str(days),
                  "days in each neighbourhood;Below number of stays in each neighbourhood lets bookings "
                  "with minimum_nights less than ", str(days), " days. limited to ", str(limit), "results.")
            # return search result
            c.execute("""select neighbourhood, count(*) from stays where minimum_nights<:min_days
                            group by neighbourhood limit :limit""", {'min_days': days, 'limit': limit})
            print(c.fetchall())

    # Search for stays with more reviews
    # takes county and no of review as positional argument and limit as optional argument returns search results
    @staticmethod
    def top_stays_in_neighbourhood(county, no_of_reviews, limit=5):
        # Check if stays available for entered input
        c.execute("""select count(*) from stays left outer join review on stays.id = review.id 
        where review.number_of_reviews>:no_of_reviews 
        and stays.neighbourhood=:county""", {'no_of_reviews': no_of_reviews, 'county': county, 'limit': limit})
        if c.fetchone()[0] == 0:
            # print if no stays available for entered input
            print("No Airbnb stays with reviews greater than ", str(no_of_reviews), " in ", county,
                  ", no top stays available in ", county)
        else:
            # print if stays available for entered input
            print("Top stays in ", county, " with reviews greater than ", str(no_of_reviews), " limited to ",
                  str(limit),
                  " results.")
            # return search results
            c.execute("""select * from stays left outer join review on stays.id = review.id
                        where review.number_of_reviews>:no_of_reviews
                        and stays.neighbourhood=:county limit :limit""",
                      {'no_of_reviews': no_of_reviews, 'county': county, 'limit': limit})
            return print(c.fetchall())
Commit
conn.commit()
ClassUpdate.py
from AirbnbParent import UpdateTable from AirbnbParent import conn

****************#
Uses Inheritance method from AirbnbParent module****#
****************#
Class UpdateStays: SQL wrapper for SQL operation update
class UpdateStays(UpdateTable):

# add new stays to stays table takes 11 positional arguments dosent return anything
@staticmethod
def add_stays(l_id, name, latitude, longitude, room_type, price, minimum_nights, availability_365,
              calculated_host_listings_count,
              host_id, neighbourhood):
    new_host = [[l_id, name, latitude, longitude, room_type, price, minimum_nights, availability_365,
                 calculated_host_listings_count,
                 host_id, neighbourhood]]
    # Invoke insert_table function from Airbnb_RDBMS
    # Inherited method from Airbnb_RDBMS
    UpdateTable.insert_table('stays', ' values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )', new_host[0])
    return
Class UpdateHost: SQL wrapper for SQL operation update
class UpdateHost(UpdateTable): # add new hosts to host table takes host id and host name as positional arguments doesn't return anything @staticmethod def add_host(host_id, host_name): host_id = host_id new_host = [[host_id, host_name]] # Invoke insert_table function from Airbnb_RDBMS # Inherited method from Airbnb_RDBMS UpdateTable.insert_table('host', ' values(?, ? )', new_host[0]) return

Class UpdateCounty: SQL wrapper for SQL operation update
class UpdateCounty(UpdateTable):
    # add new neighbourhood to county table takes name and grp as positional arguments doesn't return anything
    @staticmethod
    def add_county(name, grp):
        new_county = [[name, grp]]
        UpdateTable.insert_table('county', ' values(?, ? )', new_county[0])
        return


conn.commit()
Airbnb_UnitTest_Method.py
import sqlite3

conn = sqlite3.connect("airbnb.db")
conn.execute("PRAGMA foreign_keys = 1")
c = conn.cursor()
Unit Testing function to Test add_bookings function, takes test id as arguments
returns test results
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
drop_tables
import sqlite3

conn = sqlite3.connect("airbnb.db")
c = conn.cursor()

c.execute("""SELECT COUNT(*) FROM sqlite_master WHERE type='table' 
                AND name in('county','host','review','stays','bookings')""")
if c.fetchone()[0] >= 1:
    c.execute("DROP TABLE stays")
    c.execute("DROP TABLE host")
    c.execute("DROP TABLE review")
    c.execute("DROP TABLE county")
    c.execute("DROP TABLE bookings")
else:
    pass

conn.commit()
c.close()
