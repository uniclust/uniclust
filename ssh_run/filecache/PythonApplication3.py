#!/usr/bin/python
# -*- coding: utf-8 -*-

#import task
#import Backfill
#import fcntl

import MySQLdb
import global_vars2
import sys
import os
import datetime
import time

DEBUG = True;

import operation
import filecache
import ssh2
import db2

error_prefix = "[Error] ";

def start_work():
    if DEBUG:
        print "[START] Start work at %s"%datetime.datetime.now();

    db_error_flag=False
    try:
        db=db2.db_connect\
            (
            host=global_vars2.db_host,
            user=global_vars2.db_user,
            passwd=global_vars2.db_passwd,
			db=global_vars2.db_name
            )
        db2.db_escape_string(db);
    except:
        db_error_flag = True;

    if db_error_flag == False:
        if DEBUG:
            print "Success connect to db"

    curs=db2.db_get_cursor(db);
    filecache.check_file_used(curs);

    query=\
    """
        select 
            operations.operation_id,
            operations.file_id,
            operations.oper_type,
            operations.multiprocessor_id
        from
            operations
        where
            operations.status="new"

        order by operation_id 
    """

    if DEBUG:
        print "Run Query: %s"% query;

    db2.db_execute_query(curs, query);

    result = db2.db_fetchall(curs);
    num_tasks = len(result);
    
    if DEBUG:
        print "Num results: %d task(s)"%num_tasks
    
    if num_tasks == 0:
        return;

    ssh = ssh2.ssh_client();

    for i in range(0, num_tasks):
        oper_id = result[i][0];
        oper_fileid = result[i][1];
        oper_type = result[i][2];
        oper_multi_id = result[i][3]
        
        error=0;
        error_string = "";

        if DEBUG:
            print "Task:: '%i'"%i
            print """
            OperationID '%d'
            FileID '%d'
            OperType '%s'
            MultiID '%d'
            """%(oper_id, oper_fileid, oper_type, oper_multi_id);

        query = "SELECT `status`, `user_id`, `size` FROM `files` WHERE `file_id`='%d' LIMIT 1"%(oper_fileid);
        db2.db_execute_query(curs, query);

        if DEBUG:
            print "Query::'%s'"%query;

        result2 = db2.db_fetchall(curs);

        file_status = result2[0][0];
        file_userid = result2[0][1];
        file_size = result2[0][2];

        if DEBUG:
            print "Result File: Status %s | UID %s | SIZE %s"%(file_status, file_userid, file_size);

     
        #  Если файл в задании
        if file_status != "ready":
            error = 1;
            error_string = "%sError file status"%error_prefix;

            if DEBUG:
                print "Error Operation, error file status"

            continue;

        if oper_type == 'copyto':
            if DEBUG:
                print "Operation::Copyto"
            operation.lock(curs,oper_id, oper_fileid);

            filecache.pre_add_file_to_cache(curs, oper_fileid, oper_multi_id)

            try:
                operation.transfer_file(curs, ssh, oper_fileid, file_userid, oper_multi_id, file_size);
            except Exception as str:
                print '[ErrorTransfer]:%s'%str;
                error_string = str;
                error = 1;

            if error == 0:
                filecache.post_add_file_to_cache(curs, oper_fileid, oper_multi_id);

        if oper_type == 'copyfrom':
            operation.lock(curs,oper_id, oper_fileid);

            try:
                operation.download_file(curs, ssh, oper_fileid, file_userid, oper_multi_id, file_size);
            except Exception as str:
                print 'Error:%s'%str;
                error_string = str;
                error = 1;

        if oper_type == 'remove':
            operation.lock(curs,oper_id, oper_fileid);

            try:
                operation.delete_file(curs, ssh, oper_fileid, file_userid, oper_multi_id, file_size);
            except Exception as str:
                print 'Error:%s'%str;
                error_string = str;
                error = 1;

        if oper_type == 'removeall':
            operation.lock(curs,oper_id, oper_fileid);

            try:
                operation.delete_file_everywhere(curs, ssh, oper_fileid, file_userid, oper_multi_id, file_size);
            except Exception as str:
                print 'Error:%s'%str;
                error_string = str;
                error = 1;

        operation.unlock(error, error_string, curs, oper_id, oper_fileid);   

    ssh2.ssh_close(ssh);
    if DEBUG:
        print "[END] Start work...";
   
start_work();    
#while 1:
#    start_work();
#    time.sleep(60); 