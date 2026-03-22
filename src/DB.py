import sqlite3

def createDB():    
    dbFile = sqlite3.connect("../bdd/data.db")
    cursor = dbFile.cursor()

    cursor.execute(""" CREATE TABLE IF NOT EXISTS company (id INTEGER PRIMARY KEY AUTOINCREMENT, companyName TEXT NOT NULL, companyEmail TEXT NOT NULL,
                    parsedFile TEXT, converted TEXT, emailSent TEXT, date TEXT )""")
    dbFile.commit()
    dbFile.close()

def addCompany(companyName, email):
    dbFile = sqlite3.connect("../bdd/data.db")
    cursor = dbFile.cursor()

    cursor.execute(
        "INSERT INTO company (companyName, companyEmail) VALUES (?, ?)",
        (companyName, email)
    )
    dbFile.commit()
    dbFile.close()

def readDB():
    dbFile = sqlite3.connect("../bdd/data.db")
    cursor = dbFile.cursor()

    cursor.execute("SELECT * FROM company")
    resultats = cursor.fetchall()

    dbFile.close()
    return resultats

def removeLineInDB(id):
    dbFile = sqlite3.connect("../bdd/data.db")
    cursor = dbFile.cursor()

    cursor.execute("DELETE FROM company WHERE id = ?",(id,))
    dbFile.commit()
    dbFile.close()


####################################################################################################
# Others action
####################################################################################################

def updateDatabase(column):
    dbFile = sqlite3.connect("../bdd/data.db")
    cursor = dbFile.cursor()

    cursor.execute(f"UPDATE company SET {column} = 'YES' WHERE {column} is NULL")
    dbFile.commit()
    
    dbFile.close()

def updateDateForCompany(column, date, companyName):
    dbFile = sqlite3.connect("../bdd/data.db")
    cursor = dbFile.cursor()

    cursor.execute(
        f"UPDATE company SET {column} = ? WHERE companyName = ?",
        (date, companyName)
    )

    dbFile.commit()
    dbFile.close()

def getCompanies(data, filter): 
    dbFile = sqlite3.connect("../bdd/data.db")
    cursor = dbFile.cursor()

    cursor.execute(f"SELECT {data} FROM company WHERE {filter} is NULL")
    results = cursor.fetchall()
    
    dbFile.close()
    
    return [row[0] for row in results]

def getDB(data): 
    dbFile = sqlite3.connect("../bdd/data.db")
    cursor = dbFile.cursor()

    cursor.execute(f"SELECT {data} FROM company")
    results = cursor.fetchall()

    dbFile.close()
    
    return results



    