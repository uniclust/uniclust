import os
import paramiko
import time
import socket
import sshtunnel
from multiprocessing import Process, Event, Array, RLock, Value
from ctypes import c_bool

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


def sftp_connect(ip, username, password, port):
    transport = paramiko.Transport((ip, port))
    transport.connect(username=username, password=password)

    sftp = paramiko.SFTPClient.from_transport(transport)

    return sftp


def sp_search(ip, username, password, port):
    sftp = sftp_connect(ip, username, password, port)
    fd_test = sftp.file("cache.out", "wb")
    vr = 1
    sp_prev = [0, 256]
    flag = False
    paramiko.sftp_file.SFTPFile.MAX_REQUEST_SIZE = 256

    while True:
        try:
            paramiko.sftp_file.SFTPFile.MAX_REQUEST_SIZE += vr
            a = b'\x00' * (paramiko.sftp_file.SFTPFile.MAX_REQUEST_SIZE - 128)

            cur_sp = []

            for i in range(5):
                t1 = time.time()

                fd_test.write(a)
                fd_test.flush()

                t2 = time.time()
                cur_sp.append(len(a) / (t2 - t1))
                
                fd_test.seek(0)
            
            cur_sp = sum(sorted(cur_sp)[2:]) / 3
            if cur_sp < sp_prev[0] * 0.9:
                raise ValueError

            if cur_sp > sp_prev[0]:
                sp_prev = [cur_sp, paramiko.sftp_file.SFTPFile.MAX_REQUEST_SIZE]
            vr *= 2
            flag = True
        except Exception:
            try:
                fd_test.close()
                sftp.close()
            except:
                pass
            sftp = sftp_connect(ip, username, password, port)
            fd_test = sftp.file("cache.out", "wb")

            paramiko.sftp_file.SFTPFile.MAX_REQUEST_SIZE -= vr
            vr = 1
            if not flag:
                break
            flag = False

    paramiko.sftp_file.SFTPFile.MAX_REQUEST_SIZE = sp_prev[1]
        

def fd_of_files_local(filename, flag = "rb"):
    if filename[0] == "~":
        filename = os.path.expanduser('~') + "/" + os.path.basename(filename)
    else:
        filename = os.path.abspath(filename)

    return open(filename, flag)


def get_size_name(filename):
    if filename[0] == "~":
        filename = os.path.expanduser('~') + "/" + os.path.basename(filename)
    else:
        filename = os.path.abspath(filename)
    
    return os.path.getsize(filename)


def fd_of_files_remote(filename, sftp, flag = "rb"):
    fd_rem = sftp.file(filename, flag)
    fd_rem.set_pipelined(True)

    return fd_rem


def input_file():
    print("Enter the name/path to the files and their priorities")
    vr_param = []

    while s := input():
        try:
            vr = s.split()
            fd = fd_of_files_local(vr[0])
            vr[1] = int(vr[1])
            vr_param.append(vr)
            fd.close()
        except Exception as ex:
            print("Input is incorrect, try again")    

    return vr_param


def close_all_files(fd):
    for fd_i in fd:
        fd_i.close()


def new_priority(file_priority, bitmask):
    pass


def pre_files_upload(ip, username, password, port, file_transport, lock, flag_calc, current_transfer, num_proc):
    sftp = sftp_connect(ip, username, password, port)

    fd_local = [fd_of_files_local(f_name[0]) for f_name in file_transport]
    fd_remote = [fd_of_files_remote(os.path.basename(f_name[0]), sftp, "wb") for f_name in file_transport]
    file_priority = [i[1] for i in file_transport]

    files_upload(file_priority, fd_local, fd_remote, lock, flag_calc, current_transfer, num_proc)
    
    close_all_files(fd_local)
    close_all_files(fd_remote)

    sftp.close()
    

