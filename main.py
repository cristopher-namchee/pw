import os
import re
import sys
import time

import pexpect
import paramiko

from dotenv import load_dotenv

load_dotenv()


def connect_forticlient_vpn(vpn_host, vpn_port, vpn_username, vpn_password):
    command = f"./client/forticlientsslvpn_cli --server {vpn_host}:{vpn_port} --vpnuser {vpn_username}"
    print(command)

    vpn = pexpect.spawn(command)
    vpn.logfile = sys.stdout.buffer

    vpn.expect("Password for VPN:")
    vpn.sendline(vpn_password)

    vpn.expect(
        re.compile(
            r"Would you like to connect to this server\? \(Y/N\)", re.IGNORECASE
        ),
    )
    vpn.sendline("Y")

    vpn.expect("Press Ctrl-C to quit")

    if vpn.isalive():
        print("VPN connected successfully.")
    else:
        print("Failed to establish the VPN connection.")

    return vpn


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

    return "\n".join(table)


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

process = connect_forticlient_vpn(
    os.getenv("VPN_HOST"),
    os.getenv("VPN_PORT"),
    os.getenv("VPN_USER"),
    os.getenv("VPN_PASSWORD"),
)

time.sleep(30)

if process and process.isalive():
    ssh.connect(
        hostname=os.getenv("SSH_HOST"),
        username=os.getenv("SSH_USER"),
        password=os.getenv("SSH_PASSWORD"),
    )

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
