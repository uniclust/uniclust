#!/usr/bin/python
# -*- coding: utf-8 -*

# ? ??????? filecache ???? Operation id, ??????
# ? task_files ???????? multi_id, id
# ? task_files ????? ?? ???????? ?????????? ? ????? ??????? ??????

#paramiko переделать os.string()
import global_vars
import exceptions
import MySQLdb

def force_delete(curs, file_id, multi_id):
    query = "SELECT `user_on_it`,`host`,`path` from `multiprocessors` where `multiprocessor_id`='%d'"%(multi_id);
    curs.execute(query);

    result = curs.fetchall();
    user_on_mult = result2[0][0];
    host = result2[0][1];
    path = result2[0][2];

    if DEBUG:
        print '[ForceDelete] FID %d | UID %d | MID %d | FSIZE %d '%(file_id, user_id, multi_id, file_size);
        print query2;
        print "[Res] UID %d | HOST %s | Path %s"%(user_on_mult, host, path);

    string = "rm -f %s@%s:%s/files/%d" %\
            (
                user_on_mult,
			    host,
			    path,
                file_id
            )
    status = 0;
    #status = os.string(string);
    if DEBUG:
        print string;

    if status:
        raise "ForceRm failed(MultiID:%d)"%multi_id;

    # еще нужно удалить из filecache
    query = "DELETE FROM `filecache` WHERE `file_id`='%d' and `multiprocessor_id`='%d'"%(file_id, multi_id);
    curs.execute(query);

def get_file_size(curs, file_id):
    DEBUG = global_vars.DEBUG;

    query = "SELECT size FROM files where `file_id`='%d'"%file_id;
    curs.execute(query);

    result = curs.fetchall();
    size = result[0][0];

    if DEBUG:
        print '[GetFileSize] FID %d | Size %s'%(file_id, size);

    return size;

def delete_files(curs, multi_id, quota, file_size, sum):
    DEBUG = global_vars.DEBUG;
    query = "SELECT `file_id` FROM `filecache` WHERE `multiprocessor_id`='%d' ORDER BY (`read_counter` and `write_counter`) ASC"%multi_id;
    curs.execute(query);

    result = curs.fetchall();
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
        for j in range(i):
            file_id = result[i][0];

            if DEBUG:
                print '[Quota] Delete file %d'%file_id;

            force_delete(curs, file_id, multi_id);
    else:
        raise Exception("Error on delete files on filecache");



def get_files_sum(curs, multi_id):
    DEBUG = global_vars.DEBUG;
    query = "SELECT file_id FROM `filecache` WHERE `status` = 'OK' and `multiprocessor_id`='%d'"%multi_id;

    curs.execute(query);

   

    result = curs.fetchall();
    rlen = len(result);
    
    if DEBUG:
        print '[GET|Files|Sum] Query %s | Res Len %d'%(query, rlen);

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

    curs.execute(query);
    result = curs.fetchall();

    if DEBUG:
        print '[GET|Files|Sum] End';

    return result[0][0];


def pre_add_file_to_cache( curs, file_id, multi_id ):
    query = "INSERT INTO `filecache` (`file_id`, `multiprocessor_id`, `status`, `read_counter`, `write_counter`, `last_read`, `last_write`) \
    VALUES ('%d', '%d', 'transfer', '0', '0', '', '')"%(file_id, multi_id);
    curs.execute(query);

def post_add_file_to_cache( curs, file_id, multi_id ):
    query = "UPDATE `filecache` SET `status` = 'OK' WHERE `file_id`='%d' AND `multiprocessor_id`='%d'"%(file_id, multi_id);
    curs.execute(query);

def get_multi_id_btid( task_id ):
    DEBUG = global_vars.DEBUG;
    query = "SELECT `multiprocessor_id` from `tasks` where `task_id` = '%d'"%task_id;
    curs.execute(query);

    result = curs.fetchall();
    multi_id = result[0][0];

    if DEBUG:
        print '[GetMultiID] Query [%s] | MultiID %d'%(query, multi_id);

    return multi_id;

def check_file_used(curs):
    DEBUG = global_vars.DEBUG;
    query = "SELECT `task_id`, `file_id`, `access_mode` FROM `task_files` where `status` = '0'";
    curs.execute(query);

    result = curs.fetchall();
    rlen = len(result);

    if DEBUG:
        print '[CheckFileUsed] Query [%s] | Result len %d'%(query, rlen);


    for i in range(rlen):
        task_id = result[i][0];
        file_id = result[i][1];
        access_mode = result[i][2];

        #узнать Multi_id
        multi_id = get_multi_id_btid(task_id);

        if access_mode == 'r':
            query = "update `filecache` SET `read_counter` = `read_counter`+1 where `file_id'='%d' and multiprocessor_id='%s'"%(file_id, multi_id);
        elif access_mode == 'w':
            query = "update `filecache` SET `write_counter` = `write_counter`+1 where `file_id'='%d' and multiprocessor_id='%s'"%(file_id, multi_id);
        else:
            query = "update `filecache` SET `read_counter` = `read_counter`+1,`write_counter` = `write_counter`+1  where `file_id'='%d' and multiprocessor_id='%s'"%(file_id, multi_id);

        curs.execute(query);


        if DEBUG:
            print query;

        query = "UPDATE `task_files` SET `status` = '1' WHERE `task_id`='%d' and file_id='%d'"%(task_id, file_id);
        curs.execute(query);

        if DEBUG:
            print query;