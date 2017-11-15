#!/usr/bin/python
# -*- coding: utf-8 -*

# ПЕРЕДЕЛАТЬ files_qouta
# удалять из fcache сразу после удаления файла
from uniclust import filecache_globalvars as global_vars2
from uniclust import filecache_filecache as filecache
from uniclust import ssh2
from uniclust import filecache_db2 as db2

RUNNING_STATUS = 2;

def delete_file_all(db, operation, file):
    result = db.get_filecache_by_id(file_id = file.file_id);

    if global_vars2.DEBUG:
        print('[Delete Everywhere]');

    for item in result:
        operation.multiprocessor_id = item.multiprocessor_id;
        delete_file(db, operation, file );

    db.set_file_status(file.file_id);

    if global_vars2.DEBUG:
        print('[Delete Everywhere End]');
  
def delete_file(db, operation, file ):
    
    #Надо удалять отовсюду
    if operation.multiprocessor_id == -1:
        delete_file_all(db, operation, file)
        return

    if global_vars2.DEBUG:
        print('[Delete File]');

    multi = db.get_info_multiproc(operation.multiprocessor_id);
    ssh = ssh2.ssh_connections(connect = True, host_name = multi.host, user_name = multi.user_on_it,key_path = global_vars2.key_path);

    string = "rm -f %s@%s:%s/files/%d" %\
            (
                multi.user_on_it,
			    multi.host,
			    multi.path,
			    file.file_id,
            )
    
    status = ssh.exec(string);

    if status:
        raise Exception("Error with scp string");

    if global_vars2.DEBUG:
        print ("Task delete data: '%s'"%string);

    if status:
        raise Exception("Rm failed(MultiID:%d)"%multi_id);

    db.delete_from_filecache([file.file_id], multi.multiprocessor_id);

    if global_vars2.DEBUG:
        print('[Delete File End]');

def download_file(db, operation, file):
    if global_vars2.DEBUG:
        print('[Download File]');

    multi = db.get_info_multiproc(operation.multiprocessor_id);
    ssh = ssh2.ssh_connections(connect = True, host_name = multi.host, user_name = multi.user_on_it,key_path = global_vars2.key_path);

    # тут что?
    string="scp -r %s@%s:%s/files/%d %s/%d/%d" %\
		(
			multi.user_on_it,
			multi.host,
			multi.path,
			file.file_id,
			global_vars2.data_path,
			file.user_id,
			file.file_id
		)
    if global_vars2.DEBUG:
        print ("Task upload data: '%s'"%string);

    status = ssh.exec(string);

    if status:
        raise Exception("Error with scp string");

    if global_vars2.DEBUG:
        print('[END DowloadFile]');

def transfer_file(db, operation, file ):
    
    if global_vars2.DEBUG:
        print('[TransferFile]');

    multi = db.get_info_multiproc(operation.multiprocessor_id);
    files = db.get_filecache_by_id(multi_id=multi.multiprocessor_id, status='OK');

    list_files = list();
    if files is not False:
        for obj in files:
            list_files.append(obj.file_id);

    curr_quota =  db.get_filecache_sum(list_files);

    ssh = ssh2.ssh_connections(connect = True, host_name = multi.host, user_name = multi.user_on_it,key_path = global_vars2.key_path);

    if global_vars2.DEBUG:
        print("[Quota] %d max, %d curr_quota, %d file_size"% (multi.files_quota,curr_quota,file.size))
    
    if multi.files_quota - (file.size + curr_quota) < 0:
        res = db.get_filecache_by_id(multi_id=operation.multiprocessor_id, status='OK', sorted = True);

        snum = 0;
        lst = list();
        for item in res:
            lst.append(item.file_id);
            snum+= db.get_filecache_sum([item.file_id]);

            if ( multi.files_quota + snum) - (file.size + curr_quota)  >= 0:
                filecache.force_delete_files(db, ssh, lst, multi);
                break;

    string="scp {}/{}/{} {}@{}:{}/files/{}".format\
			(
				global_vars2.data_path,
				file.user_id,
				file.file_id,
				multi.user_on_it,
				multi.host,
				multi.path,
				file.file_id
			)

    if global_vars2.DEBUG:
        print ("Task upload data: '%s'"%string);

    status = ssh.exec(string);

    if status:
        raise Exception("Error with scp string");

    if global_vars2.DEBUG:
        print('[END TransferFile]');