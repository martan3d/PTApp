"""
Protothrottle Receiver App
"""

import toga
import asyncio
from toga.style import Pack
from toga import Button, MultilineTextInput, Label, TextInput
from toga.style.pack import COLUMN, ROW, CENTER, RIGHT, LEFT, START, END

from .xbee import *

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

# message codes for PT Receiver firmware data requests

RETURNTYPE       = 37

# Ids for buttons and text/numeric inputs

PTID  = 1000
PTIDV = 1100
BASE  = 1001
BASEV = 1101
ADDR  = 1002
ADDRV = 1102
CONS  = 1003
CONSV = 1103
COND  = 1004
CONDV = 1104
DECO  = 1005
DECOV = 1105
SRV0  = 1010
SRV0V = 1110
SRV1  = 1011
SRV1V = 1111
SRV2  = 1012
SRV2V = 1112
SRVM  = 1013
SRVMV = 1113
SVR0  = 1014
SVR0V = 1114
SVR1  = 1015
SVR1V = 1115
SVR2  = 1016
SVR2V = 1116
SV0L  = 1017
SV0LV = 1117
SV0H  = 1018
SV0HV = 1118
SV0H  = 1018
SV0HV = 1118
SV1L  = 1019
SV1LV = 1119
SV1H  = 1020
SV1HV = 1120
SV2L  = 1021
SV2LV = 1121
SV2H  = 1022
SV2HV = 1122
SRVP  = 1023
SRVPV = 1123
SRRP  = 1024
SRRPV = 1124

SRVP0  = 1025
SRVP0V = 1125
SRVP1  = 1026
SRVP1V = 1126
SRVP2  = 1027
SRVP2V = 1127

OUTX  = 1040
OUTXF = 1140
OUTXS = 1240
OUTY  = 1041
OUTYF = 1141
OUTYS = 1241
WDOG  = 1050
WDOGV = 1150
BRAT  = 1050
BRATV = 1150
BFNC  = 1061
BFNCV = 1161
ACCL  = 1062
ACCLV = 1162
DECL  = 1063
DECLV = 1163

class screens:
      SERVOSCREEN   = 3000
      PHYSICSSCREEN = 3100
      NOTCHESSCREEN = 3200



adprot = { 0x30 :'A', 0x31 :'B', 0x32 :'C', 0x33 :'D', 0x34 :'E', 0x35 :'F', 0x36 : 'G', 0x37 : 'H', 0x38 : 'I', 0x39 : 'J',
           0x3a : 'K', 0x3b : 'L', 0x3c : 'M', 0x3d : 'N', 0x3e : 'O', 0x3f : 'P', 0x40 : 'Q', 0x41 : 'R', 0x42 : 'S',
           0x43 : 'T', 0x44 : 'U', 0x45 : 'V', 0x46 : 'W', 0x47 : 'X', 0x48 : 'Y', 0x49 : 'Z' }


class PTApp(toga.App):

    def startup(self):

        self.Xbee = xbeeController()

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.setupAndroidSerialPort()
        self.displayMainWindow(0)



    def displayMainWindow(self, id):

        self.retries = 0

        self.discover_button = Button(
            'Scan',
            on_press=self.start_discover,
            style=Pack(width=120, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=12)
        )

        self.working_text = Label("", style=Pack(font_size=12, color="#000000"))

        scan_content = toga.Box(style=Pack(direction=COLUMN, align_items=CENTER, margin_top=5))
        scan_content.add(self.discover_button)
        scan_content.add(self.working_text)

        self.scroller = toga.ScrollContainer(content=scan_content, style=Pack(direction=COLUMN, align_items=CENTER))
        self.main_window.content = self.scroller
        self.main_window.show()


    async def start_discover(self, id):
        self.working_text.text = "Scanning for Receivers..."

        self.writebuff = bytearray([0x7E, 0x00, 0x04, 0x08, 0x01, 0x4E, 0x44, 0x64])
        self.writelen = len(self.writebuff)

        # send everything async so we don't impact GUI timing

        await self.connectWrite()
        await asyncio.sleep(2)
        await self.connectRead()

        # setup the screen buttons we will use for each receiver
        scan_content = toga.Box(style=Pack(direction=COLUMN, align_items=CENTER, margin_top=5))
        self.buttonDict = {}

        # set some default screen elements
        scan_content.add(self.discover_button)
        scan_content.add(self.working_text)
        self.working_text.text = ""

        # may be several responses, turn data into list of xbee api frames
        messages = await self.parseMessageData(self.readlen, self.readbuff)

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
                    style=Pack(width=230, height=120, margin_top=12, background_color="#bbbbbb", color="#000000", font_size=16))
            )

        # Render everything to the main window
        self.scroller = toga.ScrollContainer(content=scan_content, style=Pack(direction=COLUMN, align_items=CENTER))
        self.main_window.content = self.scroller
        self.main_window.show()

    # Pressed one of the receiver scanned buttons, so ask it for it's parameters
    async def connectToClient(self, widget):
        self.working_text.text = "Requesting Data from Receiver..."

        address = self.Xbee.buildAddress(widget.id)
        data = chr(RETURNTYPE) + "000000000000000000"
        buff = self.Xbee.buildXbeeTransmitData(address, data)

        self.writebuff = bytearray(buff)
        self.writelen = len(self.writebuff)
 
        # do the await thing to give time to the GUI thread
        await self.connectWrite()
        await asyncio.sleep(1)