def files_upload(file_priority, fd_local, fd_remote, lock, flag_calc, current_transfer, num_proc):
    live_fd = len(fd_local)
    n = live_fd

    bitmask = [True for i in range(n)]
    flag_w = 0

    while live_fd:
        lock.acquire()

        if flag_calc.value:
            for i in range(n):
                current_transfer[i] = fd_local[i].tell()
        flag_calc.value = False

        lock.release()

        if flag_w == 10:
            with open(f"cache_up/proc{num_proc}_offset.txt", "w") as fd:
                for i in range(n):
                    print(fd_local[i].tell(), end=' ', file=fd)
            flag_w = 0

        for i in range(n):
            if not bitmask[i]:
                continue

            for j in range(file_priority[i]):
                chunk = fd_local[i].read(paramiko.sftp_file.SFTPFile.MAX_REQUEST_SIZE - 128)
                fd_remote[i].write(chunk)
                fd_remote[i].flush()

                if not chunk:
                    bitmask[i] = False
                    live_fd -= 1

                    new_priority(file_priority, bitmask)
                    break
        flag_w += 1


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

    os.mkdir("cache_up")
    os.mkdir("cache_down")

    print("Please wait, setting up")
    sp_search(ip, username, password, port)
    
    buf_of_file_transport = []        #имена и приоритеты
    buf_of_proc = []                  #множество процессов
    buf_lock = []                     #множество Rlock для каждого процесса
    buf_flag_calc = []                #общая bool для вычисления offset
    buf_current_transfer = []         #общая Array для значние offset
    buf_size_of_file = []             #множество значений размеров файлов

    while True:
        print("Select a command:",
        "1. Wait for upload/download to complete",
        "2. Upload new files to the server",
        "3. Find out the current upload status to the server",
        "4. Download new files from the server",
        "5. Find out the current status of downloading files from the server",
        "6. Stop upload",
        "7. Stop download", 
        "8. Restart upload",
        "9. Restart download",
        "press 1,...,9", sep='\n')

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

            os.rmdir("cache_up")
            os.rmdir("cache_down")
            break
        elif comma == 2:
            vr_buf_trans = input_file() 

            buf_of_file_transport.append(vr_buf_trans)
            buf_size_of_file.append([get_size_name(f_n[0]) for f_n in vr_buf_trans])

            buf_lock.append(RLock())
            buf_flag_calc.append(Value(c_bool, False))
            buf_current_transfer.append(Array("Q", range(len(vr_buf_trans))))

            buf_of_proc.append(Process(target=pre_files_upload, \
                args=(ip, username, password, port, vr_buf_trans, buf_lock[-1], \
                buf_flag_calc[-1], buf_current_transfer[-1], len(buf_lock))))

            buf_of_proc[-1].start()
        elif comma == 3:
            for i in range(len(buf_lock)):
                buf_lock[i].acquire()
                buf_flag_calc[i].value = True
                buf_lock[i].release()

                while True:
                    buf_lock[i].acquire()
                    if buf_flag_calc[i].value == False:
                        for ofs_i in range(len(buf_current_transfer[i])):
                            print(f"{buf_of_file_transport[i][ofs_i][0]}: {buf_current_transfer[i][ofs_i]} / ", end='')
                            print(f"{buf_size_of_file[i][ofs_i]} ", end='')
                            print(f"{buf_current_transfer[i][ofs_i]/buf_size_of_file[i][ofs_i]:.2f}%")
                        buf_lock[i].release()
                        break

                    if not buf_of_proc[i].is_alive():
                        for ofs_i in range(len(buf_size_of_file[i])):
                            print(f"{buf_of_file_transport[i][ofs_i][0]}: {buf_size_of_file[i][ofs_i]} / ", end='')
                            print(f"{buf_size_of_file[i][ofs_i]} ", end='')
                            print(f"100.00%")
                        buf_lock[i].release()
                        break

                    buf_lock[i].release()


        elif comma == 4:
            pass
        else:
            pass

    tunnel.close()

            

