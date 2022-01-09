import sqlite3
from sqlite3 import Error

conn = sqlite3.connect("airbnb.db")
c = conn.cursor()

# *******************************************************Creates tables**********************************************#
# Reusable Function for table creation takes create table SQL as positional argument
# returns nothing


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


print("-------------------------------------------------------------------------------------------"
          "\n|#*#*#*#*------------Your database is created with necessary tables!!!------------*#*#*#*#|\n"
          "-------------------------------------------------------------------------------------------")