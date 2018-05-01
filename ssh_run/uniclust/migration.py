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

        for item in objList:
            #Добавляем новый атрибут для каждого элемента списка
            # атрибут хранит всю информацию о файле, в т.ч размер файла
            # Чтобы потом мы смогли по ним сортировать и не мучаться
            item.file_info = db.get_info_file( item.file_id );

        # Сортируем в порядке 'короткие раньше'
        objList.sort( key = lambda item : item.file_info.size); 
        
        #Сортировка по количеству использований файла в таблице files
        objList.sort( key = lambda item : item.file_info.num_of_reads); 

        
        # В цикле проходим по всем объектам нашего списка
        # создаем новый аттрибут objList.file_used_all_tasks = в скольких тасках он используется
        for item in objList:
            item.file_used_all_tasks = db.get_tasks_for_file_id( item.file_info.file_id );

        #Сортировка по тем файлам которые нужны наибольшему количеству тасков (всем таскам?)
        objList.sort( key = lambda item : item.file_used_all_tasks);
        

        last_task = db.get_last_task();
        #добавляем параметр file_used_first_task
        # file_used_first_task = 1 если файл не нужен для ближайшего таска, 0 - иначе
        for item in objList:
            item.file_used_first_task =( 0 if last_task is False else 0 if db.is_file_in_last_task( last_task.task_id, item.file_info.file_id ) else 1 );

        #Сортировка по тем файлам которые нужны ближайшему таску
        objList.sort( key = lambda item : item.file_used_first_task);

        return objList;

        