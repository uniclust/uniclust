#!/usr/bin/python
# -*- coding: utf-8 -*

import paramiko
import global_vars

def ssh_client():
    return paramiko.SSHClient();

def ssh_connect( ssh, host_name, user_name, key_path ):
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy());
    return ssh.connect( hostname= host_name,\
                 username = user_name,\
                 key_filename = key_path);

def ssh_exec( ssh, command ):
    stdin,stdout, stderr = ssh.exec_command( command );
    if global_vars.DEBUG:
        print stdout.readlines();

    return stderr;

def ssh_close( ssh ):
    ssh.close();