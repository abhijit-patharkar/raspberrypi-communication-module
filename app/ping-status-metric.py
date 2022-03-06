import json
from slave_metric import SlaveMetrics

data = SlaveMetrics().fetchSocketStatus()
no_of_sockets = SlaveMetrics().no_of_sockets
slave_id = 1 
sockets = []
for socket_no in range(1,(no_of_sockets)+1): 
	socket = {}
	socket['socketNo'] = socket_no
	socket['socketStatus'] = data[socket_no]
	socket['slaveId'] = slave_id 
	sockets.append(socket)
	if socket_no % 6 == 0:
		slave_id += 1
print(sockets)
