#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import global_vars
import task
import sys
import os
import datetime
import Backfill
import time
import fcntl
import filecache/PythonApplication3
import filecache/db2

from uniclust import *


flag=True
#os.unlink(global_vars.lock_path)

# read config
conffilename = "/etc/uniclust/uniclust.conf"
f=open(conffilename,"r")
config={}
for l in f.read().split('\n'):
	l=l.split('#')[0]
	if '=' in l:
	    kp=list(l.split('=',1))
	    config[kp[0].lower()]=kp[1]
f.close()

if 'pidfile' not in config:
	config[pidfile] = '/var/run/uniclust.pid'

if 'user' not in config:
	config[user] = 'root'

if 'logfile' not in config:
	config[logfile] = '/var/log/uniclust.log'

if 'errfile' not in config:
	config[errfile] = '/var/log/uniclust.err'

if 'keyfile' not in config:
	config[keyfile] = '/var/key.txt'

# privileges
from pwd import getpwnam
os.setuid(getpwnam(config[user]).pw_uid)
os.setgid(getpwnam(config[user]).pw_gid)

try: 
	f=os.open(global_vars.lock_path,os.O_CREAT|os.O_WRONLY|os.O_SYNC, 0600)
	#f = open(global_vars.lock_path, "w")
	#pid = str(os.getpid())
	#f.write("%s\n" %pid)
	fcntl.flock(f,fcntl.LOCK_EX | fcntl.LOCK_NB)
except Exception as s:
	print s
	flag=False

if flag==False:
	print "Сhecking server lock... Fail! Try to delete the locking file manually"
	print "-------------------------"
	#os.close(f)
	#f.close()
	sys.exit(1)
print "Сhecking server lock... OK!"


#sys.stdout.write("Success!")
try:
	pid = os.fork()
	if pid > 0:
		# exit first parent
		sys.exit(0)
except OSError, e:
	sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
	sys.exit(1)
# write pid file
pidfile = file(config[pidfile], 'w')
pidfile.write(pid)
pidfile.fclose()
# decouple from parent environment
os.chdir("/")
os.umask(0)
os.setsid()
# do second fork
try:
	pid = os.fork()
	if pid > 0:
		# exit from second parent
		sys.exit(0)
except OSError, e:
	sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
	sys.exit(1)
sys.stdout.write("Success!")
# redirect standard file descriptors
sys.stdout.flush()
sys.stderr.flush()
#si = file('dev/null', 'r')
so = file(config[logfile], 'a+')
se = file(config[errfile], 'a+', 0)
#os.dup2(si.fileno(), sys.stdin.fileno())
os.dup2(so.fileno(), sys.stdout.fileno())
os.dup2(se.fileno(), sys.stderr.fileno())
sys.stdout.write("Success")

#f.seek(0, 0)
os.lseek(f, 0, os.SEEK_SET)
#f.rewind()
pid = str(os.getpid())
#f.write("%s\n" %pid)
os.write(f, "%s\n" %pid)
#f.flush()


