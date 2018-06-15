import secrets
from psycopg2 import connect

#Returns connection to database, this should only get passed to search input and search functions
def connectDB():
    try:
        con = connect(dbname=secrets.pgname, user=secrets.pguser, host=secrets.pghost, password=secrets.pgpass)
    except() as e:
        print(e)
    return con



def populateDB(conn):
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE vendors (
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        )
        """,
        """ CREATE TABLE parts (
                part_id SERIAL PRIMARY KEY,
                part_name VARCHAR(255) NOT NULL
                )
        """,
        """
        CREATE TABLE part_drawings (
                part_id INTEGER PRIMARY KEY,
                file_extension VARCHAR(5) NOT NULL,
                drawing_data BYTEA NOT NULL,
                FOREIGN KEY (part_id)
                REFERENCES parts (part_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE vendor_parts (
                vendor_id INTEGER NOT NULL,
                part_id INTEGER NOT NULL,
                PRIMARY KEY (vendor_id , part_id),
                FOREIGN KEY (vendor_id)
                    REFERENCES vendors (vendor_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (part_id)
                    REFERENCES parts (part_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
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