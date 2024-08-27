import os

from dotenv import load_dotenv

from commands import SSHCommand
from ssh import SSHConnection
from vpn import VPNConnection

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

    return "\n".join(table)


try:
    ssh_client = SSHConnection(
        os.getenv("SSH_HOST"),
        os.getenv("SSH_USER"),
        os.getenv("SSH_PASSWORD"),
        os.getenv("SSH_PORT"),
    )

    vpn_client = VPNConnection(
        os.getenv("VPN_HOST"),
        os.getenv("VPN_PORT"),
        os.getenv("VPN_USER"),
        os.getenv("VPN_PASSWORD"),
        os.getenv("VPN_CERT"),
    )
    vpn_client.connect()

    if vpn_client.is_connected():
        print("Connecting to server via SSH...")

        ssh_client.connect()
        queue = ssh_client.exec(SSHCommand.QUEUE_COUNT)
        disk = ssh_client.exec(SSHCommand.DISK_USAGE)
        document_count = ssh_client.exec(SSHCommand.DOCUMENT_COUNT)

        print(queue)
        print(disk)
        print(format_sql_table(document_count))
except Exception as e:
    print(e)
finally:
    if ssh_client.is_connected():
        ssh_client.disconnect()

    if vpn_client.is_connected():
        vpn_client.disconnect()
