#!/usr/bin/env python3
import argparse
import time
import psutil
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor

def get_cpu_temp():
    """Read CPU temperature from thermal zones."""
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        return int(f.read().strip()) / 1000

def get_color_from_value(value, max_value=100):
    """Map a value (usage/temp) to a color gradient."""
    ratio = min(value / max_value, 1.0)
    if ratio < 0.5:
        return RGBColor(int(255 * ratio * 2), 255, 0)  # Green → Yellow
    else:
        return RGBColor(255, int(255 * (1 - ratio) * 2), 0)  # Yellow → Red

def main():
    parser = argparse.ArgumentParser(description="Control RGB based on CPU usage/temperature.")
    parser.add_argument("--device", type=int, default=0, help="OpenRGB device index")
    parser.add_argument("--mode", choices=["usage", "temp"], default="usage", help="Monitor mode")
    args = parser.parse_args()

    client = OpenRGBClient()
    device = client.devices[args.device]

    try:
        while True:
            if args.mode == "usage":
                value = psutil.cpu_percent(interval=1)
                print(f"CPU Usage: {value}%")
            else:
                value = get_cpu_temp()
                print(f"CPU Temp: {value}°C")

            color = get_color_from_value(value, 100 if args.mode == "usage" else 90)
            device.set_color(color)
            time.sleep(1)

    except KeyboardInterrupt:
        device.set_color(RGBColor(0, 0, 0))  # Turn off on exit

if __name__ == "__main__":
    main()