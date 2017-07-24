# -*- coding: utf-8 -*-

import os
import fcntl
import argparse

from pwd import getpwnam

def parse_config_file(config_file_name="/etc/uniclust/uniclust.conf"):
    """
    This function requires file_name in argument,
    and parse from it dictionary of parameters.
    
    If some parameters skip in config file then it is 
    assigned by default.
    """
    f=open(conffilename,"r")
    
    config=dict()
    
    #
    #
    # default parameters
    #
    #
    
    config['pid_file'] = '/var/run/uniclust.pid'
    config['log_file']  = '/var/log/uniclust.log'
    config['err_file']  = '/var/log/uniclust.err'
 
    config['user']     = 'uniclust'
    config['group']    = 'uniclust'
 
    config['private_key_file'] = '/etc/uniclust/ssh_key'
    
    config['site_address'] = 'localhost'
    config['path_on_site'] = '/uniclust'

    #
    # lock file used like pid file, to lock dataset 
    #
    config['lock_file'] = '/var/lib/uniclust/server.lock'
    config['data_path'] = '/var/lib/uniclust'

    config['db_host']        = 'localhost'
    config['db_port']        = '' #set default by database
    config['db_user']        = 'uniclust'
    config['database_name']  = 'uniclust'
    config['db_passwd_file'] = '/etc/uniclust/db_password'

    config['server_timeout'] = 300 # seconds

    config['scheduling_algorithm'] = 'FIFO'
   

    for l in f.read().split('\n'):
        l=l.split('#')[0]
        if '=' in l:
            kp=list(l.split('=',1))
            config[kp[0].lower()]=kp[1]

    f.close()

    return config;


def become_daemon(config,really_become = True):
    """
    Move server into the daemon mode.
    """
    # privileges
    goal_uid=getpwnam(config['user']).pw_uid
    goal_gid=getpwnam(config['group']).pw_gid
    
    try:
        f=os.open(config['lock_file'],os.O_CREAT|os.O_WRONLY|os.O_SYNC, 0600)
        fcntl.flock(f,fcntl.LOCK_EX | fcntl.LOCK_NB)
    except Exception as s:
        print "Сhecking server lock... Fail!"
        print "Try to delete the locking file '%s' manually" % (config['lock_file'])
        print "Reasoning is: %s" % (s)
        sys.exit(1)
    
    print "Сhecking server lock... OK!"

    if really_become == False:
        if os.geteuid() != goal_uid :
            print "warning: effective user id is not equal id for '%s'" % (config['user'])
        if os.getegid() != goal_gid :
            print "warning: effective group id is not equal id for '%s'" % (config['group'])
        return
    
    if os.geteuid()!= 0:
        print "Sorry, you need root privilegies to run it as daemon"
        sys.exit(1)
    
    #
    # Do first fork
    #
    try:
        pid = os.fork()
        if pid > 0:
                # exit first parent
                sys.exit(0)
    except OSError, e:
        sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
        sys.exit(1)
    
    #TODO do locks for it
    #
    # write pid file
    pidfile = file(config['pid_file'], 'w')
    
    # decouple from parent environment
    os.chdir("/")
    os.umask(0)
    os.setsid()
    
    # Do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent
            sys.exit(0)
    except OSError, e:
        sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
        sys.exit(1)
    
    
    sys.stdout.write("Successfully daemonization!")
    
    # redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    sys.stdin.close()
    
    #si = file('dev/null', 'r')
    so = file(config[logfile], 'a+')
    se = file(config[errfile], 'a+')
    
    #os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
    
    
    pid=os.getpid()
    pidfile.write(pid)
    
    #TODO
    # Make lock for it
    #
    pidfile.fclose()
    
    #
    # change user
    #
    os.setgid(goal_gid)
    os.setpid(goal_pid)
    os.setegid(goal_gid)
    os.seteuid(goal_uid)
    
    sys.stdout.write("Success io redirection")


def parse_arguments(argv):
    """
    Parsing arguments for server
    """
    parser = argparse.ArgumentParser(
            description=_("""
             This program is server for running users tasks on several
             supercomputers. For details see:
             https://github.com/uniclust
             """),
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
            '--config',
            dest='config_file_name',
            required=False,
            help=_('Name of config file'),
            default="/etc/uniclust/uniclust.conf"
    )
    
    parser.add_argument(
            '--become_daemon',
            dest='become_daemon',
            required=False,
            choices= [ 'yes', 'no' ],
            default='yes'
            help=_('Run not in daemon mode')
    )

    args = parser.parse_args()
    return args
   
