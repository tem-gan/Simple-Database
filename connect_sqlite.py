
import sqlite3
import pandas as pd

# Connects to an existing database file in the current directory
# If the file does not exist, it creates it in the current directory
db_connect = sqlite3.connect('test.db')

# Instantiate cursor object for executing queries
cursor = db_connect.cursor()

# STEP 3 a,b: creation and insertion
query = """
    CREATE TABLE IF NOT EXISTS Department(
    dNo INT NOT NULL,
    dName VARCHAR(100) NOT NULL UNIQUE CHECK (dName LIKE 'Department%'),
    facultyCount INT NOT NULL,
    cFirst VARCHAR(100) NOT NULL,
    cLast VARCHAR(100) NOT NULL,
    PRIMARY KEY(dNO)
    );
   
    CREATE TABLE IF NOT EXISTS Major(
    mCode VARCHAR(3) NOT NULL,
    mName VARCHAR(30) NOT NULL UNIQUE,
    dNo INT NOT NULL,
    PRIMARY KEY(mCode),
    FOREIGN KEY(dNo) references Department(dNo),
    CONSTRAINT len CHECK (LENGTH(mCode) = 3)
    );
    
    CREATE TABLE IF NOT EXISTS Student(
    sNo VARCHAR(9) NOT NULL,
    sFirst VARCHAR(30) NOT NULL,
    sLast VARCHAR(30) NOT NULL,
    sInitial VARCHAR(5) NOT NULL ,
    PRIMARY KEY(sNo),
    CONSTRAINT init CHECK(LENGTH(sInitial) > 1)
    
    );

    CREATE TABLE IF NOT EXISTS Event(
    eNo VARCHAR(9) NOT NULL,
    eName VARCHAR(100) NOT NULL,
    startDate DATE NOT NULL,
    endDate DATE NOT NULL,
    PRIMARY KEY(eNo),
    CHECK(endDate > startDate),
    CHECK(startDate > DATE('2021-12-09')),
    CHECK(endDate > DATE('2021-12-09'))
    );

    CREATE TABLE IF NOT EXISTS StudentList(
    mCode VARCHAR(3) NOT NULL,
    sNo VARCHAR(9) NOT NULL,
    PRIMARY KEY(sNo, mCode),
    FOREIGN KEY(sNo) references Student(sNo),
    FOREIGN KEY(mCode) references Major(mCode),
    CONSTRAINT len CHECK (LENGTH(mCode) = 3)
    );

    

    CREATE TABLE IF NOT EXISTS Hosting(
    eNo VARCHAR(9) NOT NULL,
    dNo INT NOT NULL,
    PRIMARY KEY(eNo, dNo),
    FOREIGN KEY(eNo) references Event(sNo),
    FOREIGN KEY(dNo) references Department(dNo)
    );

    CREATE TABLE IF NOT EXISTS Attendance(
    sNo VARCHAR(9) NOT NULL,
    eNo VARCHAR(9) NOT NULL,
    PRIMARY KEY(sNo, eNo),
    FOREIGN KEY(sNo) references Student(sNo),
    FOREIGN KEY(eNo) references Event(eNo)
    );

    INSERT OR REPLACE INTO Department(dNo, dName, facultyCount, cFirst, cLast)
    VALUES (1, "Department of Art", 10, "Henry", "Alex"),
    (2, "Department of Mathematics", 5, "Harold", "Sushui"),
    (3, "Department of Computer Science", 6, "Ye", "Chen"),
    (4, "Department of Science", 15, "Sajiv", "Sewnunden"),
    (5, "Department of Business", 20, "Peter", "Bold");
    
    INSERT OR REPLACE INTO Major(mCode, mName, dNo)
    VALUES ("BIO", "Biology", 4),
    ("ART", "Art", 1),
    ("MTH", "Mathematics", 2),
    ("BUS", "Marketing", 5),
    ("PHY", "Physics", 4);
    
    INSERT OR REPLACE INTO Student(sNo, sFirst, sLast, sInitial)
    VALUES ("S00000123", "Temuulen", "Ganbold","TG"),
    ("S00000684", "Texas", "Adam","TA"),
    ("S00007789", "Tenisha", "Anderson","TA"),
    ("S00000190", "Tenzin", "Neji","TN"),
    ("S00000098", "Tomas", "Drew","TD");
    
    
    INSERT OR REPLACE INTO StudentList(sNo, mCode)
    VALUES ("S00000123", "BIO"),
    ("S00000684", "BUS"),
    ("S00007789", "PHY"),
    ("S00000190", "ART"),
    ("S00000098", "MTH");

    INSERT OR REPLACE INTO Attendance(sNo, eNo)
    VALUES ("S00000123", "E00000005"),
    ("S00000684", "E00000004"),
    ("S00007789", "E00000005"),
    ("S00000190", "E00000002"),
    ("S00000098", "E00000001");

    INSERT OR REPLACE INTO Hosting(eNo, dNo)
    VALUES ("E00000001", 5),
    ("E00000002", 3),
    ("E00000003", 4),
    ("E00000004", 5),
    ("E00000005", 2);
    
    INSERT OR REPLACE INTO Event(eNo,eName,startDate, endDate)
    VALUES ("E00000001", "Job Expo",date('2021-12-12'),date('2021-12-13')),
     ("E00000002", "Book exchange",date('2021-12-13'),date('2021-12-14')),
     ("E00000003", "Christmas Monita",date('2021-12-16'),date('2021-12-18')),
     ("E00000004", "TedX",date('2021-12-19'),date('2021-12-20')),
     ("E00000005", "Pizza with Patrick",date('2021-12-25'),date('2021-12-26'));
    

    """
cursor.executescript(query)

#STEP 3C: 5 queries
#List of students and their majors
df = pd.read_sql_query("""
SELECT sl.sNo, s.sFirst, s.sLast, m.mName
    FROM StudentList sl
    LEFT JOIN Student s ON sl.sNo=s.sNo
    LEFT JOIN Major m ON sl.mCode=m.mCode;
    """
    , db_connect)

print(df)

#List of Majors and the Departments they belong to
df1 = pd.read_sql_query("""
SELECT m.mCode, m.mName, d.dName
    FROM Major m
    LEFT JOIN Department d ON m.dNo=d.dNo;
    """
    , db_connect)


print(df1)
#List student id, name and the events they attended/signed up for
df2 = pd.read_sql_query("""
SELECT a.sNo, s.sFirst, s.sLast, e.eName
    FROM Attendance a
    LEFT JOIN Student s ON a.sNo=s.sNo
    LEFT JOIN Event e ON a.eNo=e.eNo;
    """
    , db_connect)


print(df2)
#List the events and the departments it is being hosted by
df3 = pd.read_sql_query("""
SELECT e.eName, d.dName
    FROM Hosting h
    LEFT JOIN Event e ON h.eNo=e.eNo
    LEFT JOIN Department d ON h.dNo=d.dNo;
    """
    , db_connect)


print(df3)
#List the students in the Department of Science
df4 = pd.read_sql_query("""
SELECT sl.sNo, s.sFirst, s.sLast, m.mName, d.dName
    FROM StudentList sl
    LEFT JOIN Student s ON sl.sNo=s.sNo
    LEFT JOIN Major m ON sl.mCode=m.mCode
    LEFT JOIN Department d ON m.dNo=d.dNo
    WHERE d.dName='Department of Science'
    ;
    """
    , db_connect)


print(df4)



# Commit any changes to the database
db_connect.commit()

# Close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
db_connect.close()
