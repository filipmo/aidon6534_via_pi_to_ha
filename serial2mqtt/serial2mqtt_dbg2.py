## Debug, just to see that you got something from the serial interface
import serial
version = 'Dbg2' 

print('Dbg2: Serial Connection Debug ' + version)
print('When working correctly you should get a long string every 10:th second, and some empty b in between')
print("My string has a buffer size of 581 bytes, and starts with: ~\\xa2CA\\x08")


ser = serial.Serial(
    port='/dev/ttyAMA0',
    timeout=5,
	baudrate=115200,
)

print('Using serial settings: ' + str(ser))
while True:
	aidon=ser.read(5000)
	print('Read new buffer with length ' + str(len(aidon)) + ' bytes: ')
	print(str(aidon))