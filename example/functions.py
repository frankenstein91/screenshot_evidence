import ntplib, netifaces, platform
import time
import dns.resolver
from python_hosts import Hosts, HostsEntry

def getTimes():
    c = ntplib.NTPClient()
    servers = ["meinekiste.de", "zepto.mcl.gg", "shout.ovh"]
    timeanswers = {}
    timeinfo = {}
    for server in servers:
        try:
            response = c.request(server, version=3)
            timeanswers[server] = response.tx_timestamp
        except ntplib.NTPException:
            print("some log for Timeout")
    timeinfo["times"] = timeanswers
    timeinfo["timezone"] = time.strftime("%Z")
    return timeinfo

def getNetInfos():
    interfaces = netifaces.interfaces()
    ifadresses = {}

    for interface in interfaces:
        temp = {}
        try:
            for out in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                temp2 = {}
                temp2["addr"] = out["addr"]
                temp2["netmask"] = out["netmask"]
                temp["ipV4"] = temp2
        except KeyError:
            print("someLog: no ipV4 on interface")
        try:
            for out in netifaces.ifaddresses(interface)[netifaces.AF_INET6]:
                temp2 = {}
                temp2["addr"] = out["addr"]
                temp["ipV6"] = temp2
        except KeyError:
            print("someLog: no ipV6 on interface")

        temp["mac"] = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]["addr"]
        ifadresses[interface] = temp

    return ifadresses

def getHostname():
    return platform.node()

def GetDNSServers():
    local_resolver = dns.resolver.Resolver()
    return local_resolver.nameservers

def GetHostsFile():
    HostFilePath = ""
    data = {}
    if platform.system() == "Linux":
        HostFilePath = "/etc/hosts"

    with open(HostFilePath, "r") as myfile:
        for line in myfile.readlines():
            worker = line.replace("\n", "")
            worker = " ".join(worker.split())
            worker = worker.split(" ",1)
            data[worker[0]]=worker[1].split(" ")

    return data
