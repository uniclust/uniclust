#!/usr/bin/python
# -*- coding: utf-8 -*

import global_vars2
import exceptions
import MySQLdb

import filecache
import ssh2
import db2

RUNNING_STATUS = 2;

def delete_file_everywhere(curs, ssh, file_id, user_id, multi_id, file_size ):
    DEBUG = global_vars2.DEBUG;

    query2 = "SELECT `multiprocessor_id` from `filecache` WHERE `file_id` =%d"%file_id
    db2.db_execute_query(curs, query2);

    result = db2.db_fetchall(curs);
    num_tasks = len(result);

    if DEBUG:
        print '[DELETEF] FID %d | UID %d | MID %d | FSIZE %d '%(file_id, user_id, multi_id, file_size);
        print query2;
        print '[Res] Num %d'%num_tasks;

    for i in range(0, num_tasks):
        this = result[i][0];

        query = "SELECT `user_on_it`,`host`,`path` from `multiprocessors` where `multiprocessor_id`='%d'"%(this);
        db2.db_execute_query(curs, query);
        result2 = db2.db_fetchall(curs);

        if DEBUG:
            print query;

        user_on_mult = result2[0][0];
        host = result2[0][1];
        path = result2[0][2];

        if DEBUG:
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
            print '[DeleteFileEvery] "%s" END'%str_delete;

        query = "DELETE FROM `filecache` WHERE `file_id`='%d' and `multiprocessor_id`='%d'"%(file_id, this);
        db2.db_execute_query(curs, query);

    return 1;
# Если multi_id == -1 то удалять отовсюду
# Иначе удалять на указанном суперкомпе(если он там есть)
def delete_file(curs, ssh, file_id, user_id, multi_id, file_size ):
    DEBUG = global_vars2.DEBUG;

    if multi_id == -1:
        return delete_file_everywhere(curs, ssh,file_id, user_id, multi_id, file_size);

    query = "SELECT `user_on_it`,`host`,`path` from `multiprocessors` where `multiprocessor_id`='%d'"%(multi_id);
    db2.db_execute_query(curs, query);

    result = db2.db_fetchall(curs);
    user_on_mult = result[0][0];
    host = result[0][1];
    path = result[0][2];

    if DEBUG:
        print '[DELETEF] FID %d | UID %d | MID %d | FSIZE %d '%(file_id, user_id, multi_id, file_size);
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
        print '[DeleteFile] "%s" END'%str_delete;

    # еще нужно удалить из filecache
    query = "DELETE FROM `filecache` WHERE `file_id`='%d' and `multiprocessor_id`='%d'"%(file_id, multi_id);
    db2.db_execute_query(curs, query);

def download_file(curs, ssh, file_id, user_id, multi_id, file_size ):
    DEBUG = global_vars2.DEBUG;
    query = "SELECT `user_on_it`,`host`,`path`,`files_quota` from `multiprocessors` where `multiprocessor_id`='%d'"%(multi_id);
    db2.db_execute_query(curs, query);
    result = db2.db_fetchall(curs);

    user_on_mult = result[0][0];
    host = result[0][1];
    path = result[0][2];
    quota = result[0][3];

    file = "%s/%d/%d"%( global_vars2.data_path, user_id, file_id);
    remote_file = "%s/files/%d"%(path, file_id);

     # SSH
    if global_vars2.SSH == True:
        ssh2.ssh_connect(ssh,host, user_on_mult, global_vars2.key_path);
        sftp = ssh2.sftp_ini(ssh);
        ssh2.sftp_download(sftp, remote_file,file);
        ssh2.sftp_close(sftp);
        ssh2.ssh_close(ssh);

    if DEBUG:
        print '[DownloadFile] Remote %s | Local %s END'%(remote_file, file);

    ssh2.sftp_close(sftp);

def transfer_file(curs, ssh, file_id, user_id, multi_id, file_size ):
    DEBUG = global_vars2.DEBUG;
    query = "SELECT `user_on_it`,`host`,`path`,`files_quota` from `multiprocessors` where `multiprocessor_id`='%d' LIMIT 1"%(multi_id);
    db2.db_execute_query(curs, query);
    result = db2.db_fetchall(curs);

    curr_quota = int( filecache.get_files_sum(curs, multi_id) );

    user_on_mult = result[0][0];
    host = result[0][1];
    path = result[0][2];
    quota = result[0][3];

    if DEBUG:
        print '[TransferFile] FID %d | UID %d | MID %d | SIZE %d | CURR_QOUTA %d | QUOTA %d'%(file_id, user_id, multi_id, file_size, curr_quota,quota);
        print query;
    
    if file_size > quota:
        raise Exception("Error, too big file");
    
    if quota - (file_size+curr_quota) < 0:
        filecache.delete_files(curs, ssh, multi_id, quota, file_size,0);

    file = "%s/%d/%d"%( global_vars2.data_path, user_id, file_id);
    remote_file = "%s/files/%d"%(path, file_id);

     # SSH
    if global_vars2.SSH == True:
        ssh2.ssh_connect(ssh,host, user_on_mult, global_vars2.key_path);
        sftp = ssh2.sftp_ini(ssh);
        ssh2.sftp_transfer(sftp, file, remote_file);
        ssh2.sftp_close(sftp);
        ssh2.ssh_close(ssh);

    

    if DEBUG:
        print '[TransferFile] Local %s | Remote %s | End'%(file, remote_file);

    

def lock( curs, oper_id, file_id):
    DEBUG = global_vars2.DEBUG;

    query = " UPDATE `operations` SET `status`=%d WHERE `operation_id`='%d' "%(RUNNING_STATUS,oper_id);
    db2.db_execute_query(curs, query);

    if DEBUG:
        print "[Lock] OperId %d | FileID %d | Query:'%s'"%(oper_id,file_id,query);

    query=\
    """
        update
            files
         set
             status =2
         where
            file_id=%d
    """ %(file_id);

    db2.db_execute_query(curs, query);

    if DEBUG:
        print "[Lock] Query#2: '%s'"%query;

def unlock( type, err_str, curs, oper_id, file_id):
    
    DEBUG = global_vars2.DEBUG;

    if type == 0:
        query=\
    """
        update
            operations
        set
            operations.status = 3
            
        where
            operations.operation_id=%d
    """ %(oper_id);   
    else:
        err_str = str.replace( str(err_str), "'", "\\'");
        query=\
    """
        update
            operations
        set
            operations.status = 5,
            operations.error_message = '%s'
        where
            operations.operation_id=%d
    """ %(err_str,oper_id);

    if DEBUG:
        print "[UnLock] Type %d | OperId %d | FileID %d | Query:'%s'"%(type,oper_id,file_id,query);

    db2.db_execute_query(curs, query);

    query=\
    """
        update
            files
         set
             files.status = "ready"
        where
            files.file_id=%d
    """ %(file_id);
    db2.db_execute_query(curs, query);

    if DEBUG:
        print "[Unlock] Query#2: '%s'"%query;



