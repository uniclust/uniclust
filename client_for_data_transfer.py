import paramiko
import time

def create_sftp_client(ip, port, username, password):
    transport = paramiko.Transport((ip, port))
    transport.connect(username=username, password=password)

    sftp_client = paramiko.SFTPClient.from_transport(transport)

    return sftp_client

def upload_file_to_server(sftp_client, local_file, remote_file):
    sftp_client.put(local_file, remote_file)

def download_file_from_server(sftp_client, remote_file, local_file):
    sftp_client.get(remote_file, local_file)

if __name__ == "__main__":
    commands = ["date", "w", "whoami"]
    ip = "178.140.207.7"
    username = "chelik"
    password = ""
    port = 2011

    sftp_client = create_sftp_client(ip, port, username, password)
    upload_file_to_server(sftp_client, "input.mp4", "remote_file.mp4")
    #########жескаяобработкавидео###############
    time.sleep(100)
    download_file_from_server(sftp_client, "remote_file.mp4", "out.mp4")

    sftp_client.close()
