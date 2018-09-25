###Work points for new hires:
    DB Schema updating and insertion:
        DB creation found within dbTools.py
        Flask forms:
            Update table schema and insertion statements to add additional metadata, metadata form in uploadForm.html
        File parsing:
            Separate molecules based on "ter" string within files, insert these as separate compounds with a many-to-many relation using a junction table 
            add to file parser.py
    Systems: 
        Login process, user rights: 
            CLI acceptable, no need to make user management page
            Acct creation proc: 
                Google form -> Admin approval -> acct creation -> email pass -> reset pass on login
        Build Tools: 
            Shell script (oneliner) to complete database replication ansible book
            Add python install files
    Front End: 
        Create clean looking search results page, can use http://zinc.docking.org/ as loose guide
            Search results currently returned as a json object in the app.py file search_results function

###Tools Used:
postgresql -> database
python and flask -> front end
ansible and vagrant -> build tools


###Folder structure
build -> build tools
static -> html resources
templates -> flask page templates
util ->
    parser.py -> parses pdb files
    database ->
        dbTools -> database creation, insertion, search functions (psycopg2 used as library)
    chemdoodle -> 3d molecule viewer
app.py -> main flask app

###Additional Resources:

SQL Tutorial:
http://sqlzoo.net/

SQLAlchemy is a wrapper library for SQL languange, can build useful tools with it in the future for now i think it is best to make sure new hires have SQL knowledge first
SQLAlchemy Resources:
https://github.com/dahlia/awesome-sqlalchemy
https://github.com/kvesteri/sqlalchemy-utils
https://github.com/mitsuhiko/flask-sqlalchemy

Ansible roles:
https://github.com/pyslackers/ansible-role-postgres

Flask:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world