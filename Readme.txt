This is software for running bioinformatic tasks on remote machines.
It is suggested that remote machines are HPC clusters where user's tasks 
are queued by Job control systems like PBS, LoadLeveler, slurm and so one.

Catalogues structure:
 
 website -- catalogue which contains PHP scripts that provide Web-interface
            for user.

 ssh_run -- Python scripts which transfer data on/from remote machine and run
            user's task on cluster by means of special bash scripts.

 bash_scripts -- catalogues with scripts for submiting task into the queue on
                 computational cluser, for check result and other important 
                 tasks.


This system requires:

1. web server with support PHP. For example it may be Apache and mod_php
2. MySQL. MySQL must br supported in  the php and python
3. Python with second (not thrid) version of language.
4. SSH. You should use autorization by keys in such way, where sepecial user 
   which will connect to the remote machine must do not enter Password and
   passphrase for key.
5. Cron -- for running python scripts in certain time intervals.

You should do some actions before it will in working state:

1. Modify and then rename all files with extension '.example'.
2. Create a user and group under which scripts will be executed.
3. Install MySQL server and criate database on it. You should 
   initialise database by using db.sql script.
4. Install webserver and bind PHP scripts for it.
5. Create directories where users will store their data. Must be writeable by 
   both web server and Python script.
6. Add to cron periodical running server.py

  
 
