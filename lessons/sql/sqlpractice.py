import sqlite3

def main():
    conn = sqlite3.connect('test.db')
    print("Opened database successfully")
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS COMPANY
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME           TEXT    NOT NULL,
            AGE            INT     NOT NULL,
            ADDRESS        CHAR(50),
            SALARY         REAL);''')
    print ("Table created successfully")

    values = [("Barry", "18", "Nowhere", "3400"),
              ("Dazza", "23", "Nowhere", "8000"),
              ("Snazza", "20", "Nowhere", "10")]
    cur.executemany("INSERT INTO COMPANY (NAME, AGE, ADDRESS, SALARY) \
                VALUES (?,?,?,?)", values)
    
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()