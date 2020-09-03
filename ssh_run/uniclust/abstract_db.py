import pymysql as sql
from uniclust.db_classes import cl_file as class_files, cl_multi as class_multiproc, cl_operation as class_operations,\
                        cl_filecache as class_filecache, cl_tasksfiles as class_tasksfiles

from uniclust.task import Task as class_tasks

import uniclust.ssh2
import uniclust.filecache_globalvars as global_vars2
import datetime

from uniclust.task import *
from pprint import pprint

class Db_connection(object):

    def    __init__(self, host : str, user : str, passwd : str, db : str, key= None):
        """
        Creating database object and connecting it to
        really database
        """

        self.db = None
        self.error = False
        self.error_message = '';

        self.debug = False;

        if key is not None:
            passFile = open(key, 'r');
            passwd = passFile.read();
            passwd = passwd.strip();

            if len(passwd) < 3:
                raise Exception("[Error] Key must be at least 4 characters");

        try:
            ""
            self.db = sql.connect(host, user, passwd, db, autocommit=True );
        except sql.InternalError as str:
            raise Exception(str.args);
    
        self.curs = self.db.cursor();

    def execute( self, query, fetch_type : int = 0):
        """
        Execute query with debug and fetch the result
        @query: query to execute
        @fetch_type:
            0 - no fetch result
            1 - fetch all
            2 - fetch one
        """

        if self.debug:
            print("[Debug] %s"%query);

        self.curs.execute( query );

        return self.curs.fetchall() if fetch_type == 1 else  self.curs.fetchone() if fetch_type == 2 else True;

    # bool methods

    #Tasks
    def is_file_in_last_task(self, task_id, file_id : int) -> bool:
        """
        Возвращает True если файл с file_id нужен для ближайшего таска
        """

        query= "SELECT * FROM `tasks_files` WHERE `task_id`='{}' AND `file_id` = '{}' LIMIT 1".format(task_id, file_id);
        
        result = self.execute( query, fetch_type = 1 );

        return True if len(result) > 0 else False;

    ##############################################################
    # Get methods
    #################################################################

    #Algoritm
    def get_algoritm(self, app_id):
        """
        select algoritm from app
        """

        query= "SELECT * FROM `applications` WHERE `application_id`='%d'"%app_id;
        result = self.execute( query, fetch_type = 1 );

        if len(result) == 0:
            return False;

        lst = list();
        for obj in result:
            lst.append(class_tasks(obj, self))
        
        return lst

    #Files
    def get_info_file(self, file_id):
        """
        Возвращает объект типа `cl_file` (смотреть db_classes.py) для файла с file_id.
        Если такого file_id нет, возвращает False
        """

        query = "SELECT * FROM `files` WHERE `file_id`='%d' LIMIT 1" % file_id;
        result = self.execute( query, fetch_type = 1 );

        return class_files(result[0]) if len(result) else False;

    #Multiprocessors
    def get_info_multiproc( self, multi_id):
        """
        Возвращает объект типа `cl_multi` (смотреть db_classes.py) для мультипроцессора с multi_id.
        Если такого multi_id нет, возвращает False
        """

        query = "SELECT * from `multiprocessors` where `multiprocessor_id`='%d' LIMIT 1"%(multi_id);
        result = self.execute( query, fetch_type = 1 );

        return class_multiproc(result[0]) if len(result) else False;

    def get_multiprocs_ids( self ):
        """
        Return list of multiprocessor ids
        """

        query = "SELECT multiprocessor_id, multiprocessor_name FROM  `multiprocessors` ORDER BY  `multiprocessor_id`"
        result = self.execute( query, fetch_type = 1 );

        if len(result) == 0:
            return False;

        lst = list();
        for obj in result:
            lst.append( list(obj) )
        
        return lst

    #Operations
    def get_all_new_operations(self, super_comp_ids : list ):
        """
        Select all operations that has status 'new' and return class operations
        @test: если true то возвращает операции с любым статусом, иначе со статусом 'new'
        @super_comp_ids: лист с указанием id суперкомпьютеров, для которых будут взяты операции,
            если передать пустой список, то вернет операции для всех суперкомпьютеров
        """

        query = "SELECT * FROM `operations` where `status` = 'new' ORDER BY `operation_id`"

        if len(super_comp_ids):
            format_supercomp_for_query = ', '.join( str(ids) for ids in super_comp_ids);
            query= "SELECT * FROM `operations` where `status` = 'new' and `multiprocessor_id` IN ({})  ORDER BY `operation_id`  ".format(format_supercomp_for_query);

        result = self.execute( query, fetch_type = 1 );

        if len(result) == 0:
            return False;

        lst = list();
        for obj in result:
            lst.append(class_operations(obj))
        
        return lst

    #FileCache
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
        result = self.execute( query, fetch_type = 1 );

        if len(result) == 0:
            return False;

        lst = list();
        for obj in result:
            lst.append(class_filecache(obj))
        
        return lst

    def get_filecache_sum(self, list_files):
        """
        Return size of files by list that contains list_files
        """

        if len(list_files) == 0:
            return 0;

        lst = list();

        for file_id in list_files:
            lst.append("`file_id` = '{}'".format(file_id));

        string = ' OR '.join(lst);

        query = "SELECT SUM(size) FROM `files` WHERE (%s)"%(string);
        result = self.execute( query, fetch_type = 1 );

        return result[0][0] if len(result) else 0;

    #Tasks
    def get_all_files(self):
        """
        Get All files
        """

        query= "SELECT * FROM `files` WHERE 1"
        result = self.execute( query, fetch_type = 1 );

        if len(result) == 0:
            return False;

        lst = list();
        for obj in result:
            lst.append(class_files(obj))
        
        return lst
    def get_all_taskfiles(self):
        """
        Get All files
        """

        query= "SELECT * FROM `tasks_files` WHERE 1"
        result = self.execute( query, fetch_type = 1 );

        if len(result) == 0:
            return False;

        lst = list();
        for obj in result:
            lst.append(class_tasksfiles(obj))
        
        return lst
    def get_last_task(self):
        """
        Get last task from db table `tasks`, return class task (see db_classes.py for details)
        """

        query= "SELECT `task_id` FROM `tasks` WHERE `task_status`='new' ORDER BY `task_id` DESC LIMIT 1"
        result = self.execute( query, fetch_type = 1 );

        return result[0][0] if len(result) else False;
    def get_all_tasks(self):
        """
        GG
        """

        query= "SELECT `task_id` FROM `tasks` WHERE `task_status`='new' ORDER BY `task_id` DESC"
        result = self.execute( query, fetch_type = 1 );

        return result if len(result) else False;
    def get_info_tasks_by_taskid(self, task_id):
        """
        Select info from table tasks by task_id and return 
        """

        query= "SELECT * FROM `tasks` WHERE `task_id` ='%d' LIMIT 1"%task_id;
        result = self.execute( query, fetch_type = 1 );

        return class_tasks(result[0], self) if len(result) else False;

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
        result = self.execute( query, fetch_type = 1 );

        if len(result) == 0:
            return False;

        lst = list();
        for obj in result:
            lst.append(class_tasksfiles(obj))
        
        return lst

    def get_tasks_for_file_id(self, file_id : int):
        """
        Return number of tasks that use this file with file_id
        """

        query = """
        SELECT
            COUNT(*)
        FROM 
            `tasks_files`
        WHERE 
            `tasks_files`.`file_id` = '{}' AND
            `tasks_files`.`task_id` IN (SELECT `tasks`.`task_id` FROM `tasks` WHERE `tasks`.`task_status` = 'new')
        """.format(file_id);

        result = self.execute( query, fetch_type = 1 );

        return result[0];

    ##############################################################
    # Set and other methods
    #################################################################
    def set_task_status(self, task_id, status):
        """
        Set a 'status' to task by `task_id`
        """

        query = "update tasks set task_status='{}' where task_id={}".format(status, task_id);
        result = self.execute( query );

    def set_file_status(self, file_id, status="error"):
        """
            Function take file_id, status and update table files
        """
        query = "UPDATE `files` SET `status`='%s' WHERE `file_id`='%d'"%(status, file_id);
        result = self.execute( query );


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
        result = self.execute( query );

    def lock_operation(self, cl_oper, error=None):
        """
        Lock/Unlock операцию. Принимает минимум 1 аргумент ввиде 
        cl_oper=class_operation 
        error=string
        Use query_lock_operation(cl_oper=param) чтобы lock операцию и файл который используется в ней
        Use query_lock_operation(cl_oper=param, error="") чтобы unlock операцию без ошибки;
        Use query_lock_operation(cl_oper=param, error="Error") чтобы разблокировать операцию с ошибкой;
        """

        RUNNING_STATUS = 2;

        arg = cl_oper;

        if error is None:
            query = "UPDATE `operations` SET `status`='running' WHERE `operation_id`='%d'; UPDATE `files` set `status` ='processing' WHERE file_id = %d"%(arg.oper_id, arg.file_id);
            return self.execute(query, 1);

        arg2 = error;
        if len(arg2) and self.debug:
            print('[Error] %s' % arg2);

        query = "UPDATE `operations` SET `status`='%s', `error_message`='%s' WHERE `operation_id`='%d'; UPDATE `files` SET `status`='ready' WHERE `file_id`=%d" % ( 'finished' if len(arg2) == 0 else 'error', self.db.escape_string(arg2), arg.oper_id, arg.file_id);
        result = self.execute( query );

    def delete_from_filecache(self, file_id, multi_id):
        """
        Function take file_id and multiprocessor id and delete item from table filecache
        """

        qstr = '';
        for item in file_id:
            qstr += "`file_id` = '%d' OR " % item;

        qstr = qstr[:-4];

        query = "DELETE FROM `filecache` WHERE (%s) and `multiprocessor_id`='%d'"%(qstr, multi_id);
        result = self.execute( query );

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
        result = self.execute( query );

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
        result = self.execute( query );

