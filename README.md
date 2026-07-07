# HOW TO 
**Add temperature and humidity display to Raspberry Pi**



## Raspberry Setup
**Update packages**
> sudo apt update

**Install Python**
> sudo apt install python3

**Install Python Package Manger**
> sudo apt install python3-pip



### Enable I2C

**Check status I2C**
>ls /dev/i2c*

**Expected output**
`/dev/i2c-1`

If not;
> sudo raspi-config

-> Interface options > I2C > Enable

> sudo reboot



## Hardware Setup

### Connecting DHT20 to Raspberry Pi

Wire the DHT20 to the Raspberry Pi, use the following pins for each pinout.

| DHT20 | Raspberry Pi  |  Pin  |
| ----- |:-------------:|:-----:|
| VCC   |     3.3v      | Pin 1 |
| GND   |     GND       | Pin 6 |
| SDA   |     GPIO2     | Pin 3 |
| SCL   |     GPIO3     | Pin 5 |


### Check connection

Check connection status of the I2C
> i2cdetect -y 1

Expected output
```
            0  1  2  3  4  5  6  7  8  9  a  b  c  d
        20: -- -- -- -- -- -- -- -- -- -- -- -- -- --
        30: -- -- -- -- -- -- -- -- 38 -- -- -- -- --

```

With a dead DHT2O or Faulty wiring, it will show as
```
            0  1  2  3  4  5  6  7  8  9  a  b  c  d
        20: -- -- -- -- -- -- -- -- -- -- -- -- -- --
        30: -- -- -- -- -- -- -- -- -- -- -- -- -- --
```

This means no device has taken address 38. 





### Connecting 128 x 64 px I2C Display

Wire the I2C Display to the Raspberry Pi, use the following pins for each pinout.

I2C allows multiple devices to be wired up to the same signal lines, and will use a different address for each device.

| DHT20 | Raspberry Pi  |  Pin  |
| ----- |:-------------:|:-----:|
| VCC   |     3.3v      | Pin 1 |
| GND   |     GND       | Pin 6 |
| SDA   |     GPIO2     | Pin 3 |
| SCL   |     GPIO3     | Pin 5 |


**Check if the Raspberry detects the display**
> i2cdetect -y 1

Expected output
```
            0  1  2  3  4  5  6  7  8  9  a  b  c  d
        20: -- -- -- -- -- -- -- -- -- -- -- -- -- --
        30: -- -- -- -- -- -- -- -- 38 -- -- -- 3c --
```

With a faulty I2C Display OR (most likely) faulty wiring, it will show as follows:
```
            0  1  2  3  4  5  6  7  8  9  a  b  c  d
        20: -- -- -- -- -- -- -- -- -- -- -- -- -- --
        30: -- -- -- -- -- -- -- -- 38 -- -- -- -- --
```

- Address 0x38 - DHT20
- Address 0x3C - 128X64 Display


## Software setup

### Virtual Environment Setup

We will run this script in a virtual environment (venv) to keep everything organized and contained.

**First install Python venv support**
> sudo apt install -y python3-venv python3-full

**Create a Virtual Environment named dht20-env**
> python3 -m venv dht20-env

**Activate it**
> source dht20-env/bin/activate

**You should see**
`(dht20-env) pi@raspberrypi:~ $`


#### Installing libraries into the environment
In the Virtual Environment, install the adafruit library to read the DHT20
> pip install adafruit-circuitpython-ahtx0


**When restarting the Raspi, enter the following commands to enter the venv and activate the script.**
> source dht20-env/bin/activate

> python temphumiditydisplay.py

**OR use the following sequence as a single line to activate the venv and run the script**
> source dht20-env/bin/activate && sleep 1 && python temphumiditydisplay.py

**Exit the venv**
> deactivate


## Creating script

### Create script

**IMPORTANT** Navigate to your home folder
> cd /home/pi


Create the script with the following command
> sudo nano temphumiditydisplay.py

**Paste the contents of the provided script in scripts/temphumiditydisplay.py**


#### -OPTIONAL-
        For the printer status line, confirm the correct serial interface and change it in the script.*
        > ls /dev/serial/by-id/

        *Using the "DEVICENAME" for the string "DEVICE_NUMBER1_TEST_ITEM" will detect it*

        **Confirm if this is the correct device by unplugging the printer and seeing if it disapears, after testing again with**
        > ls /dev/serial/by-id/

        **Run the script and confirm the display shows the correct printer status**
        > source dht20-env/bin/activate && sleep 1 && python temphumiditydisplay.py



## Setting the script up for automatic startup

Here we will set up the automatic startup of the script.


#### Creating the file
We will create a .service file in systemmd, this service will get executed on startup.

**First, copy the path of your script**
> realpath temphumiditydisplay.py

`/home/pi/realpath/temphumiditydisplay.py`

Save the path somewhere in a notepad file


#### Creating the script

**Create the service in the systemmd folder**
> sudo nano /etc/systemd/system/display.service

Open the scriptgenerator.exe and enter your Raspberry Pi username, it will automatically generate the .service script for you.
Copy the contents of the script by opening it in notepad and copy paste it in the display.service file.
Or your can of course just tranfer the script to the Raspberry Pi through SFTP. 


#### Optionally; if you for any reason do not trust my script, use the following method OR open the scriptgenerator.py and run it with python.
        *Use the following script for the service file.*

        - Replace $SCRIPTPATH with the previously saved path in the notepad document, EG; "/home/raspi/temphumiditydisplay.py".
        - Replace $USERNAME with the username you are using.

        ```
        [Unit]
        Description=I2C Display Script
        After=multi-user.target

        [Service]
        User=$USERNAME
        WorkingDirectory=/home/$USERNAME/dht20-env
        ExecStart=/home/$USERNAME/dht20-env/bin/python $SCRIPTPATH
        Restart=always
        RestartSec=5

        [Install]
        WantedBy=multi-user.target
        ```

Exit and save.