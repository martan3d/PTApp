"""
Protothrottle Receiver App
"""

import toga
import asyncio
from toga.style import Pack
from toga import Button, MultilineTextInput, Label, TextInput
from toga.style.pack import COLUMN, ROW, CENTER, RIGHT, LEFT, START, END

if toga.platform.current_platform == 'android':
   from java import jclass
   from android.content import Context
   # Android Java Class names, used for permissions
   Intent = jclass('android.content.Intent')
   PendingIntent = jclass('android.app.PendingIntent')

# Silicon Labs USB constants

CP210X_IFC_ENABLE         = 0x00
UART_ENABLE               = 0x0001
REQTYPE_HOST_TO_INTERFACE = 0x41
USB_READ_TIMEOUT_MILLIS   = 5000
USB_WRITE_TIMEOUT_MILLIS  = 5000
CP210X_SET_BAUDDIV        = 0x01
BAUD_RATE_GEN_FREQ        = 0x384000
DEFAULT_BAUDRATE          = 38400
DEFAULT_READ_BUFFER_SIZE  = 256

RETURNTYPE       = 37

# Ids for buttons and text/numeric inputs

PTID = 1000
BASE = 1001
ADDR = 1002
CONS = 1003
COND = 1004
DECO = 1005
SRV0 = 1010
SRV1 = 1011
SRV2 = 1012
SRVM = 1013
SVR0 = 1014
SVR1 = 1015
SVR2 = 1016
SV0L = 1017
SV0H = 1018
SV1L = 1019
SV1H = 1020
SV2L = 1021
SV2H = 1022
SRVP = 1023
SRRP = 1024

SRVP0 = 1025
SRVP1 = 1026
SRVP2 = 1027

OUTX = 1040
OUTY = 1041
WDOG = 1050
BRAT = 1050
BFNC = 1061
ACCL = 1062
DECL = 1063

adprot = { 0x30 :'A', 0x31 :'B', 0x32 :'C', 0x33 :'D', 0x34 :'E', 0x35 :'F', 0x36 : 'G', 0x37 : 'H', 0x38 : 'I', 0x39 : 'J',
           0x3a : 'K', 0x3b : 'L', 0x3c : 'M', 0x3d : 'N', 0x3e : 'O', 0x3f : 'P', 0x40 : 'Q', 0x41 : 'R', 0x42 : 'S',
           0x43 : 'T', 0x44 : 'U', 0x45 : 'V', 0x46 : 'W', 0x47 : 'X', 0x48 : 'Y', 0x49 : 'Z' }


