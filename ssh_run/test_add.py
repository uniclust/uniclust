from uniclust import abstract_db as database
from uniclust import filecache_globalvars as global_vars2

from random import randint
import time

import test_init as mTest

class TestAdd(object):

    #Количество задач 
    num_tasks = 9;
    # Количество файлов для задач
    num_files_for_tasks = 9;
    
    # размер файлов
    # Для генерации рандомных значений укажите отрицательное число
    # При этом будет сгенерировано случайное значение от 1 до указанного числа
    fileSize = 100

    # Увеличвает или уменьшает размер реальных файлов
    # Для fileSize = 100 и multiConst = 10 получаются файлы  ~1 Кб
    # Используйте 100, 1000, 10000 и тд
    multiConst = 10

    db = None;


    def conn(self):

        if self.db != None:
            return

        self.db=database.Db_connection(
            host = global_vars2.db_host,
            user = global_vars2.db_user,
            passwd = None,
            db  = global_vars2.db_name,
            key = global_vars2.db_passwd_file)

    def clearTasks(self):
        print("Clear tables in Database")
        self.conn()
        self.db.execute("SET FOREIGN_KEY_CHECKS = 0; ")
        self.db.execute("TRUNCATE `h91184_cs-suite`.`tasks`")
        self.db.execute("TRUNCATE `h91184_cs-suite`.`operations`")
        self.db.execute("TRUNCATE `h91184_cs-suite`.`files`")
        self.db.execute("TRUNCATE `h91184_cs-suite`.`filecache`")
        self.db.execute("TRUNCATE `h91184_cs-suite`.`tasks_files`")
        self.db.execute("SET FOREIGN_KEY_CHECKS = 1; ")

    def addTasks( self ):
        self.conn()

        user_id = self.db.execute("SELECT `user_id` FROM `users` WHERE `login`='{}'".format(mTest.TestInit.user_name), 2)
        uid = user_id[0];

        print("Generate Tasks and files")
        for i in range( self.num_tasks):
            query = "INSERT INTO `tasks` VALUES ({}, (SELECT `user_id` FROM `users` WHERE `login`='{}'), (SELECT `multiprocessor_id` FROM `multiprocessors` WHERE `multiprocessor_name`='{}'), '5', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'new', NULL, NULL, NULL);".format(\
                 i+1, mTest.TestInit.user_name, mTest.TestInit.name)
            self.db.execute(query);

            for j in range( 1, self.num_files_for_tasks + 1):

                 if self.fileSize <= 0:
                     self.fileSize = randint(1, abs(self.fileSize))

                 query =  "INSERT INTO `files` VALUES ('{}{}', NULL, 'ready', (SELECT `user_id` FROM `users` WHERE `login`='{}'), '{}', '0');".format( i,j, mTest.TestInit.user_name, self.fileSize)
                 self.db.execute(query);    

                 path = global_vars2.data_path + '/' + str(uid) + '/' + (str(i) if i > 0 else '') + str(j);
                 #print(path)
                 open(path, "w").truncate(self.fileSize * self.multiConst)

            for j in range( 1, self.num_files_for_tasks + 1):
                query = "INSERT INTO `tasks_files` VALUES ('{}', '{}{}', 'r', '0');".format( i+1, i,j)
                self.db.execute(query);

            for j in range( 1, self.num_files_for_tasks + 1):
                query = "INSERT INTO `operations` VALUES (NULL, '{}{}', 'copyto', (SELECT `multiprocessor_id` FROM `multiprocessors` WHERE `multiprocessor_name`='{}'), 'new', NULL);".format( i,j, mTest.TestInit.name)
                self.db.execute(query);

    def checkTasks(self ):
        self.conn()
        tasks = self.db.execute("SELECT `task_id` FROM `tasks` ORDER by `task_id` DESC", 1);

        print("Start check tasks")

        ttime = time.time()
        for task in tasks:

            task = task[0];
            mRes = 0;
            print('Wait for start Task #' + str(task)+'')
            while mRes != self.num_files_for_tasks:

                start = (task-1) * 10 +1
                end = start +self.num_files_for_tasks;

                files = ','.join([ str(this) for this in range( start, end) ])
                res = self.db.execute("SELECT COUNT(*) FROM `filecache` WHERE `status` = 'OK' and `file_id` IN ({}) ORDER by `file_id` DESC".format(files), 2);
                mRes = res[0];
                time.sleep(1)

            print('Task #' + str(task)+' success can start')
            print( time.time() - ttime)
            #self.db.execute("UDPATE `tasks` SET `task_status` = 'finished' WHERE `task_id` = '{}'".format(task), 1);
        
        print( time.time() - ttime)

TestAdd().clearTasks();
TestAdd().addTasks();
TestAdd().checkTasks();