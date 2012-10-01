#!/usr/bin/python

import MySQLdb
import global_vars
import task
import os
import datetime
import Backfill



db=MySQLdb.connect\
(
	user=global_vars.db_user,
	host=global_vars.db_host,
	db=global_vars.db_name,
	passwd=global_vars.db_passwd
)

curs=db.cursor()


current_date=datetime.date.today()
delta_time=datetime.timedelta(hours=24)
expire_date=current_date-delta_time


# uncomment it for debug
#print current_date
#print expire_date



query=\
"""
  delete from hash where date_label < '%s'
""" % (expire_date)
curs.execute(query)


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
		( tasks.task_status="ready" or tasks.task_status="stopped" or tasks.task_status="submitted" ) and
		tasks.multiprocessor_id=multiprocessors.multiprocessor_id and
		multiprocessors.queue_alg = "simple" and
		tasks.user_id=users.user_id and
		2=1
"""

curs.execute(query)
result=curs.fetchall()
num_tasks=len(result)


for i in range(0,num_tasks):
	print "in simple"
	tsk=task.Task(result[i])
	
	#
	#
	#
	# running tasks 
	#
	#
	#
	if(tsk.task_status=="ready"):
		
		try:
			tsk.upload_data()
		except:
			print "Upload data for task %d failed" % (tsk.task_id)
			query="update tasks set task_status='stopped',priority_max=1005 where task_id=%d" % (tsk.task_id)
			curs.execute(query)
			continue
		status=tsk.run()
		if(status):
			print "Run task %d failed" % (tsk.task_id)
			query="update tasks set task_status='stopped' ,priority_max=1010 where task_id=%d" % (tsk.task_id)
			curs.execute(query)
			continue
		query="update tasks set task_status='submitted' , running_time=NOW() where task_id=%d" % (tsk.task_id)
		curs.execute(query)
	

	#
	#
	#
	# stopping tasks
	#
	#
	#
	#
	if(tsk.task_status=="stopped"):
		try:
			tsk.download_data()
		except:
			print "Download data failed"
		tsk.remote_task_delete()
		query="update tasks set task_status='refused' where task_id=%d" % (tsk.task_id)
		curs.execute(query)
		tsk.email_notify_on_finish("refused")


	
	#
	#
	# checking tasks
	#
	#
	#
	#
	if(tsk.task_status=="submitted"):
		status=tsk.check()
		print "task check: %d" % ( status )
		
		if(status==0):
			tsk.clear_remote_data()
			tsk.download_data()
			tsk.remote_task_delete()
			query="update tasks set task_status='finished',date_of_finishing=CURRENT_DATE where task_id=%d" % (tsk.task_id)
			curs.execute(query)
			tsk.email_notify_on_finish("success")
			continue
			
		if(status==2):
			continue
	
		#
		# Unknown task status or error during task code execution
		#
		tsk.clear_remote_data()
		try:
			tsk.download_data()
			tsk.remote_task_delete()
		except:
			print "##Error##"
		
		query="update tasks set task_status='refused' where task_id=%d" % (tsk.task_id)
		curs.execute(query)
		tsk.email_notify_on_finish("refused")
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
curs.execute(query)
resultM=curs.fetchall()
num_multiprocessors=len(resultM)
print num_multiprocessors
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
			( tasks.task_status="ready" or tasks.task_status="stopped" or tasks.task_status="submitted" ) and
			tasks.multiprocessor_id=multiprocessors.multiprocessor_id and
			multiprocessors.multiprocessor_id = '%d' and 
			tasks.user_id=users.user_id 
	"""%(mult_id)
	curs.execute(query)
	result=curs.fetchall()
	num_tasks=len(result)
	print "num task in %d  is %d"%(mult_id, num_tasks)
	for i in range(0,num_tasks):

		tsk=task.Task(result[i])
		tsklist[tsk.task_id]=tsk
		
		#
		#
		#
		# running tasks 
		# Add to Task List
		#
		#
		if(tsk.task_status=="ready"):
			TaskList.append([tsk.task_id,tsk.priority_max,tsk.duration_in_minutes*60,tsk.num_procs])
				
		

		#
		#
		#
		# stopping tasks
		# No changes for stopped tasks
		#
		#
		#
		if(tsk.task_status=="stopped"):
			try:
				tsk.download_data()
			except:
				print "Download data failed"
			tsk.remote_task_delete()
			query="update tasks set task_status='refused' where task_id=%d" % (tsk.task_id)
			curs.execute(query)
			tsk.email_notify_on_finish("refused")
		#
		#
		# checking tasks
		# for submitted tasks if fifnished - no changes, if not fifnied add to submitted Task list
		#
		#
		#
		if(tsk.task_status=="submitted"):
			status=tsk.check()
			print "task check: %d" % ( status )
			
			if(status==0):
				tsk.clear_remote_data()
				tsk.download_data()
				tsk.remote_task_delete()
				query="update tasks set task_status='finished',date_of_finishing=CURRENT_DATE where task_id=%d" % (tsk.task_id)
				curs.execute(query)
				tsk.email_notify_on_finish("success")
				continue
				
			if(status==2):
				SubmittedTask.append([tsk.task_id,tsk.priority_max,tsk.duration_in_minutes*60,tsk.num_procs])
				SubTaskId.append([tsk.task_id])
				query="update tasks set running_time=NOW() where task_id=%d" % (tsk.task_id)
				curs.execute(query)
				continue
			if(status==4):
				TimeDuration = datetime.timedelta(seconds=duration_in_minutes*60)
				TimeDuration = TimeDuration - (rt - tsk.running_time)
				if (TimeDuration < 0):
					TimeDuration = tsk.duration_in_minutes*60
					query="update tasks set running_time=NOW() where task_id=%d" % (tsk.task_id)
					curs.execute(query)
				SubmittedTask.append([tsk.task_id,tsk.priority_max,TimeDuration,tsk.num_procs])
				SubTaskId.append([tsk.task_id])
				curs.execute(query)
				continue
				
				
		
			#
			# Unknown task status or error during task code execution
			#
			tsk.clear_remote_data()
			try:
				tsk.download_data()
				tsk.remote_task_delete()
			except:
				print "##Error##"
			print "!!!!!!!!REFUSED!!!!!!!!!!"
			print status
			query="update tasks set task_status='refused' where task_id=%d" % (tsk.task_id)
			curs.execute(query)
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
				
			"""%{'run_t': tsklist[Tasks[0]].running_time, "num_t": tsk.task_id}
		curs.execute(query)
		if (Tasks[1]<global_vars.timeout_server):
			if (Tasks[0] not in SubTaskId):
				tsk=tsklist[Tasks[0]]
				try:
					tsk.upload_data()
				except:
					print "Upload data for task %d failed" % (tsk.task_id)
					query="update tasks set task_status='stopped',priority_max=1005 where task_id=%d" % (tsk.task_id)
					curs.execute(query)
					continue
				status=tsk.run()
				if(status):
					print "Run task %d failed" % (tsk.task_id)
					query="update tasks set task_status='stopped' ,priority_max=1010 where task_id=%d" % (tsk.task_id)
					curs.execute(query)
					continue
				query="update tasks set task_status='submitted' ,running_time=NOW(), priority_max=111  where task_id=%d" % (tsk.task_id)
				#user pay tokens 
				curs.execute(query)
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
				curs.execute(query)
print "End OK"
	