class PTApp(toga.App):

    initport = False
    clrport  = False
    portinitialized = False

    readport = False
    readbuff = ""
    readlen  = 0
    readcomplete = False

    writeport = False
    writebuff = ""
    writelen  = 0
    writecomplete = False

    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)

        self.discover_button = Button(
            'Scan',
            on_press=self.start_discover,
            style=Pack(width=120, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=12)
        )

        self.working_text = Label("", style=Pack(font_size=12, color="#000000"))

        scan_content = toga.Box(style=Pack(direction=COLUMN, align_items=CENTER, margin_top=5))
        scan_content.add(self.discover_button)
        scan_content.add(self.working_text)

        self.setupAndroidSerialPort()

        self.scroller = toga.ScrollContainer(content=scan_content, style=Pack(direction=COLUMN, align_items=CENTER))
        self.main_window.content = self.scroller
        self.main_window.show()


    async def start_discover(self, id):

        self.working_text.text = "Scanning for Receivers..."

        self.writebuff = bytearray([0x7E, 0x00, 0x04, 0x08, 0x01, 0x4E, 0x44, 0x64])
        self.writelen = len(self.writebuff)
        await self.connectWrite()
        await asyncio.sleep(2)
        await self.connectRead()

        # setup the screen buttons we will use for each receiver
        scan_content = toga.Box(style=Pack(direction=COLUMN, align_items=CENTER, margin_top=5))
        self.buttonDict = {}

        # set some screen elements
        scan_content.add(self.discover_button)
        scan_content.add(self.working_text)
        self.working_text.text = ""

        # may be several responses, turn data into list of xbee api frames
        messages = self.parseMessageData(self.readlen, self.readbuff)

        # for each message, pull out the mac address and ascii node id
        for mac in messages:
            id  = messages[mac]
            print ("mac:", mac, "id:", id)
            if mac == "" or id == "": continue
            fmstring = "{} {}".format(id, mac)
            self.buttonDict[mac] = id
            scan_content.add(
                toga.Button(id=mac, text=fmstring,
                    on_press = self.connectToClient,
                    style=Pack(width=230, height=120, margin_top=12, background_color="#bbbbbb", color="#000000", font_size=16),
                )
            )

        self.scroller = toga.ScrollContainer(content=scan_content, style=Pack(direction=COLUMN, align_items=CENTER))
        self.main_window.content = self.scroller
        self.main_window.show()

    async def connectToClient(self, widget):
        self.working_text.text = "Requesting Data from Receiver..."
        address = self.buildAddress(widget.id)
        data = chr(RETURNTYPE) + "000000000000000000"
        buff = self.buildXbeeTransmitData(address, data)
        self.writebuff = bytearray(buff)
        self.writelen = len(self.writebuff)
 
        await self.connectWrite()
        await asyncio.sleep(1)
        await self.connectRead()

        message = self.parseReturnData(self.readlen, self.readbuff)

        print ("message ",message)

        if not message:
           self.working_text.text = ""
           return

        if message[3] == 129:
           self.displayWidgetScreen(widget, message)
        
    
    # send message to Xbee
    async def connectWrite(self):
        self.connection.bulkTransfer(self.writeEndpoint, self.writebuff, self.writelen, USB_WRITE_TIMEOUT_MILLIS)

    # recieve message from Xbee
    async def connectRead(self):
        self.readbuff = bytearray(DEFAULT_READ_BUFFER_SIZE)
        self.readlen  = self.connection.bulkTransfer(self.readEndpoint, self.readbuff, DEFAULT_READ_BUFFER_SIZE, USB_READ_TIMEOUT_MILLIS)

    # Convert MAC address to Xbee message format
    def buildAddress(self, address):
        dest    = [0,0,0,0,0,0,0,0]
        dest[0] = int(address[:2], 16)           # very brute force way to pull this out!
        dest[1] = int(address[2:4], 16)
        dest[2] = int(address[4:6], 16)
        dest[3] = int(address[6:8], 16)
        dest[4] = int(address[8:10], 16)
        dest[5] = int(address[10:12], 16)
        dest[6] = int(address[12:14], 16)
        dest[7] = int(address[14:16], 16)
        return dest

    # Parse data and make a list of Node Discovery return messages
    def parseMessageData(self, size, data):
        messages = []
        msg = []
        if size > 0:
           msg.append(data[0])
        for i in range(1, size):
            if data[i] == 0x7e:
               messages.append(msg)
               msg = []
               msg.append(data[i])
            else:
               msg.append(data[i])
        messages.append(msg)

        self.nodeData = {}

        if len(messages) <= 0: 
           return self.nodeData

        for msg in messages:
            mac = ""
            id  = ""
            if len(msg) > 20:
               if msg[3] != 129:
                  for i in range(10, 18):
                     mac = mac + "{:02X}".format(msg[i])
                  for i in range(19, len(msg)-2):
                     id = id + chr(msg[i])
                  self.nodeData[mac] = id
        return self.nodeData


    # Parse return data looking for 16 bit return and EEprom data
    def parseReturnData(self, size, data):
        messages = []
        msg = []
        if size > 0:
           msg.append(data[0])
        for i in range(1, size):
            if data[i] == 0x7e:
               messages.append(msg)
               msg = []
               msg.append(data[i])
            else:
               msg.append(data[i])
        messages.append(msg)

