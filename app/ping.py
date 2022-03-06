from app.network import Network
from app.config import Config
from app.deviceinfo import DeviceInfo
import requests
import json
from app.slave_metric import SlaveMetrics
class Ping:
	def pingServer(self):
		configData = Config().fetch()
		data = SlaveMetrics().fetchSocketStatus()
		no_of_sockets = SlaveMetrics().no_of_sockets
		slave_id = 1 
		sockets = []
		for socket_no in range(1,(no_of_sockets)+1): 
			socket = {}
			socket['socketNo'] = socket_no
			if data[socket_no]==0 :
				socket['socketStatus'] = 'OFF'
			if data[socket_no]==1 :
				socket['socketStatus'] = 'ON'	
			socket['slaveId'] = slave_id 
			sockets.append(socket)
			if socket_no % 6 == 0:
				slave_id += 1				
		URL = "http://%s/api/v1/unit/ping" % (configData["mgmt_server_ip"])
		payload = {"ip": Network().fetchIp(),"sockets":sockets,"totalSockets":configData["socket_count"], "majorVersion":configData["version"]["major"], "minorVersion": configData["version"]["minor"], "serialNo": DeviceInfo().fetch(), "unitIdentifier": configData["unit_identifier"]}
		print(payload)
		headers = {"Content-Type": "application/json"}
		#r = requests.post(URL, headers=headers, data=json.dumps(payload))
		#print("Response from PING: %d" % (r.status_code))
	