from argparse import ArgumentParser
import os

from dotenv import load_dotenv

from commands import SSHCommand
from ssh import SSHConnection
from vpn import VPNConnection

load_dotenv()

parser = ArgumentParser()
parser.add_argument("src", type=int)
parser.add_argument("dest", type=int)
parser.add_argument("-c", "--count", type=int)

try:
    args = parser.parse_args()

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

        file_list = ssh_client.exec_sudo(
            SSHCommand.LIST_QUEUE.format(source=args.src)
        ).splitlines()
        file_list.sort()

        print(file_list)
        count_to_move = args.count if args.count else len(file_list) // 2
        if count_to_move > len(file_list):
            raise Exception(
                f"The number of files to be moved '{count_to_move}' cannot exceed the number of files on the queue '{len(file_list)}'"
            )

        files_to_be_moved = " ".join(file_list[-count_to_move:])

        print(
            f"mv {files_to_be_moved} /var/lib/docker/volumes/von-bot-datasaur_document-processor_backup_{args.dest}/_data/queue_downloader/"
        )

        output = ssh_client.exec_sudo(
            f"mv {files_to_be_moved} /var/lib/docker/volumes/von-bot-datasaur_document-processor_backup_{args.dest}/_data/queue_downloader/"
        )
        print(output)

        queue = ssh_client.exec(SSHCommand.QUEUE_COUNT)

        print(queue)
except Exception as e:
    print(e)
finally:
    if ssh_client.is_connected():
        ssh_client.disconnect()

    if vpn_client.is_connected():
        vpn_client.disconnect()
