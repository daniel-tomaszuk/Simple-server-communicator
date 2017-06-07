from mysql.connector import connect
from datetime import time
from getpass import getpass

import argparse

from models import *
# for clcrypto
import hashlib
import random
import string


def main():
    
    parser = argparse.ArgumentParser(description="Simple server communicator via SQL base.")
    # prevents from using -v and -q at the same time
    group = parser.add_mutually_exclusive_group()
    
    # while logging
    parser.add_argument("-u","--user", help="user login set as email!.")
    # parser.add_argument("-p","--password", help="user password")
    
    parser.add_argument('-p', '--password', action='store_true', dest='password', 
                        help='hidden password prompt')
    
    
    # parser.add_argument("-n","--new-pass", help="sets new password while logging")
    parser.add_argument('-n', '--new-pass', action='store_true', dest='new_pass', 
                        help="sets new password while logging")
    
    
    
     
    # after succesful log
    parser.add_argument("-l","--list", action="store_true", default=0, help="list all user emails")
    parser.add_argument("-d","--delete", action="store_true", default=0, help="delete logged user")
    parser.add_argument("-e","--edit", action="store_true", default=0, help="edit user email")
    
    
    group.add_argument("-v", "--verbose", action="store_true", help = "more verbose output")
    group.add_argument("-q", "--quiet", action="store_true", help = "stays quiet")
    parser.add_argument("--quit", action="store_false", default=1, help="closes the program")
    
    
    args = parser.parse_args()
    if args.password:
            password = getpass("User: {}, password: ".format(args.user))
            
            
    if args.new_pass:
            new_pass = getpass("Set new password: ")
    
    
    
# try to log in    
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
                print ("Logging in as {}".format(args.user))   
                break 
            # if there is an user to log into but password is incorrect
            elif args.user == gg_user.email and check_password(password, gg_user.hashed_password()) == False:
                print ("Wrong password..")
                break            
            counter+=1
            # if whole DB was checked with no match - set flag db_checked, create new user
            if counter == len(gg_users):
                db_checked = True            
            
        if db_checked:
            new_gg_user = User()
            new_gg_user.email = args.user
            new_gg_user.hashed_password = password_hash(password)
            # allow user to choose
            new_gg_user.username = input("Creating new user.\n Write your username: ")
            
            new_gg_user.save_to_db(cursor)
            
         
        disconnect_db(cursor, cnx)
#        
    else:
        print ("Password too short..")
    
    
    

if __name__ == "__main__":
    main()




     
