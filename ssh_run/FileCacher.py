#!/usr/bin/python
# -*- coding: utf-8 -*-

#import task
#import Backfill
#import fcntl

import sys
import os
import datetime
import time

from pprint import pprint

from uniclust import filecache_globalvars as global_vars2
from uniclust import filecache_filecache as filecache
from uniclust import filecache_operations as operations
from uniclust import ssh2

from uniclust import abstract_db as database

from uniclust import migration as sort_operations

DEBUG = True;
error_prefix = "[Error] ";

def start_work( db ):

    if DEBUG:
        print("[START] Start work at %s",datetime.datetime.now());

    if db is False:
        print("Error while conn with DB");
        return
#####
    filecache.check_file_used(db);
    result = db.get_all_new_operations(False);

    if result is False:
        return;

    #
    result = sort_operations.Mygration( db, result);
    result = sort_operations.Mygration.get_lst(result);

    for item in result:
        print("Task");
        print("""
            OperationID '%d'
            FileID '%d'
            OperType '%s'
            MultiID '%d'
        """%(item.oper_id, item.file_id, item.oper_type, item.multiprocessor_id));

        file = db.get_info_file(item.file_id);

        if file.status != 'ready':
            if DEBUG:
                print("Error Operation, error file status");

            continue;

        db.lock_operation(item);

        try:
            db.add_to_filecache(file_id=item.file_id, multiprocessor_id=item.multiprocessor_id, status='transfer') if item.oper_type == 'copyto' else """None"""

            operations.transfer_file(db, item, file) \
                if item.oper_type == 'copyto' else operations.download_file(db, item, file)\
                if item.oper_type == 'copyfrom' else operations.delete_file(db, item, file);

            db.filecache_update(item.file_id,item.multiprocessor_id, status='OK') if item.oper_type == 'copyto' else """None""" #post_add

        except Exception as err:
            db.lock_operation(item, err);

        db.lock_operation(item, error='');   

    if DEBUG:
        print("[END] Start work...");

if __name__ == '__main__':
    db=database.Db_connection(
            host = 's08.host-food.ru',
            user = 'h91184_revka',
            passwd = None,
            db  = 'h91184_cs-suite',
            key = 'C:\\Users\\Elik\\Documents\\uniclust_passwd.txt')

    start_work(db);