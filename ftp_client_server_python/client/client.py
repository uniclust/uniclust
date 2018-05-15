# -*- coding: utf-8 -*-
import ftplib
import time
import os
import threading
import pickle # serialization
import enum
import socket
import logging # logging into a log-file

import sys


class StatusOfLoad(enum.Enum):
    READY = 0
    PROCESS = 1
    PAUSED = 2
    STOPED = 3
    FINISHED = 4


class MyFTPClient():
    def __init__(self, hostname, login="anonymous", password="", port = 21, path_of_directory_for_history = "", callbacks = None):
        # Logging initializing
        self.path_to_logfile = path_of_directory_for_history + "/ftp_client.log"
        self.path_to_history_of_downloads = path_of_directory_for_history + "/downloands_history.pickle"
        if path_of_directory_for_history == "" or path_of_directory_for_history == ".":
            self.path_to_history_of_downloads = "downloads_history.pickle"
            self.path_to_history_of_uploads = "uploads_history.pickle"

        logging.debug("__init__ for ftp-client was called!")

        self.login = login
        self.password = password
        self.localWorkingDir = os.getcwd()
        self.remoteFileList = []
        

        # containers for downloadings and uploadings in other threads.
        # the elements should NOT be removed after ending of uploading or
        # downloading,
        # because funtions depends on index of elements in theese containers.
        # эти контейнеры созданы для загрузок и выгрузок обычным способом без приоритетов. 
        # Для приоритетных загрузок и выгрузок используются download_files b upload_files
        self.downloadings = []
        self.uploadings = []

        
        self.download_files = {} # container for downloading file block-by-block with function
        # download_file_block.
        self.download_files_for_synchronize_downloads = {} # синхронизационный словарь для загрузок.
        # когда происходит цикл загрузки - все загрузки перебираются в цикле, то есть перебирается словарь self.download_files.
        # Когда нужно добавить новую загрузку - нельзя так просто взять и добавить новую загрузку в словарь, ведь это
        # сменит количество элементов в словаре и собьёт цикл загрузки. Для этого при добавлении загрузки мы сначала добавляем её 
        # во временный словарь, а когда итерация загрузки завершилась и цикл не "бежит" по словарю - мы добавляем в него
        # загрузки из этого синхронизационного словаря.
        self.global_download_counter = 0 # айди для каждой загрузки

        self.upload_files = {} # container for uploading file block-by-block with function
        # upload_file_block.
        self.upload_files_for_synchronize_uploads = {} # синхронизационный словарь для выгрузок.
        # когда происходит цикл выгрузки - все выгрузки перебираются в цикле, то есть перебирается словарь self.upload_files.
        # Когда нужно добавить новую выгрузку - нельзя так просто взять и добавить новую выгрузку в словарь, ведь это
        # сменит количество элементов в словаре и собьёт цикл выгрузки. Для этого при добавлении выгрузки мы сначала добавляем её 
        # во временный словарь, а когда итерация выгрузки завершилась и цикл не "бежит" по словарю - мы добавляем в него
        # выгрузки из этого синхронизационного словаря.
        self.global_upload_counter = 0 # айди для каждой выгрузки
        
        self.common_loop_byte_size = 64000 # это общий размер для всех блоков. То есть, размер цикла передачи данных
        self.flag_of_working_control_thread = False # флаг для приостановления цикла выполнения контролирующего все передачи потока
        self.controlThread = None # сам контролирующий поток

        # функции GUI, которые будут вызываться при обновлении списка удалённых файлов, окончании обмена
        # файлами и прочее
        if callbacks != None:
            self.callback_for_refreshing_remote_file_list = callbacks['refresh_file_list']
            self.callback_for_file_uploaded = callbacks['file_uploaded']
            self.callback_for_file_downloaded = callbacks['file_downloaded']
            self.callback_for_priorioty_of_loading_changed = callbacks['priority_changed']
        else:
            self.callback_for_refreshing_remote_file_list = None
            self.callback_for_file_uploaded = None
            self.callback_for_file_downloaded = None
            self.callback_for_priorioty_of_loading_changed = None

        # extract the true hostanme for ftp-connection
        # выполняем подключение к серверу
        true_hostname = self.get_true_hostname(hostname)
        self.ftp = None
        
        try:
            self.ftp = ftplib.FTP()
            self.ftp.connect(true_hostname, port)
            logging.info("Connected to  \'" + str(true_hostname) + "\'!")
        except ConnectionRefusedError:
            # print("Error! Occured when trying to connect to the hostname. The connection to \'" + str(true_hostname) + "\' was refused!\n")
            # self.__del__()
            logging.error("Error! Occured when trying to connect to the hostname. The connection to \'" + str(true_hostname) + "\' was refused!")
            raise
        except socket.gaierror:
            # print("Error! Occured when trying to connect to the hostname. Adress info for \'" + str(true_hostname) + "\' is unavailable!\n")
            # self.__del__()
            logging.error("Error! Occured when trying to connect to the hostname. Adress info for \'" + str(true_hostname) + "\' is unavailable!\n")
            raise
        self.ftp.port = port
        self.ftp.login(login, password)
        logging.info("Logged in successfully!")
        
        self.ftp.cwd('.')
        self.refresh_remote_file_list()
        pass

    def __del__(self):
        '''self.stop_and_save_loads_before_exiting()
        if self.ftp != None and self.ftp.sock != None:
            self.ftp.close()
        logging.debug("__del__ for ftp-client called.")'''
        pass

    # return a true host adress from a string
    def get_true_hostname(self, hostname):
        from urllib import parse
        true_host = ''
        try:
            true_host = parse.urlparse(hostname).hostname
        except:
            # print("Error! Occured when trying to recognize the true hostname in the given string. Enter another string and try again.\n")
            logging.error("Error! Occured when trying to recognize the true hostname in the given string. Enter another string and try again.")
            raise
        return true_host
        

    # refresh remote file list self.remoteFileList
    # with path self.ftp.pwd()
    def refresh_remote_file_list(self):
        '''if self.ftp.sock == None:
            print("Error! Occured when trying receive a remote file list. The connection is empty. Connect to the FTP-server and try again!\n")
            return None'''
        try:
            self.ftp.voidcmd("NOOP")
        except ftplib.error_reply:
            # the connection is unavailable
            # print("Error! Occured when trying receive a remote file list. The connection is empty. Connect to the FTP-server and try again!\n")
            # return None
            logging.error("Error! Occured when trying receive a remote file list. The connection is empty. Connect to the FTP-server and try again!")
            raise
        self.remoteFileList.clear()
        self.ftp.dir(self.ftp.pwd(), self.addToRemoteFileList)
        # вызовем функцию обновления GUI, если она задана
        if self.callback_for_refreshing_remote_file_list != None:
            self.callback_for_refreshing_remote_file_list(self.remoteFileList)
        pass

    # called for every file or folder in self.ftp.dir when receiving a list of
    # remote files
    # add info of file or folder in self.remoteFileList
    def addToRemoteFileList(self, content):
        item = [f for f in content.split(' ') if f != '']
        mode, num, owner, group, size, date, filename = (item[0], item[1], item[2], item[3], item[4], ' '.join(item[5:8]), ' '.join(item[8:]))
        remote_file_or_folder = {}
        remote_file_or_folder['filename'] = filename
        remote_file_or_folder['size'] = size
        remote_file_or_folder['num'] = num
        remote_file_or_folder['mode'] = mode
        remote_file_or_folder['date'] = date
        remote_file_or_folder['owner'] = owner
        remote_file_or_folder['group'] = group
        self.remoteFileList.append(remote_file_or_folder)
        pass

    
    # print remote files self.remoteFileList in current remote work directory
    def print_remote_file_list(self):
        print("--- === LIST OF FILES IN CURRENT REMOTE DIRECTORY === ---")
        for file in self.remoteFileList:
            print(file['filename'] + "   " + file['size'])
        print("\n")
        pass
    
    # cd to remote directory remote_directory_name
    # and refresh self.remoteFileList with self.refresh_remote_file_list
    def cd_to_remote_directory(self, remote_directory_name):
        '''if self.ftp.sock == None:
            print("Error! Occured when trying to change remote work directory to \'" + remote_directory_name + "\'. The connection is empty. Connect to the FTP-server and try again later!\n")
            logging.error("Error! Occured when trying to change remote work directory to \'" + remote_directory_name + "\'. The connection is empty. Connect to the FTP-server and try again later!")'''
        try:
            self.ftp.voidcmd("NOOP")
        except ftplib.error_reply as err:
            # the connection is unavailable
            # print("Error! Occured when trying to change remote work directory to \'" + remote_directory_name + "\'. The connection is empty. Connect to the FTP-server and try again later!\n")
            # return
            logging.error("Error! Occured when trying to change remote work directory to \'" + remote_directory_name + "\'. The connection is empty. Connect to the FTP-server and try again later!")
            raise
        old_path = self.ftp.pwd()
        new_path = self.ftp.pwd()
        if old_path != "/":
            new_path = old_path + "/" + remote_directory_name + "/"
        else:
            new_path = old_path + remote_directory_name + "/"

        try:
            self.ftp.cwd(new_path)
        except ftplib.error_perm as err:
            # print("Error! Occured when trying to change remote file directory to \'" + remote_directory_name + 
            #      "\'. The directory is unavailable or doesn't exist! Error message: " + err.args[0] + ".\n")
            # self.ftp.cwd(old_path)
            logging.error("Error! Occured when trying to change remote file directory to \'" + remote_directory_name + 
                  "\'. The directory is unavailable or doesn't exist! Error message: " + err.args[0])
            raise
        self.refresh_remote_file_list()
        pass

    # cd to parent remote work directory and calls
    # self.refresh_remote_file_list
    def cd_to_remote_parent_directory(self):
        current_path = self.ftp.pwd()
        self.ftp.cwd(os.path.split(current_path)[0])
        self.refresh_remote_file_list()
        pass

    # cd to root remote work directory and calls self.refresh_remote_file_list
    def cd_to_remote_root_directory(self):
        '''if self.ftp.sock == None:
            print("Error! Occured when trying to change remote work directory to root directiry. The connection is empty. Connect to the FTP-server and try again later!\n")
            logging.error("Error! Occured when trying to change remote work directory to root directory. The connection is empty. Connect to the FTP-server and try again later!")
            return'''
        try:
            self.ftp.voidcmd("NOOP")
        except ftplib.error_reply as err:
            # the connection is unavailable
            # print("Error! Occured when trying to change remote work directory to root directory. The connection is empty. Connect to the FTP-server and try again later!\n")
            # return
            logging.error("Error! Occured when trying to change remote work directory to root directory. The connection is empty. Connect to the FTP-server and try again later!")
            raise
        self.ftp.cwd('/')
        self.refresh_remote_file_list()
        pass

    # make a new remote directory
    # returns full path to the directory
    def make_remote_directory(self, name_of_directory):
        result = self.ftp.mkd(name_of_directory)
        self.refresh_remote_file_list()
        return result

    # remove the remote file
    # If successful, returns the text of the response, otherwise raises error_perm on permission errors or error_reply on other errors.
    def remove_remote_file(self, filename):
        for (key, value) in self.download_files.items():
            print(self.download_files[key]['remote_filename'])
            if self.download_files[key]['remote_filename'] == filename:
                if self.download_files[key]['status'] != StatusOfLoad.STOPED and self.download_files[key]['status'] != StatusOfLoad.FINISHED:
                    raise ftplib.Error("You are trying to remove remote file, which you are downloading! Stop downloading the file then try again!")
                else:
                    self.download_files[key]["ftpInstance"].close()
                    self.download_files[key]["byteConnection"].close()
                    self.download_files[key]["fileDescriptor"].close()

        for (key, value) in self.upload_files.items():
            print(self.upload_files[key]['local_filename'])
            if self.upload_files[key]['local_filename'] == filename:
                print("aloha2")
                if self.upload_files[key]['status'] != StatusOfLoad.STOPED and self.upload_files[key]['status'] != StatusOfLoad.FINISHED:
                    raise ftplib.Error("You are trying to remove remote file, which you are uploading! Stop uploading the file then try again!")
                else:
                    self.upload_files[key]["ftpInstance"].close()
                    self.upload_files[key]["byteConnection"].close()
                    self.upload_files[key]["fileDescriptor"].close()
        result = self.ftp.delete(filename)
        self.refresh_remote_file_list()
        return result

    # remove the remote directory
    # if directory is not empty - exception: error_perm 550 Directory is not empty
    def remove_remote_directory(self, directory_name):
        result = self.ftp.rmd(directory_name)
        self.refresh_remote_file_list()
        return result

    # rename the remote file
    def rename_remote_file(self, from_name, to_name):
        for (key, value) in self.download_files.items():
            # print(self.download_files[key]['remote_filename'])
            if self.download_files[key]['remote_filename'] == from_name:
                if self.download_files[key]['status'] != StatusOfLoad.STOPED and self.download_files[key]['status'] != StatusOfLoad.FINISHED:
                    return "You are trying to rename remote file, which you are downloading! Stop downloading the file then try again!"

        for (key, value) in self.upload_files.items():
            # print(self.upload_files[key]['local_filename'])
            if self.upload_files[key]['local_filename'] == from_name:
                if self.upload_files[key]['status'] != StatusOfLoad.STOPED and self.upload_files[key]['status'] != StatusOfLoad.FINISHED:
                    return "You are trying to rename remote file, which you are uploading! Stop uploading the file then try again!"

        for file in self.remoteFileList:
            if file['filename'] == to_name:
                return "Such file is already exists!"
        try:
            result = self.ftp.rename(from_name, to_name)
            self.refresh_remote_file_list()
            return True
        except ftplib.error_perm as err:
            result = err.args[0]
            return result
        pass

    # function, which need to be called when you need to download a file
    # parallel with priority
    # it adds a downloading in downloadings (self.download_files) and then
    # function self.controlParallel process all downloadings in other threads.
    # Returns None, if the file has been already downloaded (because self.organize_downloading prints a message and returns None).
    def download(self, remote_filename, dst_local_path="", priority=0):
        new_downloading = self.organize_downloading(remote_filename, dst_local_path, priority)
        if new_downloading != None: # if the file has been already downloaded or error occured
            id_of_new_download = new_downloading["id"]
            self.download_files_for_synchronize_downloads[id_of_new_download] = new_downloading
        else:
            # print("Warning! You have already add the file \'" + remote_filename + "\' to downloads. Please, wait until it will be downloaded!")
            return None
        # example:
        ''' self.download_files["test1.py"] : { "full_path_to_remote_file" : '/new_user_folder/test1.py',
               "full_path_to_local_file" : 'C:/Users/Dima/Documents/test1.py',
              "priority" : 6,
             "size_of_remote_file" : 43758,
            "local_file_size" : 3432,
           "ftpInstance" : new_ftp,
          "byteConnection" : bytesConn,
          "fileDescriptor" : dst_local_file,
          "remote_filename" : "test1.py",
          "id" : 1,
          "start_of_downloading" : 0}'''
        return new_downloading
        pass


    # function, which need to be called when you need to upload a file
    # parallel with priority
    # it adds an uploading in uploadings (self.upload_files) and then
    # function self.controlParallel process all uploadings in other threads.
    # Returns None, if the file has been already uploaded (because self.organize_uploading prints a message and returns None).
    def upload(self, local_filename, priority=0):
        new_uploading = self.organize_uploading(local_filename, priority)
        if new_uploading != None: # if the file has been already downloaded or error occured
            id_of_new_upload = new_uploading["id"]
            self.upload_files_for_synchronize_uploads[id_of_new_upload] = new_uploading
        else:
            # print("Warning! You have already add the file \'" + remote_filename + "\' to downloads. Please, wait until it will be downloaded!")
            return None
        # example:
        ''' self.upload_files["test1.py"] : { "full_path_to_remote_file" : "/new_folder/test1.py",
               "full_path_to_local_file" : "C:/test1.py",
              "priority" : 1,
             "remote_file_size" : 64334,
            "local_file_size" : 4654323,
           "ftpInstance" : new_ftp,
          "byteConnection" : bytesConn,
          "fileDescriptor" : src_local_file,
          "local_filename" : "test1.py",
          "id" : 3,
          "start_of_uploading" : 0}'''
        return new_uploading
        pass


    # The function prepare the downloading information for new download and
    # returns a dictionary with its info and instances (like byteConnection,
    # connected ftpClient, openned fileDescriptor and others..)
    def organize_downloading(self, remote_filename, dst_local_path="", priority = 0):
        # form full path to remote file
        full_path_to_remote_file = self.ftp.pwd() + "/" + remote_filename
        if self.ftp.pwd == '/':
            full_path_to_remote_file = remote_filename

        # check the connection to server
        try:
            self.ftp.voidcmd("NOOP")
        except ftplib.error_reply:
            # the connection is unavailable
            # print("Error! Occured when trying to organize downloading file \'" + full_path_to_remote_file + "\'. The connection to FTP-server is empty. The downloading has been cancelled.\n")
            logging.error("Error! Occured when trying to organize downloading file \'" + full_path_to_remote_file + "\'. The connection to FTP-server is empty. The downloading has been cancelled.")
            raise
        

        # initialize a new FTP-client
        new_ftp = ftplib.FTP()
        new_ftp.connect(self.ftp.host, self.ftp.port)
        new_ftp.port = self.ftp.port
        new_ftp.login(self.login, self.password)
        new_ftp.cwd('.')

        # set the format of communication with ftp-server
        new_ftp.__class__.encoding = "utf-8"
        new_ftp.voidcmd("TYPE I")

        # check, if the remote file doesn't exist
        # get the size of remote file
        remote_file_size = 0
        try:
            remote_file_size = new_ftp.size(full_path_to_remote_file)
        except ftplib.error_perm as err:
            # print("Error! Occured when trying to organize downloading. File \'" + full_path_to_remote_file + "\' is unavailable to download. Error message: " + err.args[0] + ". The downloading has been cancelled.\n")
            logging.error("Error! Occured when trying to organize downloading. File \'" + full_path_to_remote_file + "\' is unavailable to download. Error message: " + err.args[0] + ". The downloading has been cancelled.")
            new_ftp.quit()
            raise

        # if dst_local_path == "", then we use cwd
        if dst_local_path == "":
            if os.getcwd() == "/":
                dst_local_path = remote_filename
            else:
                dst_local_path = os.getcwd() + "/" + remote_filename

        # open destination file for writing in it
        dst_local_file = None
        try:
            dst_local_file = open(dst_local_path, 'ab')
        except:
            # print("Error! Occured when trying to organize downloading (can't open file \'" + dst_local_path + "\' for appending in binary format for download remote file \'" + full_path_to_remote_file + "\')! The downloading has been cancelled.\n")
            logging.error("Error! Occured when trying to organize downloading (can't open file \'" + dst_local_path + "\' for appending in binary format for download remote file \'" + full_path_to_remote_file + "\')! The downloading has been cancelled.")
            new_ftp.quit()
            raise

        # check, how much bytes we already have
        local_file_size = os.path.getsize(dst_local_path)

        # check, if the file has been downloaded yet
        if local_file_size == remote_file_size:
            # print("Info: File \'" + full_path_to_remote_file + "\' has been already downloaded and available by this path \'" + dst_local_path + "\'! The downloading has been cancelled!\n")
            logging.info("Info: File \'" + full_path_to_remote_file + "\' has been already downloaded and available by this path \'" + dst_local_path + "\'! The downloading has been cancelled!\n")
            new_ftp.quit()
            dst_local_file.close()
            return None

        # check, if the local_file_size bigger than remote_file_size
        if local_file_size > remote_file_size:
            # print("Info: File \'" + full_path_to_remote_file + "\' has been already downloaded and available by this path \'" + dst_local_path + "\'! The downloading has been cancelled!\n")
            logging.info("Info: Remote file \'" + full_path_to_remote_file + "\' has smaller size, than local file \'" + dst_local_path + "\'! The downloading has been cancelled!\n")
            new_ftp.quit()
            dst_local_file.close()
            return None

        cmd = 'RETR ' + full_path_to_remote_file
        bytesConn = new_ftp.transfercmd(cmd, local_file_size)
        
        # увеличиваем айди для загрузок на 1, ведь это новая загрузка!
        self.global_download_counter = self.global_download_counter + 1

        return {"full_path_to_remote_file" : full_path_to_remote_file,
               "full_path_to_local_file" : dst_local_path,
              "priority" : priority,
             "remote_file_size" : remote_file_size,
            "local_file_size" : local_file_size,
           "ftpInstance" : new_ftp,
          "byteConnection" : bytesConn,
          "fileDescriptor" : dst_local_file,
          "remote_filename" : remote_filename,
          "id" : self.global_download_counter,
          "start_of_downloading" : 0,
          "status" : StatusOfLoad.READY}
        # status : READY, PROCESS, PAUSED, STOPED, FINISHED
        pass


    # The function prepare the uploading information for new upload and
    # returns a dictionary with its info and instances (like byteConnection,
    # connected ftpClient, openned fileDescriptor and others..)
    def organize_uploading(self, full_path_to_local_file, priority = 0):
        # check the connection to server
        try:
            self.ftp.voidcmd("NOOP")
        except ftplib.error_reply:
            # the connection is unavailable
            # print("Error! Occured when trying to organize uploading file \'" + full_path_to_local_file + "\'. The connection to FTP-server is empty. The uploading has been cancelled.\n")
            logging.error("Error! Occured when trying to organize uploading file \'" + full_path_to_local_file + "\'. The connection to FTP-server is empty. The uploading has been cancelled.")
            raise

        # initialize a new FTP-client
        new_ftp = ftplib.FTP()
        new_ftp.connect(self.ftp.host, self.ftp.port)
        new_ftp.port = self.ftp.port
        new_ftp.login(self.login, self.password)
        new_ftp.cwd('.')

        # extract the name of local file to form a full path to remote file
        local_filename = os.path.split(full_path_to_local_file)[1]

        # form path to new destination remote file
        full_path_to_remote_file = self.ftp.pwd() + "/" + local_filename
        if self.ftp.pwd() == '/':
            full_path_to_remote_file = local_filename

        # set the format of communication with ftp-server
        new_ftp.__class__.encoding = "utf-8"
        new_ftp.voidcmd("TYPE I")

        # open file for reading in binary format
        src_local_file = None
        try:
            src_local_file = open(full_path_to_local_file, 'rb') # r - read, b - binary
        except FileNotFoundError:
            # print("Error! Local file\'" + full_path_to_local_file + "\' doesn't exist, so you can't upload it on FTP-server! The uploading is cancelled!\n")
            logging.error("Error! Local file\'" + full_path_to_local_file + "\' doesn't exist, so you can't upload it on FTP-server! The uploading is cancelled!")
            new_ftp.close()
            raise
        
        # get the size of remote destination file
        remote_file_size = 0
        try:
            remote_file_size = new_ftp.size(full_path_to_remote_file)
        except:
            if new_ftp.lastresp == '550':
                # print("File \'" + destination_remote_path + "\' is a new on
                # FTP-server, so it's start uploading size from 0 byte.\n")
                remote_file_size = 0

        # get size of the local file
        local_file_size = os.path.getsize(full_path_to_local_file)

        # check, if file have the same size, then it do not need to be
        # uploaded
        if remote_file_size == local_file_size:
            # print("Info: File \'" + full_path_to_local_file + "\' has been already uploaded! The current uploading has been cancelled.\n")
            logging.info("Info: File \'" + full_path_to_local_file + "\' has been already uploaded! The current uploading has been cancelled.")
            new_ftp.quit()
            src_local_file.close()
            return None

        # check, if the local_file_size bigger than remote_file_size
        if local_file_size < remote_file_size:
            # print("Info: File \'" + full_path_to_remote_file + "\' has been already downloaded and available by this path \'" + dst_local_path + "\'! The downloading has been cancelled!\n")
            logging.info("Info: Remote file \'" + full_path_to_remote_file + "\' has bigger size, than local file \'" + dst_local_path + "\'! The downloading has been cancelled!\n")
            new_ftp.quit()
            dst_local_file.close()
            return None

        cmd = 'STOR ' + full_path_to_remote_file
        try:
            bytesConn =  new_ftp.transfercmd(cmd, remote_file_size)
        except ftplib.error_perm as err:
            # print("Error! Occured when trying to organize new uploading (can't open new byte connection with FTP-server). Local file \'" + full_path_to_local_file + "\'! Error message: " + err.args[0] + ". The uploading has been cancelled.\n")
            logging.error("Error! Occured when trying to organize new uploading (can't open new byte connection with FTP-server). Local file \'" + full_path_to_local_file + "\'! Error message: " + err.args[0] + ". The uploading has been cancelled.")
            new_ftp.quit()
            src_local_file.close()
            raise

        # увеличиваем айди для выгрузок на 1, ведь это новая выгрузка!
        self.global_upload_counter = self.global_upload_counter + 1

        # вернём айди выгрузки, полный путь к локальному файлу, полный путь к удалённому файлу, приоритет, время начала выгрузки = 0,
        # файловый дескриптор, фтп-сущность, байтовое соединение
        return {"full_path_to_remote_file" : full_path_to_remote_file,
               "full_path_to_local_file" : full_path_to_local_file,
              "priority" : priority,
             "remote_file_size" : remote_file_size,
            "local_file_size" : local_file_size,
           "ftpInstance" : new_ftp,
          "byteConnection" : bytesConn,
          "fileDescriptor" : src_local_file,
          "local_filename" : local_filename,
          "id" : self.global_upload_counter,
          "start_of_uploading" : 0,
          "status" : StatusOfLoad.READY}
        # status : READY, PROCESS, PAUSED, STOPED, FINISHED
        pass


    # The function downloads a part of file with: size = big_block_size, and
    # instances, which are need to be used for it.
    def download_block(self, download_id, ftp_instance, byte_connection, file_descriptor, big_block_size, small_block_size=8192, delay_in_seconds=0, callback=None):
        if delay_in_seconds != 0:
            time.sleep(delay_in_seconds)

        if ftp_instance == None or byte_connection == None or file_descriptor == None:
            # print("Error! Occured when trying to download a block of file! Some instances are None! Downloading the block of remote file \'" + self.download_files[download_id]['full_path_to_remote_file'] + "\' has been cancelled.\n")
            logging.error("Error! Occured when trying to download a block of file! Some instances are None! Downloading the block of remote file \'" + self.download_files[download_id]['full_path_to_remote_file'] + "\' has been cancelled.")
            return

        counter_of_received_bytes = 0
        next_step_bytes_download = small_block_size
        # нужно перед первым забиранием байт из буфера высчитать количество
        # байт, чтобы не скачать больше и скачать правильно, по кусочкам
        # проверим, не скачан ли уже файл!?
        if self.download_files[download_id]['local_file_size'] == self.download_files[download_id]['remote_file_size']:
            return
        # далее, если сказано, что размер скачиваемого блока будет меньше, чем
        # small_block_size, то присвоим следующему скачиваемому количеству байт
        # это число байт
        if big_block_size < small_block_size:
            next_step_bytes_download = big_block_size
        # теперь проверим, а что если до конца файла осталось меньше байт, чем
        # от нас потребовано скачать?  Тогда скачаем остаток файла до конца,
        # запишем в файл,
        # прибавим количество скачанных байт и выйдем из функции
        if next_step_bytes_download > self.download_files[download_id]['remote_file_size'] - self.download_files[download_id]['local_file_size']:
            next_step_bytes_download = self.download_files[download_id]['remote_file_size'] - self.download_files[download_id]['local_file_size']
          
        while counter_of_received_bytes < big_block_size:
            # print("\nNext step = " + str(next_step_bytes_download) + "
            # bytes\n")
            data = byte_connection.recv(next_step_bytes_download)
            data_length = len(data)
            counter_of_received_bytes = counter_of_received_bytes + data_length
            file_descriptor.write(data)
            self.download_files[download_id]['local_file_size'] = self.download_files[download_id]['local_file_size'] + data_length

            # нужно перед следующим забиранием байт из буфера высчитать
            # количество байт, чтобы не скачать больше и скачать правильно, по
            # кусочкам
            # проверим, не скачан ли уже файл!?
            if self.download_files[download_id]['local_file_size'] == self.download_files[download_id]['remote_file_size']:
                break
            # далее, если сказано, что размер скачиваемого блока будет меньше,
            # чем small_block_size, то присвоим следующему скачиваемому
            # количеству байт
            # это число байт
            if big_block_size - counter_of_received_bytes < small_block_size:
                next_step_bytes_download = big_block_size - counter_of_received_bytes
            # теперь проверим, а что если до конца файла осталось меньше байт,
            # чем от нас потребовано скачать?  Тогда скачаем остаток файла до
            # конца, запишем в файл,
            # прибавим количество скачанных байт и выйдем из функции
            if next_step_bytes_download > self.download_files[download_id]['remote_file_size'] - self.download_files[download_id]['local_file_size']:
                next_step_bytes_download = self.download_files[download_id]['remote_file_size'] - self.download_files[download_id]['local_file_size']
            if not data:
                break
            # end while
        # print("\n" + self.download_files[download_id]['full_path_to_remote_file'] + " === It was need to download block " + str(big_block_size) + " bytes, but downloaded " + str(counter_of_received_bytes) + " bytes.\n")
        if callback:
            callback(self.download_files[download_id]['full_path_to_remote_file'], counter_of_received_bytes)
        pass


    # The function downloads a part of file with: size = big_block_size, and
    # instances, which are need to be used for it.
    def upload_block(self, upload_id, ftp_instance, byte_connection, file_descriptor, big_block_size, small_block_size=8192, delay_in_seconds=0, callback=None):
        if delay_in_seconds != 0:
            time.sleep(delay_in_seconds)

        if ftp_instance == None or byte_connection == None or file_descriptor == None:
            # print("Error! Occured when trying to upload a block of file! Some instances are None! Downloading the block of remote file \'" + self.upload_files[upload_id]['full_path_to_remote_file'] + "\' has been cancelled.\n")
            logging.error("Error! Occured when trying to upload a block of file! Some instances are None! Uploading the block of remote file \'" + self.upload_files[upload_id]['full_path_to_remote_file'] + "\' has been cancelled.")
            return

        counter_of_sended_bytes = 0
        next_step_bytes_upload = small_block_size
        # нужно перед первой отдачей байт в буфер высчитать количество
        # байт, чтобы не отдать больше и отдать правильно, по кусочкам
        # проверим, не скачан ли уже файл!?
        if self.upload_files[upload_id]['local_file_size'] == self.upload_files[upload_id]['remote_file_size']:
            return
        # далее, если сказано, что размер отдаваемого блока будет меньше, чем
        # small_block_size, то присвоим следующему отдаваемому количеству байт
        # это число байт
        if big_block_size < small_block_size:
            next_step_bytes_upload = big_block_size
        # теперь проверим, а что если до конца файла осталось меньше байт, чем
        # от нас потребовано отдать?  Тогда отдадим остаток файла до конца
        # прибавим количество отданных байт и выйдем из функции
        if next_step_bytes_upload > self.upload_files[upload_id]['local_file_size'] - self.upload_files[upload_id]['remote_file_size']:
            next_step_bytes_upload = self.upload_files[upload_id]['local_file_size'] - self.upload_files[upload_id]['remote_file_size']
          
        while counter_of_sended_bytes < big_block_size:
            # print("\nNext step = " + str(next_step_bytes_upload) + "bytes\n")

            data = file_descriptor.read(next_step_bytes_upload)
            if not data:
                break
            byte_connection.sendall(data)
            data_length = len(data)
            counter_of_sended_bytes = counter_of_sended_bytes + data_length
            
            self.upload_files[upload_id]['remote_file_size'] = self.upload_files[upload_id]['remote_file_size'] + data_length

            # нужно перед следующей отдачей байт высчитать
            # количество байт, чтобы не отдать больше и отдать правильно, по
            # кусочкам
            # проверим, не отдан ли уже файл!?
            if self.upload_files[upload_id]['remote_file_size'] == self.upload_files[upload_id]['local_file_size']:
                break
            # далее, если сказано, что размер отдаваемого блока будет меньше,
            # чем small_block_size, то присвоим следующему отдаваемому
            # количеству байт это число байт
            if big_block_size - counter_of_sended_bytes < small_block_size:
                next_step_bytes_upload = big_block_size - counter_of_sended_bytes
            # теперь проверим, а что если до конца файла осталось меньше байт,
            # чем от нас потребовано отдать?  Тогда отдадим остаток файла до
            # конца,
            # прибавим количество отданных байт и выйдем из функции
            if next_step_bytes_upload > self.upload_files[upload_id]['local_file_size'] - self.upload_files[upload_id]['remote_file_size']:
                next_step_bytes_upload = self.upload_files[upload_id]['local_file_size'] - self.upload_files[upload_id]['remote_file_size']
            # end while
        # print("\n" + self.download_files[download_id]['full_path_to_remote_file'] + " === It was need to download block " + str(big_block_size) + " bytes, but downloaded " + str(counter_of_received_bytes) + " bytes.\n")
        if callback:
            callback(self.upload_files[upload_id]['full_path_to_remote_file'], counter_of_sended_bytes)
        pass



    # The function control parallel downloadings and uploadings
    # It is needed to be call in other thread
    # It starts download_block/upload_block for every downloading/uploading in
    # dedicated thread and then
    # synchronize it for created threads with join.  After that, the new loop
    # of block downloading/uploading begins and e.t.c.  while flag = True
    def controlParallel(self, callback_for_every_downloaded_file = None, callback_for_every_uploaded_file = None):
        while self.flag_of_working_control_thread:
            '''print("bbbbbbbbbbbbbbbbbbbNew iteration!bbbbbbbbbbbbbbbbbbbbb")
            print("Number of elements in download_files" + str(len(self.download_files.items())))
            print("Number of elements in download_files_synchr" + str(len(self.download_files_for_synchronize_downloads.items())))
            print("Number of elements in upload_files" + str(len(self.upload_files.items())))
            print("Number of elements in upload_files_synchr" + str(len(self.upload_files_for_synchronize_uploads.items())))'''
            if len(self.download_files.items()) == 0 and len(self.upload_files.items()) == 0:
                if len(self.download_files_for_synchronize_downloads.items()) == 0 and len(self.upload_files_for_synchronize_uploads.items()) == 0:
                    time.sleep(0.15)
                    # print("waiting for new loads...")
                    continue
                # append dictionary of downloadings
                for (key, downloading) in self.download_files_for_synchronize_downloads.items():
                    # check, what if file is not ready for downloading
                    if downloading['status'] == StatusOfLoad.STOPED or downloading['status'] == StatusOfLoad.FINISHED:
                        continue

                    self.download_files[key] = self.download_files_for_synchronize_downloads[key]
                    self.download_files[key]['status'] = StatusOfLoad.PROCESS
                    self.download_files[key]["start_of_downloading"] = time.time()
                    # print("File \'" + self.download_files[key]["full_path_to_remote_file"] + "\' added to downloadings!\n")
                    logging.info("File \'" + self.download_files[key]["full_path_to_remote_file"] + "\' added to downloadings!")
                self.download_files_for_synchronize_downloads.clear()

                # append dictionary of uploadings
                for (key, uploading) in self.upload_files_for_synchronize_uploads.items():
                    # check, what if file is not ready for uploading
                    if uploading['status'] == StatusOfLoad.STOPED or uploading['status'] == StatusOfLoad.FINISHED:
                        continue
                    
                    self.upload_files[key] = self.upload_files_for_synchronize_uploads[key]
                    self.upload_files[key]['status'] = StatusOfLoad.PROCESS
                    self.upload_files[key]["start_of_uploading"] = time.time()
                    # print("File \'" + self.upload_files[key]["full_path_to_local_file"] + "\' added to uploadings!\n")
                    logging.info("File \'" + self.upload_files[key]["full_path_to_local_file"] + "\' added to uploadings!")
                self.upload_files_for_synchronize_uploads.clear()
                continue
            
            threads = []

            # find in priority max, min and sum of all
            min_priority = 1
            max_priority = 1
            sum_of_priorities = 1
            
            for (key, downloading) in self.download_files.items():
                if downloading['status'] == StatusOfLoad.PROCESS:
                    if min_priority > downloading['priority']:
                        min_priority = downloading['priority']
                    if max_priority < downloading['priority']:
                        max_priority = downloading['priority']
                    sum_of_priorities = sum_of_priorities + downloading['priority']

            for (key, uploading) in self.upload_files.items():
                if uploading['status'] == StatusOfLoad.PROCESS:
                    if min_priority > uploading['priority']:
                        min_priority = uploading['priority']
                    if max_priority < uploading['priority']:
                        max_priority = uploading['priority']
                    sum_of_priorities = sum_of_priorities + uploading['priority']

            average_priority = int((max_priority - min_priority) / 2)

            one_block = self.common_loop_byte_size / sum_of_priorities



            # a function, which will be called, when the block will be received
            def callback_for_downloaded_block(full_path_to_remote_file, length_of_downloaded_block):
                # print("Block (" + str(length_of_uploaded_block) + " bytes) of remote file \'" + full_path_to_remote_file + "\' is received.\n")
                pass

            # download block for every download
            for (key, downloading) in self.download_files.items():
                if downloading['status'] != StatusOfLoad.PROCESS:
                    continue
                t = threading.Thread()
                t._target = self.download_block
                t._args = (downloading['id'], 
                           downloading['ftpInstance'], 
                           downloading['byteConnection'],
                           downloading['fileDescriptor'],
                           int(one_block * downloading['priority']), 
                           8192, 
                           0.0, 
                           callback_for_downloaded_block)
                t.start()
                threads.append(t)

            # a function, which will be called, when the block will be sended
            def callback_for_uploaded_block(full_path_to_local_file, length_of_uploaded_block):
                # print("Block (" + str(length_of_uploaded_block) + " bytes) of local file \'" + full_path_to_local_file + "\' is sended.\n")
                pass

            # upload block for every upload
            for (key, uploading) in self.upload_files.items():
                if uploading['status'] != StatusOfLoad.PROCESS:
                    continue
                t = threading.Thread()
                t._target = self.upload_block
                t._args = (uploading['id'], 
                           uploading['ftpInstance'], 
                           uploading['byteConnection'],
                           uploading['fileDescriptor'],
                           int(one_block * uploading['priority']), 
                           8192, 
                           0.0, 
                           callback_for_uploaded_block)
                t.start()
                threads.append(t)

            # waiting, when all blocks will be downloaded
            for thread in threads:
                thread.join()

            # append dictionary of downloadings
            for (key, downloading) in self.download_files_for_synchronize_downloads.items():
                # check, what if file is not ready for downloading
                if downloading['status'] != StatusOfLoad.READY:
                    continue
                self.download_files[key] = self.download_files_for_synchronize_downloads[key]
                self.download_files[key]["start_of_downloading"] = time.time()
                self.download_files[key]["status"] = StatusOfLoad.PROCESS
                # print("File \'" + self.download_files[key]["full_path_to_remote_file"] + "\' added to downloadings!\n")
                logging.info("File \'" + self.download_files[key]["full_path_to_remote_file"] + "\' added to downloadings!")
            self.download_files_for_synchronize_downloads.clear()

            # append dictionary of uploadings
            for (key, uploading) in self.upload_files_for_synchronize_uploads.items():
                # check, what if file is not ready for downloading
                if uploading['status'] != StatusOfLoad.READY:
                    continue
                self.upload_files[key] = self.upload_files_for_synchronize_uploads[key]
                self.upload_files[key]["start_of_uploading"] = time.time()
                self.upload_files[key]['status'] = StatusOfLoad.PROCESS
                # print("File \'" + self.upload_files[key]["full_path_to_local_file"] + "\' added to uploadings!\n")
                logging.info("File \'" + self.upload_files[key]["full_path_to_local_file"] + "\' added to uploadings!")
            self.upload_files_for_synchronize_uploads.clear()
            
            
            # finish downloadings if it has been downloaded
            # Нельзя пробегать по словарю в цикле и удалять из него элементы в
            # этом же цикле.
            # Если файл полностью загружен, то создадим список с ключами, которые удалим в цикле дальше из
            # словаря
            list_of_downloads_keys_for_deleting = []
            for (key, downloading) in self.download_files.items():
                if self.download_files[key]['remote_file_size'] == self.download_files[key]['local_file_size'] or self.download_files[key]['status'] == StatusOfLoad.STOPED:
                    self.download_files[key]['status'] = StatusOfLoad.FINISHED
                    # print("File \'" + self.download_files[key]["full_path_to_remote_file"] + "\' has been downloaded successfully! The time spent to download it is = " + str(time.time() - self.download_files[key]["start_of_downloading"]) + " seconds. Size of the file = " + format(self.upload_files[key]['remote_file_size'] / 1024 / 1024, ".4f") + " MB.")
                    logging.info("File \'" + self.download_files[key]["full_path_to_remote_file"] + "\' has been downloaded successfully! The time spent to download it is = " + str(time.time() - self.download_files[key]["start_of_downloading"]) + " seconds. Size of the file = " + format(self.download_files[key]['remote_file_size'] / 1024 / 1024, ".4f") + " MB.")
                    list_of_downloads_keys_for_deleting.append(key)


            for key in list_of_downloads_keys_for_deleting:
                # для каждого загруженного файла вызовем функцию обратного вызова
                if callback_for_every_downloaded_file != None:
                    callback_for_every_downloaded_file(self.download_files[key])
                self.download_files[key]["ftpInstance"].quit()
                self.download_files[key]["byteConnection"].close()
                self.download_files[key]["fileDescriptor"].close()
                # перед удалением из списка выгрузок вызовем каллбэк-метод
                self.callback_for_file_downloaded(self.download_files[key]['full_path_to_local_file'])
                self.download_files.pop(key)

            list_of_downloads_keys_for_deleting.clear()

            # finish uploadings if it has been uploaded
            # Нельзя пробегать по словарю в цикле и удалять из него элементы в
            # этом же цикле.
            # Если файл полностью выгружен, то создадим список с ключами, которые удалим в цикле дальше из
            # словаря
            counter_for_deleting_uploads = 0
            list_of_uploads_keys_for_deleting = []
            for (key, uploading) in self.upload_files.items():
                if self.upload_files[key]['remote_file_size'] == self.upload_files[key]['local_file_size'] or self.upload_files[key]['status'] == StatusOfLoad.STOPED:
                    self.upload_files[key]['status'] = StatusOfLoad.FINISHED
                    # print("File \'" + self.upload_files[key]["full_path_to_local_file"] + "\' has been uploaded successfully! The time spent to upload it is = " + str(time.time() - self.upload_files[key]["start_of_uploading"]) + " seconds. Size of the file = " + format(self.upload_files[key]['remote_file_size'] / 1024 / 1024, ".4f") + " MB.")
                    logging.info("File \'" + self.upload_files[key]["full_path_to_local_file"] + "\' has been uploaded successfully! The time spent to upload it is = " + str(time.time() - self.upload_files[key]["start_of_uploading"]) + " seconds. Size of the file = " + format(self.upload_files[key]['remote_file_size'] / 1024 / 1024, ".4f") + " MB.")
                    list_of_uploads_keys_for_deleting.append(key)
                    counter_for_deleting_uploads = counter_for_deleting_uploads + 1

            

            for key in list_of_uploads_keys_for_deleting:
                # для каждого выгруженного файла вызовем функцию обратного вызова
                if callback_for_every_uploaded_file != None:
                    callback_for_every_uploaded_file(self.upload_files[key])
                self.upload_files[key]["ftpInstance"].quit()
                self.upload_files[key]["byteConnection"].close()
                self.upload_files[key]["fileDescriptor"].close()
                # перед удалением из списка выгрузок вызовем каллбэк-метод
                if self.callback_for_file_uploaded != None:
                    self.callback_for_file_uploaded(self.upload_files[key]['full_path_to_local_file'])
                self.upload_files.pop(key)

            # какие-то файл загрузились на сервер. Нужно обновить список файлов
            if counter_for_deleting_uploads != 0:
                self.refresh_remote_file_list()

            list_of_uploads_keys_for_deleting.clear()
        pass

    def start_control(self):
        self.flag_of_working_control_thread = True
        self.controlThread = threading.Thread()
        self.controlThread._target = self.controlParallel
        self.controlThread.start()
        # print("Info: The control thread has been started!\n")
        logging.info("Info: The control thread has been started!")
        pass

    def stop_control(self):
        self.flag_of_working_control_thread = False
        # print("Info: The control thread has been stopped! The last iteration of control loop is waited for completing.\n")
        # ogging.info("Info: The control thread has been stopped! The last iteration of control loop is waited for completing.") 
        # logging не работает в __del__, т.к. логгинг очищается и в нём ничего не остаётся
        f = os.open(self.path_to_logfile, os.O_RDWR|os.O_CREAT| os.O_APPEND)
        os.write(f, (time.strftime('%Y-%m-%d %H:%M:%S ') + "INFO: The control thread (loop) has been signalled to stop! The last iteration of control thread (loop) is waited for completing.\n").encode('utf-8'))
        os.close(f)
        # print("-stop_and_save_loads_before_exiting- joining controlThread")
        # дожидаемся, когда последние блоки будут приняты\переданы и дописываем последние принятые блоки в файлы
        if self.controlThread != None:
            self.controlThread.join()

        f = os.open(self.path_to_logfile, os.O_RDWR|os.O_CREAT| os.O_APPEND)
        os.write(f, (time.strftime('%Y-%m-%d %H:%M:%S ') + "INFO: The control thread (loop) has been completely stoped (the thread was joined).\n").encode('utf-8'))
        os.close(f)
        pass

    # Function saves all downloadings and uploadings before the instance of the class will be deleting
    def stop_and_save_loads_before_exiting(self):
        # print("-stop_and_save_loads_before_exiting- self.flag_of_working_control_thread = False")
        # останавливаем передачу и приём блоков от фалйов
        self.stop_control()        
        # print("-stop_and_save_loads_before_exiting- closing instances")
        # закрываем важные обекты (подключения, файловые дескрипторы, закрываем фтп-соединение)
        self.close_downloads_instances()
        self.close_uploads_instances()
        self.ftp.close()
        # print("-stop_and_save_loads_before_exiting- saving downloads in file")
        # logging.info("Saving downloads in file \'" + self.path_to_history_of_downloads + "\'")
        f = os.open(self.path_to_logfile, os.O_RDWR|os.O_CREAT| os.O_APPEND)
        os.write(f, (time.strftime('%Y-%m-%d %H:%M:%S ') + "INFO: Saving downloads in file \'" + self.path_to_history_of_downloads + "\'\n").encode('utf-8'))
        os.close(f)
        # сериализуем все загрузки в файл
        # будем сериализовать всё, кроме фтп-сущности, файлового дескриптора, байтового соединения
        dict_of_downloads_for_saving = {}
        for (key, value) in self.download_files.items():
            dict_of_downloads_for_saving[key] = { 'remote_filename' : self.download_files[key]['remote_filename'],
                                                 'full_path_to_remote_file' : self.download_files[key]['full_path_to_remote_file'],
                                                 'full_path_to_local_file' : self.download_files[key]['full_path_to_local_file'],
                                                 'priority' : self.download_files[key]['priority'],
                                                 'start_of_downloading' : self.download_files[key]['start_of_downloading'],
                                                 'local_file_size' : self.download_files[key]['local_file_size'],
                                                 'remote_file_size' : self.download_files[key]['remote_file_size'],
                                                 'status' : self.download_files[key]['status']}
            if self.download_files[key]['status'] == StatusOfLoad.PROCESS:
                dict_of_downloads_for_saving[key]['status'] = StatusOfLoad.PAUSED
        if os.path.exists(self.path_to_history_of_downloads):
            os.remove(self.path_to_history_of_downloads)
        f = os.open(self.path_to_history_of_downloads, os.O_WRONLY|os.O_CREAT)
        os.write(f, pickle.dumps(dict_of_downloads_for_saving))
        os.close(f)
        self.download_files.clear()

        # logging.info("Saving uploads in file \'" + self.path_to_history_of_uploads + "\'")
        f = os.open(self.path_to_logfile, os.O_RDWR|os.O_CREAT| os.O_APPEND)
        os.write(f, (time.strftime('%Y-%m-%d %H:%M:%S ') + "INFO: Saving uploads in file \'" + self.path_to_history_of_uploads + "\'\n").encode('utf-8'))
        os.close(f)
        # сериализуем все выгрузки в файл
        # будем сериализовать всё, кроме фтп-сущности, файлового дескриптора, байтового соединения
        dict_of_uploads_for_saving = {}
        for (key, value) in self.upload_files.items():
            dict_of_uploads_for_saving[key] = { 'local_filename' : self.upload_files[key]['local_filename'],
                                                 'full_path_to_remote_file' : self.upload_files[key]['full_path_to_remote_file'],
                                                 'full_path_to_local_file' : self.upload_files[key]['full_path_to_local_file'],
                                                 'priority' : self.upload_files[key]['priority'],
                                                 'start_of_uploading' : self.upload_files[key]['start_of_uploading'],
                                                 'local_file_size' : self.upload_files[key]['local_file_size'],
                                                 'remote_file_size' : self.upload_files[key]['remote_file_size'],
                                                 'status' : self.upload_files[key]['status']}
            if self.upload_files[key]['status'] == StatusOfLoad.PROCESS:
                dict_of_uploads_for_saving[key]['status'] = StatusOfLoad.PAUSED
        if os.path.exists(self.path_to_history_of_uploads):
            os.remove(self.path_to_history_of_uploads)
        f = os.open(self.path_to_history_of_uploads, os.O_WRONLY|os.O_CREAT)
        os.write(f, pickle.dumps(dict_of_uploads_for_saving))
        os.close(f)
        self.upload_files.clear()
        pass

    # Function closes all ftp_clients (including main ftp-client), closes BytesConnections and FileDescriptors
    # ONLY FOR DOWNLOADS
    def close_downloads_instances(self):
        for (key, downloading) in self.download_files.items():
            # print("-close_downloads_instances- self.download_files[key]['ftpInstance'].close()")
            self.download_files[key]["ftpInstance"].close()
            # print("-close_downloads_instances- self.download_files[key]['byteConnection'].close()")
            self.download_files[key]["byteConnection"].close()
            # print("-close_downloads_instances- self.download_files[key]['fileDescriptor'].close()")
            self.download_files[key]["fileDescriptor"].close()
        pass

    # Function closes all ftp_clients (including main ftp-client), closes BytesConnections and FileDescriptors
    # ONLY FOR UPLOADS
    def close_uploads_instances(self):
        for (key, uploading) in self.upload_files.items():
            # print("-close_uploads_instances- self.upload_files[key]['ftpInstance'].close()")
            self.upload_files[key]["ftpInstance"].close()
            # print("-close_uploads_instances- self.upload_files[key]['byteConnection'].close()")
            self.upload_files[key]["byteConnection"].close()
            # print("-close_uploads_instances- self.upload_files[key]['fileDescriptor'].close()")
            self.upload_files[key]["fileDescriptor"].close()
        pass


    # Renew all loads from history
    def renew_all_loads_from_history(self):
        self.renew_downloadings_from_history()
        self.renew_uploadings_from_history()
        pass


    # Function renew downloadings from history file
    def renew_downloadings_from_history(self):
        logging.info("Renewing downloadings from history-file \'" + self.path_to_history_of_downloads + "\'.")
        # сначала выгрузим из файла историю загрузок
        #with open(self.path_to_history_of_downloads, 'rb') as f:
        #    downloadings_history = pickle.load(f)
        f = os.open(self.path_to_history_of_downloads, os.O_RDONLY)
        bytes_history_downloads = os.read(f, os.path.getsize(self.path_to_history_of_downloads))
        os.close(f)
        downloadings_history = pickle.loads(bytes_history_downloads)
        # print("************" + str(downloadings_history) + "*************")

        # для каждой старой загрузки создадим новую загрузку, только с теми же путями, размерами и так далее
        for (key, downloading) in downloadings_history.items():
            # print( str(key) + "==================" + str(downloading))
            # initialize a new FTP-client
            new_ftp = ftplib.FTP()
            new_ftp.connect(self.ftp.host, self.ftp.port)
            new_ftp.port = self.ftp.port
            new_ftp.login(self.login, self.password)
            new_ftp.cwd('.')
            # set the format of communication with ftp-server
            new_ftp.__class__.encoding = "utf-8"
            new_ftp.voidcmd("TYPE I")

            # check, if the remote file doesn't exist
            # get the size of remote file
            remote_file_size = 0
            try:
                remote_file_size = new_ftp.size(downloading['full_path_to_remote_file'])
            except ftplib.error_perm as err:
                if new_ftp.lastresp == '550':
                    # print("Error occured when trying to renew downloading remote file \'" + downloading['full_path_to_remote_file'] + "\' from history. The remote file is unavailable to download. Renewing current downloading has been skipped. Error message:" + err.args[0] + "\n")
                    logging.error("Error occured when trying to renew downloading remote file \'" + downloading['full_path_to_remote_file'] + "\' from history. The remote file is unavailable to download. Renewing current downloading has been skipped. Error message:" + err.args[0])
                continue

            # open destination file for writing in it
            dst_local_file = None
            try:
                dst_local_file = open(downloading['full_path_to_local_file'], 'ab')
            except:
                # print("Error occured when trying to renew downloading remote file \'" + downloading['full_path_to_local_file'] + "\' from history. Can not open the file in binary format for appending! Renewing current downloading has been skipped.\n")
                # new_ftp.quit()
                # continue
                logging.error("Error occured when trying to renew downloading remote file \'" + downloading['full_path_to_local_file'] + "\' from history. Can not open the file in binary format for appending! Renewing current downloading has been skipped.")
                new_ftp.quit()
                continue

            # check, how much bytes we already have
            local_file_size = os.path.getsize(downloading['full_path_to_local_file'])

            # check, if the file has been downloaded yet
            if local_file_size == remote_file_size:
                # print("Info. Try to renew downloading remote file \'" + downloading['full_path_to_remote_file'] + "\' from history. The file has been already downloaded! Renewing downloading of this file has been skipped.\n")
                # new_ftp.quit()
                # dst_local_file.close()
                # continue
                logging.info("Info. Try to renew downloading remote file \'" + downloading['full_path_to_remote_file'] + "\' from history. The file has been already downloaded! Renewing downloading of this file has been skipped.")
                new_ftp.quit()
                dst_local_file.close()
                continue
            elif local_file_size > remote_file_size:
                # print("Error! Occured when trying to renew downloading from history! Local file \'" + downloading['full_path_to_local_file'] + "\' has size bigger, than the remote \'" + downloading['full_path_to_remote_file'] + "\' file! Renewing downloading of this file has been skipped.\n")
                # continue
                logging.error("Error! Occured when trying to renew downloading from history! Local file \'" + downloading['full_path_to_local_file'] + "\' has size bigger, than the remote \'" + downloading['full_path_to_remote_file'] + "\' file! Renewing downloading of this file has been skipped.")
                continue

            cmd = 'RETR ' + downloading['full_path_to_remote_file']
            bytesConn = new_ftp.transfercmd(cmd, local_file_size)
        
            # увеличиваем айди для загрузок на 1, ведь это новая загрузка!
            self.global_download_counter = self.global_download_counter + 1

            old_downloading_for_renew = {"full_path_to_remote_file" : downloading['full_path_to_remote_file'],
                   "full_path_to_local_file" : downloading['full_path_to_local_file'],
                  "priority" : downloading['priority'],
                 "remote_file_size" : remote_file_size,
                "local_file_size" : local_file_size,
               "ftpInstance" : new_ftp,
              "byteConnection" : bytesConn,
              "fileDescriptor" : dst_local_file,
              "remote_filename" : downloading['remote_filename'],
              "id" : self.global_download_counter,
              "start_of_downloading" : downloading['start_of_downloading'],
              "status" : downloading['status']}

            self.download_files_for_synchronize_downloads[self.global_download_counter] = old_downloading_for_renew
        pass

    # Function renew uploadings from history file
    def renew_uploadings_from_history(self):
        logging.info("Renewing uploadings from history-file \'" + self.path_to_history_of_downloads + "\'.")
        # сначала выгрузим из файла историю выгрузок
        #with open(self.path_to_history_of_uploads, 'rb') as f:
        #    uploadings_history = pickle.load(f)
        f = os.open(self.path_to_history_of_uploads, os.O_RDONLY)
        bytes_history_uploads = os.read(f, os.path.getsize(self.path_to_history_of_uploads))
        os.close(f)
        uploadings_history = pickle.loads(bytes_history_uploads)

        # для каждой старой выгрузки создадим новую выгрузку, только с теми же путями, размерами и так далее
        for (key, uploading) in uploadings_history.items():
            # initialize a new FTP-client
            new_ftp = ftplib.FTP()
            new_ftp.connect(self.ftp.host, self.ftp.port)
            new_ftp.port = self.ftp.port
            new_ftp.login(self.login, self.password)
            new_ftp.cwd('.')
            # set the format of communication with ftp-server
            new_ftp.__class__.encoding = "utf-8"
            new_ftp.voidcmd("TYPE I")

            # check, how much bytes ftp-server already has of the file
            remote_file_size = 0
            try:
                remote_file_size = new_ftp.size(uploading['full_path_to_remote_file'])
            except ftplib.error_perm as err:
                if new_ftp.lastresp == '550':
                    remote_file_size = 0

            # open source file for reading it
            src_local_file = None
            try:
                src_local_file = open(uploading['full_path_to_local_file'], 'rb')
            except:
                # print("Error occured when trying to renew uploading of local file \'" + uploading['full_path_to_local_file'] + "\' from histroy. Can not to open for reading in binary format! Renewing uploading of this file has been skipped.")
                # new_ftp.quit()
                # continue
                logging.error("Error occured when trying to renew uploading of local file \'" + uploading['full_path_to_local_file'] + "\' from histroy. Can not to open for reading in binary format! Renewing uploading of this file has been skipped.")
                new_ftp.quit()
                continue
                

            # get size of local file (what if it was changed?)
            local_file_size = os.path.getsize(uploading['full_path_to_local_file'])

            # check, if file have the same size, then it do not need to be uploaded
            if remote_file_size == local_file_size:
                # print("Info. Try to renew uploading local file \'" + uploading['full_path_to_local_file'] + "\' from history. The file has been already uploaded! Renewing uploading of this file has been skipped.\n")
                # new_ftp.quit()
                # src_local_file.close()
                # continue
                logging.info("Info: Try to renew uploading local file \'" + uploading['full_path_to_local_file'] + "\' from history. The file has been already uploaded! Renewing uploading of this file has been skipped.")
                new_ftp.quit()
                src_local_file.close()
                continue
            elif remote_file_size > local_file_size:
                # print("Error when trying to renew uploading from history! Remote file \'" + uploading['full_path_to_remote_file'] + "\' has size bigger, than the local \'" + uploading['full_path_to_local_file'] + "\' file! Renewing uploading of this file has been skipped.\n")
                # continue
                logging.error("Error! Occured when trying to renew uploading from history! Remote file \'" + uploading['full_path_to_remote_file'] + "\' has size bigger, than the local \'" + uploading['full_path_to_local_file'] + "\' file! Renewing uploading of this file has been skipped.")
                continue

            cmd = 'STOR ' + uploading['full_path_to_remote_file']
            try:
                bytesConn =  new_ftp.transfercmd(cmd, remote_file_size)
            except ftplib.error_perm as err:
                # print("Error! Occured when trying to renew uploading local file \'" + uploading['full_path_to_remote_file'] + "\' from history! Error message: " + err.args[0] + ". The renewing uploading has been cancelled.\n")
                # new_ftp.quit()
                # src_local_file.close()
                # continue
                logging.warning("Warning! Occured when trying to renew uploading local file \'" + uploading['full_path_to_remote_file'] + "\' from history! Error message: " + err.args[0] + ". The renewing uploading has been cancelled.")
                new_ftp.quit()
                src_local_file.close()
                continue

            # увеличиваем айди для выгрузок на 1, ведь это новая выгрузка!
            self.global_upload_counter = self.global_upload_counter + 1

            old_uploading_for_renew = {"full_path_to_remote_file" : uploading['full_path_to_remote_file'],
                   "full_path_to_local_file" : uploading['full_path_to_local_file'],
                  "priority" : uploading['priority'],
                 "remote_file_size" : remote_file_size,
                "local_file_size" : local_file_size,
               "ftpInstance" : new_ftp,
              "byteConnection" : bytesConn,
              "fileDescriptor" : src_local_file,
              "local_filename" : uploading['local_filename'],
              "id" : self.global_upload_counter,
              "start_of_uploading" : uploading['start_of_uploading'],
              "status" : uploading['status']}

            self.upload_files_for_synchronize_uploads[self.global_upload_counter] = old_uploading_for_renew
        pass

    def set_priority_of_downloading(self, full_path_to_remote_file, new_priority):
        flag_of_changed = False
        for (key,value) in self.download_files.items():
            if value['full_path_to_remote_file'] == full_path_to_remote_file:
                flag_of_changed = True
                value['priority'] = new_priority
        if flag_of_changed == False:
            # print("Error! Occured when trying to change priority of downloading remote file\'" + full_path_to_remote_file + "\'. There is no such downloading file. The action has been skipped.\n")
            logging.error("Error! Occured when trying to change priority of downloading remote file\'" + full_path_to_remote_file + "\'. There is no such downloading file. The action has been skipped.")
        pass

    def set_priority_of_uploading(self, full_path_to_local_file, new_priority):
        flag_of_changed = False
        for (key,value) in self.upload_files.items():
            if value['full_path_to_local_file'] == full_path_to_local_file:
                flag_of_changed = True
                value['priority'] = new_priority
        if flag_of_changed == False:
            # print("Error! Occured when trying to change priority of downloading remote file\'" + full_path_to_remote_file + "\'. There is no such downloading file. The action has been skipped.\n")
            logging.error("Error! Occured when trying to change priority of uploading local file\'" + full_path_to_local_file + "\'. There is no such uploading file. The action has been skipped.")
        pass


    def set_priority_of_loading(self, full_path_to_local_file, new_priority):
        flag_of_changed = False
        for (key,value) in self.upload_files.items():
            if value['full_path_to_local_file'] == full_path_to_local_file:
                old_priority = value['priority']
                value['priority'] = new_priority
                flag_of_changed = True
                logging.debug("Priority of uploading file with local path \'" + full_path_to_local_file +"\' was set from " + str(old_priority) + " to " + str(new_priority) + ".")
        if flag_of_changed == True:
            self.callback_for_priorioty_of_loading_changed(full_path_to_local_file, new_priority)
            return True

        flag_of_changed = False
        for (key,value) in self.download_files.items():
            if value['full_path_to_local_file'] == full_path_to_local_file:
                old_priority = value['priority']
                value['priority'] = new_priority
                flag_of_changed = True
                logging.debug("Priority of downloading file with local path \'" + full_path_to_local_file +"\' was set from " + str(old_priority) + " to " + str(new_priority) + ".")
        if flag_of_changed == True:
            self.callback_for_priorioty_of_loading_changed(full_path_to_local_file, new_priority)
            return True

        # print("Error! Occured when trying to change priority of downloading remote file\'" + full_path_to_remote_file + "\'. There is no such downloading file. The action has been skipped.\n")
        logging.error("Warning! Occured when trying to change priority of (down/up)loading local file\'" + full_path_to_local_file + "\'. There is no such uploading and downloading file. The action has been skipped.")
        return False
        pass

    def pause_downloading(self, full_path_to_local_file):
        flag_of_changed = False
        for (key,value) in self.download_files.items():
            if value['full_path_to_local_file'] == full_path_to_local_file:
                flag_of_changed = True
                value['status'] = StatusOfLoad.PAUSED
                logging.info("Downloading remote file with local path \'" + full_path_to_local_file + "\' has been PAUSED forcibly.")
        if flag_of_changed == False:
            # print("Error! Occured when trying to change priority of downloading remote file\'" + full_path_to_remote_file + "\'. There is no such downloading file. The action has been skipped.\n")
            logging.debug("Warning! Occured when trying to PAUSE downloading remote file with local path \'" + full_path_to_local_file + "\'. There is no such uploading file. The action has been skipped.")
            return False
        return True
        pass

    def pause_uploading(self, full_path_to_local_file):
        flag_of_changed = False
        for (key,value) in self.upload_files.items():
            if value['full_path_to_local_file'] == full_path_to_local_file:
                flag_of_changed = True
                value['status'] = StatusOfLoad.PAUSED
                logging.info("Uploading local file\'" + full_path_to_local_file + "\' has been PAUSED forcibly.")
        if flag_of_changed == False:
            # print("Error! Occured when trying to change priority of downloading remote file\'" + full_path_to_remote_file + "\'. There is no such downloading file. The action has been skipped.\n")
            logging.debug("Warning! Occured when trying to PAUSE uploading local file\'" + full_path_to_local_file + "\'. There is no such uploading file. The action has been skipped.")
            return False
        return True
        pass

    def stop_downloading(self, full_path_to_local_file):
        flag_of_changed = False
        for (key,value) in self.download_files.items():
            if value['full_path_to_local_file'] == full_path_to_local_file:
                flag_of_changed = True
                value['status'] = StatusOfLoad.STOPED
                logging.info("Downloading remote file with local path \'" + full_path_to_local_file + "\' has been STOPPED forcibly.")
        if flag_of_changed == False:
            # print("Error! Occured when trying to change priority of downloading remote file\'" + full_path_to_remote_file + "\'. There is no such downloading file. The action has been skipped.\n")
            logging.debug("Warning! Occured when trying to STOP downloading remote file with local path \'" + full_path_to_local_file + "\'. There is no such uploading file. The action has been skipped.")
            return False
        return True
        pass

    def stop_uploading(self, full_path_to_local_file):
        flag_of_changed = False
        for (key,value) in self.upload_files.items():
            if value['full_path_to_local_file'] == full_path_to_local_file:
                flag_of_changed = True
                value['status'] = StatusOfLoad.STOPED
                logging.info("Uploading local file\'" + full_path_to_local_file + "\' has been STOPPED forcibly.")
        if flag_of_changed == False:
            # print("Error! Occured when trying to change priority of downloading remote file\'" + full_path_to_remote_file + "\'. There is no such downloading file. The action has been skipped.\n")
            logging.debug("Error! Occured when trying to STOP uploading local file\'" + full_path_to_local_file + "\'. There is no such uploading file. The action has been skipped.")
            return False
        return True
        pass

    def continue_downloading(self, full_path_to_local_file):
        flag_of_changed = False
        for (key,value) in self.download_files.items():
            if value['full_path_to_local_file'] == full_path_to_local_file:
                flag_of_changed = True
                value['status'] = StatusOfLoad.PROCESS
                logging.info("Downloading remote file with local path \'" + full_path_to_local_file + "\' has been continued(PROCESSES) forcibly.")
        if flag_of_changed == False:
            # print("Error! Occured when trying to change priority of downloading remote file\'" + full_path_to_remote_file + "\'. There is no such downloading file. The action has been skipped.\n")
            logging.debug("Warning! Occured when trying to continue(PROCESS) downloading remote file with local path \'" + full_path_to_local_file + "\'. There is no such uploading file. The action has been skipped.")
            return False
        return True
        pass

    def continue_uploading(self, full_path_to_local_file):
        flag_of_changed = False
        for (key,value) in self.upload_files.items():
            if value['full_path_to_local_file'] == full_path_to_local_file:
                flag_of_changed = True
                value['status'] = StatusOfLoad.PROCESS
                logging.info("Uploading local file\'" + full_path_to_local_file + "\' has been continued(PROCESSED) forcibly.")
        if flag_of_changed == False:
            # print("Error! Occured when trying to change priority of downloading remote file\'" + full_path_to_remote_file + "\'. There is no such downloading file. The action has been skipped.\n")
            logging.debug("Error! Occured when trying to continue(PROCESS) uploading local file\'" + full_path_to_local_file + "\'. There is no such uploading file. The action has been skipped.")
            return False
        return True
        pass

    # download remote file with the main class ftp client (self.ftp)
    def download_file(self, filename, destination_path, blocksize=8192, delay_in_seconds=0):
        try:
            self.ftp.voidcmd("NOOP")
        except ftplib.error_reply:
            # the connection is unavailable
            print("Error occured when trying to download a file \'" + filename + "\'. The connection is empty.\n")
            raise

        # form path to src remote file
        # srcfile = os.path.join(self.ftp.pwd(), filename) # в Windows
        # добавляет обратную косую черту и потом не понимает путь
        srcfile = self.ftp.pwd() + "/" + filename
        if self.ftp.pwd() == '/':
            srcfile = filename

        # set the format of communication with ftp-server
        self.ftp.__class__.encoding = "utf-8"
        self.ftp.voidcmd("TYPE I")

        # get the size of remote destination file
        remote_file_size = 0
        try:
            remote_file_size = self.ftp.size(srcfile)
        except:
            if self.ftp.lastresp == '550':
                print("Error. File \'" + srcfile + "\' is unavailable or doesn't exist on FTP-server!\n")
                return 550

        # open file for appending
        dst_file = open(destination_path, 'ab') # a - append, b - binary
        
        local_file_size = os.path.getsize(destination_path)
        #local_file_size = 0

        # check, if files have the same size, then it do not need to be
        # downloaded
        if remote_file_size == local_file_size:
            print("File \'" + filename + "\' has been already downloaded!\n")
            dst_file.close()
            return

        def callback(data):
            dst_file.write(data)
            # print("Receive a block of data (" + str(len(data)) + "). Now i wanna sleep " + str(delay_in_seconds) + " seconds.")
            if delay_in_seconds != 0:
                time.sleep(delay_in_seconds)
            # можно добавить time.sleep(1) и так контролить время загрузки
            #print("Получен кусок из файла " + srcfile + " размером " +
            #str(len(data)) + " байт.")
            pass

        print("Start downloading file \'" + srcfile + "\' starts downloading. File size = " + format(remote_file_size / 1024 / 1024, ".3f") + " MB. \n")
        print("Downloading starts from " + str(local_file_size) + " byte.\n")
        timeOfDownloading = time.time()
        self.ftp.retrbinary(cmd='RETR ' + srcfile, rest=local_file_size, callback=callback, blocksize=blocksize)
        timeOfDownloading = time.time() - timeOfDownloading
        dst_file.close()
        print("Finish downloading file \'" + srcfile + "\'.Time of downloading = " + format(timeOfDownloading, ".3f") + " seconds.\n")

        pass

    # download remote file with new ftp client (new_ftp)
    def download_file_in_dedicated_FTP_client(self, filename, full_destination_path, blocksize=8192, delay_in_seconds=0):
        try:
            self.ftp.voidcmd("NOOP")
        except ftplib.error_reply:
            # the connection is unavailable
            print("Error occured when trying to download a file \'" + filename + "\'. The connection is empty.\n")
            raise
        # initialize a new FTP-client
        new_ftp = ftplib.FTP()
        new_ftp.connect(self.ftp.host, self.ftp.port)
        new_ftp.port = self.ftp.port
        new_ftp.login(self.login, self.password)
        new_ftp.cwd('.')


        # form path to src remote file
        # srcfile = os.path.join(self.ftp.pwd(), filename) # в Windows
        # добавляет обратную косую черту и потом не понимает путь
        # new_ftp is connecting with self.ftp by path
        srcfile = self.ftp.pwd() + "/" + filename
        if self.ftp.pwd() == '/':
            srcfile = filename

        # set the format of communication with ftp-server
        new_ftp.__class__.encoding = "utf-8"
        new_ftp.voidcmd("TYPE I")

        # get the size of remote destination file
        remote_file_size = 0
        try:
            remote_file_size = new_ftp.size(srcfile)
        except:
            if new_ftp.lastresp == '550':
                print("Error. File \'" + srcfile + "\' is unavailable or doesn't exist on FTP-server!\n")
                new_ftp.quit()
                return 550

        # open file for appending
        dst_file = open(full_destination_path, 'ab') # a - append, b - binary
        
        local_file_size = os.path.getsize(full_destination_path)
        #local_file_size = 0

        # check, if files have the same size, then it do not need to be
        # downloaded
        if remote_file_size == local_file_size:
            print("File \'" + srcfile + "\' has been already downloaded!\n")
            dst_file.close()
            return

        def callback(data):
            dst_file.write(data)
            print("Receive a block of data (" + str(len(data)) + "). Now i wanna sleep " + str(delay_in_seconds) + " seconds.\n")
            if delay_in_seconds != 0:
                time.sleep(delay_in_seconds)
            # можно добавить time.sleep(1) и так контролить время загрузки
            #print("Получен кусок из файла " + srcfile + " размером " +
            #str(len(data)) + " байт.")
            pass

        print("Start downloading file \'" + srcfile + "\' starts downloading. File size = " + format(remote_file_size / 1024 / 1024, ".3f") + " MB. \n")
        print("Downloading starts from " + str(local_file_size) + " byte.\n")
        timeOfDownloading = time.time()
        new_ftp.retrbinary(cmd='RETR ' + srcfile, rest=local_file_size, callback = callback, blocksize = blocksize)
        timeOfDownloading = time.time() - timeOfDownloading
        dst_file.close()
        print("Finish downloading file \'" + srcfile + "'\.Time of downloading = " + format(timeOfDownloading, ".3f") + " seconds.\n")

        new_ftp.quit()
        pass

    def download_file_in_dedicated_FTP_client_in_new_thread(self, index_of_downloading):
        filename = self.downloadings[index_of_downloading]['filename']
        full_destination_path = self.downloadings[index_of_downloading]['full_destination_path']
        try:
            self.ftp.voidcmd("NOOP")
        except ftplib.error_reply:
            # the connection is unavailable
            print("Error occured when trying to download a file \'" + filename + "\'. The connection is empty.\n")
            raise
        # initialize a new FTP-client
        new_ftp = ftplib.FTP()
        new_ftp.connect(self.ftp.host, self.ftp.port)
        new_ftp.port = self.ftp.port
        new_ftp.login(self.login, self.password)
        new_ftp.cwd('.')


        # form path to src remote file
        # srcfile = os.path.join(self.ftp.pwd(), filename) # в Windows
        # добавляет обратную косую черту и потом не понимает путь
        # new_ftp is connecting with self.ftp by path
        srcfile = self.ftp.pwd() + "/" + filename
        if self.ftp.pwd() == '/':
            srcfile = filename

        # set the format of communication with ftp-server
        new_ftp.__class__.encoding = "utf-8"
        new_ftp.voidcmd("TYPE I")

        # get the size of remote destination file
        remote_file_size = 0
        try:
            remote_file_size = new_ftp.size(srcfile)
            # print("Remote file size is " + str(remote_file_size))
        except ftplib.error_perm:
            if new_ftp.lastresp == '550':
                print("Error. File \'" + srcfile + "\' is unavailable or doesn't exist on FTP-server!\n")
                new_ftp.quit()
                return 550

        # open file for appending
        dst_file = open(full_destination_path, 'ab') # a - append, b - binary
        
        local_file_size = os.path.getsize(full_destination_path)
        #local_file_size = 0

        # check, if files have the same size, then it do not need to be
        # downloaded
        if remote_file_size == local_file_size:
            print("File \'" + filename + "\' has been already downloaded!\n")
            dst_file.close()
            return

        def callback(data):
            dst_file.write(data)
            print("Receive a block of data (" + str(len(data)) + "). Now i wanna sleep " + str(self.downloadings[index_of_downloading]['delay_in_seconds']) + " seconds.")
            if self.downloadings[index_of_downloading]['delay_in_seconds'] != 0:
                time.sleep(self.downloadings[index_of_downloading]['delay_in_seconds'])
            # можно добавить time.sleep(1) и так контролить время загрузки
            #print("Получен кусок из файла " + srcfile + " размером " +
            #str(len(data)) + " байт.")
            pass

        print("Start downloading file \'" + srcfile + "\' starts downloading. File size = " + format(remote_file_size / 1024 / 1024, ".3f") + " MB. \n")
        print("Downloading starts from " + str(local_file_size) + " byte.\n")
        timeOfDownloading = time.time()
        # new_ftp.retrbinary(cmd='RETR ' + srcfile, rest=local_file_size,
        # callback = callback, blocksize =
        # self.downloadings[index_of_downloading]['blocksize'])
        new_ftp.voidcmd('TYPE I')
        cmd = 'RETR ' + srcfile
        with new_ftp.transfercmd(cmd, local_file_size) as conn:
            while 1:
                data = conn.recv(self.downloadings[index_of_downloading]['blocksize'])
                if not data:
                    break
                callback(data)
            # shutdown ssl layer
            #if _SSLSocket is not None and isinstance(conn, _SSLSocket):
            #    conn.unwrap()
        try:
            new_ftp.voidcmd('NOOP')
        except ftplib.error_reply:
            print("Error occured after downloading file \'" + srcfile + "\'! Error in voidcmd()! Exiting from downloading.\n")
            new_ftp.quit()
            dst_file.close()
            return


        timeOfDownloading = time.time() - timeOfDownloading
        dst_file.close()
        print("Finish downloading file \'" + filename + "'\.Time of downloading = " + format(timeOfDownloading, ".3f") + " seconds.\n")

        new_ftp.quit()
        pass

    def download_file_in_dedicated_thread(self, filename, full_destination_path, blocksize=8192, delay_in_seconds=0):
        # new_downloading = threading.Thread(target =
        # self.download_file_in_dedicated_FTP_client, args = (filename,
        # destination_path, blocksize, delay_in_seconds))
        new_downloading = threading.Thread()
        
        parameters_for_new_downloading = {'filename' : filename, 
                                          'full_destination_path' : full_destination_path, 
                                          'message_from_main_thread' : '', 
                                          'blocksize' : blocksize, 
                                          'delay_in_seconds' : delay_in_seconds, 
                                          'thread' : new_downloading}
        self.downloadings.append(parameters_for_new_downloading)
        new_downloading._target = self.download_file_in_dedicated_FTP_client_in_new_thread
        new_downloading._args = (self.downloadings.index(parameters_for_new_downloading),)
        new_downloading.start()
        pass

    # upload file with the main class ftp client (self.ftp) in current remote
    # work directory self.ftp.pwd()
    def upload_file(self, full_path_to_local_file, blocksize=8192, delay_in_seconds=0):
        try:
            self.ftp.voidcmd("NOOP")
        except ftplib.error_reply:
            # the connection is unavailable
            print("Error occured when trying to upload a file \'" + full_path_to_local_file + "\'. The connection is empty.\n")
            raise

        local_filename = os.path.split(full_path_to_local_file)[1]

        # form path to new destination remote file
        destination_remote_path = self.ftp.pwd() + "/" + local_filename
        if self.ftp.pwd() == '/':
            destination_remote_path = local_filename

        # set the format of communication with ftp-server
        self.ftp.__class__.encoding = "utf-8"
        self.ftp.voidcmd("TYPE I")


        # open file for reading in binary format
        src_local_file = None
        try:
            src_local_file = open(full_path_to_local_file, 'rb') # r - read, b - binary
        except FileNotFoundError:
            print("Error! Local file \'" + full_path_to_local_file + "\' does not exitst! It is unavailable to upload on FTP-server!\n")
            raise
        
        # get the size of remote destination file
        remote_file_size = 0
        try:
            remote_file_size = self.ftp.size(destination_remote_path)
        except:
            if self.ftp.lastresp == '550':
                # print("File \'" + destination_remote_path + "\' is a new on
                # FTP-server, so it's start uploading size from 0 byte.\n")
                remote_file_size = 0
        
        local_file_size = os.path.getsize(full_path_to_local_file)
        #local_file_size = 0

        # check, if files have the same size, then it do not need to be
        # uploaded
        if remote_file_size == local_file_size:
            print("File \'" + local_filename + "\' has been already uploaded!\n")
            src_local_file.close()
            return

        def callback(data):
            if delay_in_seconds != 0:
                time.sleep(delay_in_seconds)
            # можно добавить time.sleep(1) и так контролить время загрузки
            # print("Отправлен кусок из файла " + full_path_to_local_file + "
            # размером " +
            # str(len(data)) + " байт.")
            pass

        print("Start uploading file \'" + full_path_to_local_file + "\'.. File size = " + format(local_file_size / 1024 / 1024, ".3f") + " MB.")
        if remote_file_size != 0:
            print("Uploading starts from " + str(remote_file_size) + " byte, because the part of file has been uploaded yet.\n")
        timeOfUploading = time.time()
        try:
            self.ftp.storbinary(cmd='STOR ' + destination_remote_path, fp=src_local_file, blocksize = blocksize, rest=remote_file_size, callback=callback)
        except ftplib.error_perm as err:
            print("Error occured when trying to upload file \'" + full_path_to_local_file + "\'! " + err.args[0] + "\n")
            raise
        timeOfUploading = time.time() - timeOfUploading
        src_local_file.close()
        print("Finish downloading file \'" + full_path_to_local_file + "'\.Time of uploading = " + format(timeOfUploading, ".3f") + " seconds.\n")

        pass

    # upload remote file with new ftp client (new_ftp)
    def upload_file_in_dedicated_FTP_client(self, full_path_to_local_file, blocksize=8192, delay_in_seconds=0):
        try:
            self.ftp.voidcmd("NOOP")
        except ftplib.error_reply:
            # the connection is unavailable
            print("Error occured when trying to upload a file \'" + full_path_to_local_file + "\'. The connection is empty.\n")
            raise
        # initialize a new FTP-client
        new_ftp = ftplib.FTP()
        new_ftp.connect(self.ftp.host, self.ftp.port)
        new_ftp.port = self.ftp.port
        new_ftp.login(self.login, self.password)
        new_ftp.cwd('.')

        local_filename = os.path.split(full_path_to_local_file)[1]

        # form path to new destination remote file
        destination_remote_path = self.ftp.pwd() + "/" + local_filename
        if self.ftp.pwd() == '/':
            destination_remote_path = local_filename

        # set the format of communication with ftp-server
        new_ftp.__class__.encoding = "utf-8"
        new_ftp.voidcmd("TYPE I")

        # open file for reading in binary format
        src_local_file = None
        try:
            src_local_file = open(full_path_to_local_file, 'rb') # r - read, b - binary
        except FileNotFoundError:
            print("Error! Local file \'" + full_path_to_local_file + "\' does not exitst! It is unavailable to upload on FTP-server!\n")
            new_ftp.close()
            raise
        
        # get the size of remote destination file
        remote_file_size = 0
        try:
            remote_file_size = new_ftp.size(destination_remote_path)
        except:
            if new_ftp.lastresp == '550':
                # print("File \'" + destination_remote_path + "\' is a new on
                # FTP-server, so it's start uploading size from 0 byte.\n")
                remote_file_size = 0

        local_file_size = os.path.getsize(full_path_to_local_file)
        #local_file_size = 0

        # check, if files have the same size, then it do not need to be
        # uploaded
        if remote_file_size == local_file_size:
            print("File \'" + local_filename + "\' has been already uploaded!\n")
            src_local_file.close()
            return

        def callback(data):
            if delay_in_seconds != 0:
                time.sleep(delay_in_seconds)
            # можно добавить time.sleep(1) и так контролить время загрузки
            # print("Отправлен кусок из файла " + full_path_to_local_file + "
            # размером " +
            # str(len(data)) + " байт.")
            pass

        print("Start uploading file \'" + full_path_to_local_file + "\'.. File size = " + format(local_file_size / 1024 / 1024, ".3f") + " MB.")
        if remote_file_size != 0:
            print("Uploading starts from " + str(remote_file_size) + " byte, because the part of file has been uploaded yet.\n")
        timeOfUploading = time.time()
        try:
            new_ftp.storbinary(cmd='STOR ' + destination_remote_path, fp=src_local_file, blocksize = blocksize, rest=remote_file_size, callback=callback)
        except ftplib.error_perm as err:
            print("Error occured when trying to upload file \'" + full_path_to_local_file + "\'! " + err.args[0] + "\n")
            raise
        timeOfUploading = time.time() - timeOfUploading
        src_local_file.close()
        print("Finish uploading file \'" + full_path_to_local_file + "'\. Time of uploading = " + format(timeOfUploading, ".3f") + " seconds.\n")
        new_ftp.quit()
        pass

    def upload_file_in_dedicated_FTP_client_in_new_thread(self, index_of_uploading):
        full_path_to_local_file = self.uploadings[index_of_uploading]['full_path_to_local_file']
        full_destination_remote_path = self.uploadings[index_of_uploading]['full_destination_remote_path']
        local_filename = os.path.split(full_path_to_local_file)[1]
        
        # check the connection
        try:
            self.ftp.voidcmd("NOOP")
        except ftplib.error_reply:
            # the connection is unavailable
            print("Error occured when trying to upload a file \'" + full_path_to_local_file + "\'. The connection is empty.\n")
            raise
        # initialize a new FTP-client
        new_ftp = ftplib.FTP()
        new_ftp.connect(self.ftp.host, self.ftp.port)
        new_ftp.port = self.ftp.port
        new_ftp.login(self.login, self.password)
        new_ftp.cwd('.')

        # set the format of communication with ftp-server
        new_ftp.__class__.encoding = "utf-8"
        new_ftp.voidcmd("TYPE I")
        
        # open file for reading in binary format
        src_local_file = None
        try:
            src_local_file = open(full_path_to_local_file, 'rb') # r - read, b - binary
        except FileNotFoundError:
            print("Error! Local file \'" + full_path_to_local_file + "\' does not exitst! It is unavailable to upload on FTP-server!\n")
            new_ftp.close()
            raise
        
        # get the size of remote destination file
        remote_file_size = 0
        try:
            remote_file_size = new_ftp.size(full_destination_remote_path)
        except:
            if new_ftp.lastresp == '550':
                # print("File \'" + destination_remote_path + "\' is a new on
                # FTP-server, so it's start uploading size from 0 byte.\n")
                remote_file_size = 0


        local_file_size = os.path.getsize(full_path_to_local_file)
        #local_file_size = 0

        # check, if files have the same size, then it do not need to be
        # uploaded
        if remote_file_size == local_file_size:
            print("File \'" + local_filename + "\' has been already uploaded!\n")
            src_local_file.close()
            new_ftp.quit()
            return

        def callback(data):
            print("Sent a block of data (" + str(len(data)) + "). Now i wanna sleep " + str(self.uploadings[index_of_uploading]['delay_in_seconds']) + " seconds.")
            if self.uploadings[index_of_uploading]['delay_in_seconds'] != 0:
                time.sleep(self.uploadings[index_of_uploading]['delay_in_seconds'])
            pass


        print("Start uploading file \'" + full_path_to_local_file + "\'.. File size = " + format(local_file_size / 1024 / 1024, ".3f") + " MB.")
        if remote_file_size != 0:
            print("Uploading starts from " + str(remote_file_size) + " byte, because the part of file has been uploaded yet.\n")
        timeOfUploading = time.time()
        try:
            with new_ftp.transfercmd('STOR ' + full_destination_remote_path , remote_file_size) as conn:
                while 1:
                    buf = src_local_file.read(self.uploadings[index_of_uploading]['blocksize'])
                    if not buf:
                        break
                    conn.sendall(buf)
                    callback(buf)
                # shutdown ssl layer
                # if _SSLSocket is not None and isinstance(conn, _SSLSocket):
                #    conn.unwrap()
        except ftplib.error_perm as err:
            print("Error occured when trying to upload file \'" + full_path_to_local_file + "\'! " + err.args[0] + "\n")
            raise
        timeOfUploading = time.time() - timeOfUploading
        src_local_file.close()
        print("Finish downloading file \'" + full_path_to_local_file + "'\.Time of uploading = " + format(timeOfUploading, ".3f") + " seconds.\n")
        new_ftp.quit()

        pass

    def upload_file_in_dedicated_thread(self, full_path_to_local_file, blocksize=8192, delay_in_seconds=0):
        # new_downloading = threading.Thread(target =
        # self.download_file_in_dedicated_FTP_client, args = (filename,
        # destination_path, blocksize, delay_in_seconds))
        new_uploading = threading.Thread()

        local_filename = os.path.split(full_path_to_local_file)[1]

        # form path to new destination remote file
        full_destination_remote_path = self.ftp.pwd() + "/" + local_filename
        if self.ftp.pwd() == '/':
            full_destination_remote_path = local_filename
        
        parameters_for_new_uploading = {'full_path_to_local_file' : full_path_to_local_file, 
                                          'full_destination_remote_path' : full_destination_remote_path, 
                                          'message_from_main_thread' : '', 
                                          'blocksize' : blocksize, 
                                          'delay_in_seconds' : delay_in_seconds, 
                                          'thread' : new_uploading}
        self.uploadings.append(parameters_for_new_uploading)
        new_uploading._target = self.upload_file_in_dedicated_FTP_client_in_new_thread
        new_uploading._args = (self.uploadings.index(parameters_for_new_uploading),)
        new_uploading.start()
        pass


def main():
	logging.basicConfig(filename = os.path.curdir + "/ftp_client.log", level = logging.DEBUG, format = '%(asctime)s %(levelname)s: %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')
	logging.info("===START===")
	client = MyFTPClient('ftp://127.0.0.1', login = "user1", password = "qwerty", port = 3100, path_of_directory_for_history = os.path.curdir, callbacks = None)
	client.start_control()
	client.cd_to_remote_directory("download_files")
	client.download("file_for_downloading_from_server_1","", 20)
	client.cd_to_remote_parent_directory()
	client.cd_to_remote_directory("uploaded_files")
	client.upload("file1_up", 20)
	client.upload("file2_up", 120)
	
	client.controlThread.join()
	logging.info("===STOP===\n\n\n")
	pass

if __name__ == "__main__":
	main()
    