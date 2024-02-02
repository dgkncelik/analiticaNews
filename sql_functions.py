def insert_row(db_connection_object, nd):
    try:
        iso8601_date_str = nd["date"].isoformat()
    except Exception as e:
        print("Error on date parsing for sql, ignore inserting %s" % str(e))
        return

    insert_string = ("INSERT INTO HABERLER (TITLE,DATE,LINK,SUMMARY,AUTHOR) VALUES ('%s', '%s', '%s', '%s', '%s')" %
                     (nd["title"].replace("'", " "),
                      iso8601_date_str,
                      nd["link"],
                      nd["summary"].replace("'", " "),
                      nd["author"]))
    db_connection_object.execute(insert_string)
    db_connection_object.commit()
    print("[+] Saved to database")


def create_table(db_connection_object):
    db_connection_object.execute('''CREATE TABLE HABERLER
             (ID             INTEGER PRIMARY KEY AUTOINCREMENT,
             TITLE           TEXT    NOT NULL,
             DATE            TEXT    NOT NULL,
             LINK            TEXT    NOT NULL,
             SUMMARY         TEXT,
             AUTHOR          TEXT);''')


def read_all_news(db_connection_object):
    cursor = db_connection_object.execute('''SELECT * FROM HABERLER''')
    return cursor
