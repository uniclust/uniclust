

from uniclust import abstract_db as database
from uniclust import filecache_globalvars as global_vars2

class TestInit(object):
    
    # Минимальные данные для Базы данных

    # Имя юзера
    user_name = "unkown"

    # Суперкомпьютер
    name = "mAngel"
    rootPath = "test"
    
    host = "angel.cs.msu.ru"

    # Имя пользователя на вычислительном кластере
    user_on_cluster = "elizarov"
    
    #Квота на кластере
    fileQuota = 2048


    def initTest( self ):
        db=database.Db_connection(
            host = global_vars2.db_host,
            user = global_vars2.db_user,
            passwd = None,
            db  = global_vars2.db_name,
            key = global_vars2.db_passwd_file)

        db.execute( "INSERT INTO `users` VALUES (NULL, '{}', '', '', NULL, NULL, '10');".format( self.user_name));

        db.execute( "INSERT INTO `multiprocessors` VALUES ('', '{}', '1', '', '{}', '{}', '{}', 22, '{}', NULL, NULL);" \
            .format( self.name, self.rootPath, self.user_on_cluster,\
                     self.host, self.fileQuota))

if __name__ == '__main__':
    TestInit().initTest();

