import os
import paramiko
import time
import socket
import sshtunnel

def sp_check(*args):
    return 32768

def new_priority(mask, ar_file, key):
    key_pr = ar_file[key][1]
    for i in range(len(mask)):
        if not mask[i]:
            continue
        
        if ar_file[i][1] > key_pr:
            ar_file[i][1] -= 1
    
    return ar_file

ip = "178.140.207.7"
username = "chelik"
password = input()
port = 2011

with sshtunnel.SSHTunnelForwarder(
            ssh_address_or_host = ip,
            ssh_username=username,
            ssh_password=password,
            ssh_port=2011,
            ssh_private_key_password = "",
            remote_bind_address=('127.0.0.1', 22),
    ) as tunnel:
    tunnel.start()
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

    sftp = cl.open_sftp()
    #transport = paramiko.Transport((ip, port))
    #transport.connect(username=username, password=password)

    #sftp = paramiko.SFTPClient.from_transport(transport)
    b_size = sp_check()

    print("Введите файлы и приоритеты в формате (('in.txt', 2), ('in2.txt', 1))")
    
    file_mas = eval(input())
    fd_loc = [open(i, "rb") for i, j in file_mas] 
    fd_rem = [sftp.file(f"mul_test{i}", 'w') for i, j in file_mas]
    for i in range(len(fd_rem)):
        fd_rem[i].set_pipelined(True)
    bit_mask = [True for i in range(len(file_mas))]

    tom = time.time()
    while any(bit_mask):
        for i in range(len(file_mas)):
            if not bit_mask[i]:
                continue
            for j in range(file_mas[i][1]):
                check_size = fd_loc[i].read(b_size)
                fd_rem[i].write(check_size)
                fd_rem[i].flush()
                if not check_size:
                    bit_mask[i] = False
                    fd_loc[i].close()
                    fd_rem[i].close()
                    file_mas = new_priority(bit_mask, file_mas, i)
                    break

    tom = time.time() - tom
    print(tom)

    sftp.close()
    cl.close()