#        print ("XBEE PROTOTHROTTLE REQUEST")

#        start = 16
#        length = 12
#        laddr = start & 0x00ff
#        haddr = (start & 0xff00) >> 8

        # now send a PT exclusive message out, memory read and see what comes back
#        xbeeMessage = self.Xbee.xbeeBroadCastRequest(48, 154, [ord('R'), laddr, haddr, length])

#        self.writebuff = bytearray(xbeeMessage)
#        self.writelen = len(self.writebuff)

        # do the await thing to give time to the GUI thread
#        await self.connectWrite()
#        await asyncio.sleep(1)

        # one or the other will answer
        await self.connectRead()

        # find the message we need, it's a specific API response from the receiver
        self.message = await self.parseReturnData(self.readlen, self.readbuff)

        print ("self.message ", self.message)

        # save the mac address
        self.macAddress = widget.id

        if not self.message:   # generally don't get it on the first try, just let user try again...
           self.working_text.text = "Failed, try again..."
           await asyncio.sleep(0.5)
           self.working_text.text = ""
           return

        if self.message[3] == 129:     # got a valid one, extract the data and build the display
           self.displayMainWidgetScreen(widget, self.message)
       
    
    # send message to Xbee
    async def connectWrite(self):
        self.connection.bulkTransfer(self.writeEndpoint, self.writebuff, self.writelen, USB_WRITE_TIMEOUT_MILLIS)

    # recieve message from Xbee
    async def connectRead(self):
        self.readbuff = bytearray(DEFAULT_READ_BUFFER_SIZE)
        self.readlen  = self.connection.bulkTransfer(self.readEndpoint, self.readbuff, DEFAULT_READ_BUFFER_SIZE, USB_READ_TIMEOUT_MILLIS)

    # Parse data and make a list of Node Discovery return messages
    async def parseMessageData(self, size, data):
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
        self.Protothrottle = {}

        if len(messages) <= 0: 
           return self.nodeData

        for msg in messages:
            mac = ""
            id  = ""
            adr16 = ""
            if len(msg) > 20:
               if msg[3] != 129:                  # Node discovery returned message, mac and ascii ID
                  for i in range(10, 18):
                     mac = mac + "{:02X}".format(msg[i])
                  for i in range(19, len(msg)-2):
                     id = id + chr(msg[i])
                  self.nodeData[mac] = id
               elif msg[7] == 2:                  # otherwise, it's broadcast data fram from PT, save 16 bit addr (always 0000?)
                  for i in range(4, 5):
                     adr16 = adr16 + "{:02X}".format(msg[i])
                  self.Protothrottle[adr16] = adr16
        return self.nodeData


    # Parse return data looking for 16 bit return and EEprom data
    async def parseReturnData(self, size, data):
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

