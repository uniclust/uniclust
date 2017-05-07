#!/usr/bin/python
# -*- coding: utf-8 -*

import global_vars2
import exceptions
import MySQLdb
import ssh2
import datetime

import db2

def force_delete(curs, ssh, file_id, multi_id):
    DEBUG = global_vars2.DEBUG;
    query = "SELECT `user_on_it`,`host`,`path` from `multiprocessors` where `multiprocessor_id`='%d'"%(multi_id);
    db2.db_execute_query(curs, query);

    result = db2.db_fetchall(curs);
    user_on_mult = result[0][0];
    host = result[0][1];
    path = result[0][2];

    if DEBUG:
        print '[ForceDelete] FID %d | MID %d'%(file_id, multi_id);
        print query;
        print "[Res] UID %s | HOST %s | Path %s"%(user_on_mult, host, path);

    str_delete = "%s/files/%d"%(path,
                file_id);
    # SSH
    if global_vars2.SSH == True:
        ssh2.ssh_connect(ssh,host, user_on_mult, global_vars2.key_path);
        sftp = ssh2.sftp_ini(ssh);
        ssh2.sftp_delete(sftp, str_delete);
        ssh2.sftp_close(sftp);
        ssh2.ssh_close(ssh);

    if DEBUG:
        print '[ForceDelete] "%s" END'%str_delete;

    # еще нужно удалить из filecache
    query = "DELETE FROM `filecache` WHERE `file_id`='%d' and `multiprocessor_id`='%d'"%(file_id, multi_id);
    db2.db_execute_query(curs, query);

def get_file_size(curs, file_id):
    DEBUG = global_vars2.DEBUG;

    query = "SELECT size FROM files where `file_id`='%d'"%file_id;
    db2.db_execute_query(curs, query);

    result = db2.db_fetchall(curs);
    size = result[0][0];

    if DEBUG:
        print '[GetFileSize] FID %d | Size %s'%(file_id, size);

    return size;

def delete_files(curs, ssh, multi_id, quota, file_size, sum):
    DEBUG = global_vars2.DEBUG;
    query = "SELECT `file_id` FROM `filecache` WHERE `multiprocessor_id`='%d' and `status`='OK' ORDER BY (`read_counter` and `write_counter`) ASC"%multi_id;
    db2.db_execute_query(curs, query);

    result = db2.db_fetchall(curs);
    rlen = len(result);

    snum = 0;
    take = False;

    i = 0;

    if DEBUG:
        print '[QuotaClear] query [%s] | Len %d | quota %d | Fsize %d | sum %d'%(query, rlen, quota, file_size, sum);
    for i in range(rlen):
        file_id = result[i][0];

        snum+=get_file_size(curs, file_id);

        if (quota+snum) - (file_size+sum) >= 0 :
            take = True;

            if DEBUG:
                print '[TAKEBreak] SNum %d | i %d'%(snum, i);
            break;
        

    if take == True:
        for j in range(i+1):
            file_id = result[i][0];

            if DEBUG:
                print '[Quota] Delete file %d'%file_id;

            force_delete(curs, ssh, file_id, multi_id);
    else:
        raise Exception("Error on delete files on filecache");



def get_files_sum(curs, multi_id):
    DEBUG = global_vars2.DEBUG;
    query = "SELECT file_id FROM `filecache` WHERE `status` = 'OK' and `multiprocessor_id`='%d'"%multi_id;

    db2.db_execute_query(curs, query);

    result = db2.db_fetchall(curs);
    rlen = len(result);
    
    if DEBUG:
        print '[GET|Files|Sum] Query %s | Res Len %d'%(query, rlen);

    if rlen == 0:
        return 0;

    query2 = "";
    for i in range(rlen):
        fid = result[i][0];

        if i == rlen - 1:
            query2+=" `file_id` = '%d' "%fid;
            
        else:
            query2+=" `file_id` = '%d' OR"%fid;

    query = "SELECT SUM(size) FROM `files` WHERE (%s)"%query2;

    if DEBUG:
        print query;

    db2.db_execute_query(curs, query);
    result = db2.db_fetchall(curs);

    if DEBUG:
        print '[GET|Files|Sum] End';

    return result[0][0];


def pre_add_file_to_cache( curs, file_id, multi_id ):
    query = "INSERT INTO `filecache` (`file_id`, `multiprocessor_id`, `status`, `read_counter`, `write_counter`) \
    VALUES ('%d', '%d', 'transfer', '0', '0')"%(file_id, multi_id);
    db2.db_execute_query(curs, query);

def post_add_file_to_cache( curs, file_id, multi_id ):
    query = "UPDATE `filecache` SET `status` = 'OK' WHERE `file_id`='%d' AND `multiprocessor_id`='%d'"%(file_id, multi_id);
    db2.db_execute_query(curs, query);

def get_multi_id_btid(curs, task_id ):
    DEBUG = global_vars2.DEBUG;
    query = "SELECT `multiprocessor_id` from `tasks` where `task_id` = '%d'"%task_id;
    db2.db_execute_query(curs, query);

    result = db2.db_fetchall(curs);
    multi_id = result[0][0];

    if DEBUG:
        print '[GetMultiID] Query [%s] | MultiID %d'%(query, multi_id);

    return multi_id;

def check_file_used(curs):
    DEBUG = global_vars2.DEBUG;
    query = "SELECT `task_id`, `file_id`, `access_mode` FROM `tasks_files` where `status` = '0'";
    db2.db_execute_query(curs, query);

    result = db2.db_fetchall(curs);
    rlen = len(result);

    if DEBUG:
        print '[Start] Check file used';
        print '[CheckFileUsed] Query [%s] | Result len %d'%(query, rlen);

    mytime = datetime.datetime.now();

    for i in range(rlen):
        task_id = result[i][0];
        file_id = result[i][1];
        access_mode = result[i][2];

        #узнать Multi_id
        multi_id = get_multi_id_btid(curs, task_id);

        if access_mode == 'r':
            query = "update `filecache` SET `read_counter` = `read_counter`+1,`last_read`='%s' where `file_id`='%d' and multiprocessor_id='%s'"%(mytime,file_id, multi_id);
        elif access_mode == 'w':
            query = "update `filecache` SET `write_counter` = `write_counter`+1,`last_write`='%s' where `file_id`='%d' and multiprocessor_id='%s'"%(mytime, file_id, multi_id);
        else:
            query = "update `filecache` SET `read_counter` = `read_counter`+1,`write_counter` = `write_counter`+1, `last_read`='%s', `last_write`='%s'  where `file_id`='%d' and multiprocessor_id='%s'"%(mytime,mytime,file_id, multi_id);

        db2.db_execute_query(curs, query);


        if DEBUG:
            print query;

        query = "UPDATE `tasks_files` SET `status` = '1' WHERE `task_id`='%d' and file_id='%d'"%(task_id, file_id);
        db2.db_execute_query(curs, query);

        if DEBUG:
            print query;
    if DEBUG:
        print '[End File Check]';