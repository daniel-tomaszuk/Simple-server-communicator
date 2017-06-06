def connect_db():
    print("Connecting..")
    username = "root"
    passwd = "coderslab"
    hostname = "localhost"
    database = "cinemas_db" 
    cnx = connect(user=username,
          password=passwd,
          host=hostname,
          database=database)
    return cnx
