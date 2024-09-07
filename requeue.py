from argparse import ArgumentParser
import os
import time

from dotenv import load_dotenv
from halo import Halo

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

        spinner.text = "Fetching file list from server..."

        src_folder = f"/var/lib/docker/volumes/von-bot-datasaur_document-processor_backup_{args.src}/_data/queue_downloader"
        dest_folder = f"/var/lib/docker/volumes/von-bot-datasaur_document-processor_backup_{args.dest}/_data/queue_downloader/"

        file_list = ssh_client.exec_sudo(
            SSHCommand.LIST_QUEUE.format(source=src_folder)
        ).splitlines()
        file_list.sort()

        count_to_move = args.count if args.count else len(file_list) // 2
        if count_to_move > len(file_list):
            raise Exception(
                f"The number of files to be moved '{count_to_move}' cannot exceed the number of files on the queue '{len(file_list)}'"
            )

        files_to_be_moved = file_list[-count_to_move:]
        files_to_be_moved = map(lambda file: src_folder + "/" + file, files_to_be_moved)
        files_to_be_moved = " ".join(files_to_be_moved)

        spinner.text = "Moving files to destination folder..."

        output = ssh_client.exec_sudo(
            SSHCommand.MOVE_QUEUE.format(dest=dest_folder, files=files_to_be_moved)
        )

        spinner.text = "Calculating current queue..."

        queue = ssh_client.exec(SSHCommand.QUEUE_COUNT)

        print("\n")
        print(queue)

        spinner.succeed(f"Done in {(time.time() - start):.2f}s")
except Exception as e:
    spinner.fail("Operation failed due to: " + str(e))
finally:
    if ssh_client.is_connected():
        ssh_client.disconnect()

    if vpn_client.is_connected():
        vpn_client.disconnect()
