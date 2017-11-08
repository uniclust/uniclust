#!/usr/bin/python
# -*- coding: utf-8 -*

import paramiko

SSH_USE = False;
SSH_DEBUG = True;

def ssh_client():
    if SSH_USE == False:
        return 0;

    return paramiko.SSHClient();

def ssh_connect( ssh, host_name, user_name, key_path ):
    if SSH_USE == False:
        return 0;

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy());
    return ssh.connect( hostname= host_name,\
                 username = user_name,\
                 key_filename = key_path);

def ssh_exec( ssh, command ):
    if SSH_USE == False:

        if SSH_DEBUG:
            print (command);

        return 0;

    stdin,stdout, stderr = ssh.exec_command( command );
    if SSH_DEBUG:
        print (stdout.readlines());

    return stderr;

def ssh_close( ssh ):
    if SSH_USE == False:
        return 0;

    ssh.close();