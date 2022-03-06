import json
import socket
json_loc = "/etc/smartpdu/conf/config.json"
class Config:
	
	def fetch(self):
		#Reading config file 
		with open(json_loc) as json_data_file:
			data = json.load(json_data_file)
			return(data)

	def updateUnitIdentifier(self,unit_identifier):
		data = self.fetch()
		data["unit_identifier"] = unit_identifier
		with open(json_loc, "w") as json_data_file:
			json.dump(data, json_data_file)
		return 1

	def updateMgmtServerIp(self,mgmtServerIp):
		data = self.fetch()
		try:
			socket.inet_aton(mgmtServerIp)
			data["mgmt_server_ip"] = mgmtServerIp
			with open(json_loc, "w") as json_data_file:
				json.dump(data, json_data_file)
			return 1
		except socket.error:
			print("invalid")
			return 0				

	def updateVersion(self,major, minor):
		data = self.fetch()
		data["version"]["major"] = major
		data["version"]["minor"] = minor
		with open(json_loc,"w") as json_data_file:
			json.dump(data, json_data_file)
		return 1
			
	def isComplete(self):
		data = self.fetch()
		unit_identifier = data["unit_identifier"]
		mgmtServerIp = data["mgmt_server_ip"]
		if(unit_identifier=="" or mgmtServerIp==""):
			print("invalid")
			return 0
		else:
			return 1	

	def updateNetworkSettings(self, address, netmask, gateway, dns_servers, search_domains):
		data = self.fetch()
		data["address"] = address
		data["netmask"] = netmask
		data["gateway"] = gateway
		data["dns_servers"] = dns_servers
		data["search_domains"] = search_domains
		with open(json_loc, "w") as json_data_file:
			json.dump(data, json_data_file)
