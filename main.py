import os
import re
import subprocess
import sys

import pexpect
import paramiko

from dotenv import load_dotenv

load_dotenv()

# vpn_host = os.getenv("VPN_HOST")
# vpn_port = os.getenv("VPN_PORT")
# vpn_user = os.getenv("VPN_USER")
# vpn_password = os.getenv("VPN_PASSWORD")

# child = pexpect.spawn(
#     f"./client/forticlientsslvpn_cli --server {vpn_host}:{vpn_port} --vpnuser {vpn_user}"
# )

# child.expect("Password for VPN:")
# child.sendline(vpn_password)

# child.expect(
#     re.compile(r"Would you like to connect to this server\? \(Y/N\)", re.IGNORECASE)
# )
# child.sendline("Y")

# child.expect("Press Ctrl-C to quit")

# child = pexpect.spawn(f"ssh {os.getenv('SSH_USER')}@{os.getenv('SSH_HOST')}")
# child.logfile = sys.stdout.buffer

# child.expect(f"{os.getenv('SSH_USER')}@{os.getenv('SSH_HOST')}'s password:")
# child.sendline(os.getenv("SSH_PASSWORD"))

# child.interact()

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
paramiko.util.log_to_file("ssh.log")

print("paramiko created")

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(
    hostname=os.getenv("SSH_HOST"),
    username=os.getenv("SSH_USER"),
    password=os.getenv("SSH_PASSWORD"),
)

print("SSH connected!")

stdin, stdout, stderr = ssh.exec_command("~/dpo_logs/count_queue.sh")
stdout.channel.set_combine_stderr(True)
queue = stdout.readlines()

stdin, stdout, stderr = ssh.exec_command("df -h")
stdout.channel.set_combine_stderr(True)
disk = stdout.read().decode()

ssh.exec_command("docker exec -it datasaur-mariadb bash")
ssh.exec_command("mysql -h$DATABASE_HOST -u$DATABASE_USERNAME -p$DATABASE_PASSWORD")
ssh.exec_command("use datasaur;")

stdin, stdout, stderr = ssh.exec_command(
    "select status, count(*) from llm_vector_store_document WHERE llmVectorStoreId=9 GROUP BY status;"
)
stdout.channel.set_combine_stderr(True)
document_count = stdout.read().decode()

print(queue)
print(disk)
print(document_count)

if ssh is not None:
    ssh.close()
    del ssh, stdin, stdout, stderr
