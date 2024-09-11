import os
import time

from dotenv import load_dotenv
from halo import Halo

from commands import SSHCommand
from table import format_sql_table
from ssh import SSHConnection
from vpn import VPNConnection

load_dotenv()

try:
    start = time.time()
    spinner = Halo(text="Initalizing clients...")
    spinner.start()

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

    spinner.text = "Establishing connection to VPN..."
    vpn_client.connect()

    if vpn_client.is_connected():
        spinner.text = "Connecting to VPS via SSH..."

        ssh_client.connect()

        spinner.text = "Fetching data from server..."

        queue = ssh_client.exec(SSHCommand.QUEUE_COUNT)
        disk = ssh_client.exec(SSHCommand.DISK_USAGE)
        document_count = ssh_client.exec(SSHCommand.DOCUMENT_COUNT)

        spinner.text = "Formatting data..."

        print("\n")

        print(queue)
        print(disk)
        print(format_sql_table(document_count))

        spinner.succeed(f"Done in {(time.time() - start):.2f}s")
except Exception as e:
    spinner.fail("Operation failed due to: " + str(e))
finally:
    if ssh_client.is_connected():
        ssh_client.disconnect()

    if vpn_client.is_connected():
        vpn_client.disconnect()
