import sqlite3

db_name = 'MindYourStudy.db'

def RunQuery(query, parameters = ()):
    global db_name
    with sqlite3.connect(db_name) as conn:
        try:
            cursor = conn.cursor()
            consulta = cursor.execute(query, parameters)
            conn.commit()
        except sqlite3.IntegrityError:
            return -1
    return consulta