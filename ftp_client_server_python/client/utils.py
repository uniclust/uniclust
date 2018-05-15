#!/usr/bin/python3
#--*--encoding:utf8--*--


import grp
import pwd
import time
import os
import stat

class fileInfo():
    def __init__(self, name, mode, number, user, group, size, last_modification_time):
        self.Name = name
        self.Mode = mode
        self.Number = number
        self.User = user
        self.Group = group
        self.Size = size
        self.LastModificationTime = last_modification_time

#ф-я получения свойств файла
def fileProperty(filepath):

    st = os.stat(filepath)
    fileMessage = [ ]
    def _getFileMode( ):
        modes = [
            stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR,
            stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP,
            stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH,
        ]
        mode     = st.st_mode
        fullmode = ''
        fullmode += os.path.isdir(filepath) and 'd' or '-'

        for i in range(9):
            fullmode += bool(mode & modes[i]) and 'rwxrwxrwx'[i] or '-'
        return fullmode


    # внутренние функции
    def _getFilesNumber( ):
        return str(st.st_nlink)

    def _getUser( ):
        return pwd.getpwuid(st.st_uid).pw_name

    def _getGroup( ):
        return grp.getgrgid(st.st_gid).gr_name

    def _getSize( ):
        return str(st.st_size)

    def _getLastTime( ):
        return time.strftime('%b %d %H:%M', time.gmtime(st.st_mtime))

    file_info = fileInfo(os.path.basename(filepath), _getFileMode(),_getFilesNumber(), _getUser(), _getGroup(), _getSize(), _getLastTime())

    return file_info