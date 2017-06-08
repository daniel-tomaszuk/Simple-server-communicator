from mysql.connector import connect

from datetime import time
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
            SELECT id,  email, username, hashed_password FROM Users
            WHERE id ={}""".format(id)           
        cursor.execute(sql)
        data = cursor.fetchone()
        if data is not None:
            # creates instance of class User
            loaded_user = User()
            # set attributes
            loaded_user.__id = data[0]            
            loaded_user.email = data[1]
            loaded_user.username = data[2]
            
            loaded_user.__hashed_password = data[3]
            return loaded_user
        else:
            return None
          
    @staticmethod    
    def load_all_users(cursor):
        sql = 'SELECT id,  email, username, hashed_password FROM Users'
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
  
########################################################################################### 
  
  
  
                       
import hashlib
import random
import string

"""
ALPHABET is a global variable, that keeps all uppercase letter, all lowercase
letters and digits.
"""
ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits


def generate_salt():
    """
    Generates a 16-character random salt.
    :return: str with generated salt
    """
    salt = ""
    for i in range(0, 16):

        # get a random element from the iterable
        salt += random.choice(ALPHABET)
    return salt


def password_hash(password, salt=None):
    """
    Hashes the password with salt as an optional parameter.
    If salt is not provided, generates random salt.
    If salt is less than 16 chars, fills the string to 16 chars.
    If salt is longer than 16 chars, cuts salt to 16 chars.
    """

    # generate salt if not provided
    if salt is None:
        salt = generate_salt()

    # fill to 16 chars if too short
    if len(salt) < 16:
        salt += ("a" * (16 - len(salt)))

    # cut to 16 if too long
    if len(salt) > 16:
        salt = salt[:16]

    # use sha256 algorithm to generate hash
    t_sha = hashlib.sha256()

    # we have to encode salt & password to utf-8, this is required by the
    # hashlib library.
    t_sha.update(salt.encode('utf-8') + password.encode('utf-8'))

    # return salt & hash joined
    return salt + t_sha.hexdigest()


def check_password(pass_to_check, hashed):
    """
    Checks the password.
    The function does the following:
        - gets the salt + hash joined,
        - extracts salt and hash,
        - hashes `pass_to_check` with extracted salt,
        - compares `hashed` with hashed `pass_to_check`.
        - returns True if password is correct, or False. :)
    """

    # extract salt
    salt = hashed[:16]

    # extract hash to compare with
    hash_to_check = hashed[16:]

    # hash password with extracted salt
    new_hash = password_hash(pass_to_check, salt)

    # compare hashes. If equal, return True
    if new_hash[16:] == hash_to_check:
        return True
    else:
        return False

                  
         