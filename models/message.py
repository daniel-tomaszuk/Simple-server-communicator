from connect_db import *
from datetime import time
from mysql.connector import connect    

         
            
class Message(object): 
       
    __cursor = None
    __cnx = None
    
    def __init__(self):
        self.__id = -1
        self.u_from = 0
        self.u_to = 0
        self.text = 0
        self.creation_date = 0
                     
    @property
    def cnx(self):
        return self.__cnx
        
    @cnx.setter  # #??
    def cnx(self, cnx):
        self.__cnx = cnx
        sefl.__cursor = self.cnx.cursor()

    
    @property
    def id(self):
        return self.__id
    

    @staticmethod   
    def load_by_id(cursor, id):         
        sql = """
            SELECT id, sender_id, reciver_id, communicate, send_date FROM Comunicates
            WHERE id = {}""".format(id)           
        cursor.execute(sql)
        data = cursor.fetchone()
        if data is not None:
            # creates instance of class User
            loaded_communicate = Message()
            # set attributes
            loaded_communicate.__id = data[0]
            loaded_communicate.u_from = data[1]
            loaded_communicate.u_to = data[2]
            loaded_communicate.text = data[3]
            loaded_communicate.creation_date = data[4]        
            return loaded_communicate
        else:
            return None              
            
    
    @staticmethod    
    def load_all_message_for_user(cursor, id):
        sql = """SELECT id, sender_id, reciver_id, communicate, send_date FROM Comunicates
                 WHERE sender_id = {}
                 OR reciver_id = {} """.format(id, id)
        ret = []            
        cursor.execute(sql)
        result = cursor.fetchall()  
        for data in result:       
            loaded_communicate = Message()
            # set attributes
            loaded_communicate.__id = data[0]
            loaded_communicate.u_from = data[1]
            loaded_communicate.u_to = data[2]
            loaded_communicate.text = data[3]
            loaded_communicate.creation_date = data[4] 
            ret.append(loaded_communicate)
        return ret    
           
    @staticmethod    
    def load_all_message(cursor):
        sql = """SELECT id, sender_id, reciver_id, communicate, send_date FROM Comunicates"""
        ret = []            
        cursor.execute(sql)
        result = cursor.fetchall()  
        for data in result:       
            loaded_communicate = Message()
            # set attributes
            loaded_communicate.__id = data[0]
            loaded_communicate.u_from = data[1]
            loaded_communicate.u_to = data[2]
            loaded_communicate.text = data[3]
            loaded_communicate.creation_date = data[4] 
            ret.append(loaded_communicate)
        return ret          
            
            
    def save_to_db(self, cursor):
        # if Message instance id isn't already in DB
        if self.__id == -1:
            # saving new instance (new_message) using prepared statements
            sql = """
                  INSERT INTO Comunicates(sender_id, reciver_id,communicate)
                  VALUES ({}, {}, "{}")
                  """.format(self.u_from, self.u_to, self.text)
            
            cursor.execute(sql)
            # User instance id as last used row in DB
            self.__id = cursor.lastrowid 
            print ("Saved..")
            return True                 
        return False        
                        
            
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
# 
    messages = Message.load_all_message(cursor)
     
    for message in messages:
        print(message.text)
#     

    
    
    
    disconnect_db(cursor, cnx)  
    
    
    
    
    
    
    
    
    
    
    
    