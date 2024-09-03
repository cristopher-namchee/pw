# Vowel Reporter Script

A simple Python script to collect metrics from Vowel's server

## Requirements

1. Python 3.10+
2. `openfortivpn`   

## Roadmap

- [x] Working SSH Client
- [x] Working VPN Client
- [x] Add requeue
- [ ] ~~Comparison with previous day with Redis~~
- [ ] ~~Slack Integration~~

## Installation

1. Clone the repository
2. Create a new virtual environment by running `python -m venv env` and activate it `source env/bin/activate`
3. Install all required dependencies by running `pip install -r requirements.txt`
4. Create a new `.env` in the root folder of the project using examples from `.env.example`
5. [Install openfortivpn](#installing-openfortivpn)
6. Execute the [commands](#usage) using `sudo`

## Installing `openfortivpn`

```bash
# For Linux users
sudo apt install openfortivpn

# For Mac users
brew install openfortivpn
```

## Usage

There are 2 functionality that exist in this application:

### Monitoring

Reports queue for each workers, disk usage, and document statuses. Usage:

```bash
sudo python3 monitor.py
```

### Requeue

Move document queue from `<source>` to `<destination>` by `-c <count>` documents. To ensure safety, it will prioritize document queue from the last items

```bash
sudo python3 requeue.py <source> <destination> [-c, --count <count>]
```

> [!NOTE]
> `-c` or `--count` is an optional flag. If `-c` flag is not provided, it will move half of the document queue from source to destination.


## FAQ

1. Why do we need `sudo`?

`openfortivpn` needs a [privileged access](https://github.com/adrienverge/openfortivpn?tab=readme-ov-file#running-as-root)

2. I can't connect to the VPN due to certificate issue!

Try to run `sudo openfortivpn <server>:<port> --username <username>` and connect it through `openfortivpn`. If there's an error, copy the `trusted-cert` hash code to your environment.

3. Can I use this CLI on Windows?

Unfortunately no since `openfortivpn` doesn't have a Windows build. However, you can still run this script inside a WSL.