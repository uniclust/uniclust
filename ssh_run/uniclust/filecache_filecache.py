#!/usr/bin/python
# -*- coding: utf-8 -*

# ? ??????? filecache ???? Operation id, ??????
# ? task_files ???????? multi_id, id
# ? task_files ????? ?? ???????? ?????????? ? ????? ??????? ??????

#paramiko переделать os.string()

from uniclust import filecache_globalvars as global_vars2
from uniclust import ssh2

import datetime

def force_delete_files(db, ssh, list_files, multi ):
    if len(list_files) == 0:
        return ;

    if global_vars2.DEBUG:
        print("[Start Force Delete]");

    string = '';
    for item in list_files:
        string += "rm -f {}@{}:{}/files/{};".format(
                    multi.user_on_it,
				    multi.host,
				    multi.path,
                    item
                )
    
    if global_vars2.DEBUG:
        print ("Task upload data: '%s'"%string);

    status = ssh.exec(string);

    if status:
        raise Exception("Error with scp Force delete");

    db.delete_from_filecache(list_files, multi.multiprocessor_id);

    if global_vars2.DEBUG:
        print("[End Force Delete]");

def check_file_used(db):
    result = db.get_info_tasksfiles_by_params(status=0);

    if global_vars2.DEBUG:
        print("[Start File Check]")

    if result is False:
        return;

    mytime = datetime.datetime.now();

    for item in result:
        multiproc = db.get_info_tasks_by_taskid(item.task_id);

        db.filecache_update(item.file_id, multiproc.multiprocessor_id, read_counter='+', last_read=mytime) if item.access_mode == 'r'\
            else db.filecache_update(item.file_id, multiproc.multiprocessor_id, write_counter='+', last_write=mytime) if item.access_mode == 'w' \
            else db.filecache_update(item.file_id, multiproc.multiprocessor_id, read_counter='+', write_counter='+', last_write=mytime, last_read=mytime)

        db.update_taskfiles_by_tid_and_fid(item.task_id, item.file_id, status='1');

    if global_vars2.DEBUG:
        print("[End File Check]")