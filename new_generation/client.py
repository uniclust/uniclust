import os
import sys
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
                
                try:
                    fd_test.write(a)
                    fd_test.flush()
                except:
                    raise 

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
        

def fd_of_files_local(filename, flag = "rb", offset=0):
    if filename[0] == "~":
        filename = os.path.expanduser('~') + "/" + os.path.basename(filename)
    else:
        filename = os.path.abspath(filename)

    fd = open(filename, flag)
    fd.seek(offset)

    return fd


def get_size_name(filename):
    if filename[0] == "~":
        filename = os.path.expanduser('~') + "/" + os.path.basename(filename)
    else:
        filename = os.path.abspath(filename)
    
    return os.path.getsize(filename)


def fd_of_files_remote(filename, sftp, flag = "rb", offset=0):
    fd_rem = sftp.file(filename, flag)
    fd_rem.set_pipelined(True)
    fd_rem.seek(offset)

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


def input_file_re(fd_ch):
    vr_param = []

    while s := fd_ch.readline():
        try:
            vr = s.split()
            fd = fd_of_files_local(vr[0])
            vr[1] = int(vr[1])
            vr_param.append(vr)
            fd.close()
        except Exception as ex:
            return None    

    return vr_param


def close_all_files(fd):
    for fd_i in fd:
        fd_i.close()


def new_priority(file_priority, bitmask):
    sum_all = sum(file_priority)
    sum_live = sum([i * j for i, j in zip(file_priority, bitmask)])
    
    for i in range(len(file_priority)):
        if bitmask[i]:
            file_priority[i] += int((file_priority[i] / sum_live) * (sum_all - sum_live))
        else:
            file_priority[i] = 0


def pre_files_upload(ip, username, password, port, file_transport, lock, flag_calc, current_transfer, num_proc, offset):
    sftp = sftp_connect(ip, username, password, port)

    fd_local = [fd_of_files_local(f_name[0], offset=offset[i]) for i, f_name in enumerate(file_transport)]
    fd_remote = [fd_of_files_remote(os.path.basename(f_name[0]), sftp, "wb", offset=offset[i]) for i, f_name in enumerate(file_transport)]
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
            lock.acquire()

            with open(f"cache_up/proc{num_proc}_offset.txt", "w") as fd:
                for i in range(n):
                    print(fd_local[i].tell(), end=' ', file=fd)
            flag_w = 0

            lock.release()

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
    
        with open(f"cache_up/proc{num_proc}_offset.txt", "w") as fd:
            for i in range(n):
                print(fd_local[i].tell(), end=' ', file=fd)


