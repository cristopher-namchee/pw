import paramiko


class SSHConnection:
    """Class that represents an SSH connection

    Properties:
        host (str): Host the server
        username (str): Authentication username
        password (str = None): Authentication password
    """

    def __init__(self, host, username, password=None):
        self.host = host
        self.username = username
        self.password = password

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.alive = False

    def connect(self):
        """Initiate an SSH connection to a server."""
        self.client.connect(
            hostname=self.host, username=self.username, password=self.password
        )

        self.alive = True

    def disconnect(self):
        """Terminate an SSH session with the server"""
        if self.alive:
            self.client.close()
            self.alive = False
        else:
            raise Exception("SSH is not connected!")

    def exec(self, command: str) -> str:
        """Execute a command on the server

        Args:
            command (str): Command to execute

        Returns:
            str: Command output"""
        if not self.alive:
            raise Exception("SSH is not connected!")

        _, stdout, _ = self.client.exec_command(command)

        return stdout.read().decode()

    def exec_sudo(self, command: str) -> str:
        """Execute a command on the server with `sudo`

        Args:
            command (str): Command to execute

        Returns:
            str: Command output
        """
        if not self.alive:
            raise Exception("SSH is not connected!")

        stdin, stdout, _ = self.client.exec_command(f"sudo -S {command}")

        stdin.write(f"{self.password}\n")
        stdin.flush()

        return stdout.read().decode("utf-8")

    def is_connected(self) -> str:
        """Check SSH connection status

        Returns:
            bool: True if connection is alive, False otherwise
        """
        return self.alive
