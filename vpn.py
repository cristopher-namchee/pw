import subprocess
import signal
import time

from shutil import which


class VPNConnection:
    """Class that represents a VPN connection

    Properties:
        host (str): Hostname of the gateway
        port (int): Port of the gateway
        username (str): Username that will be used to authenticate to the gateway
        password (str): Password that will be used to authenticate to the gateway
        cert (str): CA fingerprint of the certificate that will be used to authenticate to the gateway
    """

    def __init__(self, host, port, username, password, cert):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.cert = cert

        self.process = None

    def connect(self, wait_time=50):
        """Connect to a VPN gateway using the provided credentials

        Args:
            wait_time (int = 50): Time in seconds to wait for the connection to be established
        """
        if which("openfortivpn") is None:
            raise Exception("openfortivpn is not installed!")

        command = [
            "openfortivpn",
            f"{self.host}:{self.port}",
            "--username",
            self.username,
            "--password",
            self.password,
            "--trusted-cert",
            self.cert,
        ]

        self.process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        time.sleep(wait_time)

    def disconnect(self):
        """Terminate the VPN connection"""
        if self.process:
            self.process.send_signal(signal.SIGINT)
            self.process.wait()

            self.process = None
        else:
            raise Exception("VPN is not connected!")

    def is_connected(self):
        return self.process is not None