#        for msg in messages:   # DEBUG
#            hexString = ""
#            for m in msg:
#                hexString = hexString + hex(m) + " "
#            print (hexString)

        if len(messages) <= 0: 
           return []

        for msg in messages:
            if len(msg) > 20:
               if msg[3] == 129 and msg[9] == 87:   # must be 16 bit return packet and a 'W' in the message to be valid
                  return msg

        # otherwise, see if there is a protothrottle return memory message in the list
        for msg in messages:
          if len(msg) > 13:
             if msg[13] == 0x72 and msg[7] == 2:   # lower case 'r' and broadcast
                return msg

        return []


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

        # Check USB Permissions, get them if needed, this does not return if you don't accept
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
    # NOTE: This will hang here if you choose 'no' when it asks you for permission

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

    def displayProtothrottleQuery(self, widget):
        print ("PROTOTHROTTLE")
        pass



    def displayMainWidgetScreen(self, button, message):
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

        ########################################################################  Build Receiver Main Screen

        adr = adprot[message[11]]   # pull value from received message, PT Main Address

        # Render PT address on the screen
        btn    = toga.Button(id=PTID, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Protothrottle ID", style=Pack(width=265, align_items=END, font_size=18))
        entry  = toga.TextInput(id=PTIDV, on_change=self.change_ptid, value=adr, style=Pack(height=45, justify_content="center", width=SNUMWIDTH, margin_bottom=2, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry, btn], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        ######################################################################## PT Base Address

        addrbase = str(message[10]) # PT base returned from receiver

        # Render PT base
        btn    = toga.Button(id=BASE, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Base ID", style=Pack(width=265, align_items=END, font_size=18))
        entry  = toga.NumberInput(id=BASEV, on_change=self.change_ptid, value=addrbase, style=Pack(flex=1, height=45, width=SNUMWIDTH, margin_bottom=2, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry, btn], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        ######################################################################## Loco Address, the address on the PT that the receiver responds to

        locoaddr = message[12]
        ch = message[13] << 8
        locoaddr = locoaddr | ch     # 16 bit loco address, this is the address that matches the PT address

        btn    = toga.Button(id=ADDR, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Loco Address", style=Pack(width=244, align_items=END, font_size=18))
        entry  = toga.NumberInput(id=ADDRV, on_change=self.change_ptid, value=locoaddr, min=0, max=9999, style=Pack(justify_content="start", height=48, width=LNUMWIDTH, margin_bottom=2, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry, btn], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        ######################################################################### Consist Address and setting

        cdir = message[16]
        consist = 'OFF'
        if cdir == 1: consist = 'FWD'
        if cdir == 2: consist = 'REV'

        consistaddr = message[14]
        ch = message[15] << 8
        consistaddr = consistaddr | ch

        btn0   = toga.Button(id=COND, text=consist, on_press = self.sendPrgCommand, style=Pack(width=80, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=14))
        btn1   = toga.Button(id=CONS, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Consist Address", style=Pack(width=164, align_items=END, font_size=18))
        entry  = toga.NumberInput(id=CONDV, on_change=self.change_ptid, value=consistaddr, min=0, max=9999, style=Pack(flex=1, height=48, width=LNUMWIDTH, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, btn0, entry, btn1], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        # ??
        
        btn    = toga.Button(id=DECO, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=10, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("DCC Addr", style=Pack(width=160, align_items=END, font_size=18))
        passth = toga.Switch("Fixed", id=SVR0, value=False, on_change=self.change_ptid)
        entry  = toga.NumberInput(id=DECOV, on_change=self.change_ptid, min=0, max=9999, style=Pack(flex=1, height=48, width=LNUMWIDTH, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, passth, entry, btn], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        wdog = 0  #adprot[message[11]]   # pull value from received message

        # WatchDog
        btn    = toga.Button(id=WDOG, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Watch Dog", style=Pack(width=265, align_items=END, font_size=18))
        entry  = toga.TextInput(id=WDOGV, on_change=self.change_ptid, value=wdog, style=Pack(height=45, justify_content="center", width=SNUMWIDTH, margin_bottom=2, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry, btn], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        # output X
        btn    = toga.Button(id=OUTX, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Output X", style=Pack(width=220, align_items=END, font_size=18))
        entry0 = toga.TextInput(id=OUTXF, on_change=self.change_ptid, value=wdog, style=Pack(height=45, justify_content="center", width=SNUMWIDTH, margin_bottom=2, font_size=18, background_color="#eeeeee", color="#000000"))
        entry1 = toga.TextInput(id=OUTXS, on_change=self.change_ptid, value=wdog, style=Pack(height=45, justify_content="center", width=SNUMWIDTH, margin_bottom=2, margin_left=4, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry0, entry1, btn], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        # output Y
        btn    = toga.Button(id=OUTY, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Output Y", style=Pack(width=220, align_items=END, font_size=18))
        entry0 = toga.TextInput(id=OUTYF, on_change=self.change_ptid, value=wdog, style=Pack(height=45, justify_content="center", width=SNUMWIDTH, margin_bottom=2, font_size=18, background_color="#eeeeee", color="#000000"))
        entry1 = toga.TextInput(id=OUTYS, on_change=self.change_ptid, value=wdog, style=Pack(height=45, justify_content="center", width=SNUMWIDTH, margin_bottom=2, margin_left=4, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry0, entry1, btn], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        boxrow = toga.Box(style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP, height=40))
        scan_content.add(boxrow)

        self.buttonSave = button

        scan = Button(
            'Scan',
            on_press=self.displayMainWindow,
            style=Pack(width=90, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=12)
        )

        servos = Button(
            'Servos',
            id=button.id,
            on_press=self.callServoScreen,
            style=Pack(width=90, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=12)
        )

        physics = Button(
            'Physics',
            on_press=self.callPhysicsScreen,
            style=Pack(width=90, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=12)
        )

        notches = Button(
            'Notch',
            on_press=self.callNotchesScreen,
            style=Pack(width=90, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=12)
        )

        boxrow = toga.Box(children=[scan, servos, physics, notches], style=Pack(direction=ROW, align_items=CENTER, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        self.scroller = toga.ScrollContainer(content=scan_content, style=Pack(direction=COLUMN, align_items=CENTER))
        self.main_window.content = self.scroller
        self.main_window.show()

    def sendPrgCommand(self, value):
        pass

    def change_ptid(self, widget):
        pass

    def callMainWidgetWindow(self, widget):
        self.displayMainWidgetScreen(widget, self.message)

    def callServoScreen(self, widget):
        self.displayServoScreen(self.buttonSave, self.message)

    def callPhysicsScreen(self, widget):
        self.displayPhysicsScreen(self.buttonSave, self.message)

    def callNotchesScreen(self, widget):
        self.displayNotchesScreen(self.buttonSave, self.message)


    #####################################################################

    # Servo Configure Screen
    def displayServoScreen(self, button, message):

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

        #############################################################  Servo Mode

        blank  = toga.Label("   ")
        boxrow = toga.Box(children=[blank, toga.Divider(), blank], style=Pack(direction=COLUMN, margin_top=20))
        scan_content.add(boxrow)

        btn    = toga.Button(id=SRVP, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Servo Mode", style=Pack(width=273, align_items=END, margin_bottom=10, font_size=18))
        mode   = toga.Button(id=SRVM, text="ESC", on_press = self.sendPrgCommand, style=Pack(width=90, height=55, background_color="#bbbbbb", color="#000000", font_size=12))
        boxrow = toga.Box(children=[desc, mode], style=Pack(direction=ROW, align_items=END, margin_top=20))
        scan_content.add(boxrow)

       ############################################################# 

        boxrow = toga.Box(children=[blank, toga.Divider(), blank], style=Pack(direction=COLUMN, margin_top=20))
        scan_content.add(boxrow)

       ############################################################# Servo 0 Config

        desc   = toga.Label("Servo 0", style=Pack(width=270, align_items=END, font_size=18))
        rev    = toga.Switch("Reverse", id=SVR0, value=False, on_change=self.change_ptid)
        boxrow = toga.Box(children=[desc, rev], style=Pack(direction=ROW, align_items=END, margin_top=8))
        scan_content.add(boxrow)

        btn    = toga.Button(id=SRVP0, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("     Function Code", style=Pack(width=282, align_items=END, font_size=12))
        func   = toga.NumberInput(on_change=self.change_ptid, min=0, max=99, style=Pack(flex=1, height=48, width=24, font_size=12, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, func, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        desc   = toga.Label("     Low Limit", style=Pack(width=244, align_items=END, font_size=12))
        entry0 = toga.NumberInput(on_change=self.change_ptid, min=0, max=1000, style=Pack(flex=1, height=48, width=LNUMWIDTH, font_size=18, background_color="#eeeeee", color="#000000"))
        btn    = toga.Button(id=SV0L, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        boxrow = toga.Box(children=[desc, entry0, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        desc   = toga.Label(" ", style=Pack(width=20, align_items=END, font_size=18))
        adj0   = toga.Slider(value=0, min=0, max=1000, on_change=self.setLimit, style=Pack(width=320, height=20))
        boxrow = toga.Box(children=[desc, adj0], style=Pack(direction=ROW, align_items=END))
        scan_content.add(boxrow)

        btn    = toga.Button(id=SV0H, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("     High Limit", style=Pack(width=244, align_items=END, font_size=12))
        entry1  = toga.NumberInput(on_change=self.change_ptid, min=0, max=9999, style=Pack(flex=1, height=48, width=LNUMWIDTH, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry1, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        desc   = toga.Label(" ", style=Pack(width=20, align_items=END, font_size=18))
        adj0   = toga.Slider(value=0, min=0, max=1000, on_change=self.setLimit, style=Pack(width=320, height=20))
        boxrow = toga.Box(children=[desc, adj0], style=Pack(direction=ROW, align_items=END))
        scan_content.add(boxrow)

        ############################################################# 

        boxrow = toga.Box(children=[blank, toga.Divider(), blank], style=Pack(direction=COLUMN, margin_top=20))
        scan_content.add(boxrow)

       ############################################################# Servo 1 Config

        desc   = toga.Label("Servo 1", style=Pack(width=270, align_items=END, font_size=18))
        rev    = toga.Switch("Reverse", id=SVR1, value=False, on_change=self.change_ptid)
        boxrow = toga.Box(children=[desc, rev], style=Pack(direction=ROW, align_items=END, margin_top=8))
        scan_content.add(boxrow)

        btn    = toga.Button(id=SRVP1, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("     Function Code", style=Pack(width=282, align_items=END, font_size=12))
        func   = toga.NumberInput(on_change=self.change_ptid, min=0, max=99, style=Pack(flex=1, height=48, width=24, font_size=12, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, func, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        desc   = toga.Label("     Low Limit", style=Pack(width=244, align_items=END, font_size=12))
        entry0 = toga.NumberInput(on_change=self.change_ptid, min=0, max=1000, style=Pack(flex=1, height=48, width=LNUMWIDTH, font_size=18, background_color="#eeeeee", color="#000000"))
        btn    = toga.Button(id=SV1L, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        boxrow = toga.Box(children=[desc, entry0, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        desc   = toga.Label(" ", style=Pack(width=20, align_items=END, font_size=18))
        adj0   = toga.Slider(value=0, min=0, max=1000, on_change=self.setLimit, style=Pack(width=320, height=20))
        boxrow = toga.Box(children=[desc, adj0], style=Pack(direction=ROW, align_items=END))
        scan_content.add(boxrow)

        btn    = toga.Button(id=SV1H, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("     High Limit", style=Pack(width=244, align_items=END, font_size=12))
        entry1  = toga.NumberInput(on_change=self.change_ptid, min=0, max=9999, style=Pack(flex=1, height=48, width=LNUMWIDTH, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry1, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        desc   = toga.Label(" ", style=Pack(width=20, align_items=END, font_size=18))
        adj0   = toga.Slider(value=0, min=0, max=1000, on_change=self.setLimit, style=Pack(width=320, height=20))
        boxrow = toga.Box(children=[desc, adj0], style=Pack(direction=ROW, align_items=END))
        scan_content.add(boxrow)

        ############################################################# 

        boxrow = toga.Box(children=[blank, toga.Divider(), blank], style=Pack(direction=COLUMN, margin_top=20))
        scan_content.add(boxrow)

        ############################################################# Servo 2 Config

        desc   = toga.Label("Servo 2", style=Pack(width=270, align_items=END, font_size=18))
        rev    = toga.Switch("Reverse", id=SVR2, value=False, on_change=self.change_ptid)
        boxrow = toga.Box(children=[desc, rev], style=Pack(direction=ROW, align_items=END, margin_top=8))
        scan_content.add(boxrow)

        btn    = toga.Button(id=SRVP2, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("     Function Code", style=Pack(width=282, align_items=END, font_size=12))
        func   = toga.NumberInput(on_change=self.change_ptid, min=0, max=99, style=Pack(flex=1, height=48, width=24, font_size=12, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, func, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        desc   = toga.Label("     Low Limit", style=Pack(width=244, align_items=END, font_size=12))
        entry0 = toga.NumberInput(on_change=self.change_ptid, min=0, max=1000, style=Pack(flex=1, height=48, width=LNUMWIDTH, font_size=18, background_color="#eeeeee", color="#000000"))
        btn    = toga.Button(id=SV2L, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        boxrow = toga.Box(children=[desc, entry0, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        desc   = toga.Label(" ", style=Pack(width=20, align_items=END, font_size=18))
        adj0   = toga.Slider(value=0, min=0, max=1000, on_change=self.setLimit, style=Pack(width=320, height=20))
        boxrow = toga.Box(children=[desc, adj0], style=Pack(direction=ROW, align_items=END))
        scan_content.add(boxrow)

        btn    = toga.Button(id=SV2H, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("     High Limit", style=Pack(width=244, align_items=END, font_size=12))
        entry1  = toga.NumberInput(on_change=self.change_ptid, min=0, max=9999, style=Pack(flex=1, height=48, width=LNUMWIDTH, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry1, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        desc   = toga.Label(" ", style=Pack(width=20, align_items=END, font_size=18))
        adj0   = toga.Slider(value=0, min=0, max=1000, on_change=self.setLimit, style=Pack(width=320, height=20))
        boxrow = toga.Box(children=[desc, adj0], style=Pack(direction=ROW, align_items=END))
        scan_content.add(boxrow)

        scan = Button(
            'Scan',
            on_press=self.displayMainWindow,
            style=Pack(width=120, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=12)
        )

        main = Button(
            'Main',
            id=button.id,
            on_press=self.callMainWidgetWindow,
            style=Pack(width=120, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=12)
        )

        boxrow = toga.Box(children=[scan, main], style=Pack(direction=ROW, align_items=CENTER, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        self.scroller = toga.ScrollContainer(content=scan_content, style=Pack(direction=COLUMN, align_items=CENTER))
        self.main_window.content = self.scroller
        self.main_window.show()


    def setLimit(self, id):
        pass


    def displayPhysicsScreen(self, button, message):
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

        btn    = toga.Button(id=BRAT, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Brake Rate", style=Pack(width=262, align_items=END, font_size=18))
        func   = toga.NumberInput(id=BRATV, on_change=self.change_ptid, min=0, max=99, style=Pack(flex=1, height=48, width=48, font_size=12, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, func, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        btn    = toga.Button(id=BFNC, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Brake Rate FnCode", style=Pack(width=262, align_items=END, font_size=18))
        func   = toga.NumberInput(id=BFNCV, on_change=self.change_ptid, min=0, max=99, style=Pack(flex=1, height=48, width=48, font_size=12, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, func, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        btn    = toga.Button(id=ACCL, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Acceleration", style=Pack(width=262, align_items=END, font_size=18))
        func   = toga.NumberInput(id=ACCLV, on_change=self.change_ptid, min=0, max=99, style=Pack(flex=1, height=48, width=48, font_size=12, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, func, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        btn    = toga.Button(id=DECL, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Deceleration", style=Pack(width=262, align_items=END, font_size=18))
        func   = toga.NumberInput(id=DECLV, on_change=self.change_ptid, min=0, max=99, style=Pack(flex=1, height=48, width=48, font_size=12, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, func, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)


        scan = Button(
            'Scan',
            on_press=self.displayMainWindow,
            style=Pack(width=120, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=12)
        )

        main = Button(
            'Main',
            id=button.id,
            on_press=self.callMainWidgetWindow,
            style=Pack(width=120, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=12)
        )


        boxrow = toga.Box(children=[scan, main], style=Pack(direction=ROW, align_items=CENTER, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        self.scroller = toga.ScrollContainer(content=scan_content, style=Pack(direction=COLUMN, align_items=CENTER))
        self.main_window.content = self.scroller
        self.main_window.show()


    def displayNotchesScreen(self, button, message):
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

        scan = Button(
            'Scan',
            on_press=self.displayMainWindow,
            style=Pack(width=120, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=12)
        )

        main = Button(
            'Main',
            id=button.id,
            on_press=self.callMainWidgetWindow,
            style=Pack(width=120, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=12)
        )


        boxrow = toga.Box(children=[scan, main], style=Pack(direction=ROW, align_items=CENTER, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        self.scroller = toga.ScrollContainer(content=scan_content, style=Pack(direction=COLUMN, align_items=CENTER))
        self.main_window.content = self.scroller
        self.main_window.show()






def main():
    return PTApp()