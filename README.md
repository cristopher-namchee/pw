# Vowel Reporter Script

## Requirements

1. FortiClient SSL VPN CLI

## Installation

1. Clone the repository
2. Create a new virtual environment by running `python -m venv env` and activate it `source env/bin/activate`
3. Install all required dependencies by running `pip install -r requirements.txt`
4. [Install FortiClient](#installing-forticlient)
5. Launch the application by running `python main.py`

## Installing FortiClient

1. Download the latest FortiClient SSL VPN CLI

```bash
wget http://cdn.software-mirrors.com/forticlientsslvpn_linux_4.4.2328.tar.gz
```

2. Extract the content of package

```bash
tar -xzvf forticlientsslvpn_linux_4.4.2328.tar.gz
```

3. (Optional) Install `ppp` to build the SSL Client

```bash
sudo apt-get install ppp
```

4. Go to the installer setup directory

```bash
cd ./forticlientsslvpn/64bit/helper
```

5. Run the setup file 

```bash
sudo ./setup.linux.sh
```

> [!NOTE]
> You will be asked about licensing here. Just press `Yes` without reading like you usually do :)

> [!NOTE]
> You can test the client installation using `./client/forticlientsslvpn_cli --server serveraddress:port --vpnuser username`
