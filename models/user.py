from clcrypto import password_hash
from connect_db import *
from mysql.connector import connect


class User(object):

    __cursor = None
    __cnx = None
    
        
    @property
    def cnx(self):
        return self.__cnx
        
    @cnx.setter  # #??
    def cnx(self, cnx):
        self.__cnx = cnx
        sefl.__cursor = self.cnx.cursor()

    def __init__(self):
        self.__id = -1
        self.username = ""
        self.email = ""
        self.__hashed_password = ""
    
    @property
    def id(self):
        return self.__id
        
    def hashed_password(self):
        return self.__hashed_password
    
    def set_password(self, password, salt):
        self.__hashed_password = password_hash(password, salt)

        
    @staticmethod   
    def load_by_id(id, cursor):         
        sql = """
            SELECT id, username, email, hashed_password FROM Users
            WHERE id ={}""".format(id)           
        cursor.execute(sql)
        data = cursor.fetchone()
        if data is not None:
            # creates instance of class User
            loaded_user = User()
            # set attributes
            loaded_user.__id = data[0]
            loaded_user.username = data[2]
            loaded_user.email = data[1]
            
            loaded_user.__hashed_password = data[3]
            return loaded_user
        else:
            return None
          
    @staticmethod    
    def load_all_users(cursor):
        sql = 'SELECT id, username, email, hashed_password FROM Users'
        ret = []            
        cursor.execute(sql)
        result = cursor.fetchall()  
        for data in result:       
            loaded_user = User()
            # set attributes
            loaded_user.__id = data[0]
            loaded_user.username = data[2]
            loaded_user.email = data[1]            
            loaded_user.__hashed_password = data[3]
            ret.append(loaded_user)
        return ret
                
                
    def save_to_db(self, cursor):
        # if User instance id isn't already in DB
        if self.__id == -1:
            # saving new instance using prepared statements
            sql = """
                  INSERT INTO Users (username, email, hashed_password)
                  VALUES ('{}','{}','{}')
                  """.format(self.username, self.email, self.hashed_password)
            
            cursor.execute(sql)
            # User instance id as last used row in DB
            self.__id = cursor.lastrowid 
            print ("Saved..")
            return True        
        # if User instance is already in the DB 
        else:
            sql = """UPDATE Users SET username = '{}', email = '{}',  hashed_password = '{}'
                   WHERE id = {}""".format(self.username,
                                           self.email, 
                                           self.hashed_password, 
                                           self.id)
            cursor.execute(sql)  
            print ("Updated..")
            return True
        
        return False
            
            
    def delete(self, cursor):
        sql  = "DELETE FROM Users WHERE id={}".format(self.__id)
        cursor.execute(sql)
        self.__id = -1
        print("Deleted..")
        return True       
         
     
            
if __name__ == "__main__":
     
    cnx = connect_db()        
    cnx.autocommit = True
    cursor = cnx.cursor() 
    
#     message = Message()
#     message.u_from = 6
#     message.u_to = 5
#     message.text = "Nothing much. You?"
#     
#     message.save_to_db(cursor)
  

#     user.email = "Testowy@mail.test"
#     user.hashed_password = password_hash("testowe123451","solsolsolsolsolsol")
#     
        
    disconnect_db(cursor, cnx)      
    
#        

      
#             
#             
#             
#             
#             
            
            
            
            
            
            
            
            
            
        
