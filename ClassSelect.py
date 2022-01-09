import sqlite3

conn = sqlite3.connect("airbnb.db")
c = conn.cursor()


# Class Select: SQL wrapper for SQL operation Select has three static method
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


# Commit
conn.commit()