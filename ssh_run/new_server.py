import sys
import os
import datetime
import time

import FileCacher as fCache

from uniclust.abstract_db import *
from uniclust.server_common import parse_config_file as server_parse_config, parse_arguments as server_args_parse, become_daemon as server_become_daemon
   
from uniclust.task import *

debug = True;
# db_passwd_file, че это
# в db_classes нужно полностью описывать класс tasks
def main(argv=None):
    """
    Main function of  Server
    """
    if argv == None:
        argv=sys.argv
         
    args=server_args_parse(argv)
    config=server_parse_config(args.config_file_name)
    

    if args.become_daemon == 'no':
        server_become_daemon(config,False)
    else:
        server_become_daemon(config,True)
    
    try:
        #db=Db_connection(
         #   host = config['db_host'],
        #    user = config['db_user'],
        #    passwd = config['db_passwd_file'],
        #    db  = config['database_name'])
        db=Db_connection(
            host = 's08.host-food.ru',
            user = 'h91184_revka',
            passwd = None,
            db  = 'h91184_cs-suite',
            key = 'C:\\Users\\Elik\\Documents\\uniclust_passwd.txt',)
    except Exception as err:
           sys.stderr.write(err)

    while True:
        #time.sleep(60);
        fCache.start_work(db) 

        tasks = db.get_all_tasks();

        if tasks is False:
            continue;

        for tsk in tasks:

            if debug:
                print('Task: {} ID'.format(tsk.task_id))

            #
		    #
		    # running tasks
		    #
		    #
            if tsk.task_status == 'ready':

                try:
                    tsk.upload_data();
                except Exception as err:
                    print ("    Upload data for task #{} failed![Error:{}]".format(tsk.task_id, err));
                    db.set_task_status( tsk.task_id, 'stopped')
                    continue;

                try:
                    tsk.run();
                except Exception as err:
                    print ("    Run task #{} failed![Error:{}]".format(tsk.task_id, err));
                    db.set_task_status( tsk.task_id, 'stopped')

                db.set_task_status( tsk.task_id, 'submitted');

            

            #
		    #
		    # stopping tasks
		    #
		    #
            if tsk.task_status == 'stopped':
                try:
                    tsk.download_data();
                except Exception as err:
                    print ("    Download data failed[Error:{}]!".format(err))

                tsk.remote_task_delete();
                tsk.email_notify_on_finish();
                db.set_task_status(tsk.task_id, 'refused');


        time.sleep(60);
    return 0

 
if __name__ == "__main__":
        main()
