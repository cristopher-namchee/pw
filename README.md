# Vowel Reporter Script

A simple Python script to collect metrics from Vowel's server

## Requirements

1. Python 3.10+
2. `openfortivpn`   

## Roadmap

- [x] Working SSH Client
- [x] Working VPN Client
- [ ] Comparison with previous day with Redis
- [ ] Slack Integration

## Installation

1. Clone the repository
2. Create a new virtual environment by running `python -m venv env` and activate it `source env/bin/activate`
3. Install all required dependencies by running `pip install -r requirements.txt`
4. [Install openfortivpn](#installing-openfortivpn)
5. Launch the application by running `sudo python main.py`

## Installing `openfortivpn`

```bash
# For Linux users
sudo apt install openfortivpn

# For Mac users
brew install openfortivpn

# For Windows users
# TBD
```

## FAQ

1. Why do we need `sudo`?

`openfortivpn` needs a [privileged access](https://github.com/adrienverge/openfortivpn?tab=readme-ov-file#running-as-root)

2. I can't connect to the VPN due to certificate issue!

Try to run `sudo openfortivpn <server>:<port> --username <username>` and connect it through `openfortivpn`. If there's an error, copy the `trusted-cert` hash code to your environment.