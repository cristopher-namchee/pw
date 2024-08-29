import os

from dotenv import load_dotenv

from commands import SSHCommand
from table import format_sql_table
from ssh import SSHConnection
from vpn import VPNConnection

load_dotenv()

try:
    ssh_client = SSHConnection(
        os.getenv("SSH_HOST"),
        os.getenv("SSH_USER"),
        os.getenv("SSH_PASSWORD"),
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
