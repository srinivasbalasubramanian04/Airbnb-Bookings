import sqlite3

conn = sqlite3.connect("airbnb.db")
c = conn.cursor()


# Class Delete: SQL wrapper for SQL operation delete has one static method
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


# Commit
conn.commit()
