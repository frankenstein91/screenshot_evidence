#!/usr/bin/env python3
import io, uuid, hmac, hashlib, mss,email.mime.image
from functions import *
from PIL import Image
import xml.etree.cElementTree as ET
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

version = "Test 0.3"

def TakeScreenShot():
    with mss.mss() as sct:
        sct_img = sct.grab(sct.monitors[0])
        HostName = getHostname()
        Times = getTimes()
        TimeZone = Times["timezone"]
        Times = Times["times"]
        NetInfo = getNetInfos()
        DNS = GetDNSServers()
        HostsFile = GetHostsFile()
        root = ET.Element("screenshot_evidence")
        ET.SubElement(root, "HostName").text = HostName
        PicID = str(uuid.uuid1()).replace("-", "")
        FileFunctionsPY = open("functions.py", "r")
        hmacFunctionsPY = hmac.new(PicID.encode(), msg=FileFunctionsPY.read().encode(),
                                   digestmod=hashlib.sha512).hexdigest()
        FileMainPY = open("main.py", "r")
        hmacMainPY = hmac.new(PicID.encode(), msg=FileMainPY.read().encode(), digestmod=hashlib.sha512).hexdigest()
        xml_Software = ET.SubElement(root, "Software", {"Name": "Python Demo SSE", "Version": version})
        ET.SubElement(xml_Software, "File", {"Name": "functions.py"}).text = hmacFunctionsPY
        ET.SubElement(xml_Software, "File", {"Name": "main.py"}).text = hmacMainPY
        ET.SubElement(root, "PicID", {"sequencenumber": str(getCounter())}).text = PicID
        xml_Times = ET.SubElement(root, "ExtTimes", {"timezone": TimeZone})
        for server, EXTtime in Times.items():
            ET.SubElement(xml_Times, "Time", {"Server": server}).text = str(EXTtime)
        XML_DNS = ET.SubElement(root, "DNS_Servers")
        for Server in DNS:
            ET.SubElement(XML_DNS, "Server", {"IP": Server, "Function": "DNS"})
        XML_HostsFile = ET.SubElement(root, "HostsFile")
        for ip, Names in HostsFile.items():
            xml_client = ET.SubElement(XML_HostsFile, "Client", {"IP": ip})
            for name in Names:
                ET.SubElement(xml_client, "name").text = name
        XML_NetWorkHarware = ET.SubElement(root, "NetWorkHarware")
        for InterfaceName, InterfaceMeta in NetInfo.items():
            ThisInterface = ET.SubElement(XML_NetWorkHarware, "Interface",
                                          {"Name": InterfaceName, "MAC": InterfaceMeta["mac"]})
            if "ipV4" in InterfaceMeta:
                for ipV4 in InterfaceMeta["ipV4"]:
                    ET.SubElement(ThisInterface, "address", {"Typ": "ipV4", "Netmask": ipV4["netmask"]}).text = ipV4[
                        "addr"]
            if "ipV6" in InterfaceMeta:
                for ipV6 in InterfaceMeta["ipV6"]:
                    ET.SubElement(ThisInterface, "address", {"Typ": "ipV6"}).text = ipV6["addr"].split("%")[0]

        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        imgByteArr = io.BytesIO()
        img.save(imgByteArr, format='PNG', optimize=True)

        # imgByteArr.getvalue()
        try:
            ET.SubElement(root, "Pic_Checksum", {"Typ": "MD5"}).text = hashlib.md5(imgByteArr.getvalue()).hexdigest()
        except AttributeError:
            pass
        try:
            ET.SubElement(root, "Pic_Checksum", {"Typ": "SHA512"}).text = hashlib.sha512(
                imgByteArr.getvalue()).hexdigest()
        except AttributeError:
            pass
        try:
            ET.SubElement(root, "Pic_Checksum", {"Typ": "SHA3_512"}).text = hashlib.sha3_512(
                imgByteArr.getvalue()).hexdigest()
        except AttributeError:
            pass
        try:
            ET.SubElement(root, "Pic_Checksum", {"Typ": "SHA256"}).text = hashlib.sha256(
                imgByteArr.getvalue()).hexdigest()
        except AttributeError:
            pass

        #######Test
        msg = MIMEMultipart()
        imgMime = email.mime.image.MIMEImage(imgByteArr.getvalue())
        msg.attach(imgMime)
        XMLText = BeautifulSoup(ET.tostring(root), "xml").prettify()
        TextMime = MIMEText(XMLText)
        XMLhash = hashlib.sha512(XMLText.encode()).hexdigest() + "|" + hashlib.md5(XMLText.encode()).hexdigest()
        TextMime2 = MIMEText(XMLhash)
        msg.attach(TextMime)
        msg.attach(TextMime2)

        with open("test.sse", "wb") as f:
            f.write(msg.as_bytes())


TakeScreenShot()
