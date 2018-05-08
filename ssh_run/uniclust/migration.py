from uniclust import db_classes
from uniclust import abstract_db

class Mygration(object):
    """
    Take a list of class_operations. See db_classes.py
    Return list with priority
    """
    def __init__(self, db, objList : list):
        self.lst = list();

        if len(objList) <= 0:
            return print("[Migration] Empty Result");

        if db is None or db is False:
            return print("[Migration] Invalid db connections")

        list_by_oper_types = self.sort_by_oper_type(objList);

        # Сортируем операция с типом 'copyto' 
        list_by_oper_types[2] = self.sort_prior_oper_copyto( db, objList);

        for i in range(3):
            for item in list_by_oper_types[i]:
                self.lst.append(item);
       
    def get_lst(self):
        return self.lst;

    "Take a list of operations and return list with 3 list of diff operation"
    def sort_by_oper_type(self, objList : list):
        lst = list( list() for i in range(3));

        #lst[0] = all operations 'remove'
        #lst[1] = all operations 'copyfrom'
        #lst[2] = all operations 'copyto'
        for item in objList:
            lst[0].append(item) if item.oper_type == 'remove' else\
            lst[1].append(item) if item.oper_type == 'copyfrom' else\
            lst[2].append(item);

        return lst;

    def sort_prior_oper_copyto(self, db, objList : list):

        files = db.get_all_files();
        for item in objList:
            for file in files:
                if file.file_id == item.file_id:
                    item.file_size = file.size
                    item.num_of_reads = file.num_of_reads

        # Сортируем в порядке 'короткие раньше'
        objList.sort( key = lambda item : item.file_size); 
        
        #Сортировка по количеству использований файла в таблице files
        # Обратная сортировка, то есть те, у кого большое количество чтений должны передаваться раньше
        objList.sort( key = lambda item : item.num_of_reads, reverse = True); 

        
        # В цикле проходим по всем объектам нашего списка
        # создаем новый аттрибут objList.file_used_all_tasks = в скольких тасках он используется

        tskFiles = db.get_all_taskfiles()
        allTsk = db.get_all_tasks()

        if allTsk is False:
            return

        for item in objList:
            item.file_used_all_tasks = 0;

            for tsk in tskFiles:
                if item.file_id == tsk.file_id and (tsk.task_id,) in allTsk:
                    item.file_used_all_tasks += 1
            
            #item.file_used_all_tasks = db.get_tasks_for_file_id( item.file_id );

        #Сортировка по тем файлам которые нужны наибольшему количеству тасков (всем таскам?
        # Обратная сортировка, то есть те файлы, которые используют чаще, должны оказаться первее
        objList.sort( key = lambda item : item.file_used_all_tasks, reverse = True);
        
        #добавляем параметр file_used_first_task
        # file_used_first_task = 1 если файл не нужен для ближайшего таска, 0 - иначе

        for i in range( len(allTsk)):
            task = allTsk[i][0]

            for item in objList:

                item.file_used_first_task = 1
                for tsk in tskFiles:
                    if task == tsk.task_id and item.file_id == tsk.file_id:
                         item.file_used_first_task = 0

           # for item in objList:
           #     item.file_used_first_task = (   0 if db.is_file_in_last_task( task, item.file_id ) else 1 );

            objList.sort( key = lambda item : item.file_used_first_task, reverse= True);
        

        #Сортировка по тем файлам которые нужны ближайшему таску
        #objList.sort( key = lambda item : item.file_used_first_task);

        return objList;

        