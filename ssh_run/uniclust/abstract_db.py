# -*- coding: utf-8 -*
try:
    import pymysql as sql
    sql.install_as_MySQLdb()
except ImportError:
    pass

class Db_connection(object):
    def    __init__(self, *args, **kwargs):
        """
        Creating database object and connecting it to
        really database
        """
        self.db = None
        self.error = False
        self.error_message = '';

        self.debug = False;
        try:
            self.db = sql.connect(*args, **kwargs);
        except sql.InternalError as str:
            print(str.args);
    
        self.curs = self.db.cursor();
    def get_cursor(self):
        return self.db.cursor();

    def get_error(self):
        if self.error == True:
            return self.error_message;
        
        return False;
    def execute_query( self, query ):
        return self.curs.execute( query );

    def fetchall(self):
        return self.curs.fetchall();

    def main_select_query(self):
        """
        Select all operations that has status 'new' and return list
        """
        query=\
        """
        select 
            operations.operation_id,
            operations.file_id,
            operations.oper_type,
            operations.multiprocessor_id
        from
            operations
        where
            operations.status="new"
        """
        if self.debug:
            print(query);

        result = self.execute_query(query);
        return self.fetchall();

    def stock_checkfile_query(self, file_id):
        """
        Check file status for executing operation,
        return [0] => `status`, [1] => `user_id`, [2] => `size`
        """
        query =\
        """
        SELECT 
            `status`,
            `user_id`,
            `size`
        FROM 
            `files`
        WHERE 
            `file_id`='%d' LIMIT 1
        
        """ % file_id;
        if self.debug:
            print(query);

        result = self.execute_query(query);
        fetch = self.fetchall();
        fstatus = fetch[0][0];

        if fstatus != 'ready':
            raise Exception("Error File status")

        return fetch;
