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
        query=\
        """
        select 
            *
        from
            operations

        """
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

        query =\
        """
        SELECT 
            *
        FROM 
            `files`
        WHERE 
            `file_id`='%d' LIMIT 1
        
        """ % file_id;
        if self.debug:
            print(query);

        result = self.execute_query(query);
        result = self.fetchall()

        if len(result):
            return class_files.cl_file(result[0]);

        return False;
