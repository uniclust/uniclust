import MySQLdb
import global_vars
import task
import os
import datetime
import Backfill

#flag=1

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
#current_datetime= date

# uncomment it for debug
#print current_date
#print expire_date



query="delete from hash where date_label < '%s'" % (expire_date)
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
		tasks.multiprocessor_id=multiprocessors.multiprocessor_id and
		tasks.user_id=users.user_id 
"""

curs.execute(query)
result=curs.fetchall()
num_tasks=len(result)
for i in range(0,num_tasks):
	tsk=task.Task(result[i])
	if (tsk.running_time != None):
		#rt = datetime.datetime.strptime(tsk.running_time, "%y-%m-%d %H:%M:%S")
		rt = datetime.datetime.today() #- tsk.running_time
		runt = datetime.timedelta(seconds=40)
		rt = rt + runt
		query=\
		"""
		update 
			tasks 
		set 
			tasks.running_time='%(run_t)s'
		where 
			tasks.task_id=%(num_t)d 
			
		"""%{'run_t': rt, "num_t": tsk.task_id}
		curs.execute(query)

print num_tasks
	
