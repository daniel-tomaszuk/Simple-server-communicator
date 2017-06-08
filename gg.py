from mysql.connector import connect
from datetime import time
from getpass import getpass

import argparse

from models import *
# for clcrypto
import hashlib
import random
import string

def log_in(args):
    # try to log in    
    if args.password:
        password = getpass("User: {}, password: ".format(args.user))
  
    if (len(password) >= 8):
        # connect into DB
        cnx = connect_db()        
        cnx.autocommit = True
        cursor = cnx.cursor() 
        # create instance of User - get all users in DB
        gg_users = User.load_all_users(cursor)        
        db_checked = False
        counter = 0
        for gg_user in gg_users:            
            # if there is an user to log into and his password is correct
            if args.user == gg_user.email and check_password(password, gg_user.hashed_password()):
                print ("Logged as {}".format(args.user)) 
                disconnect_db(cursor, cnx)
                # logged in  
                return gg_user.id
            # if there is an user to log into but password is incorrect
            elif args.user == gg_user.email and check_password(password, gg_user.hashed_password()) == False:
                print ("Wrong password..")
                disconnect_db(cursor, cnx)
                # wrong pass - log in failed
                return False            
            counter+=1
            # if whole DB was checked with no match - set flag db_checked, create new user
            if counter == len(gg_users):
                db_checked = True            
                    
        if db_checked:
            new_gg_user = User()
            new_gg_user.email = args.user
            new_gg_user.hashed_password = password_hash(password)
            # allow user to choose his username
            new_gg_user.username = input("Creating new user.\nWrite your username: ")            
            new_gg_user.save_to_db(cursor)
            print("New user made..")
            disconnect_db(cursor, cnx)
            # new user and logged in
            return new_gg_user.id
        else:
            print("Error while checking DB..")
            disconnect_db(cursor, cnx)
            return False
            
    else:
        print ("Password too short..")
        disconnect_db(cursor, cnx)
        # log in failed
        return False


def new_pass(args):
    # set new pass only if proper -u and -p were given as well as -n 
    log_in_result = log_in(args)   
    if log_in_result != False and args.new_pass:
            new_pass = getpass("Set new password: ")  
            if len(new_pass) >= 8:
                cnx = connect_db()        
                cnx.autocommit = True
                cursor = cnx.cursor()
                user = User.load_by_id(log_in_result, cursor) 
                # set new password           
                user.hashed_password = password_hash(new_pass)
                # update new password in DB
                sql = """UPDATE Users SET hashed_password = '{}'
                         WHERE id = {}""".format(user.hashed_password, user.id)            
                cursor.execute(sql)
                disconnect_db(cursor,cnx)
                print ("New password set!")
                return True
            else:
                print("Password too short..")
                return False

        


def delete(args):
    log_in_result = log_in(args)
    if log_in_result != False and args.delete: 
        cnx = connect_db()        
        cnx.autocommit = True
        cursor = cnx.cursor()        
        user = User.load_by_id(log_in_result, cursor)
        in_del = input("Do you want to delete user {}? y/n ".format(user.username))
        if in_del.lower() == 'y':
            user.delete(cursor)
            disconnect_db(cursor,cnx)
            return True
        else:
            print("Deletion cancelled..")
            disconnect_db(cursor,cnx)
            return False

def list(args):
    log_in_result = log_in(args)
    if log_in_result != False and args.list: 
        cnx = connect_db()        
        cnx.autocommit = True
        cursor = cnx.cursor() 
        gg_users = User.load_all_users(cursor)
        print("All users:")
        # print all users
        for gg_user in gg_users:            
            print(gg_user.id,gg_user.email, gg_user.username) 
        disconnect_db(cursor,cnx)   
        return True
    else:
        print("Error..")
        disconnect_db(cursor,cnx)
        return False

        

def main():    
    parser = argparse.ArgumentParser(description="Simple server communicator via SQL base.")
    # prevents from using -v and -q at the same time
    group = parser.add_mutually_exclusive_group()
    group2 = parser.add_mutually_exclusive_group()
    
    # while logging
    parser.add_argument("-u","--user", help="user login, email in DB")
    # parser.add_argument("-p","--password", help="user password")
    
    parser.add_argument('-p', '--password', action='store_true', dest='password', 
                        help='hidden password prompt')
    
    
    # parser.add_argument("-n","--new-pass", help="sets new password while logging")
    group2.add_argument('-n', '--new-pass', action='store_true', dest='new_pass', 
                        help="sets new password while logging")
    
    

     

    group2.add_argument("-l","--list", action="store_true", help="list all users")
    group2.add_argument("-d","--delete", action="store_true", help="delete logged user")
    group2.add_argument("-e","--edit", action="store_true", help="edit user email")
    
    group2.add_argument("-t","--to", help="to whom send your message")
    group2.add_argument("-s","--send", action="store_true", help="send message")
    
    
    
    group.add_argument("-v", "--verbose", action="store_true", help = "more verbose output")
    group.add_argument("-q", "--quiet", action="store_true", help = "stays quiet")
    
    parser.add_argument("--quit", action="store_false", help="closes the program")
        
                
    args = parser.parse_args()
    
#     args_g2 = group2.parse_args()
#     help = parser.print_help()
        
        
    print(args.list)
    # log in, create new user, delete user  
    if (args.new_pass == False) and (args.delete == False) and (args.list == False):
        log_in(args)
    elif (args.new_pass):
        new_pass(args)        
    # delete user after loggin in    
    elif (args.delete):
        delete(args)
    # list all users
    elif args.list:
        list(args)
       
    

if __name__ == "__main__":
    main()




     