#        for msg in messages:
#            hexString = ""
#            for m in msg:
#                hexString = hexString + hex(m) + " "
#            print (hexString)

        if len(messages) <= 0: 
           return []

        for msg in messages:
            mac = ""
            id  = ""
            if len(msg) > 20:
               if msg[3] == 129 and msg[9] == 87:   # must be 16 bit return packet and a 'W' in the message to be valid
                  return msg
        return []



    # create a valid transmit frame for Xbee API message
    def buildXbeeTransmitData(self, dest, data):
        txdata = []
        dl = len(data)
        for d in data:     # make sure it's in valid bytes for transmit
            try:
               txdata.append(int(ord(d)))
            except:
               txdata.append(int(d))

        frame = []
        frame.append(0x7e)	# header
        frame.append(0)	        # our data is always < 256
        frame.append(dl+11)     # all data except header, length and checksum
        frame.append(0x00)      # TRANSMIT REQUEST 64bit (mac) address - send Query to Xbee module
        frame.append(0x00)      # frame ID for ack- 0 = disable

        frame.append(dest[0])   # 64 bit address (mac)
        frame.append(dest[1])
        frame.append(dest[2])
        frame.append(dest[3])
        frame.append(dest[4])
        frame.append(dest[5])
        frame.append(dest[6])
        frame.append(dest[7])

        frame.append(0x00)      # always reserved

        for i in txdata:        # move data to transmit buffer
            frame.append(i)
        frame.append(0)         # checksum position
        cks = 0;
        for i in range(3, dl+14):	# compute checksum
            cks += int(frame[i])

        i = (255-cks) & 0x00ff
        frame[dl+14] = i        # insert checksum in message
        return frame


    # Android open serial port thread
    def setupAndroidSerialPort(self):
        # for now, Android
        self.context = jclass('org.beeware.android.MainActivity').singletonThis
        self.usbmanager = self.context.getSystemService(self.context.USB_SERVICE)
        self.usbDevices = self.usbmanager.getDeviceList()

        # Check to see if Xbee device is connected, should only be one
        iterator = self.usbDevices.entrySet().iterator()
        while iterator.hasNext():
           entry = iterator.next()
           self.device = entry.getValue()

        # Check USB Permissions, get them if needed
        self.checkPermission()

        print ("Get connection")
        self.connection = self.usbmanager.openDevice(self.device)
        self.interface = self.device.getInterface(0)
        self.readEndpoint = self.interface.getEndpoint(0)
        self.writeEndpoint = self.interface.getEndpoint(1)
        print ("done connection")

        buf = None

        result = self.connection.controlTransfer(
                 REQTYPE_HOST_TO_INTERFACE,
                 CP210X_IFC_ENABLE,
                 UART_ENABLE,
                 0,
                 buf,
                 (0 if buf is None else len(buf)),
                 USB_WRITE_TIMEOUT_MILLIS,
                 )

        result = self.connection.controlTransfer(
                 REQTYPE_HOST_TO_INTERFACE,
                 CP210X_SET_BAUDDIV,
                 int(BAUD_RATE_GEN_FREQ / DEFAULT_BAUDRATE),
                 0,
                 buf,
                 (0 if buf is None else len(buf)),
                 USB_WRITE_TIMEOUT_MILLIS,
                 )

        print ("PORT INITIALIZED AND OPEN")


    # check for permission from the user and wait if required
    def checkPermission(self):
        ACTION_USB_PERMISSION = "com.access.device.USB_PERMISSION"
        intent = Intent(ACTION_USB_PERMISSION)
        try:
           pintent = PendingIntent.getBroadcast(self.context, 0, intent, 0)
        except Exception:
           pintent = PendingIntent.getBroadcast(self.context, 0, intent, PendingIntent.FLAG_IMMUTABLE)
        
        try:
           self.usbmanager.requestPermission(self.device, pintent)
           self.hasPermission = self.usbmanager.hasPermission(self.device)
        except:
           print ("no USB device")
           return False

        while not self.hasPermission:
            self.hasPermission = self.usbmanager.hasPermission(self.device)


    def displayWidgetScreen(self, button, message):
        MARGINTOP = 2
        LNUMWIDTH = 64
        SNUMWIDTH = 42

        scan_content = toga.Box(style=Pack(direction=COLUMN, margin=30))

        # Ascii ID and Mac at top of display
        idlabel  = toga.Label(self.buttonDict[button.id], style=Pack(flex=1, color="#000000", align_items=CENTER, font_size=32))
        maclabel = toga.Label(button.id, style=Pack(flex=1, color="#000000", align_items=CENTER, font_size=12))
        boxrowA  = toga.Box(children=[idlabel], style=Pack(direction=ROW, align_items=END, margin_top=4))
        boxrowB  = toga.Box(children=[maclabel], style=Pack(direction=ROW, align_items=END, margin_top=2))

        scan_content.add(boxrowA)
        scan_content.add(boxrowB)

        print (message)
        print (message[10])

        adr = adprot[message[11]]

        btn    = toga.Button(id=PTID, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Protothrottle ID", style=Pack(width=265, align_items=END, font_size=18))
        entry  = toga.TextInput(on_change=self.change_ptid, value=adr, style=Pack(height=45, justify_content="center", width=SNUMWIDTH, margin_bottom=2, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry, btn], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        addrbase = str(message[10])

        btn    = toga.Button(id=BASE, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Base ID", style=Pack(width=265, align_items=END, font_size=18))
        entry  = toga.NumberInput(on_change=self.change_ptid, value=addrbase, style=Pack(flex=1, height=45, width=SNUMWIDTH, margin_bottom=2, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry, btn], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        locoaddr = message[12]
        ch = message[13] << 8
        locoaddr = locoaddr | ch

        btn    = toga.Button(id=ADDR, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Loco Address", style=Pack(width=244, align_items=END, font_size=18))
        entry  = toga.NumberInput(on_change=self.change_ptid, value=locoaddr, min=0, max=9999, style=Pack(justify_content="start", height=48, width=LNUMWIDTH, margin_bottom=2, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry, btn], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        btn0   = toga.Button(id=COND, text="OFF", on_press = self.sendPrgCommand, style=Pack(width=80, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=14))
        btn1   = toga.Button(id=CONS, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Consist Address", style=Pack(width=164, align_items=END, font_size=18))
        entry  = toga.NumberInput(on_change=self.change_ptid, min=0, max=9999, style=Pack(flex=1, height=48, width=LNUMWIDTH, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, btn0, entry, btn1], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)
        
        btn    = toga.Button(id=DECO, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=10, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("DCC Addr", style=Pack(width=160, align_items=END, font_size=18))
        passth = toga.Switch("Fixed", id=SVR0, value=False, on_change=self.change_ptid)
        entry  = toga.NumberInput(on_change=self.change_ptid, min=0, max=9999, style=Pack(flex=1, height=48, width=LNUMWIDTH, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, passth, entry, btn], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        self.scroller = toga.ScrollContainer(content=scan_content, style=Pack(direction=COLUMN, align_items=CENTER))
        self.main_window.content = self.scroller
        self.main_window.show()


    def sendPrgCommand(self, widget):
        pass

    def change_ptid(self, widget):
        pass

def main():
    return PTApp()