#!/usr/bin/env python3
import argparse
import time
import psutil
import sys
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor


def get_cpu_temp():
    """Read CPU temperature from thermal zones."""
    try:
        with open("/sys/class/thermal/thermal_zone2/temp", "r") as f:
            return int(f.read().strip()) / 1000
    except FileNotFoundError:
        print("Thermal zone not found. Are you on a compatible system?")
        return 0


def get_color_from_value(value, max_value=100):
    """Map a value (usage/temp) to a color gradient."""
    ratio = min(value / max_value, 1.0)
    if ratio < 0.5:
        return RGBColor(int(255 * ratio * 2), 0, 255)  # Black → Blue → Cyan
    else:
        return RGBColor(255, 0, max(255 - int(255 * (ratio - 0.5) * 2), 0))  # Cyan → Red


# --- OFF mode (shutdown RGB) ---
if "--off" in sys.argv:
    try:
        client = OpenRGBClient()
        for device in client.devices:
            for led in device.leds:
                led.set_color((0, 0, 0))
    except Exception as e:
        print(f"Failed to turn off RGB: {e}")
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Control RGB based on CPU usage/temperature.")
    parser.add_argument("--device", type=int, default=0, help="OpenRGB device index")
    parser.add_argument("--mode", choices=["usage", "temp"], default="temp", help="Monitor mode")
    parser.add_argument("--max", type=float, help="Max value for color scaling")
    parser.add_argument("--test", action="store_true", help="Run in test mode (preview gradient)")
    args = parser.parse_args()

    try:
        client = OpenRGBClient()
    except Exception as e:
        print(f"Failed to connect to OpenRGB server: {e}")
        return

    try:
        device = client.devices[args.device]
    except IndexError:
        print(f"No RGB device found at index {args.device}")
        return

    if args.test:
        print("Running test gradient...")
        for i in range(0, 101, 5):
            color = get_color_from_value(i, args.max or 100)
            for led in device.leds:
                led.set_color(color)
            time.sleep(0.1)
        device.set_color(RGBColor(0, 0, 0))
        return

    max_value = args.max or (100 if args.mode == "usage" else 90)

    try:
        while True:
            if args.mode == "usage":
                value = psutil.cpu_percent(interval=1)
                print(f"CPU Usage: {value:.1f}%")
            else:
                value = get_cpu_temp()
                print(f"CPU Temp: {value:.1f}°C")

            color = get_color_from_value(value, max_value)
            print(f"Color: R={color.red}, G={color.green}, B={color.blue}")
            for led in device.leds:
                led.set_color(color)
            time.sleep(1)

    except KeyboardInterrupt:
        print("Shutting down...")
        device.set_color(RGBColor(0, 0, 0))


if __name__ == "__main__":
    main()
