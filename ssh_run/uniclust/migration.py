from uniclust import db_classes

class Mygration(object):
    """
    Take a list of class_operations. See db_classes.py
    Return list with priority
    """
    def __init__(self, db, objList : list):
        list_by_oper_types = self.sort_by_oper_type(objList);
        
        lst = list();
        for i in range(2):
            for item in list_by_oper_types[i]:
                lst.append(item);

        return lst;

    "Take a list of operations and return list with 3 list of diff operation"
    def sort_by_oper_type(self, objList : list):
        lst = list( list(), list(), list());

        #lst[0] = all operations 'remove'
        #lst[1] = all operations 'copyfrom'
        #lst[2] = all operations 'copyto'
        for item in objList:
            lst[0].append(item) if item.oper_type == 'remove' else\
            lst[1].append(item) if item.oper_type == 'copyfrom' else\
            lst[2].append(item);

        return lst;

    def sort_prior_oper_copyto(self, db, objList : list):
        task_lst = list(); # Получить все таски 

        resLst = list(); # Возвращаемый упорядоченный список

        for item in objList:
            #Добавляем новый атрибут для каждого элемента списка
            # атрибут хранит всю информацию о файле, в т.ч размер файла
            # Чтобы потом мы смогли по ним сортировать и не мучаться
            item.file_info = db.get_info_file( item.file_id );


        # Сортируем в порядке 'короткие раньше'
        objList.sort( key = lambda item : item.file_id.size); 
        
        #Сортировка по количеству использований файла в таблице files
        objList.sort( key = lambda item : item.file_id.num_of_reads); 

        #Создаем словарь типа {file_id : num_count} то есть каждому file_id ставим в соответствие количество его использований в тасках
        # Проверяем наличие каждого file_id из objList в task_lst
        # Потому что taskov меньше чем файлов

        count = 0; # для подсчета использований
        for item in objList:
            count = 0
            for tsk in task_lst:

                if (item.file_id in tsk):# если файл нужен для таска
                    count +=1;

            objList.file_used_all_tasks = count;

        #Сортировка по тем файлам которые нужны наибольшему количеству тасков (всем таскам?)
        objList.sort( key = lambda item : item.file_used_all_tasks);
        
        #добавляем параметр file_used_first_task
        # file_used_first_task = 1 если файл не нужен для ближайшего таска, 0 - иначе
        for item in objList:
            item.file_used_first_task =( 0 if item.file_id in task_lst[0] else 1 );

        #Сортировка по тем файлам которые нужны ближайшему таску
        objList.sort( key = lambda item : item.file_used_first_task);

        
        return objList;

        