# SF Weather Display

A home weather display based on my [sf-weather-dashboard project](https://github.com/rguidice/sf-weather-dashboard), which pulls data from the [SF Microclimates API](https://microclimates.solofounders.com/).

This is a personal project I plan to set-and-forget.

## Hardware

- Raspberry Pi Zero W
- [7" 1024x600 IPS HDMI LCD](https://www.amazon.com/dp/B0FR5B5M28) (Amazon link, but seems like a generic design that can be found on many other retailers such as AliExpress)

## OS Setup

Flashed the SD card using Raspberry Pi Imager v2.0.6:

- Board: Raspberry Pi Zero
- OS: Raspberry Pi OS (other) → Raspberry Pi OS Lite (32-bit)
- Configure Wi-Fi and enable SSH

## Install Procedure

### 1. Update packages

```sh
sudo apt update && sudo apt full-upgrade -y
```

### 2. Install dependencies

```sh
sudo apt install unclutter surf matchbox-window-manager \
  xserver-xorg-video-all xserver-xorg-input-all xserver-xorg-core \
  xinit x11-xserver-utils vim python3-gpiozero -y
```

> `surf` is used instead of Chromium because the Pi Zero W's ARMv6 CPU lacks NEON SIMD extensions required by newer Chromium builds.

### 3. Change graphics driver

Edit `/boot/firmware/config.txt` (note: older Pi OS placed this at `/boot/config.txt`):

```sh
sudo sed -i 's/dtoverlay=vc4-kms-v3d/dtoverlay=vc4-fkms-v3d/' /boot/firmware/config.txt
```

> Fix found in an [Amazon review](https://www.amazon.com/dp/B0FR5B5M28) for the display.

### 4. Enable auto-login

```sh
sudo raspi-config
```

Navigate to: **1 System Options → S6 Auto Login**

> Running raspi-config version 20251202.

> Can use **8 Update** to update raspi-config, seems like menu locations change frequently.

### 5. Configure `.bash_profile`

Auto-start X on tty1 at login:

```sh
cat > ~/.bash_profile << 'EOF'
# Source .bashrc if it exists
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi

# Auto-start X on tty1
if [ -z "$DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
    exec startx
fi
EOF
```

### 6. Configure `.xinitrc`

Set up the kiosk session:

```sh
cat > ~/.xinitrc << 'EOF'
#!/usr/bin/env sh
xset -dpms
xset s off
xset s noblank

unclutter &

matchbox-window-manager -use_titlebar no &
python3 ~/refresh-button.py &
sleep 1
surf -F -z 1.0 http://weather.local/kiosk
EOF
chmod +x ~/.xinitrc
```

### 7. [_Optional_] Install refresh button

Used to manually refresh the browser display if some map tiles don't render correctly. GPIO inputs monitored via `refresh_button.py`. Adjust `refresh_button.py` path in `.xinitrc` if needed.

Solder a push button between GPIO 17 (pin 11) and GND (pin 9 is closest but any will work).

## References

- [Minimal Raspberry Pi Kiosk](https://blog.r0b.io/post/minimal-rpi-kiosk/) — helpful starting point for the kiosk setup
