import serial, glob
import re
import subprocess

def scan():
    # scan for available ports. return a list of tuples (num, name)
    available = []
    for i in range(256):
        try:
            s = serial.Serial(i)
            available.append( (i, s.portstr))
            print(s.portstr)
            s.close()
        except serial.SerialException:
            pass
    return available

def serialConnect(): 
    serlocations=['/dev/ttyACM', '/dev/ttyACM0', '/dev/ttyACM1',
    '/dev/ttyACM2', '/dev/ttyACM3','/dev/ttyACM4', '/dev/ttyACM5',
    '/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3',
    '/dev/ttyUSB4', '/dev/ttyUSB5', '/dev/ttyUSB6', '/dev/ttyUSB7',
    '/dev/ttyUSB8', '/dev/ttyUSB9', '/dev/ttyUSB10','/dev/ttyS0',
    '/dev/ttyS1', '/dev/ttyS2', 'com2', 'com3', 'com4', 'com5',
    'com6', 'com7', 'com8', 'com9', 'com10', 'com11', 'com12',
    'com13', 'com14', 'com15', 'com16', 'com17', 'com18', 'com19',
    'com20', 'com21', 'com1', 'end']
    #for device in scan():

    found = False
    try:
        ser = serial.Serial("/dev/pts/9", 9600, 8, 'N', 1, timeout=5)
        found = True
        return ser  
    except Exception as e:
        print(e)
        x=0 
    if found == False:
        print("No Device Found")
    else:
        print("found")

ser = serialConnect()
if ser:
    ser.write("TEST")
    print("print TEST")
    ser.timeout=5
    print("waited 5 seconds")
    print(ser.readline())
    print("read serial")

def devices():
    device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
    df = subprocess.check_output("lsusb")
    devices = []
    for i in df.split('\n'):
        if i:
            info = device_re.match(i)
            if info:
                dinfo = info.groupdict()
                dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                devices.append(dinfo)
    print(devices)

#devices()

#print "Found ports:"
#scan()

#print "Found ports:"
#for name in scan(): print name