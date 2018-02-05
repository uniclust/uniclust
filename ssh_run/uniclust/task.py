from uniclust import filecache_globalvars as fGlobal
from uniclust.ssh2 import *
class Task(object):
    """Obj of tasks class"""

    debug = True;

    def __init__(self,  task_obj, db_obj ):

        self.task_id =                  task_obj[0];
        self.user_id =                  task_obj[1];
        self.multiprocessor_id =        task_obj[2];
        self.duration_in_minutes =      task_obj[3];
        self.num_procs =                task_obj[4];
        self.num_nodes =                task_obj[5];
        self.application_id =           task_obj[6];
        self.arguments =                task_obj[7];
        self.date_of_creation =         task_obj[8];
        self.date_of_finishing =        task_obj[9];
        self.comments =                 task_obj[10];
        self.running_time =             task_obj[11];
        self.task_status =              task_obj[12];
        self.priority =                 task_obj[13];
        self.tokens_used =              task_obj[14];
        self.tokenes_allowed =          task_obj[15];
        
        self.ssh = ssh_connections(connect=False);

        self.multi = db_obj.get_info_multiproc(self.multiprocessor_id);
        self.app = db_obj.get_algoritm(self.application_id);

        self.ssh.connect(self.multi.host, self.multi.user_on_mult, fGlobal.key_path);

    def __del__(self):
        self.ssh.close();

    def upload_data(self, db_obj):
        if self.app is not False:
            return ; # test

        string="scp %s/%d/%d/sequences.fasta %s@%s:%s/%d.fasta" %\
			(
				fGlobal.data_path,
				self.user_id,
				self.task_id,
				self.multi.user_on_mult,
				self.multi.host,
				self.multi.path,
				self.task_id
			)

        if self.debug:
            print ("    Task.upload_data(): %s" %string)

        status = self.ssh.exec(string);

        if status:
            raise Exception("Error with scp string");

    def run(self):
        string="ssh %s@%s \"cd %s; ./scheduler_make_align.sh %d %d %d.fasta %d '%s'\"" %\
		(
			self.multi.user_on_mult,
			self.multi.host,
			self.multi.path,
			self.task_id,
			self.num_procs,
			self.task_id,
			self.duration_in_minutes,
			self.app.name if self.app is not False else ''
		)
        
        if self.debug:
            print ("    Task.run(): %s" %string)

        status = self.ssh.exec(string);

        if status:
            raise Exception("Error with scp string");

    def check(self):
        string="ssh %s@%s \"cd %s; ./scheduler_check_align.sh %d '%s'\"" %\
		(
			self.multi.user_on_mult,
			self.multi.host,
			self.multi.path,
			self.task_id,
			self.app.name if self.app is not False else ''
		)
        
        if self.debug:
            print (string)
            
        status = self.ssh.exec(string);
        print ("    Task.check(): status length = %d" % status)
        return status
    def download_data(self):
        ...

    def remote_task_delete(self):
        ...
    
    def email_notify_on_finish(self, notify_status = 'refused'):
        ...