#
# get current date and time (without microseconds)
#
while 1:
	#time.sleep(10)
	cur_time=str(datetime.datetime.now())
	for i in range(len(cur_time),0,-1):
		if cur_time[i-1]=='.':
			break
	if i>0:
		cur_time=cur_time[:i-1]


	#print "(%s)" %cur_time
	#sys.stdout.write('(%s)' %cur_time)


	#if flag:
	#	print "Сhecking server lock... Fail! Try to delete the locking file manually"
	#	print "-------------------------"
	#	f.close()
	#	sys.exit(1)
	#print "Сhecking server lock... OK!"

	PythonApplication3.start_work();
	
	db_error_flag=False
	try:
		db = db2.db_connect(\
			user=global_vars.db_user,
			host=global_vars.db_host,
			db=global_vars.db_name,
			passwd=global_vars.db_passwd
		)
	except:
		db_error_flag=True
		
	if db_error_flag:
		print "Couldn't connect to the database!"
		print "-------------------------"
		if flag:
			os.unlink(global_vars.lock_path)
		sys.exit(1)


	#f=open(global_vars.lock_path,"w")
	#f.write("Do not delete it!")
	#pid = str(os.getpid())
	#f.write("%s\n" %pid)
	#f.close()


	curs=db2.db_get_cursor(db)
	

	current_date=datetime.date.today()
	delta_time=datetime.timedelta(hours=24)
	expire_date=current_date-delta_time


	# uncomment it for debug
	#
	#print current_date
	#print expire_date



	query="delete from hash where date_label < '%s'" %expire_date
	db2.db_execute_query(curs, query);
	

	query=\
	"""
		select 
			tasks.user_id,
			tasks.task_id,
			tasks.algorithm,
			tasks.num_procs,
			tasks.duration_in_minutes,
			tasks.task_status,
			multiprocessors.host,
			multiprocessors.path,
			multiprocessors.user_on_it,
			users.email,
			tasks.priority_run,
			tasks.priority_max,
			tasks.running_time,
			tasks.queue_num,
			tasks.db_set
		from
			tasks,
			multiprocessors,
			users
		where
			((tasks.task_status="ready") or (tasks.task_status="stopped") or (tasks.task_status="submitted")) and
			(tasks.multiprocessor_id=multiprocessors.multiprocessor_id) and (multiprocessors.queue_alg = "simple") and
			(tasks.user_id=users.user_id)
	"""

	db2.db_execute_query(curs, query);
	result=db2.db_fetchall(curs)
	num_tasks=len(result)
	#if num_tasks>0:
	#	print "Processing %d tasks..." %num_tasks
	#else:
	#	print "No tasks to process!"

	for i in range(0,num_tasks):

		
		
		#
		# create Task object
		#
		tsk=task.Task(result[i])

		print "  task %d %d:" %(i, tsk.task_id)

		query=\
		"""
			select
				seq_type,
				blast_outp_detail_lvl,
				lower_thrshld
			from
				blast_tasks
			where
				task_id=%d
		""" %tsk.task_id
		db2.db_execute_query(curs, query);
		
		#
		# if BLAST was used, define ending elements of the Task object
		#
		tsk.init_blast_task(db2.db_fetchall(curs))
		
		
		#
		#
		# running tasks 
		#
		#
		if tsk.task_status=="ready":
			
			try:
				tsk.upload_data()
			except:
				print "    Upload data for task %d failed!" %tsk.task_id
				query="update tasks set task_status='stopped', priority_max=1005 where task_id=%d" %tsk.task_id
				db2.db_execute_query(curs, query);
				continue
			status=tsk.run()
			if status:
				print "    Run task %d failed!" %tsk.task_id
				query="update tasks set task_status='stopped', priority_max=1010 where task_id=%d" %tsk.task_id
				db2.db_execute_query(curs, query);
				continue
			query="update tasks set task_status='submitted', running_time=NOW() where task_id=%d" %tsk.task_id
			db2.db_execute_query(curs, query);

		#
		#
		# stopping tasks
		#
		#
		if tsk.task_status=="stopped":
			try:
				tsk.download_data()
			except:
				print "    Download data failed!"
			tsk.remote_task_delete()
			query="update tasks set task_status='refused' where task_id=%d" %tsk.task_id
			db2.db_execute_query(curs, query);
			tsk.email_notify_on_finish("refused")

		#
		#
		# checking tasks
		#
		#
		if tsk.task_status=="submitted":
			status=tsk.check()
			print "    Task check: %d" %status
			
			if status==0:
				tsk.clear_remote_data()
				tsk.download_data()
				tsk.remote_task_delete()
				query="update tasks set task_status='finished',date_of_finishing=CURRENT_DATE where task_id=%d" %tsk.task_id
				db2.db_execute_query(curs, query);
				tsk.email_notify_on_finish("success")
				continue
				
			if status==2:
				continue
		
			#
			# Unknown task status or error during task code execution
			#
			tsk.clear_remote_data()
			try:
				tsk.download_data()
				tsk.remote_task_delete()
			except:
				print "    TASK ERROR!!"
			
			query="update tasks set task_status='refused' where task_id=%d" %tsk.task_id
			db2.db_execute_query(curs, query);
			tsk.email_notify_on_finish("refused")


	#mpfpfs tasks

	query=\
	"""
		select 
			multiprocessors.num_available_procs,
			multiprocessors.multiprocessor_id
		from
			multiprocessors
		where
			multiprocessors.queue_alg = "mpfpfs"
	"""
	db2.db_execute_query(curs, query);
	resultM=db2.db_fetchall(curs)
	num_multiprocessors=len(resultM)
	#print "%d multiprocessor(s) use(s) algorithm 'mpfpfs':" %num_multiprocessors
	rt = datetime.datetime.today()

	for i in range(0,num_multiprocessors):
		num_mult_proc=resultM[i][0]
		mult_id=resultM[i][1]
		
		proc_num = num_mult_proc
		
		SubmittedTask = []
		SubTaskId = []
		TaskList = [] 
		RunTaskList = []
		SbmTaskList = []
		StopTaskList = []
		ReadyTaskLst = []
		NqTaskList = []
		NewRunTaskList = []
		NewSbmTaskList = []
		tsklist = {}
		#select queued & not queued 
		query=\
		"""
			select 
				tasks.user_id,
				tasks.task_id,
				tasks.algorithm,
				tasks.num_procs,
				tasks.duration_in_minutes,
				tasks.task_status,
				multiprocessors.host,
				multiprocessors.path,
				multiprocessors.user_on_it,
				users.email,
				tasks.priority_run,
				tasks.priority_max,
				tasks.running_time,
				tasks.queue_num,
				tasks.db_set
				
			from
				tasks,
				multiprocessors,
				users
			where
				(tasks.queue_num is NULL) and (tasks.task_status="ready") and
				(tasks.multiprocessor_id=multiprocessors.multiprocessor_id) and
				(multiprocessors.multiprocessor_id = %d) and 
				(tasks.user_id=users.user_id)
		"""%mult_id
		db2.db_execute_query(curs, query);
		result_q1=db2.db_fetchall(curs)
		num_tasks_q1=len(result_q1)
		
		query=\
		"""
			select 
				tasks.user_id,
				tasks.task_id,
				tasks.algorithm,
				tasks.num_procs,
				tasks.duration_in_minutes,
				tasks.task_status,
				multiprocessors.host,
				multiprocessors.path,
				multiprocessors.user_on_it,
				users.email,
				tasks.priority_run,
				tasks.priority_max,
				tasks.running_time,
				tasks.queue_num,
				tasks.db_set
				
			from
				tasks,
				multiprocessors,
				users
			where
				!(tasks.queue_num is NULL) and 
				((tasks.task_status="ready") or (tasks.task_status="stopped") or (tasks.task_status="submitted")) and
				(tasks.multiprocessor_id=multiprocessors.multiprocessor_id) and
				(multiprocessors.multiprocessor_id = %d) and 
				(tasks.user_id=users.user_id)
		"""%mult_id
		db2.db_execute_query(curs, query);
		result_q2=db2.db_fetchall(curs)
		num_tasks_q2=len(result_q2)
		
		#print "\tnumber of not queued tasks on multiproc with ID %d is %d" %(mult_id, num_tasks_q1)
		#print "\tnumber of queued tasks on multiproc with ID %d is %d" %(mult_id, num_tasks_q2)
		
		
		#select broken tasks
		query=\
		"""
			select 
				tasks.user_id,
				tasks.task_id,
				tasks.algorithm,
				tasks.num_procs,
				tasks.duration_in_minutes,
				tasks.task_status,
				multiprocessors.host,
				multiprocessors.path,
				multiprocessors.user_on_it,
				users.email,
				tasks.priority_run,
				tasks.priority_max,
				tasks.running_time,
				tasks.queue_num,
				tasks.db_set
				
			from
				tasks,
				multiprocessors,
				users
			where
				(tasks.queue_num is NULL) and (tasks.task_status="stopped") and
				(tasks.multiprocessor_id=multiprocessors.multiprocessor_id) and
				(multiprocessors.multiprocessor_id = %d) and 
				(tasks.user_id=users.user_id)
		"""%mult_id
		db2.db_execute_query(curs, query);
		result_q3=db2.db_fetchall(curs)
		
		#delete broken tasks
		for i in range(0, len(result_q3)):
			tsk=task.Task(result_q3[i])
			try:
				tsk.download_data()
			except:
				print "    Download data failed!"
			tsk.remote_task_delete()
			query="update tasks set task_status='refused' where task_id=%d" %tsk.task_id
			db2.db_execute_query(curs, query);
			tsk.email_notify_on_finish("refused")
		
		if (num_tasks_q1 == 0) and (num_tasks_q2 == 0):
			continue
		
		#fill task status lists
		for i in range(0,num_tasks_q1):
			tsk=task.Task(result_q1[i])
			#NqTaskList.append([tsk.task_id, tsk.duration_in_minutes*60, tsk.num_procs])
			NqTaskList.append(tsk)
		
		for i in range(0,num_tasks_q2):
			tsk=task.Task(result_q2[i])
			if (tsk.task_status == "submitted"):			
				#SbmTaskList.append([tsk.task_id, tsk.duration_in_minutes*60, tsk.num_procs, tsk.queue_num])
				SbmTaskList.append(tsk)
				proc_num = max(0, proc_num - tsk.num_procs)
			#do we need it?
			elif (tsk.task_status == "running"):
				#RunTaskList.append([tsk.task_id, tsk.duration_in_minutes*60, tsk.num_procs, tsk.queue_num])
				RunTaskList.append(tsk)
				proc_num = max(0, proc_num - tsk.num_procs)
			elif (tsk.task_status == "stopped"):
				#StopTaskList.append([tsk.task_id, tsk.duration_in_minutes*60, tsk.num_procs, tsk.queue_num])
				StopTaskList.append(tsk)
				proc_num = max(0, proc_num - tsk.num_procs)
			#do we need it?	
			elif (tsk.task_status == "ready"):	
				#ReadyTaskList.append([tsk.task_id, tsk.duration_in_minutes*60, tsk.num_procs, tsk.queue_num])
				ReadyTaskList.append(tsk)
		#
		# stopping tasks
		#
		for i in range (0, len(StopTaskList)): 	
			try:
				StopTaskList[i].download_data()
			except:
				print "    Download data failed!"
			StopTaskList[i].remote_task_delete()
			query="update tasks set task_status='refused' where task_id=%d" %StopTaskList[i].task_id
			db2.db_execute_query(curs, query);
			StopTaskList[i].email_notify_on_finish("refused")
			proc_num = min(num_mult_proc, proc_num + StopTaskList[i].num_procs)
			
		
		#do we need it?
		#
		#check tasks
		#
		for i in range (0, len(RunTaskList)): 
			
			status=RunTaskList[i].check()
			print "    Task check: %d" %status
			
			if status==0:
				RunTaskList[i].clear_remote_data()
				RunTaskList[i].download_data()
				RunTaskList[i].remote_task_delete()
				query="update tasks set task_status='finished',date_of_finishing=CURRENT_DATE where task_id=%d" %RunTaskList[i].task_id
				#RunTaskList[i].task_status = 'finished'
				db2.db_execute_query(curs, query);
				RunTaskList[i].email_notify_on_finish("success")
				proc_num = min(num_mult_proc, proc_num + RunTaskList[i].num_procs)
				#del RunTaskList[i]
				continue
				
			if status==2:
				NewRunTaskList.append(RunList[i])
				continue
				
		#
		#check tasks
		#
		for i in range (0, len(SbmTaskList)):
			
			status=SbmTaskList[i].check()
			print "    Task check: %d" %status
			
			if status==0:
				SbmTaskList[i].clear_remote_data()
				SbmTaskList[i].download_data()
				SbmTaskList[i].remote_task_delete()
				query="update tasks set task_status='finished',date_of_finishing=CURRENT_DATE where task_id=%d" %SbmTaskList[i].task_id
				db2.db_execute_query(curs, query);
				SbmTaskList[i].email_notify_on_finish("success")
				proc_num = min(num_mult_proc, proc_num + SbmTaskList[i].num_procs)
				#del SbmTaskList[i]
				continue
				
			if status==2:
				NewSbmTaskList.append(SbmTaskList[i])
				continue
				
			#
			# Unknown task status or error during task code execution
			#
			SbmTaskList[i].clear_remote_data()
			try:
				SbmTaskList[i].download_data()
				SbmTaskList[i].remote_task_delete()
			except:
				print "    TASK ERROR!!"
			
			query="update tasks set task_status='refused' where task_id=%d" %SbmTaskList[i].task_id
			db2.db_execute_query(curs, query);
			SbmTaskList[i].email_notify_on_finish("refused")
			proc_num = min(num_mult_proc, proc_num + SbmTaskList[i].num_procs)
			
		#sort by queue_num
		#l1 = len(SbmTaskList)
		NewSbmTaskList.sort(lambda Task1,Task2: cmp(Task1.queue_num,Task2.queue_num))
		#updating queue_num
		for i in range (0, len(NewSbmTaskList)):
			NewSbmTaskList[i].queue_num = i
			query = "update tasks set queue_num=%d where task_id=%d" %\
			(
				i,
				NewSbmTaskList[i].task_id
			)
		
		#sort by procs num
		#print len(NqTaskList)
		NqTaskList.sort(lambda Task1,Task2: cmp(Task2.num_procs,Task1.num_procs))
		#queue and run tasks
		place = len(NewSbmTaskList)
		for i in range (0, len(NqTaskList)):
			if (NqTaskList[i].num_procs <= proc_num):
				proc_num = proc_num - NqTaskList[i].num_procs
				NqTaskList[i].queue_num = place
				place = place + 1
				#
				# running tasks 
				#			
				try:
					NqTaskList[i].upload_data()
				except:
					print "    Upload data for task %d failed!" %NqTaskList[i].task_id
					query="update tasks set task_status='stopped', priority_max=1005 where task_id=%d" %NqTaskList[i].task_id
					db2.db_execute_query(curs, query);
					continue
				status=NqTaskList[i].run()
				if status:
					print "    Run task %d failed!" %NqTaskList[i].task_id
					query="update tasks set task_status='stopped', priority_max=1010 where task_id=%d" %NqTaskList[i].task_id
					db2.db_execute_query(curs, query);
					continue
				query="update tasks set task_status='submitted', running_time=NOW(), queue_num=%d where task_id=%d" %\
				(
					NqTaskList[i].queue_num,
					NqTaskList[i].task_id
				)
				db2.db_execute_query(curs, query);
				if proc_num == 0:
					break			




	#backfill tasks

	query=\
	"""
		select 
			multiprocessors.num_available_procs,
			multiprocessors.multiprocessor_id
		from
			multiprocessors
		where
			multiprocessors.queue_alg = "backfill" 
	"""
	db2.db_execute_query(curs, query);
	resultM=db2.db_fetchall(curs)
	num_multiprocessors=len(resultM)
	#print "%d multiprocessor(s) use(s) algorithm 'backfill':" %num_multiprocessors
	rt = datetime.datetime.today()

	for i in range(0,num_multiprocessors):
		num_mult_proc=resultM[i][0]
		mult_id=resultM[i][1]
		
		SubmittedTask = []
		SubTaskId = []
		TaskList = [] 
		tsklist = {}
		query=\
		"""
			select 
				tasks.user_id,
				tasks.task_id,
				tasks.algorithm,
				tasks.num_procs,
				tasks.duration_in_minutes,
				tasks.task_status,
				multiprocessors.host,
				multiprocessors.path,
				multiprocessors.user_on_it,
				users.email,
				tasks.priority_run,
				tasks.priority_max,
				tasks.running_time
				
			from
				tasks,
				multiprocessors,
				users
			where
				((tasks.task_status="ready") or (tasks.task_status="stopped") or (tasks.task_status="running") or (tasks.task_status="submitted")) and
				(tasks.multiprocessor_id=multiprocessors.multiprocessor_id) and
				(multiprocessors.multiprocessor_id = %d) and 
				(tasks.user_id=users.user_id)
		"""%mult_id
		db2.db_execute_query(curs, query);
		result=db2.db_fetchall(curs)
		num_tasks=len(result)
		
		print "\tnumber of tasks on multiproc with ID %d is %d" %(mult_id, num_tasks)
		
		for i in range(0,num_tasks):

			tsk=task.Task(result[i])
			tsklist[tsk.task_id]=tsk

			#
			#
			# running tasks 
			# Add to Task List
			#
			#
			if tsk.task_status=="ready":
				TaskList.append([tsk.task_id,tsk.priority_max,tsk.duration_in_minutes*60,tsk.num_procs])

			#
			#
			# stopping tasks
			# No changes for stopped tasks
			#
			#
			if tsk.task_status=="stopped":
				try:
					tsk.download_data()
				except:
					print "    Download data failed!"
				tsk.remote_task_delete()
				query="update tasks set task_status='refused' where task_id=%d" %tsk.task_id
				db2.db_execute_query(curs, query);
				tsk.email_notify_on_finish("refused")

			#
			#
			# checking tasks
			# for submitted tasks if finished - no changes, if not finished add to submitted Task list
			#
			#
			if (tsk.task_status=="submitted") or (tsk.task_status=="running"):
				status=tsk.check()
				print "Task check: %d" %status
				
				if status==0:
					tsk.clear_remote_data()
					tsk.download_data()
					tsk.remote_task_delete()
					query="update tasks set task_status='finished',date_of_finishing=CURRENT_DATE where task_id=%d" %tsk.task_id
					db2.db_execute_query(curs, query);
					tsk.email_notify_on_finish("success")
					continue
					
				if status==2:
					SubmittedTask.append([tsk.task_id,tsk.priority_max,tsk.duration_in_minutes*60,tsk.num_procs])
					SubTaskId.append([tsk.task_id])
					query="update tasks set running_time=NOW() where task_id=%d" %tsk.task_id
					db2.db_execute_query(curs, query);
					continue
					
				if (status==4) or (status==3):
					TimeDuration = datetime.timedelta(seconds=tsk.duration_in_minutes*60)
					TimeDuration = TimeDuration - (rt - tsk.running_time)
					if TimeDuration < datetime.timedelta(seconds=0):
						TimeDuration = datetime.timedelta(seconds=tsk.duration_in_minutes*60)
						query="update tasks set running_time=NOW(), task_status='running' where task_id=%d" %tsk.task_id
						db2.db_execute_query(curs, query);
					SubmittedTask.append([tsk.task_id,tsk.priority_max,TimeDuration.seconds,tsk.num_procs])
					SubTaskId.append(tsk.task_id)
					query="update tasks set task_status='running' where task_id=%d" %tsk.task_id
					db2.db_execute_query(curs, query);
					continue

				#
				# Unknown task status or error during task code execution
				#
				tsk.clear_remote_data()
				try:
					tsk.download_data()
					tsk.remote_task_delete()
				except:
					print "   ##Error##"
				print "    !!!!!!!!REFUSED!!!!!!!!!!"
				print status
				query="update tasks set task_status='refused' where task_id=%d" %tsk.task_id
				db2.db_execute_query(curs, query);
				tsk.email_notify_on_finish("refused")

		#run backfill
		[TaskSchedule,WindowFree] = Backfill.MakeSchedule(SubmittedTask,TaskList,num_mult_proc)
		for Tasks in TaskSchedule:
			#update running time
			runt = datetime.timedelta(seconds=Tasks[1])
			tsklist[Tasks[0]].running_time = rt + runt
			query=\
				"""
				update 
					tasks 
				set 
					tasks.running_time='%(run_t)s'
				where 
					tasks.task_id=%(num_t)d 
					
				"""%{'run_t': tsklist[Tasks[0]].running_time, "num_t": tsklist[Tasks[0]].task_id}
			db2.db_execute_query(curs, query);
			if Tasks[1]<global_vars.timeout_server:
				if tsklist[Tasks[0]].task_id not in SubTaskId:
					print "subtasks"
					print SubTaskId
					print "task id"
					print Tasks[0]
					print tsklist[Tasks[0]].task_id
					tsk=tsklist[Tasks[0]]
					try:
						tsk.upload_data()
					except:
						print "    Upload data for task %d failed!" %tsk.task_id
						query="update tasks set task_status='stopped',priority_max=1005 where task_id=%d" %tsk.task_id
						db2.db_execute_query(curs, query);
						continue
					status=tsk.run()
					if status:
						print "    Run task %d failed!" %tsk.task_id
						query="update tasks set task_status='stopped' ,priority_max=1010 where task_id=%d" %tsk.task_id
						db2.db_execute_query(curs, query);
						continue
					query="update tasks set task_status='submitted', running_time=NOW(), priority_max=111 where task_id=%d" %tsk.task_id
					#user pay tokens 
					db2.db_execute_query(curs, query);
					query=\
					"""
						update 
							users,
							tasks 
						set
							users.priority_tokens=users.priority_tokens+tasks.priority_max-tasks.priority_run 
						where 
							tasks.task_id='%d' and 
							users.user_id=tasks.user_id
					"""%(Tasks[0])
					db2.db_execute_query(curs, query);
					
	time.sleep(60)			
print "Server ends successfully!"
print "-------------------------"


os.unlink(global_vars.lock_path)


#
#
# New style of server.py
#
#

def main(argv=None):
    """
    Main function of  Server
    """
    if argv == None:
        argv=sys.argv

    args=server_common.parse_arguments(argv)

    config=server_common.parse_config_file(args.config_file_name)

    
    if args.become_daemon == 'no':
        server_common.become_daemon(config,False)
    else:
        server_common.become_daemon(config,True)
    
    try:
        db=abstract_db(config)
        if db == None:
           sys.stderr.write(_("Database connection failed")
           return 1

    while True:
            



    return 0

    


if __name__ == "__main__":
        sys.exit(main())


