class db_classes(object):
    """Description of db classes
        This file contaion main classes based on database
        cl_file: table files
        cl_oper: table operation
        cl_multi: table multiprocessor
        """

class cl_multi(db_classes):
    """Obj of multiproccessor class"""
    def __init__(self,  multi_obj ):
        self.multiprocessor_id =       multi_obj[0];
        self.multiprocessor_name =     multi_obj[1];
        self.num_avaible_procs =        multi_obj[2];
        self.path =                     multi_obj[4].decode("utf-8");
        self.user_on_it =               multi_obj[5];
        self.host =                     multi_obj[6];
        self.files_quota =              multi_obj[8];

class cl_file(db_classes):
    """description of class"""
    def __init__(self,  file_object ):
        self.file_id =      file_object[0];
        self.name =         file_object[1];
        self.status =       file_object[2];
        self.user_id =      file_object[3];
        self.size =         file_object[4];
        self.num_of_reads = file_object[5];

class cl_operation(db_classes):
    """description of class"""
    def __init__(self,  oper_object ):
        self.oper_id =              oper_object[0];
        self.file_id =              oper_object[1];
        self.oper_type =            oper_object[2];
        self.multiprocessor_id =    oper_object[3];
        self.status =               oper_object[4];
        self.error_message =        oper_object[5];

class cl_filecache(db_classes):
    """description of class"""
    def __init__(self,  filecache_object ):
        self.id =                   filecache_object[0];
        self.file_id =              filecache_object[1];
        self.multiprocessor_id =    filecache_object[2];
        self.status =               filecache_object[3];
        self.read_counter =         filecache_object[4];
        self.write_counter =        filecache_object[5];
        self.last_read =            filecache_object[6];
        self.last_write =           filecache_object[7];

class cl_tasksfiles(db_classes):
    """description of class"""
    def __init__(self,  task_object ):
        self.task_id =      task_object[0];
        self.file_id =      task_object[1];
        self.access_mode =  task_object[2];
        self.status =       task_object[3];