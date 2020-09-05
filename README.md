# aidon6534_via_pi_to_ha
HW description and SW(python, yaml, instructions) to get my Aidon 6534 electrical meter from "Tekniska verken" using P1 interface to work with my homeassistant.
Make sure you have a 6 pins RJ12 connection. There are other variants of Aidon6534 with a complete differnt interface with RJ45 connection (Norwegian interface)

## HW overview
Aidon6534 -> serial interface -> pi -> mqtt -> ha

# HW needed
* Aidon 6534 (As you found this, you most probably have one
* pi (I use an old 1B with 2 GB SD card)
* An half RJ12 cable (I bought from Kjell o Company) (max length 1,5 meters according to Aidon spec)
* NPN transistor, some resistors
* Board for the electronics

## Install
* Aidon. Ask "Tekniska verken" to open the HAN port. (for me it took < 1 day via support)
* Build your serial interface (TODO, add drawing)
* Burn Raspberry Pi Lite to your SD card: https://downloads.raspberrypi.org/raspios_lite_armhf_latest
* Insert card in PI and connect to network (I use Putty and ssh)
* Connect the R12 to the HAN port
* pip install (TODO what did I add)
* Copy the aidon2mqtt.py to a folder on your pi
* Run: 'sudo python3 aidon2mqtt.py'
* On HA, install the Mosquitto MQTT broker (TODO instructions)
* TODO: yaml code for the HA



