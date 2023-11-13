import os
import paramiko
import time
import socket
import sshtunnel

def sp_check(*args):
    return 1000 

def new_priority(*args):
    pass

ip = "178.140.207.7"
username = "chelik"
password = ""
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
    b_size = sp_check()
    
    file_mas = eval(input())
    fd_loc = [open(i, "rb") for i, j in file_mas] 
    fd_rem = [sftp.file(f"mul_test{i}", 'w') for i, j in file_mas]
    bit_mask = [True for i in range(len(file_mas))]

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
                    #new_priority()
                    break

    sftp.close()
    cl.close()
