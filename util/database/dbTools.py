import secrets
from psycopg2 import connect


# Returns connection to database, this should only get passed to search input and search functions
def connectDB():
    try:
        con = connect(dbname=secrets.pgname, user=secrets.pguser, host=secrets.pghost, password=secrets.pgpass)
    except() as e:
        print(e)
    return con

## creation of DB through sql language
def populateDB(conn):
    """ create tables in the PostgreSQL database"""
    commands = (
        """
CREATE TABLE compound (
	compound_id SERIAL PRIMARY KEY,
	notation TEXT
)

        """,
        """ CREATE TABLE compound_info (
	compound_id SERIAL NOT NULL,
	name TEXT,
	author TEXT,
	dateCreated DATE,
	theoretical_mass float8,
	scientific_mass float8,
	time_passed INT,
	PRIMARY KEY(compound_id)
)
        """,
        """
CREATE TABLE storage (
	compound_id SERIAL NOT NULL,
	file_loc TEXT,
	PRIMARY KEY(compound_id)
)
        """,
        """
CREATE TABLE atom_info (
	compound_id SERIAL NOT NULL,
	molecule_id TEXT,
	atom_type char(2),
	x_coord float8,
	y_coord float8,
	z_coord float8,
	PRIMARY KEY(compound_id)
)
      """)
    try:
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
            # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except() as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()


### Block for sqlAlchemy functions ###


### Main ###
if __name__ == "__main__":
    populateDB(connectDB())
