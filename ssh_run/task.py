import global_vars
import os
import exceptions
import smtplib
import email.mime.text

class Task_exception(exceptions.Exception):
	def __init__(self,message):
		self.message=message
	
	def __str__(self):
		return "    Task error:"+message

class Task:
	def __init__(self,db_row):
		self.user_id              = db_row[0]
		self.task_id              = db_row[1]
		self.algorithm            = db_row[2]
		self.num_procs            = db_row[3]
		self.duration_in_minutes  = db_row[4]
		self.task_status          = db_row[5]
		self.host                 = db_row[6]
		self.path                 = db_row[7]
		self.user_on_mult         = db_row[8]
		self.email                = db_row[9]
		self.priority_run         = db_row[10]
		self.priority_max         = db_row[11]
		self.running_time         = db_row[12]
		self.seq_type             = ""
		self.blast_outp_detail_lvl= 0
		self.seq_simil_thrshld    = 0

	def init_blast_task(self,db_row):
		if len(db_row)>0:
			self.seq_type              = db_row[0]
			self.blast_outp_detail_lvl = db_row[1]
			self.seq_simil_thrshld     = db_row[2]
	
	def upload_data(self):
		string="scp %s/%d/%d/sequences.fasta %s@%s:%s/%d.fasta" %\
		(
			global_vars.data_path,
			self.user_id,
			self.task_id,
			self.user_on_mult,
			self.host,
			self.path,
			self.task_id
		)

		print "    Task.upload_data(): %s" %string
		status=os.system(string)
		if status:
			raise Task_exception("scp failed!")
		
	def run(self):
		string="ssh %s@%s \"cd %s; ./scheduler_make_align.sh %d %d %d.fasta %d '%s'\"" %\
		(
			self.user_on_mult,
			self.host,
			self.path,
			self.task_id,
			self.num_procs,
			self.task_id,
			self.duration_in_minutes,
			self.algorithm
		)
		print "    Task.run(): %s" %string
		status=os.system(string)
		return status / 256

	def check(self):
		string="ssh %s@%s \"cd %s; ./scheduler_check_align.sh %d\"" %\
		(
			self.user_on_mult,
			self.host,
			self.path,
			self.task_id
		)
		print string
		status=os.system(string) / 256
		print "    Task.check(): status length = %d" % status
		return status

	def download_data(self):
		string="scp -r %s@%s:%s/%d/\* %s/%d/%d/" %\
		(
			self.user_on_mult,
			self.host,
			self.path,
			self.task_id,
			global_vars.data_path,
			self.user_id,
			self.task_id
		)
		print "    Task.download_data(): %s" %string
		status=os.system(string)
		if status:
			raise Task_exception("scp failed!")
		
		string="chmod -Rf g+wrX %s/%d/%d" %\
		(
			global_vars.data_path,
			self.user_id,
			self.task_id
		)
		status=os.system(string)
		string="chgrp -Rf %s %s/%d/%d" %\
		(
			 global_vars.local_group,
			 global_vars.data_path,
			 self.user_id,
			 self.task_id
		)
		status=os.system(string)

	def clear_remote_data(self):
		string="ssh %s@%s \"cd %s; ./clear_data_align.sh %d\"" %\
		(
			self.user_on_mult,
			self.host,
			self.path,
			self.task_id,
		)
		print "   ",string
		status=os.system(string)
		return status / 256

	def remote_task_delete(self):
		string="ssh %s@%s \"cd %s; ./scheduler_delete_align.sh %d\"" %\
		(
			self.user_on_mult,
			self.host,
			self.path,
			self.task_id,
		)
		print "   ",string
		status=os.system(string)
		return status / 256
	
	def email_notify_on_finish(self,status):
		msg_text=\
		"""
Dear user, your task with ID %d was finished on multiprocessor with status '%s'.
Please, visit page

https://%s/%s/pages/edit_task.php?task_id=%d

		""" %\
		(
			self.task_id,
			status,
			global_vars.site_address,
			global_vars.path_on_site,
			self.task_id
		)

		msg= email.mime.text.MIMEText(msg_text)
		msg['Subject']= "Information about state of the task with number %d on the Aligner website" % (self.task_id)
		from_str="\"Aligner site administration\" <webmaster@%s>" % (global_vars.site_address)
		msg['From']= from_str
		msg['To']=self.email

		server = smtplib.SMTP('localhost')
		server.sendmail("webmaster@%s" %global_vars.site_address,[self.email],msg.as_string())
		server.quit()
	
