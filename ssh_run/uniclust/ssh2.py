#!/usr/bin/python
# -*- coding: utf-8 -*

import paramiko

SSH_USE = False;
SSH_DEBUG = True;

class ssh_connections(object):

    enableSSH = False;
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
        self.key = key_path;

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
            ssh.connect( hostname= host_name,\
                 username = user_name,\
                 key_filename = key_path) if host_name is not None else \
            ssh.connect( hostname= self.host,\
                 username = self.user,\
                 key_filename = self.key)
        except Exception as error:
            return error;

        return True;

    def exec(self, command):
        """
        Exec ssh command, and return error value > 0
        """
        if self.enableSSH is False:
            return

        stdin,stdout, stderr = self.ssh.exec_command( command );
        if self.debugSSH:
            print(stdout.readlines());

        return stderr;

    def close(self):
        if self.enableSSH is False:
            return

        ssh.close();