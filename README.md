# Unicorn Pi 2: The clockening

## Installation

- `sudo apt install libwebpdemux2 libopenjp2-7 libwebpmux3 liblcms2-2` (Pillow dependencies)
- `sudo apt install python3-pip python3-dev python3-spidev` (Numpy dependencies)
- `python3 -m venv .venv` (Create a virtual environment)
- `source .venv/bin/activate` (Activate the virtual environment)
- `pip install -r requirements.txt` (Install Python dependencies)

### Systemd Unit

```
[Unit]
Description=Unicorn Main Script Service
After=network.target

[Service]
ExecStart=/home/pi/src/unicorn/.venv/bin/python /home/pi/src/unicorn/main.py
WorkingDirectory=/home/pi/src/unicorn/
StandardOutput=journal
StandardError=journal
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Write to `/etc/systemd/system/unicorn.service` and enable it with:

```bash
sudo systemctl enable unicorn.service
sudo systemctl start unicorn.service
```
