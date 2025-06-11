# OpenRGB System Monitor

Control your RGB lighting based on CPU usage/temperature using OpenRGB.

## Features
- CPU usage → color gradient (green → yellow → red)
- CPU temperature → dynamic RGB response
- Easy Python script with OpenRGB SDK

## Requirements
- OpenRGB (running in server mode)
- Python 3.x
- `psutil`, `openrgb-python` (see `requirements.txt`)

# Setup

1. Clone the repo:

   ```bash
   git clone https://github.com/yourusername/open-rgb-system-monitor.git
   cd open-rgb-system-monitor

2. (Optional) Create a virtual environment:

    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt

3. Copy the script to a system-wide path:

    sudo cp cpu_rgb.py /usr/local/bin/cpu_rgb.py
    sudo chmod +x /usr/local/bin/cpu_rgb.py

4. Set up the systemd service:

    # /etc/systemd/system/openrgb-monitor.service
    [Unit]
    Description=OpenRGB CPU Monitor
    After=openrgb.service
    Requires=openrgb.service

    [Service]
    ExecStart=/usr/bin/env python3 /usr/local/bin/cpu_rgb.py
    User=yourusername
    Environment=PYTHONUNBUFFERED=1
    Environment=DISPLAY=:0
    Environment=XAUTHORITY=/home/yourusername/.Xauthority
    Restart=always
    RestartSec=3

    [Install]
    WantedBy=multi-user.target

5. Enable and start the service

    sudo systemctl daemon-reload
    sudo systemctl enable openrgb-monitor.service
    sudo systemctl start openrgb-monitor.service

## Customisation

If you're actively editing the source script in your GitHub repo , consider symlinking it:

    sudo ln -sf /home/yourusername/Documents/GitHub/open-rgb-system-monitor/cpu_rgb.py /usr/local/bin/cpu_rgb.py

Now, updates to the original file will reflect in the systemd service.

## License

MIT License


Let me know if you'd like it tailored further — e.g. with config options or screenshot badges.