class cl_file(object):
    """description of class"""
    def __init__(self,  file_object ):
        self.file_id =      file_object[0];
        self.name =         file_object[1];
        self.status =       file_object[2];
        self.user_id =      file_object[3];
        self.size =         file_object[4];
