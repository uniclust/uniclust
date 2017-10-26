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
        
        try:
            self.db = sql.connect(*args, **kwargs);
        except sql.InternalError as str:
            print(str.args);
            
        self.curs = self.db.cursor();
        
    def get_cursor(self):
        return self.db.cursor();
        return False;
    def execute_query( self, query ):
        return self.curs.execute( query );

    def fetchall(self):
        return self.curs.fetchall();