def filling_up(vr_buf_trans, buf_of_file_transport_up, buf_of_proc_up, buf_lock_up, 
               buf_flag_calc_up, buf_current_transfer_up, buf_size_of_file_up, offset):
    buf_of_file_transport_up.append(vr_buf_trans)
    buf_size_of_file_up.append([get_size_name(f_n[0]) for f_n in vr_buf_trans])

    buf_lock_up.append(RLock())
    buf_flag_calc_up.append(Value(c_bool, False))
    buf_current_transfer_up.append(Array("Q", range(len(vr_buf_trans))))

    buf_of_proc_up.append(Process(target=pre_files_upload, \
        args=(ip, username, password, port, vr_buf_trans, buf_lock_up[-1], \
        buf_flag_calc_up[-1], buf_current_transfer_up[-1], len(buf_lock_up) - 1, offset, )))

    buf_of_proc_up[-1].start()


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
            tunnel.start()
        except sshtunnel.BaseSSHTunnelForwarderError:
            print("Unable to connect")
            print("Want to try again?[y/n]")
            pr = input()
            if pr != 'y':
                sys.exit()
        else:
            break

    print("Please wait, setting up")
    #sp_search(ip, username, password, port)

    if not os.path.isdir("cache_up"):
        os.mkdir("cache_up")
    if not os.path.isdir("cache_down"):
        os.mkdir("cache_down")
    
    buf_of_file_transport_up = []        #имена и приоритеты
    buf_of_proc_up = []                  #множество процессов
    buf_lock_up = []                     #множество Rlock для каждого процесса
    buf_flag_calc_up = []                #общая bool для вычисления offset
    buf_current_transfer_up = []         #общая Array для значние offset
    buf_size_of_file_up = []             #множество значений размеров файлов

    buf_of_file_transport_down = []        #имена и приоритеты
    buf_of_proc_down = []                  #множество процессов
    buf_lock_down = []                     #множество Rlock для каждого процесса
    buf_flag_calc_down = []                #общая bool для вычисления offset
    buf_current_transfer_down = []         #общая Array для значние offset
    buf_size_of_file_down = []             #множество значений размеров файлов


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
        "10. Show files on server", 
        "11. Delete a file on the server",
        "press 1,...,11", sep='\n')

        while True:
            try:
                comma = int(input())
                if not (1 <= comma <= 11):
                    raise ValueError
            except Exception:
                print("Command is incorrect, try again")
            else:
                break

        if comma == 1:
            for procc in buf_of_proc_up:
                procc.join()
                procc.terminate()

            for procc in buf_of_proc_down:
                procc.join()
                procc.terminate()

            for f_l in os.listdir("cache_up"):
                os.remove(f"cache_up/{f_l}")

            for f_l in os.listdir("cache_down"):
                os.remove(f"cache_down/{f_l}")
            
            os.rmdir("cache_up")
            os.rmdir("cache_down")
            
            break

        elif comma == 2:
            vr_buf_trans = input_file() 

            with open(f"cache_up/proc{len(buf_lock_up)}_file.txt", "w") as fd:
                for i in range(len(vr_buf_trans)):
                    print(*vr_buf_trans[i], file=fd)

            with open(f"cache_up/proc{len(buf_lock_up)}_offset.txt", "w") as fd:
                for i in range(len(vr_buf_trans)):
                    print(0, end=' ', file=fd)

            buf_offset = [0] * len(vr_buf_trans) 

            filling_up(vr_buf_trans, buf_of_file_transport_up, buf_of_proc_up, buf_lock_up, buf_flag_calc_up, \
                       buf_current_transfer_up, buf_size_of_file_up, buf_offset)

        elif comma == 3:
            for i in range(len(buf_lock_up)):
                buf_lock_up[i].acquire()
                buf_flag_calc_up[i].value = True
                buf_lock_up[i].release()

                buf_lock_up[i].acquire()
                fd = open(f"cache_up/proc{i}_offset.txt", "r")
                loc_offs = list(map(int, fd.readline().split()))
                fd.close()
                buf_lock_up[i].release()

                while True:
                    buf_lock_up[i].acquire()
                    if buf_flag_calc_up[i].value == False:
                        for ofs_i in range(len(buf_current_transfer_up[i])):
                            print(f"{buf_of_file_transport_up[i][ofs_i][0]}: {buf_current_transfer_up[i][ofs_i]} / ", end='')
                            print(f"{buf_size_of_file_up[i][ofs_i]} ", end='')
                            print(f"{100 * buf_current_transfer_up[i][ofs_i]/buf_size_of_file_up[i][ofs_i]:.2f}%")
                        buf_lock_up[i].release()
                        break

                    if not buf_of_proc_up[i].is_alive():
                        for ofs_i in range(len(buf_size_of_file_up[i])):
                            print(f"{buf_of_file_transport_up[i][ofs_i][0]}: {loc_offs[ofs_i]} / ", end='')
                            print(f"{buf_size_of_file_up[i][ofs_i]} ", end='')
                            print(f"{100 * loc_offs[ofs_i]/buf_size_of_file_up[i][ofs_i]:.2f}%")
                        buf_lock_up[i].release()
                        break

                    buf_lock_up[i].release()

        elif comma == 4:
            sftp = sftp_connect(ip, username, password, port)
            print('-'*20)

            for i in sftp.listdir():
                if i[0] != '.':
                    print(i) 

            print('-'*20)
            sftp.close()
        elif comma == 5:
            pass
        elif comma == 6:
            for proc in buf_of_proc_up:
                proc.terminate()

        elif comma == 7:
            for proc in buf_of_proc_down:
                proc.terminate()

        elif comma == 8:
            buf_of_file_transport_up = []        
            buf_of_proc_up = []                  
            buf_lock_up = []                     
            buf_flag_calc_up = []                
            buf_current_transfer_up = []         
            buf_size_of_file_up = []  

            num_proc = int(len(os.listdir("cache_up")) / 2)

            for num in range(num_proc):
                with open(f"cache_up/proc{num}_file.txt", "r") as fd:
                    vr_buf_trans = input_file_re(fd)

                with open(f"cache_up/proc{num}_offset.txt", "r") as fd:
                    buf_offset = list(map(int, fd.readline().split()))
                
                filling_up(vr_buf_trans, buf_of_file_transport_up, buf_of_proc_up, buf_lock_up, \
                           buf_flag_calc_up, buf_current_transfer_up, buf_size_of_file_up, buf_offset)

        elif comma == 9:
            buf_of_file_transport_down = []        
            buf_of_proc_down = []                  
            buf_lock_down = []                     
            buf_flag_calc_down = []                
            buf_current_transfer_down = []         
            buf_size_of_file_down = []   

            num_proc = int(len(os.listdir("cache_down")) / 2)

        elif comma == 10:
            sftp = sftp_connect(ip, username, password, port)
            print('-'*20)

            for i in sftp.listdir():
                if i[0] != '.':
                    print(i) 
            print('-'*20)

            sftp.close()

        elif comma == 11:
            sftp = sftp_connect(ip, username, password, port)
            buf_f_r = list(filter(lambda x: x[0] != '.', sftp.listdir()))

            print('-'*20)

            for f_r in buf_f_r:
                print(f_r)

            print('-'*20)

            while f_r := input():
                sftp.remove(f_r)

            sftp.close()

    tunnel.close()

            

