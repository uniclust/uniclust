class cl_operation(object):
    """description of class"""
    def __init__(self,  oper_object ):
        self.oper_id =              oper_object[0];
        self.file_id =              oper_object[1];
        self.oper_type =            oper_object[2];
        self.multiprocessor_id =    oper_object[3];
        self.status =               oper_object[4];
        self.error_message =        oper_object[5];
