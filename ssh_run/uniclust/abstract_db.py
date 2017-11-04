import pymysql as sql
from db_classes import cl_file as class_files, cl_multi as class_multiproc, cl_operation as class_operations,\
                        cl_filecache as class_filecache, cl_tasks as class_tasks, cl_tasksfiles as class_tasksfiles

class Db_connection(object):
    def    __init__(self, host, user, passwd, db):
        """
        Creating database object and connecting it to
        really database
        """
        self.db = None
        self.error = False
        self.error_message = '';

        self.debug = False;
        try:
            self.db = sql.connect(host, user, passwd, db);
        except sql.InternalError as str:
            print(str.args);
    
        self.curs = self.db.cursor();
    def execute_query( self, query ):
        return self.curs.execute( query );

    def fetchall(self):
        return self.curs.fetchall();

    def query_get_all_new_operations(self):
        """
        Select all operations that has status 'new' and return class operations
        """
        query= "SELECT * FROM `operations` ORDER BY `operation_id` ";
        if self.debug:
            print(query);

        result = self.execute_query(query);
        result = self.fetchall()

        lst = list();
        if len(result):
            for obj in result:
                lst.append(class_operations(obj))

            return lst;

        raise Exception("[{}]Empty Result...".format(query_get_all_new_operations.__name__));

    def query_info_by_fileid(self, file_id):
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

        raise Exception("[{}]Empty Result...".format(query_info_by_fileid.__name__));
    def query_set_file_status(self, file_id, status="error"):
        """
            Function take file_id, status and update table files
        """
        query = "UPDATE `files` SET `status`='%s' WHERE `file_id`='%d'"%(status, file_id);
        if self.debug:
            print(query);

        result =self.execute_query(query);

        return True;
    def query_lock_operation(self, cl_oper, error=None):
        """
        Lock/Unlock операцию. Принимает минимум 1 аргумент ввиде 
        cl_oper=class_operation 
        error=string
        Use query_lock_operation(cl_oper=this) чтобы lock операцию и файл который используется в ней
        Use query_lock_operation(cl_oper=this, error="") чтобы unlock операцию без ошибки;
        Use query_lock_operation(cl_oper=this, error="Error") чтобы разблокировать операцию с ошибкой;
        """

        RUNNING_STATUS = 2;

        if error is None:
            arg = cl_oper
            query = "UPDATE `operations` SET `status`=%d WHERE `operation_id`='%d'; UPDATE `files` set `status` = 2 WHERE file_id = %d"%(RUNNING_STATUS,arg.oper_id, arg.file_id);
            self.execute_query(query);

            if self.debug:
                print (query);

            return;

        arg2 = error;
        query = "UPDATE `operations` SET `status`=%d, `error_message`='%s' WHERE operation_id`='%d';\
                UPDATE `files` SET `status`='ready' WHERE `file_id`=%d" % ( 3 if not len(arg2) else 5, arg2, arg.oper_id, arg.file_id);

    def query_info_by_multiid( self, multi_id):
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

            raise Exception("[{}]Empty Result...".format(query_info_by_multiid.__name__));

    def query_delete_from_filecache(self, file_id, multi_id):
            """
            Function take file_id and multiproccessor id and delete item from table filecache
            """
            query = "DELETE FROM `filecache` WHERE `file_id`='%d' and `multiprocessor_id`='%d'"%(file_id, multi_id);
            if self.debug:
                print(query);

            result =self.execute_query(query);

            return True;

    def query_filecache_by_id(self, multi_id = None, file_id = None, file_status = None, sorted = False):
            """
            Return `cl_filecache` python class
            multi_id : multiproccessor_id
            file_id : file id
            file_status: from table filecache; If need select with unique file_status
            sorted: if true select  ORDER BY (`read_counter` and `write_counter`) ASC
            """

            need_sort = "ORDER BY (`read_counter` and `write_counter`) ASC" if sorted else "";
            with_status = " AND `status` = '{}'".format(file_status) if file_status is not None else "";
            by_multi_id = "`multiprocessor_id`='{}' ".format(multi_id) if multi_id is not None else "";
            by_file_id = "`file_id`='{}' ".format(file_id) if file_id is not None else "";

            query = "SELECT * from `filecache` where %s %s %s %s"%(by_multi_id, by_file_id, with_status, need_sort);
            if self.debug:
                print(query);

            result = self.execute_query(query);
            result = self.fetchall()

            lst = list();
            if len(result):
                for obj in result:
                    lst.append(class_filecache(obj))

                return lst;

            raise Exception("[{}]Empty Result...".format(query_filecache_by_id.__name__));

    def query_filecache_sum(self, list_files):
            """
            Return size of files by list that contains file_id
            """

            str = '';

            for file_id in list_files:
                str += " `file_id` = '%d' "%(file_id);

            if not len(str):
                return False;

            query = "SELECT SUM(size) FROM `files` WHERE (%s)"%(str);
            if self.debug:
                print(query);

            result = self.execute_query(query);
            result = self.fetchall()

            if len(result):
                return result[0][0];

            raise Exception("[{}]Empty Result...".format(query_filecache_sum.__name__));

    def query_filecache_update(self, fid, mid, **kwargs):
            """
            update table filecache 
            mid : multiproccessor_id
            fid : file id
            **kwargs : field in table filecache, give "+" if you want add: write_counter="+" ~ write_counter = write_counter +1 
            Example query_filecache_update( fid=0, mid=0, file_id="1", write_counter="5" )
            See class filecache for more info about params
            """

            if not len(kwargs):
                raise Exception("[{}]Empty args...".format(query_filecache_update.__name__));

            lst = list();
            for value, key in kwargs.items():
                lst.append("`"+value+"`='"+key+"'") if key != '+' else lst.append("`"+value+"`=`"+value+"` + 1");

            str = ', '.join(lst);

            query = "UPDATE `filecache` SET %s WHERE `file_id`='%d' and `multiproccessor_id`='%d'"%(str, fid, mid);
            if self.debug:
                print(query);

            result = self.execute_query(query);

            return True;
    def query_add_to_filecache(self, **params):
            """
            Insert into table filecache
            **params : field in table filecache 
            See class filecache for more info about params
            Example query_add_to_filecache( file_id="1", write_counter="5" )
            """
            if not len(params):
                raise Exception("[{}]Empty args...".format(query_add_to_filecache.__name__));

            lst_1 = list();
            lst_2 = list();
            for value, key in params.items():
                lst_1.append("`"+value+"`");
                lst_2.append("'"+key+"'");

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

            raise Exception("[{}]Empty Result...".format(get_info_tasks_by_taskid.__name__));

    def get_info_tasksfiles_by_params(self, **params):
            """
            Select all operations that has status 'new' and return class operations
            See class taskfiles for more info about params
            Example get_info_taskfiles_by_params(status='0')
            """

            lst = list();
            for value, key in params.items():
                lst.append("`"+value+"`='"+key+"'");

            str = ', '.join(lst);

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

            raise Exception("[{}]Empty Result...".format(get_info_taskfiles_by_params.__name__));
