
import sqlite3
import pandas as pd

# Connects to an existing database file in the current directory
# If the file does not exist, it creates it in the current directory
db_connect = sqlite3.connect('test.db')

# Instantiate cursor object for executing queries
cursor = db_connect.cursor()

# String variable for passing queries to cursor
query = """
    CREATE TABLE IF NOT EXISTS Staff(
    NIN INT NOT NULL,
    eName VARCHAR(100) NOT NULL,
    PRIMARY KEY(NIN)
    );
   
    CREATE TABLE IF NOT EXISTS Hotel(
    hNo VARCHAR(50) NOT NULL,
    hLoc VARCHAR(100) NOT NULL,
    PRIMARY KEY(hNo)
    );
    
    CREATE TABLE IF NOT EXISTS Contract(
    NIN INT NOT NULL,
    contractNo VARCHAR(100) NOT NULL,
    hours INT NOT NULL,
    hNO INT NOT NULL,
    PRIMARY KEY(NIN, contractNo),
    FOREIGN KEY(NIN) references Staff(NIN),
    FOREIGN KEY(hNo) references Hotel(hNo)
    );
    
    INSERT OR REPLACE INTO Staff(NIN,eName)
    VALUES (1135, "Smith J"),
     (1057, "Hocine D"),
    (1068, "White T");
    
    INSERT OR REPLACE INTO Hotel(hNo,hLoc)
    VALUES ("H25", "East Kilbride"),
    ("H4", "Glasglow");
    
    INSERT OR REPLACE INTO Contract(NIN,contractNo,hours,hNo)
    VALUES (1135, "C1024","16","H25"),
    (1057, "C1024","24","H25"),
    (1068, "C1025","28","H4"),
     (1135, "C1025","15","H4");
    
    
    """
cursor.executescript(query)

# Extract column names from cursor


# Fetch data and load into a pandas dataframe
# table_data = cursor.fetchall()
df = pd.read_sql_query("""
SELECT *
    FROM Contract
    LEFT OUTER JOIN Staff using (NIN)
    LEFT OUTER JOIN Hotel using (hNo);
    """
    , db_connect)

# Examine dataframe
print(df)


# Example to extract a specific column
# print(df['name'])


# Commit any changes to the database
db_connect.commit()

# Close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
db_connect.close()
