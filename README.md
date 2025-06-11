# OpenRGB System Monitor

Control your RGB lighting based on CPU usage and temperature using OpenRGB.

## Features

- CPU usage → color gradient (green → yellow → red)  
- CPU temperature → dynamic RGB response  
- Lightweight Python script using OpenRGB SDK  

## Requirements

- OpenRGB (running in server mode)
- Python 3.x
- Python packages: `psutil`, `openrgb-python` (see `requirements.txt`)

## Setup

1. **Clone the repo:**

   ```bash
   git clone https://github.com/yourusername/open-rgb-system-monitor.git
   cd open-rgb-system-monitor
   ```

2. **(Optional) Create a virtual environment:**

   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. **Copy the script to a system-wide path:**

   ```bash
   sudo cp cpu_rgb.py /usr/local/bin/cpu_rgb.py
   sudo chmod +x /usr/local/bin/cpu_rgb.py
   ```

4. **Set up the systemd service:**

   Create the file `/etc/systemd/system/openrgb-monitor.service` with the following contents:

   ```ini
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
   ```

5. **Enable and start the service:**

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable openrgb-monitor.service
   sudo systemctl start openrgb-monitor.service
   ```

## Customization

If you're actively editing the source script in your GitHub repo, consider symlinking it instead of copying:

```bash
sudo ln -sf /home/yourusername/Documents/GitHub/open-rgb-system-monitor/cpu_rgb.py /usr/local/bin/cpu_rgb.py
```

Now, any changes to the script will immediately be used by the systemd service.

## License

MIT License