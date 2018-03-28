import ntplib, netifaces, platform
import time
import dns.resolver
import tempfile,os,re

def getCounter(reset=False):
    Path = os.path.join(tempfile.gettempdir(),"SSE.counter")
    if reset or not os.path.isfile(Path):
        TempCounter = 0
    else:
        TempCounter = 0
        with open(Path,"r") as f:
            try:
                TempCounter = int(re.sub("[^0-9]", "", f.readline().strip()))
            except:
                TempCounter = 0

            try:
                TempCounter += 1
                TempCounter -= 1
            except TypeError:
                TempCounter = 0
    Counter = TempCounter
    Counter += 1
    with open(Path,"w") as f:
        f.write(str(Counter))
    return Counter


def getTimes():
    c = ntplib.NTPClient()
    servers = ["meinekiste.de", "zepto.mcl.gg", "shout.ovh", "time-a-g.nist.gov", "time-b-g.nist.gov",
               "time-a-wwv.nist.gov", "time-a-b.nist.gov", "0.pool.ntp.org"]
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
        temp["ipV4"] = []
        temp["ipV6"] = []
        try:
            for out in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                temp2 = {}
                temp2["addr"] = out["addr"]
                temp2["netmask"] = out["netmask"]
                temp["ipV4"].append(temp2)
        except KeyError:
            print("someLog: no ipV4 on interface")
        try:
            for out in netifaces.ifaddresses(interface)[netifaces.AF_INET6]:
                temp2 = {}
                temp2["addr"] = out["addr"]
                temp["ipV6"].append(temp2)
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
    elif platform.system() == "Windows":
        HostFilePath = "C:/Windows/System32/drivers/etc/hosts"

    with open(HostFilePath, "r") as myfile:
        for line in myfile.readlines():
            if line.startswith("#"):
                continue
            worker = line.split("#")[0].replace("\n", "")
            if worker == "":
                continue
            worker = " ".join(worker.split())
            worker = worker.split(" ", 1)
            data[worker[0]] = worker[1].split(" ")

    return data

def GetWindows():
    windows =[]
    if platform.system() == "Windows":
        import ctypes
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        GetWindowText = ctypes.windll.user32.GetWindowTextW
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible
        titles = []
        def foreach_window(hwnd, lParam):
            if IsWindowVisible(hwnd):
                length = GetWindowTextLength(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, buff, length + 1)
                titles.append(buff.value)
            return True
        EnumWindows(EnumWindowsProc(foreach_window), 0)
        for title in titles:
            title = str(title).strip()
            if not title == "":
                windows.append(title)
    return windows