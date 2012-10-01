#!/usr/bin/python
def CloseWindowInInterval(CloseWindowFreeStart,CloseWindowFreeEnd,NumProcClosed,WindowFreeToClose ):
#procedure close all interval of define Number of processor(and only in it) and define time interval
    try:
        i2 = -1 
	#go throw all interval since 0
	while i2 < len(WindowFreeToClose[NumProcClosed]):
	    i2 = i2+1	
	    #print 'i2 ',i2
	    #it maybe out of range because we ins and del some elem
	    if i2 == len(WindowFreeToClose[NumProcClosed]):
	        break
	    #if window start after interval no action could be made
	    if WindowFreeToClose[NumProcClosed][i2][0] > CloseWindowFreeEnd:
	        continue
	    #if window ends before interval start no action could be made
	    if WindowFreeToClose[NumProcClosed][i2][1] < CloseWindowFreeStart and WindowFreeToClose[NumProcClosed][i2][1] != -1:
	        continue
	    #if window start in interval (...[....
	    if WindowFreeToClose[NumProcClosed][i2][0] >= CloseWindowFreeStart:  
		# if window end  out of interval (...[...)...] we increase interval start
	        if WindowFreeToClose[NumProcClosed][i2][1] > CloseWindowFreeEnd or WindowFreeToClose[NumProcClosed][i2][1] == -1:
                    print ' start big from ', NumProcClosed,'interval',WindowFreeToClose[NumProcClosed][i2][0],' and ',WindowFreeToClose[NumProcClosed][i2][1], ' and window  ', CloseWindowFreeStart, CloseWindowFreeEnd
		    WindowFreeToClose[NumProcClosed][i2][0] = CloseWindowFreeEnd
		    continue
                else: #window in interval (....[...]...) we delete interval
		    #print ' del from ', NumProcClosed,'interval',WindowFreeToClose[NumProcClosed][i2][0],' and ',WindowFreeToClose[NumProcClosed][i2][1], ' and window  ', CloseWindowFreeStart, CloseWindowFreeEnd
		    del WindowFreeToClose[NumProcClosed][i2]
		    i2 = i2 - 1
		    continue
            else: #window start before interval [...(...
		# if window end after interval or window have no end  [...(....)..]we insert new interval and increase interval start to have result  [..](  )[..]
                if (WindowFreeToClose[NumProcClosed][i2][1]>CloseWindowFreeEnd) or (WindowFreeToClose[NumProcClosed][i2][1] == -1):
		    print ' ins in',NumProcClosed,'interval', WindowFreeToClose[NumProcClosed][i2][0],' and ',CloseWindowFreeStart,' and interval change to ',  CloseWindowFreeEnd, ' and  ',  WindowFreeToClose[NumProcClosed][i2][1]
		    #WindowFreeToClose[NumProcClosed][i2][0] = CloseWindowFreeEnd
		    WindowFreeToClose[NumProcClosed].insert(i2, [WindowFreeToClose[NumProcClosed][i2][0],CloseWindowFreeStart])
		    WindowFreeToClose[NumProcClosed][i2+1][0] = CloseWindowFreeEnd
                    i2=i2+1
	            continue
	        else:  #Window end before interval [...(...]...)  We reduse interval end
		    #print ' End small from ', NumProcClosed,'interval',WindowFreeToClose[NumProcClosed][i2][0],' and ',WindowFreeToClose[NumProcClosed][i2][1], ' and window  ', CloseWindowFreeStart, CloseWindowFreeEnd
	            WindowFreeToClose[NumProcClosed][i2][1] = CloseWindowFreeStart
                    continue
	    #error section
	   # print ' error ', NumProcClosed,'interval',WindowFreeToClose[NumProcClosed][i2][0],' and ',WindowFreeToClose[NumProcClosed][i2][1], ' and window  ', CloseWindowFreeStart, CloseWindowFreeEnd
    except:
		print '  FAIL  iteratot',i2,' NumProc  ',NumProcClosed,'  lenght windowfreee   ', len(WindowFreeToClose[NumProcClosed]), ' xrange   ', xrange(0,len(WindowFreeToClose[NumProcClosed]))
    #print ' WindowFree after closed interval', WindowFreeToClose
    return WindowFreeToClose
