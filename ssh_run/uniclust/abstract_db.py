import pymysql as sql
import cl_operation as class_operations
import cl_file as class_files

class Db_connection(object):
    def    __init__(self,**kwargs):
        """
        Creating database object and connecting it to
        really database
        """
        self.db = None
        self.error = False
        self.error_message = '';

        self.debug = False;
        try:
            self.db = sql.connect(**kwargs);
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
                lst.append(class_operations.cl_operation(obj))

            return lst;

        return False;

    def query_get_fileinfo_by_fileid(self, file_id):
        """
        Return `cl_file` python class
        """

        query = "SELECT * FROM `files` WHERE `file_id`='%d' LIMIT 1" % file_id;

        if self.debug:
            print(query);

        result = self.execute_query(query);
        result = self.fetchall()

        if len(result):
            return class_files.cl_file(result[0]);

        return False;
    
    def query_lock_operation(self, **kwargs):
        """
        Lock/Unlock операцию. Принимает минимум 1 аргумент ввиде 
        cl_oper=class_operation 
        error=string
        Use query_lock_operation(cl_oper=this) чтобы lock операцию и файл который используется в ней
        Use query_lock_operation(cl_oper=this, error="") чтобы unlock операцию без ошибки;
        Use query_lock_operation(cl_oper=this, error="Error") чтобы разблокировать операцию с ошибкой;
        """

        RUNNING_STATUS = 2;

        if len(kwargs) < 1 or 'cl_oper' not in kwargs.keys():
            return -1; # Error

        if len(kwargs) == 1:
            arg = kwargs['cl_oper'];
            query = "UPDATE `operations` SET `status`=%d WHERE `operation_id`='%d'; UPDATE `files` set `status` = 2 WHERE file_id = %d"%(RUNNING_STATUS,arg.oper_id, arg.file_id);
            self.execute_query(query);

            if self.debug:
                print (query);

            return;

        arg2 = kwargs['error'];
        query = "UPDATE `operations` SET `status`=%d, `error_message`='%s' WHERE operation_id`='%d';\
                UPDATE `files` SET `status`='ready' WHERE `file_id`=%d" % ( 3 if not len(arg2) else 5, arg2, arg.oper_id, arg.file_id);

