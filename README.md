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

## Usage
1. Start OpenRGB server:
   ```bash
   openrgb --server