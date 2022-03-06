import serial
import time
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
from deviceinfo import DeviceInfo
import requests
import json

#PORT = 7
PORT = 'COM7'
index = 0
v_start_index = 0
i_start_index = 1
f_start_index = 7
ap_start_index = 8
app_start_index = 20
rp_start_index = 32
pc_start_index = 44
pf_start_index = 56
register_count = 2
 
def calculate_Voltage(list):
	return(float(list[v_start_index]))

def calculate_Current(list,socket_no):
	return(float(list[i_start_index*socket_no]))

def calculate_Frequency(list):
	return(list[f_start_index])

def calculate_Active_Power(list,socket_no):
	index = ap_start_index+((socket_no-1)*register_count)
	return(float("%d.%d" % (list[index],list[index+1])))

def calculate_Apparent_Power(list,socket_no):
	index = app_start_index+((socket_no-1)*register_count)
	return(float("%d.%d" % (list[index],list[index+1])))

def calculate_Reactive_Power(list,socket_no):
	index = rp_start_index+((socket_no-1)*register_count)
	return(float("%d.%d" % (list[index],list[index+1])))

def calculate_Power_Consumption(list,socket_no):
	index = pc_start_index+((socket_no-1)*register_count)
	return(int("%d%d" % (list[index],list[index+1])))

def calculate_Power_Factor(list,socket_no):
	return(float(list[pf_start_index+(socket_no-1)]))

def main():
    """main"""
    logger = modbus_tk.utils.create_logger("console")
    try:
        #Connect to the slave
        master = modbus_rtu.RtuMaster(
            serial.Serial(port=PORT, baudrate=57600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
        )
        master.set_timeout(10.0)
        master.set_verbose(True)
        logger.info("connected")
        #while 1:
        #logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 61))
        list=master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 61)
        #print(list)
        socketArr=[]
        for socket_no in range(0,6):
	        socket={}
	        socket['f']=calculate_Frequency(list)
	        socket['pc']=calculate_Power_Consumption(list,socket_no)
	        socket['soNo']=socket_no+1
	        socket['v']=calculate_Voltage(list)
	        socket['c']=calculate_Current(list,socket_no)
	        socket['ap']=calculate_Active_Power(list,socket_no)
	        socket['apw']=calculate_Apparent_Power(list,socket_no)
	        socket['rp']=calculate_Reactive_Power(list,socket_no)
	        socket['pf']=calculate_Power_Factor(list,socket_no)
	        socketArr.append(socket)
        print(socketArr)
        data = json.dumps(socketArr)
        print(data)
        URL = "http://192.168.0.103:10101/api/v1/metric/serial/2001"
        headers = {"Content-Type": "application/json"}
        r = requests.post(URL,headers=headers,data=data)
        print("Response from PING: %d" % (r.status_code))    
        #send some queries
        #logger.info(master.execute(1, cst.READ_COILS, 0, 10))
        #logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 8))
        #logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 100, 3))
        #logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 12))
        #logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 7, output_value=1))
        #logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, 100, output_value=54))
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 0, 1, 1, 0, 1, 1]))
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 100, output_value=xrange(12)))

    except modbus_tk.modbus.ModbusError as exc:
        logger.error("%s- Code=%d", exc, exc.get_exception_code())

if __name__ == "__main__":
    main()
    