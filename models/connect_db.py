from mysql.connector import connect

def connect_db():
    print("Connecting..")
    username = "root"
    passwd = "coderslab"
    hostname = "localhost"
    database = "Python_with_MySQL" 
    cnx = connect(user=username,
          password=passwd,
          host=hostname,
          database=database)
    return cnx


def disconnect_db(cursor, cnx):
    cursor.close()
    cnx.close()
    print('Disconnected..')
    