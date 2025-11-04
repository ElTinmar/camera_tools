# camera_tools

handle various camera

```
pip install git+https://github.com/ElTinmar/camera_tools.git@main
```

# PyUVC

On ubuntu you need to add udev rules for each webcam:

```
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="046d", ATTR{idProduct}=="085b", MODE="0664", GROUP="plugdev"' | sudo tee /etc/udev/rules.d/99-webcams.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

# Ximea

Install xiAPI

```
wget https://www.ximea.com/downloads/recent/XIMEA_Linux_SP.tgz
tar xzf XIMEA_Linux_SP.tgz
cd package
./install -pcie
cp api/Python/v3/ximea <path/to/python/site-packages/>
```

# Spinnaker


## Download SDK and python whl from Teledyne's website

https://www.teledynevisionsolutions.com/products/spinnaker-sdk

## Install dependencies

```
sudo apt-get install libusb-1.0-0 libpcre2-16-0 libdouble-conversion3 libxcb-xinput0 libxcb-xinerama0 qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools libturbojpeg-dev libusb-1.0-0-dev
```

## Install old version of ffmpeg

Spinnaker uses an old version of ffmpeg, install in environment

```
conda activate ZebVR2
conda install -c conda-forge ffmpeg==4.4.2
```


## Modify install script for newer systemctl

```
vim configure_spinnaker.sh
```

replace (line 77)

```
/etc/init.d/udev restart
```

with 

```
sudo systemctl restart systemd-udevd
```

## Install the SDK 

```
sudo sh install_spinnaker.sh
```

## Install python wheel

```
pip install ~/Downloads/spinnaker_python-4.2.0.46-cp38-cp38-linux_x86_64-20.04/spinnaker_python-4.2.0.46-cp38-cp38-linux_x86_64.whl
```
