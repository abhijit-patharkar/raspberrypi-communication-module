import serial
import time
from app.config import Config
#from config import Config
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
from app.deviceinfo import DeviceInfo
#from deviceinfo import DeviceInfo
import requests
import json
import asyncio
import datetime

#PORT = 7
no_of_sockets_in_slave= 6
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
configData = Config().fetch()


class SlaveMetrics:

	no_of_slaves = configData["slave_count"]
	no_of_sockets = configData["socket_count"]

	def calculate_Voltage(self,list):
		return(float(list[v_start_index]))

	def calculate_Current(self,list,socket_no):
		return(float(list[i_start_index*socket_no]))

	def calculate_Frequency(self,list):
		return(list[f_start_index])

	def calculate_Active_Power(self,list,socket_no):
		index = ap_start_index+((socket_no-1)*register_count)
		return(float("%d.%d" % (list[index],list[index+1])))

	def calculate_Apparent_Power(self,list,socket_no):
		index = app_start_index+((socket_no-1)*register_count)
		return(float("%d.%d" % (list[index],list[index+1])))

	def calculate_Reactive_Power(self,list,socket_no):
		index = rp_start_index+((socket_no-1)*register_count)
		return(float("%d.%d" % (list[index],list[index+1])))

	def calculate_Power_Consumption(self,list,socket_no):
		index = pc_start_index+((socket_no-1)*register_count)
		return(int("%d%d" % (list[index],list[index+1])))

	def calculate_Power_Factor(self,list,socket_no):
		return(float(list[pf_start_index+(socket_no-1)]))

	@asyncio.coroutine
	def sendMetricsOfSlave(self,slave_id):
		print("Processing slave : " + str(slave_id) + " at " + str(datetime.datetime.now()))
		logger = modbus_tk.utils.create_logger("console")
		try:
		    #Connect to the slave
		    master = modbus_rtu.RtuMaster(
		        serial.Serial(port=PORT, baudrate=57600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
		    )
		    master.set_timeout(0.1)
		    master.set_verbose(True)
		    logger.info("connected")
		    list=master.execute(slave_id, cst.READ_HOLDING_REGISTERS, 0, 61)
		    print(list)
		    sockets_in_slave = no_of_sockets_in_slave
		    if slave_id * no_of_sockets_in_slave > SlaveMetrics().no_of_sockets :
		    	sockets_in_slave = no_of_sockets_in_slave-((no_of_sockets_in_slave*slave_id)-SlaveMetrics().no_of_sockets)
		    socketArr=[]
		    for socket_no in range(0,sockets_in_slave):
			    socket={}
			    socket['f']=SlaveMetrics().calculate_Frequency(list)
			    socket['pc']=SlaveMetrics().calculate_Power_Consumption(list,socket_no)
			    socket['soNo']=socket_no+1
			    socket['v']=SlaveMetrics().calculate_Voltage(list)
			    socket['c']=SlaveMetrics().calculate_Current(list,socket_no)
			    socket['ap']=SlaveMetrics().calculate_Active_Power(list,socket_no)
			    socket['apw']=SlaveMetrics().calculate_Apparent_Power(list,socket_no)
			    socket['rp']=SlaveMetrics().calculate_Reactive_Power(list,socket_no)
			    socket['pf']=SlaveMetrics().calculate_Power_Factor(list,socket_no)
			    socket['cd']=int(round(time.time() * 1000))
			    socketArr.append(socket)
		    data = json.dumps(socketArr)
		    print(data)
		    URL = "http://%s/api/v1/metric/serial/2001" % (configData["mgmt_server_ip"])
		    headers = {"Content-Type": "application/json"}
		    #r = requests.post(URL,headers=headers,data=data)
		    #print("Response from PING: %d" % (r.status_code))    
		    master.close()          
		except modbus_tk.modbus.ModbusError as exc:
			master.close()
			logger.error("%s- Code=%d", exc, exc.get_exception_code())

	def processMetrics(self):
		futures = [SlaveMetrics().sendMetricsOfSlave(slave_id) for slave_id in range(1,(SlaveMetrics().no_of_slaves)+1)]
		loop = asyncio.get_event_loop()
		loop.run_until_complete(asyncio.wait(futures))	
			    	            
	def fetchSocketStatus(self):
		logger = modbus_tk.utils.create_logger("console")
		try:
		    #Connect to the slave
			master = modbus_rtu.RtuMaster(
			    serial.Serial(port=PORT, baudrate=57600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
			)
			master.set_timeout(0.1)
			master.set_verbose(True)
			logger.info("connected")
			socket_status={}
			slave_id=1
			socket_id=1	
			i=1
			for slave_id in range(1,(SlaveMetrics().no_of_slaves)+1):
				sockets_in_slave = no_of_sockets_in_slave
				if slave_id * no_of_sockets_in_slave > SlaveMetrics().no_of_sockets :
					sockets_in_slave = no_of_sockets_in_slave-((no_of_sockets_in_slave*slave_id)-SlaveMetrics().no_of_sockets)	
				status = master.execute(slave_id, cst.READ_COILS, 0, sockets_in_slave)
				for socket_no in range(0,sockets_in_slave):
					socket_status[i] = status[socket_no]
					i+=1	
			#socket_status = json.dumps(socket_status)		  
			return socket_status
			master.close()
		except modbus_tk.modbus.ModbusError as exc:
			master.close()
			logger.error("%s- Code=%d", exc, exc.get_exception_code())			

	def getSocketMetrics(self,socket_no):
		master = modbus_rtu.RtuMaster(
		        serial.Serial(port=PORT, baudrate=57600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
		    )
		master.set_timeout(0.1)
		master.set_verbose(True)
		list=master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 61)
		socket={}
		socket['f']=SlaveMetrics().calculate_Frequency(list)
		socket['pc']=SlaveMetrics().calculate_Power_Consumption(list,socket_no)
		socket['soNo']=socket_no+1
		socket['v']=SlaveMetrics().calculate_Voltage(list)
		socket['c']=SlaveMetrics().calculate_Current(list,socket_no)
		socket['ap']=SlaveMetrics().calculate_Active_Power(list,socket_no)
		socket['apw']=SlaveMetrics().calculate_Apparent_Power(list,socket_no)
		socket['rp']=SlaveMetrics().calculate_Reactive_Power(list,socket_no)
		socket['pf']=SlaveMetrics().calculate_Power_Factor(list,socket_no)
		socket['cd']=int(round(time.time() * 1000))
		master.close()
		data=SlaveMetrics().fetchSocketStatus()
		socket['Status']=data[socket_no]			
		return socket   
		   	