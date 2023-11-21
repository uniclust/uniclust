import os
import paramiko
import time
import socket
import sshtunnel
from multiprocessing import Process, Event, Array, RLock, Value

def tunnel_connect(ip, username, password, port, remote_bind_address):
    tunnel = sshtunnel.SSHTunnelForwarder(
            ssh_address_or_host = ip,
            ssh_username=username,
            ssh_password=password,
            ssh_port=port,
            remote_bind_address=remote_bind_address
    )
    return tunnel


def ssh_connect(ip, username, password, port):
    cl = paramiko.SSHClient()
    cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cl.connect(
        hostname=ip,
        username=username,
        password=password,
        port=port,
        look_for_keys=False,
        allow_agent=False,
    )
    return cl


def sftp_connect(ssh):
    return ssh.open_sftp()


def fd_of_files_local(filename, flag = "rb"):
    if filename[0] == "~":
        filename = os.path.expanduser('~') + "/" + os.path.basename(filename)
    else:
        filename = os.path.abspath(filename)
    
    return open(filename, flag)


def fd_of_files_remote(filename, sftp, flag = "r"):
    fd_rem = sftp.file(filename, flag)
    fd_rem.set_pipelined(True)

    return fd_rem


def input_file():
    print("Enter the name/path to the files and their priorities")
    vr_param = []

    while s := input():
        try:
            vr = s.split()
            fd = fd_of_file_local(vr[0])
            vr[1] = int(vr[1])
            vr_param.append(vr)
            fd.close()
        except Exception:
            print("Input is incorrect, try again")    

    return vr_param


def close_all_files(fd_local, fd_remote):
    for fd in fd_local:
        fd.close()

    for fd in fd_remote:
        fd.close()


def new_priority(file_priority, bitmask):
    pass


def pre_file_upload(sftp, file_transport, lock, flag_calc, current_transfer):
    fd_local = [fd_of_files_local(f_name[0]) for f_name in file_transport]
    fd_remote = [fd_of_files_remote(os.path.basename(f_name[0]), sftp, "wb") for f_name in file_transport]
    file_priority = [i[1] for i in file_transport]

    files_upload(file_priority, fd_local, fd_remote, lock, flag_calc, current_transfer)
    
    close_all_files(fd_local, fd_remote)
    

def files_upload(file_priority, fd_local, fd_remote, lock, flag_calc, current_transfer):
    live_fd = len(fd_local)
    n = live_fd

    bitmask = [True for i in range(n)]

    while live_fd:
        for i in range(n):
            if not bitmask[i]:
                continue

            for j in range(file_transport[i][1]):
                chunk = fd_local[i].read(MAX_REQUEST_SIZE)
                fd_remote[i].write(chunk)
                fd_remote[i].flush()

                if chunk < MAX_REQUEST_SIZE:
                    bitmask[i] = False

                    new_priority(file_priority, bitmask)
                    break


if __name__ == "__main__":
    print('Hello, please enter your password to get started.')

    ip = "178.140.207.7"
    username = "chelik"
    port = 2011
    password = ''

    while True:
        password = input("Password: ")
        try:
            tunnel = tunnel_connect(ip, username, password, port, (ip, 22)) 
        except Exception:
            print("Password is incorrect, try again")
        else:
            break

    tunnel.start()
    ssh = ssh_connect(ip, username, password, port)
    sftp = sftp_connect(ssh)
    
    buf_of_file_transport = []    #имена и приоритеты
    buf_of_proc = []              #множество процессов
    buf_lock = []                     #множество Rlock для каждого процесса
    buf_flag_calc = []                #общая bool для вычисления offset
    buf_current_transfer = []         #общая Array для значние offset

    while True:
        print("Select a command:",
        "1. Wait for download to complete",
        "2. Upload new files to the server",
        "3. Find out the current upload status to the server",
        "4. Download new files from the server",
        "5. Find out the current status of downloading files from the server",
        "press 1,...,5", sep='\n')

        while True:
            try:
                comma = int(input())
                if not (1 <= comma <= 5):
                    raise ValueError
            except Exception:
                print("Command is incorrect, try again")
            else:
                break

        if comma == 1:
            for procc in buf_of_proc:
                procc.join()
                procc.terminate()

            close_all_files(None)
            break
        elif comma == 2:
            vr_buf_trans = input_file() 

            buf_of_file_transport.append(vr_buf_trans)

            buf_lock.append(multiprocessing.Rlock())
            buf_flag_calc.append(Value("?", False))
            buf_current_transfer.append(Array("Q", range(len(vr_buf_trans))))

            buf_of_proc.append(Process(target=files_upload, \
                args=(vr_buf_trans, buf_lock[-1], buf_flag_calc[-1], buf_current_transfer[-1], )))

            buf_of_proc[-1].start()
        elif comma == 3:
            pass
        elif comma == 4:
            pass
        else:
            pass

    sftp.close()
    ssh.close()
    tunnel.close()

            

