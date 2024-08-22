import os
import re
import subprocess
import sys

import pexpect
import paramiko

from dotenv import load_dotenv

load_dotenv()


def format_sql_table(data: str) -> str:
    lines = [line.strip() for line in data.strip().splitlines() if line.strip()]

    headers = lines[0].split()

    data = [line.split() for line in lines[1:]]

    max_status_length = max(len(headers[0]), max(len(row[0]) for row in data))
    max_count_length = max(len(headers[1]), max(len(row[1]) for row in data))

    table = []
    table.append(f"+{'-' * (max_status_length + 2)}+{'-' * (max_count_length + 2)}+")
    table.append(
        f"| {headers[0].ljust(max_status_length)} | {headers[1].rjust(max_count_length)} |"
    )
    table.append(f"+{'-' * (max_status_length + 2)}+{'-' * (max_count_length + 2)}+")

    for row in data:
        table.append(
            f"| {row[0].ljust(max_status_length)} | {row[1].rjust(max_count_length)} |"
        )

    table.append(f"+{'-' * (max_status_length + 2)}+{'-' * (max_count_length + 2)}+")

    # Join the table rows with newline characters
    return "\n".join(table)


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
queue = stdout.read().decode()

stdin, stdout, stderr = ssh.exec_command("df -h")
stdout.channel.set_combine_stderr(True)
disk = stdout.read().decode()

stdin, stdout, stderr = ssh.exec_command(
    "docker exec datasaur-mariadb bash -c 'mysql -h$DATABASE_HOST -u$DATABASE_USERNAME -p$DATABASE_PASSWORD -e \"use datasaur; select status, count(*) from llm_vector_store_document WHERE llmVectorStoreId=9 GROUP BY status;\"'",
    get_pty=True,
)
stdout.channel.set_combine_stderr(True)
document_count = stdout.read().decode()

print(queue)
print(disk)
print(format_sql_table(document_count))

if ssh is not None:
    ssh.close()
    del ssh, stdin, stdout, stderr
