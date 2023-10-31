import paramiko
import time
import socket
import command_for_data_transfer

def send_show_command(
    com_num,
    ip,
    username,
    password,
    command,
    port,
    max_bytes=60000,
    short_pause=1,
    long_pause=5,
):
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
    with cl.invoke_shell() as ssh:
        sftp_client = create_sftp_client(ip, port, username, password)

        while s:= input():
            if com_num == 0:
                upload_file_to_server(sftp_client, s, s)
            elif com_num == 1:
                upload_file_to_server(sftp_client, s, f"{s}_1")
            else:
                download_file_from_server(sftp_client, s, s)
            '''result = {}
            for command in commands:
                ssh.send(f"{command}\n")
                ssh.settimeout(5)

                output = ""
                while True:
                    try:
                        page = ssh.recv(max_bytes).decode("utf-8")
                        output += page
                        time.sleep(0.5)
                    except socket.timeout:
                        break
                result[command] = output

            return result'''

            sftp_client.close()


if __name__ == "__main__":
    commands = [
        "ch_upload", #загрузить 
        "ch_replace", #заменить
        "ch_unload" #сгрузить на компьютер 
    ]
    ip = "178.140.207.7"
    username = "chelik"
    password = ""
    port = 2011
    while True:
        com_num = int(input()) # 0 1 2
        print(send_show_command(com_num, ip, username, password, commands, port))
