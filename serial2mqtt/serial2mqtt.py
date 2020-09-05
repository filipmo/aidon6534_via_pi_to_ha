## 0.4 Test to send one value to mqtt
version = '0.4' 

import serial
import paho.mqtt.client as mqtt


print('serial2mqtt, version: ' + version)


ser = serial.Serial(
    port='/dev/ttyAMA0',
    timeout=5,
	baudrate=115200,
)

def setDate(name, unit, d):
	month = str(d[0])
	day = str(d[1])
	week_day = str(d[2])
	hour = str(d[3]+1)
	minute = str(d[4])
	second = str(d[5])
	value='{}_{} {}:{}:{}'.format(month, day, hour, minute, second)
	print('Datetime is ' + value)
	return(value)
	
def format83(name, unit, d):
	value=str(int.from_bytes(d, byteorder='big')/1000)
	print('{} is {} {}'.format(name, value, unit))
	return(value)

def format31(name, unit, d):
	#Format 3.1, xxx.x V4 Long-unsigned
	value=str(int.from_bytes(d[0:2], byteorder='big')/10)
	print('{} is {} {}'.format(name, value, unit))
	return(value)
	
	

aidon_map={
	b'\x00\x01\x00\x00\xff': {'name': 'datetime', 'unit': '',
		'd0': 4, 'dn': 6, 'mqtt': 'n', 'func': setDate },
	b'\x00\x01\x08\x00\xff': {'name': 'active_import_energy', 'unit': 'kWh',
		'd0': 1, 'dn': 4, 'mqtt': 'y', 'func': format83 },
	b'\x00\x20\x07\x00\xff': {'name': 'phase_voltage_L1', 'unit': 'V',
		'd0': 1, 'dn': 2, 'mqtt': 'y', 'func': format31 },
	b'\x00\x34\x07\x00\xff': {'name': 'phase_voltage_L2', 'unit': 'V',
		'd0': 1, 'dn': 2, 'mqtt': 'n', 'func': format31 },
	b'\x00\x48\x07\x00\xff': {'name': 'phase_voltage_L3', 'unit': 'V',
		'd0': 1, 'dn': 2, 'mqtt': 'n', 'func': format31 },
	b'\x00\x71\x07\x00\xff': {'name': 'justthelastoneasimissthedot', 'unit': 'None',
		'd0': 5, 'dn': 6, 'func': setDate }
}


print('Using serial settings: ' + str(ser))

mqClient = mqtt.Client("han")
mqClient.username_pw_set("user", "pwd")
mqClient.connect("mqtt-host", 1883)

while True:
	current_data={}	#array with read data in bytearrys, indexed by numerical strings.
	raw_data=ser.read(5000)
	if (len(raw_data) > 0):
		x='0'
		current_data[x]=bytearray(b'')
		for b in range(len(raw_data)):
			current_data[x].append(raw_data[b])
			if (raw_data[b] == 255): #ff
				x = str(int(x) + 1)
				current_data[x]=bytearray(b'')
	if (current_data != {}):	# There are data. May this sometimes be in between. Maybe. Ignore that for now
		for i in range(len(current_data)):
			row = current_data[str(i)]
			key = bytes(row[max(0, len(row)-5):len(row)])
			#print('key: ' + str(key))
			#print('row: ' + str(row))
			#print(aidon_map)
			if key in aidon_map:
				name = aidon_map[key]['name']
				unit = aidon_map[key]['unit']
				publish = aidon_map[key]['mqtt']
				d0 = aidon_map[key]['d0']
				dn = aidon_map[key]['dn']
				
				next_row = current_data[str(i+1)]	# Data is in beginning of next row. A little bit dangerous TODO
				data = next_row[d0:d0+dn]
				
				value=aidon_map[key]['func'](name, unit, data)
				print('value is: ' + value)
				if (publish == 'y'):
					mqClient.publish(name, value)
				
	
	#print(current_data)

		