def AddTask(MaxTimeEvalution,NumProcRequire,NumProc,WindowFree):
#the procedure closed appropriate free processors interval, and return task Start and End time and new free processors intervals
    TaskStart=0
    TaskEnd=0
    #search for avialible time to run task, we search only in NumProcequire free process window
    for i in xrange(0,len(WindowFree[NumProcRequire])-1):
        if  WindowFree[NumProcRequire][i][1] - WindowFree[NumProcRequire][i][0] >= MaxTimeEvalution:
            TaskStart=WindowFree[NumProcRequire][i][0] 
            TaskEnd=WindowFree[NumProcRequire][i][0]+MaxTimeEvalution  
	    
	    break
    if TaskEnd == 0:
        TaskStart=WindowFree[NumProcRequire][len(WindowFree[NumProcRequire])-1][0]
	TaskEnd=WindowFree[NumProcRequire][len(WindowFree[NumProcRequire])-1][0]+MaxTimeEvalution 
      #for all proccessors if is no interval for N processors we don't have N - NumProcRequire processors in programm run time, and must closed this interval
    for N in xrange(NumProcRequire+1,NumProc+1):
	#print ' N', N,'intervals',WindowFree[N] 
	#we see to the start of first interval
	if WindowFree[N][0][0] > TaskStart:
            CloseWindowInIntervalStart =  TaskStart
	    CloseWindowInIntervalEnd =  min(TaskEnd,WindowFree[N][0][0])
	    WindowFree = CloseWindowInInterval(CloseWindowInIntervalStart,CloseWindowInIntervalEnd,N-NumProcRequire,WindowFree)
        # for the each interval we see if task running time is before the start of next interval
        for i1 in xrange(0,len(WindowFree[N])-1):
	  #we ins and del some interval in window free therefore we mut check index out of range	
	    if i1 == len(WindowFree[N])-1:
                break
          #if next interval start before TaskStart no action
            if  WindowFree[N][i1+1][0] < TaskStart :
	        continue       
	#if this interval end after Task end no action
            if WindowFree[N][i1][1] > TaskEnd: 
	        continue               
	#in other case we choose intersection of interrapton in interval and task running tie
	    CloseWindowInIntervalStart =  max(TaskStart,WindowFree[N][i1][1])
	    CloseWindowInIntervalEnd =  min(TaskEnd,WindowFree[N][i1+1][0])
	  #  print 'Advanced Closed in N', N
            WindowFree = CloseWindowInInterval(CloseWindowInIntervalStart,CloseWindowInIntervalEnd,N-NumProcRequire,WindowFree)
    #we don't have NumProc-NumProcRequire+1 processor in task running time - close appropriate intervals
    for N2 in xrange(NumProc-NumProcRequire+1,NumProc+1):
        WindowFree = CloseWindowInInterval(TaskStart,TaskEnd,N2,WindowFree)
    #print WindowFree
    return([TaskStart,TaskEnd,WindowFree])
def MakeSchedule(SubmittedTask,TaskList,NumProc):
#procesdure generate first fulltime free intervals and add task on the assumption of it's priority
    WindowFree=[]
    TaskSchedule=[]
    #generate first interval - all processors free full time
    for i in xrange(0,NumProc+1):
    #    print i, ' processors  '
	WindowFree.append([])
	WindowFree[i].append([0,-1])
	#print WindowFree[i], ' Window Free '
    #Add submitted tasks no difference with common task 
    for SubTask in SubmittedTask:
	#print ' SubTask Number ', SubTask[0], 'processor need  ',SubTask[3]
        [TaskStart,TaskEnd,WindowFree] = AddTask(SubTask[2],SubTask[3],NumProc,WindowFree)
	TaskSchedule.append([SubTask[0],TaskStart,TaskEnd,SubTask[3]])        
    #sorting tasks by priority from biggest to smaller
    TaskList.sort(lambda Task1,Task2: cmp(Task2[1],Task1[1]))
    #add tasks
    for Task in TaskList:
       # print ' Task Number ', Task[0],' processor need  ', Task[3] 
	try:
	    df = WindowFree[Task[3]][0][0]
            [TaskStart,TaskEnd,WindowFree] = AddTask(Task[2],Task[3],NumProc,WindowFree)
	except:
	     print ' Crash Task Number   ', Task[0], ' WindowFree ', WindowFree[Task[3]] 
	TaskSchedule.append([Task[0],TaskStart,TaskEnd,Task[3]])
    return [TaskSchedule,WindowFree]

