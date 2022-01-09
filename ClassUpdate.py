from AirbnbParent import UpdateTable
from AirbnbParent import conn

# ********************************************************************************************************************#
# ********************************Uses Inheritance method from AirbnbParent module************************************#
# ********************************************************************************************************************#


# Class UpdateStays: SQL wrapper for SQL operation update
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


# Class UpdateHost: SQL wrapper for SQL operation update
class UpdateHost(UpdateTable):
    # add new hosts to host table takes host id and host name as positional arguments doesn't return anything
    @staticmethod
    def add_host(host_id, host_name):
        host_id = host_id
        new_host = [[host_id, host_name]]
        # Invoke insert_table function from Airbnb_RDBMS
        # Inherited method from Airbnb_RDBMS
        UpdateTable.insert_table('host', ' values(?, ? )', new_host[0])
        return


# Class UpdateCounty: SQL wrapper for SQL operation update
class UpdateCounty(UpdateTable):
    # add new neighbourhood to county table takes name and grp as positional arguments doesn't return anything
    @staticmethod
    def add_county(name, grp):
        new_county = [[name, grp]]
        UpdateTable.insert_table('county', ' values(?, ? )', new_county[0])
        return


conn.commit()
