import pymysql as sql
from uniclust.db_classes import cl_file as class_files, cl_multi as class_multiproc, cl_operation as class_operations,\
                        cl_filecache as class_filecache

from uniclust.task import Task as class_tasks

import uniclust.ssh2
import uniclust.filecache_globalvars as global_vars2
import datetime

from uniclust.task import *

class Db_connection(object):
    def    __init__(self, host : str, user : str, passwd : str, db : str, key= None):
        """
        Creating database object and connecting it to
        really database
        """
        self.db = None
        self.error = False
        self.error_message = '';

        self.debug = True;

        if key is not None:
            passFile = open(key, 'r');
            passwd = passFile.read();
            passwd = passwd.strip();

            if len(passwd) < 3:
                raise Exception("Invalid passwd from file...");


        try:
            self.db = sql.connect(host, user, passwd, db);
        except sql.InternalError as str:
            raise Exception(str.args);
    
        self.curs = self.db.cursor();
    def execute_query( self, query ):
        return self.curs.execute( query );

    def fetchall(self):
        return self.curs.fetchall();

    def get_all_tasks(self):
        """
        Get all tasks from db table `tasks`, return [list] class task (see db_classes.py for details)
        """
        query= "SELECT * FROM `tasks` WHERE 1"

        if self.debug:
            print(query);

        result = self.execute_query(query);
        result = self.fetchall()

        lst = list();
        if len(result):
            for obj in result:
                lst.append(Task(obj, self))

            return lst;

        return False
    def set_task_status(self, task_id, status):
        """
        Set a 'status' to task by `task_id`
        """

        query = "update tasks set task_status='{}' where task_id={}".format(status, task_id);

        if self.debug:
            print(query);

        self.execute_query(query);

    def get_algoritm(self, app_id):
        """
        select algoritm from app
        """
        query= "SELECT * FROM `applications` WHERE `application_id`='%d'"%app_id;

        if self.debug:
            print(query);

        result = self.execute_query(query);
        result = self.fetchall()

        lst = list();
        if len(result):
            for obj in result:
                lst.append(class_tasks(obj))

            return lst;

        return False
    def get_all_new_operations(self, test = False):
        """
        Select all operations that has status 'new' and return class operations
        """
        query= "SELECT * FROM `operations` ORDER BY `operation_id` " if test is True else "SELECT * FROM `operations` where `status` = 'new' ORDER BY `operation_id`  ";
        if self.debug:
            print(query);

        result = self.execute_query(query);
        result = self.fetchall()

        lst = list();
        if len(result):
            for obj in result:
                lst.append(class_operations(obj))

            return lst;
        
        # No exception
        return False;

    def get_info_file(self, file_id):
        """
        Return `cl_file` python class
        """

        query = "SELECT * FROM `files` WHERE `file_id`='%d' LIMIT 1" % file_id;

        if self.debug:
            print(query);

        result = self.execute_query(query);
        result = self.fetchall()

        if len(result):
            return class_files(result[0]);

        raise Exception("[{}]Empty Result...".format(self.get_info_file.__name__));
    def set_file_status(self, file_id, status="error"):
        """
            Function take file_id, status and update table files
        """
        query = "UPDATE `files` SET `status`='%s' WHERE `file_id`='%d'"%(status, file_id);
        if self.debug:
            print(query);

        result =self.execute_query(query);

        return True;
    def lock_operation(self, cl_oper, error=None):
        """
        Lock/Unlock операцию. Принимает минимум 1 аргумент ввиде 
        cl_oper=class_operation 
        error=string
        Use query_lock_operation(cl_oper=this) чтобы lock операцию и файл который используется в ней
        Use query_lock_operation(cl_oper=this, error="") чтобы unlock операцию без ошибки;
        Use query_lock_operation(cl_oper=this, error="Error") чтобы разблокировать операцию с ошибкой;
        """

        RUNNING_STATUS = 2;

        arg = cl_oper;
        if error is None:
            
            query = "UPDATE `operations` SET `status`='running' WHERE `operation_id`='%d'; UPDATE `files` set `status` ='processing' WHERE file_id = %d"%(arg.oper_id, arg.file_id);
            self.execute_query(query);

            if self.debug:
                print (query);

            return;

        arg2 = error;
        print('[Error] [{}]'.format(arg2));
        if len(arg2) and self.debug:
            print('[Error] %s' % arg2);

        query = "UPDATE `operations` SET `status`='%s', `error_message`='%s' WHERE `operation_id`='%d'; UPDATE `files` SET `status`='ready' WHERE `file_id`=%d" % ( 'finished' if len(arg2) == 0 else 'error', arg2, arg.oper_id, arg.file_id);
        self.execute_query(query);

        if self.debug:
            print (query);

    def get_info_multiproc( self, multi_id):
            """
            Take multiproccessor id and return `cl_multi` python class
            """

            query = "SELECT * from `multiprocessors` where `multiprocessor_id`='%d' LIMIT 1"%(multi_id);
            if self.debug:
                print(query);

            result = self.execute_query(query);
            result = self.fetchall()

            if len(result):
                return class_multiproc(result[0]);

            raise Exception("[{}]Empty Result...".format(self.get_info_multiproc.__name__));

    def delete_from_filecache(self, file_id, multi_id):
            """
            Function take file_id and multiprocessor id and delete item from table filecache
            """

            qstr = '';
            for item in file_id:
                qstr += "`file_id` = '%d' OR " % item;

            qstr = qstr[:-4];

            query = "DELETE FROM `filecache` WHERE (%s) and `multiprocessor_id`='%d'"%(qstr, multi_id);
            if self.debug:
                print(query);

            result =self.execute_query(query);

            return True;

    def get_filecache_by_id(self, multi_id = None, file_id = None, status = None, sorted = False):
            """
            Return `cl_filecache` python class
            multi_id : multiproccessor_id
            file_id : file id
            file_status: from table filecache; If need select with unique file_status
            sorted: if true select  ORDER BY (`read_counter` and `write_counter`) ASC
            """

            need_sort = "ORDER BY (`read_counter` and `write_counter`) ASC" if sorted else "";
            with_status = " AND `status` = '{}'".format(status) if status is not None else "";
            by_multi_id = "`multiprocessor_id`='{}' ".format(multi_id) if multi_id is not None else "";
            by_file_id = "`file_id`='{}' ".format(file_id) if file_id is not None else "";

            query = "SELECT * from `filecache` where {} {} {} {}".format(by_multi_id, by_file_id, with_status, need_sort);
            if self.debug:
                print(query);

            result = self.execute_query(query);
            result = self.fetchall()

            lst = list();
            if len(result):
                for obj in result:
                    lst.append(class_filecache(obj))

                return lst;

            return False;

    def get_filecache_sum(self, list_files):
            """
            Return size of files by list that contains file_id
            """

            if len(list_files) == 0:
                return 0;

            lst = list();

            for file_id in list_files:
                lst.append("`file_id` = '{}'".format(file_id));

            string = ' OR '.join(lst);

            if len(string) < 6:
                return False;

            query = "SELECT SUM(size) FROM `files` WHERE (%s)"%(string);
            if self.debug:
                print(query);

            result = self.execute_query(query);
            result = self.fetchall()

            if len(result):
                return result[0][0];

            raise Exception("[{}]Empty Result...".format(self.get_filecache_sum.__name__));

    def filecache_update(self, fid, mid, **kwargs):
            """
            update table filecache 
            mid : multiproccessor_id
            fid : file id
            **kwargs : field in table filecache, give "+" if you want add: write_counter="+" ~ write_counter = write_counter +1 
            Example query_filecache_update( fid=0, mid=0, file_id="1", write_counter="5" )
            See class filecache for more info about params
            """

            if not len(kwargs):
                raise Exception("[{}]Empty args...".format(self.filecache_update.__name__));

            lst = list();
            for value, key in kwargs.items():
                lst.append("`{}`='{}'".format(value, key)) if key != '+' else lst.append("`{}`=`{}` + 1".format(value, value));

            qstr = ', '.join(lst);

            query = "UPDATE `filecache` SET %s WHERE `file_id`='%d' and `multiprocessor_id`='%d'"%(qstr, fid, mid);
            if self.debug:
                print(query);

            result = self.execute_query(query);

            return True;
    def add_to_filecache(self, **params):
            """
            Insert into table filecache
            **params : field in table filecache 
            See class filecache for more info about params
            Example query_add_to_filecache( file_id="1", write_counter="5" )
            """
            if not len(params):
                raise Exception("[{}]Empty args...".format(self.add_to_filecache.__name__));

            lst_1 = list();
            lst_2 = list();
            for value, key in params.items():
                lst_1.append("`{}`".format(value));
                lst_2.append("'{}'".format(key));

            str_values = ','.join(lst_1);
            str_keys = ','.join(lst_2);

            query = "INSERT INTO `filecache` (%s) VALUES (%s)"%(str_values, str_keys);

            if self.debug:
                print(query);

            result = self.execute_query(query);

            return True;
    def get_info_tasks_by_taskid(self, task_id):
            """
            Select info from table tasks by task_id and return 
            """
            query= "SELECT * FROM `tasks` WHERE `task_id` ='%d'"%task_id;
            if self.debug:
                print(query);

            result = self.execute_query(query);
            result = self.fetchall()

            lst = list();
            if len(result):
                return class_tasks(result[0]);

            raise Exception("[{}]Empty Result...".format(self.get_info_tasks_by_taskid.__name__));

    def get_info_tasksfiles_by_params(self, **params):
            """
            Select rows from taskfiles by params
            See class taskfiles for more info about params
            Example get_info_taskfiles_by_params(status='0') <> return all rows with status=0
            """

            lst = list();
            for value, key in params.items():
                lst.append("`{}`='{}'".format(value, key));

            str = ' AND '.join(lst);

            query= "SELECT * FROM `tasks_files` WHERE %s"%str;
            if self.debug:
                print(query);

            result = self.execute_query(query);
            result = self.fetchall()

            lst = list();
            if len(result):
                for obj in result:
                    lst.append(class_tasksfiles(obj))

                return lst;

            return False;
    
    def update_taskfiles_by_tid_and_fid(self, task_id, file_id, **params):
            """
            update taskfiles by task_id and file_id
            See class taskfiles for more info about params
            Example update_taskfiles_by_tid_and_fid(0,0, status='1')
            """

            lst = list();
            for value, key in params.items():
                lst.append("`{}`='{}'".format(value, key));

            qstr = ', '.join(lst);

            query= "UPDATE `tasks_files` SET {} WHERE `task_id`='{}' AND `file_id`='{}'".format(qstr, task_id, file_id);
            if self.debug:
                print(query);

            result = self.execute_query(query);

