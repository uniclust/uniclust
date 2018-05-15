#!/usr/bin/env python
#--*--encoding:utf8--*--
import os
from sys import stdin
import errno
from pyftpdlib.handlers import FTPHandler #импорт класса обработчиков
from pyftpdlib.servers import FTPServer #импорт класса сервера
from pyftpdlib.authorizers import DummyAuthorizer #импорт класса авторизации юникс
import logging # logging into a log-file
import threading

def listen_commands(authorizer, handler, server):
    while True:
        print("---===MENU OF COMMANDS===---")
        print("1. Add user")
        print("2. Remove user")
        choice = str(input())
        if choice == "1":
            print("--Enter login of the new user:")
            login = str(input())
            # если такой логин уже есть, то при добавлении попадём в except
            print("--Enter password of the new user:")
            password = str(input())
            print("--Enter rights for a new user (example: elrad):")
            print("-Read permissions-")
            print("'e' = change directory (CWD, CDUP commands)")
            print("'l' = list files (LIST, NLST, STAT, MLSD, MLST, SIZE commands)")
            print("'r' = retrieve file from the server (RETR command)")
            print("-Write permissions-")
            print("'a' = append data to an existing file (APPE command)")
            print("'d' = delete file or directory (DELE, RMD commands)")
            print("'f' = rename file or directory (RNFR, RNTO commands)")
            print("'m' = create directory (MKD command)")
            print("'w' = store a file to the server (STOR, STOU commands)")
            print("'M' = change file mode / permission (SITE CHMOD command)")
            print("'T' = change file modification time (SITE MFMT command)")
            permissions = str(input())
            try:
                add_user(login, password, permissions, os.path.join(os.getcwd(),'users_data/'), authorizer)
                logging.info("Administrator added a new user with (login, permissions, homedir) as (" + login + ", " + permissions +", " + home_directory + ")")
            except ValueError as err:
                print("Error! " + err + " Try again...")
        if choice == '2':
            print("--Enter login of the user, you want to remove:")
            remove_login = str(input())
            try:
                authorizer.remove_user(remove_login)
                logging.info("Administrator removed user with login :" + remove_login)
            except:
                print("Error occured when trying to remove user. Try again!")

def add_user(login, password, permissions, path_of_data_directory, authorizer):
    path_to_user_directory = os.path.join(path_of_data_directory, login)
    try:
        os.makedirs(path_to_user_directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            logging.error("Error occured when trying to create a new directory for user. Err text:" + e.args[0])
            raise
    authorizer.add_user(login, password, homedir=path_to_user_directory, perm=permissions)
    logging.info("New user was added a new user with (login, permissions, homedir) as (" + login + ", " + permissions +", " + path_to_user_directory + ")")
    pass

def main(): # точка входа в приложение

    logging.basicConfig(filename = "ftp_server.log", level = logging.DEBUG, format = '%(asctime)s %(levelname)s: %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')

    try:
        os.makedirs(os.path.join(os.getcwd(),'users_data'))
        os.makedirs(os.path.join(os.getcwd(),'users_data/anonim'))
    except OSError as e:
        if e.errno != errno.EEXIST:
            logging.error("Error occured when trying to create a new directory for user. Err text:" + e.args[0])
            raise

    authorizer = DummyAuthorizer()
    add_user("user1", "qwerty", "elradfmwMT", "users_data", authorizer) # добавляет одного пользователя
    # раскомментировать строку ниже при необходимости добавления анонимного пользователя
    # authorizer.add_anonymous(homedir='users_data/anonim') 

    # конфигурируем сервер
    handler = FTPHandler # создание объектра обработки событий
    handler.authorizer = authorizer # присваивание объектра авторизации
    handler.passive_ports = range(10000, 65535)
    handler.banner = "Hello! I am Asynchronious Supercomputer FTP-server."
    handler.timeout = None # максимальный промежуток времени между коммандами клиента

    serv = FTPServer(('0.0.0.0', 3100), handler) # создание объектра сервера
    serv.max_cons = 55535
    # включим прослушку команд в отдельном потоке
    command_thread = threading.Thread()
    command_thread._target = listen_commands
    command_thread._args = (authorizer, handler, serv)
    command_thread.start()
    serv.serve_forever() # запуск прослушивания порта в бесконечном цыкле

if __name__ == "__main__":
    main()