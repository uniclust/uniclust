#!/usr/bin/python
# -*- coding: utf-8 -*

import paramiko

SSH_USE = False;
SSH_DEBUG = True;

class ssh_connections(object):

    enableSSH = True;
    debugSSH = True;

    def __init__(self, connect = False, host_name = None, user_name = None, key_path = None):
        """
        Create SSH Obj
        If you want connect at once, set param connect to True
        """
        if self.enableSSH is False:
            return

        self.host = host_name;
        self.user = user_name;

        passFile = open(key_path, 'r');
        passwd = passFile.read();
        passwd = passwd.strip();

        self.key = passwd;

        self.ssh = paramiko.SSHClient();
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy());

        if connect:
            self.connect();

    def connect(self, host_name = None, user_name = None, key_path = None):
        """
        Create SSH connection
        If run without any param, use default params to connect
        Return true if all OK
        Return string error value when except an error
        """

        if self.enableSSH is False:
            return

        try:
            self.ssh.connect( hostname= host_name,\
                 username = user_name,\
                 password = key_path) if host_name is not None else \
            self.ssh.connect( hostname= self.host,\
                 username = self.user,\
                 password = self.key)
        except Exception as error:
            return error;

        self.sftp = self.ssh.open_sftp();
        return True;

    def exec(self, command):
        """
        Exec ssh command, and return error value > 0
        """
        if self.enableSSH is False:
            return

        stdin,stdout, stderr = self.ssh.exec_command( command );
        if self.debugSSH:
            print(str(stdout.read()) + ' ' + str(stderr.read()));

        return stderr;

    def close(self):
        if self.enableSSH is False:
            return

        self.sftp.close();
        self.ssh.close();
        


    def transfer_file( self, local, remote):
        if self.enableSSH is False:
            return

        if self.debugSSH:
            print( ' Copy from local: ['+local+']' + 'to remote [' + remote +']')

        self.sftp.put(local, remote)

    def download_file( self, remote, local):
        if self.enableSSH is False:
            return

        if self.debugSSH:
            print( ' Download from remote: ['+remote+']' + 'to local [' + local +']')

        self.sftp.get( remote, local );

    def delete_file( self, file):
        if self.enableSSH is False:
            return

        if self.debugSSH:
            print( ' Download from remote: ['+remote+']' + 'to local [' + local +']')

        self.sftp.remove( file );