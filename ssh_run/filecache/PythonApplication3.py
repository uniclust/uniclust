#!/usr/bin/python
# -*- coding: utf-8 -*-

#import task
#import Backfill
#import fcntl

import MySQLdb
import global_vars
import sys
import os
import datetime
import time

DEBUG = True;

import operation
import filecache
import ssh2

def start_work():
    if DEBUG:
        print "Start work...";

    db_error_flag=False
    try:
        db=MySQLdb.connect\
            (
            host=global_vars.db_host,
            user=global_vars.db_user,
            passwd=global_vars.db_passwd,
			db=global_vars.db_name
            )
    except:
        db_error_flag = True;

    if db_error_flag:
        print "Can't connect to DB"
    else:
        if DEBUG:
            print "Success connect to db"

    curs=db.cursor();

   # filecache.check_file_used(curs);

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
    """

    if DEBUG:
        print "Run Query: %s"% query;

    curs.execute(query);

    result = curs.fetchall();
    num_tasks = len(result);
    
    if DEBUG:
        print "Num results: %d task(s)"%num_tasks
    
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
        curs.execute(query);

        if DEBUG:
            print "Query::'%s'"%query;

        result2 = curs.fetchall();

        file_status = result2[0][0];
        file_userid = result2[0][1];
        file_size = result2[0][2];

        if DEBUG:
            print "Result File: Status %s | UID %s | SIZE %s"%(file_status, file_userid, file_size);

        #  Если файл в задании
        if file_status != "ready":
            error = 1;
            if DEBUG:
                print "Error Operation, error file status"

        if oper_type == 'copyto' and error==0:
            if DEBUG:
                print "Operation::Copyto"
            operation.lock(curs,oper_id, oper_fileid);

            filecache.pre_add_file_to_cache(curs, oper_fileid, oper_multi_id)

            try:
                operation.transfer_file(curs, ssh, oper_fileid, file_userid, oper_multi_id, file_size);
            except Exception as str:
                print 'Error:%s'%str;
                error_string = str;
                error = 1;

            if error == 0:
                filecache.post_add_file_to_cache(curs, oper_fileid, oper_multi_id);

        if oper_type == 'copyfrom' and error==0:
            operation.lock(curs,oper_id, oper_fileid);

            try:
                operation.download_file(curs, ssh, oper_fileid, file_userid, oper_multi_id, file_size);
            except:
                error = 1;

        if oper_type == 'remove' and error==0:
            operation.lock(curs,oper_id, oper_fileid);

            try:
                operation.delete_file(curs, ssh, oper_fileid, file_userid, oper_multi_id, file_size);
            except:
                error = 1;

        operation.unlock(error, error_string, curs, oper_id, oper_fileid);   

    ssh2.ssh_close(ssh);
        
while 1:
    start_work();
    time.sleep(60); 