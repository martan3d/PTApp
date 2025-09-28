"""
Protothrottle Receiver App
"""

import toga
import asyncio
from toga.style import Pack
from toga import Button, MultilineTextInput, Label, TextInput
from toga.style.pack import COLUMN, ROW, CENTER, RIGHT, LEFT, START, END, HIDDEN, VISIBLE

from .xbee import *

if toga.platform.current_platform == 'android':
   from java import jclass
   from android.content import Context
   # Android Java Class names, used for permissions
   Intent = jclass('android.content.Intent')
   PendingIntent = jclass('android.app.PendingIntent')
   from android.content import ContentResolver
   from android.provider import MediaStore
   from android.app import Activity


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

# Ids for buttons and text/numeric inputs

PTID  = 'PTID'
PTIDV = 'PTIDV'
BASE  = 'BASE'
BASEV = 'BASEV'
ADDR  = 'ADDR'
ADDRV = 'ADDRV'
CONS  = 'CONS'
CONSV = 'CONSV'
COND  = 'COND'
CONDV = 'CONDV'
DECO  = 'DECO'
DECOV = 'DECOV'

# Servo screen widget IDs

SV0R   = 'SV0R'      # reverse switch
SV0LP  = 'SV0LP'     # low program button
SV0LV  = 'SV0LV'     # low limit value
SV0LVS = 'SV0LVS'    # low limit slider value
SV0HP  = 'SV0HP'     # High limit program button
SV0HV  = 'SV0HV'     # High Limit value
SV0HVS = 'SV0HVS'    # Hight Limit Slider value

SV1R   = 'SV1R'      # reverse switch
SV1LP  = 'SV1LP'     # low program button
SV1LV  = 'SV1LV'     # low limit value
SV1LVS = 'SV1LVS'    # low limit slider value
SV1HP  = 'SV1HP'     # High Limit Program
SV1HV  = 'SV1HV'     # High Limit Value
SV1HVS = 'SV1HVS'    # High Limit Slider Value
SV1FC  = 'SV1FC'     # Function code
SV1FCP = 'SV1FCP'    # Function code program button

SV2R   = 'SV2R'      # reverse switch
SV2LP  = 'SV2LP'     # low program button
SV2LV  = 'SV2LV'     # low limit value
SV2LVS = 'SV2LVS'    # low limit slider value
SV2HP  = 'SV2HP'     # High Limit Program Button
SV2HV  = 'SV2HV'     # High Limit value
SV2HVS = 'SV2HVS'    # High Limit slider value
SV2FC  = 'SV2FC'     # Function code
SV2FCP = 'SV2FCP'    # Function code program button

DCCM  = 'DCCM'       # DCC Address fixed or pass through
DCCA  = 'DCCA'       # DCC Address if fixed

SVRM  = 'SVRM'
SRVP  = 'SRVP'
SRVPV = 'SRVPV'
SRRP  = 'SRRP'
SRRPV = 'SRRPV'

SRVP0  = 'SRVP0'
SRVP0V = 'SRVP0V'
SRVP1  = 'SRVP1'
SRVP1V = 'SRVP1V'
SRVP2  = 'SRVP2'
SRVP2V = 'SRVP2V'

OUTX  = 'OUTX'
OUTXF = 'OUTXF'
OUTXS = 'OUTXS'
OUTY  = 'OUTY'
OUTYF = 'OUTYF'
OUTYS = 'OUTYS'
WDOG  = 'WDOG'
WDOGV = 'WDOGV'
BRAT  = 'BRAT'
BRATV = 'BRATV'
BFNC  = 'BFNC'
BFNCV = 'BFNCV'
ACCL  = 'ACCL'
ACCLV = 'ACCLV'
DECL  = 'DECL'
DECLV = 'DECLV'

NTINL1 = 'NTINL1'
NTINL2 = 'NTINL2'
NTINL3 = 'NTINL3'
NTINL4 = 'NTINL4'
NTINL5 = 'NTINL5'
NTINL6 = 'NTINL6'
NTINL7 = 'NTINL7'
NTINL8 = 'NTINL8'

NTINH1 = 'NTINH1'
NTINH2 = 'NTINH2'
NTINH3 = 'NTINH3'
NTINH4 = 'NTINH4'
NTINH5 = 'NTINH5'
NTINH6 = 'NTINH6'
NTINH7 = 'NTINH7'
NTINH8 = 'NTINH8'

NTOUT1 = 'NTOUT1'
NTOUT2 = 'NTOUT2'
NTOUT3 = 'NTOUT3'
NTOUT4 = 'NTOUT4'
NTOUT5 = 'NTOUT5'
NTOUT6 = 'NTOUT6'
NTOUT7 = 'NTOUT7'
NTOUT8 = 'NTOUT8'

NTPRG1 = 'NTPRG1'
NTPRG2 = 'NTPRG2'
NTPRG3 = 'NTPRG3'
NTPRG4 = 'NTPRG4'
NTPRG5 = 'NTPRG5'
NTPRG6 = 'NTPRG6'
NTPRG7 = 'NTPRG7'
NTPRG8 = 'NTPRG8'

XBEA   = 'XBEA'


# MESSAGE IDS for Receiver message side
GETPHYSICS           = 53
RETURNNOTCHES        = 36 
RETURNTYPE           = 37

SETBASEADDRESS       = 38
SETPROTOADDRESS      = 39
SETLOCOADDRESS       = 40
SETCONSISTADDRESS    = 45
SETCONSISTDIRECTION  = 46
SETSERVOCONFIG       = 47
SETTIMEOUT           = 25
SETOUTPUTSMODE       = 26
SETSERVOMODE         = 48
SETACCELERATION      = 54
SETDECELERATION      = 55
SETBRAKERATE         = 56
SETBRAKEFUNCTION     = 57
FACTORYRESET         = 58
SETNOTCHMASK         = 51
SETDCCCVPACKET       = 16
SETDCCPASSTHRU       = 63
SETDCCADDRESS        = 62

adprot = { 0x30 :'A', 0x31 :'B', 0x32 :'C', 0x33 :'D', 0x34 :'E', 0x35 :'F', 0x36 : 'G', 0x37 : 'H', 0x38 : 'I', 0x39 : 'J',
           0x3a : 'K', 0x3b : 'L', 0x3c : 'M', 0x3d : 'N', 0x3e : 'O', 0x3f : 'P', 0x40 : 'Q', 0x41 : 'R', 0x42 : 'S',
           0x43 : 'T', 0x44 : 'U', 0x45 : 'V', 0x46 : 'W', 0x47 : 'X', 0x48 : 'Y', 0x49 : 'Z' }

##
## Main Toga Class and startup
##

class PTApp(toga.App):

    def startup(self):

        self.Xbee = xbeeController()
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.setupAndroidSerialPort()
        self.displayMainWindow(0)

##
## Main window, construct it here, make it's parts available to this class
##

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

        throttle = Button(
            'Throttle',
            on_press=self.callThrottleScreen,
            style=Pack(width=120, height=60, margin_top=10, background_color="#cccccc", color="#000000", font_size=12)
        )

        boxrow = toga.Box(children=[throttle], style=Pack(direction=ROW, align_items=CENTER, margin_top=20))
        scan_content.add(boxrow)

        self.scroller = toga.ScrollContainer(content=scan_content, style=Pack(direction=COLUMN, align_items=CENTER))
        self.main_window.content = self.scroller
        self.main_window.show()

##
## Pressed Scan button, look for all Xbees on the Network
##

    async def start_discover(self, id):
        self.working_text.text = "Scanning Network for Xbee Devices..."

        self.saveWidgetId = None

        # Broadcast Network Discovery, all Xbees respond with MAC and ascii ID
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

##
## Pressed one of the resulting device buttons, ask it for it's parameters
##

    async def connectToClient(self, widget):
        self.working_text.text = "Requesting Data from Receiver..."
        self.message = []

        if self.saveWidgetId != widget.id:
           self.retries = 0

        self.saveWidgetId = widget.id

        # if we have tried > 2 times and no answer, probably not a receiver, look for a protothrottle
        if self.retries > 1:
           self.retries = 0
           self.working_text.text = "Searching for Protothrottle..."
           await self.getProtothrottle()
           return

        # assume it's a receiver
        address = self.Xbee.buildAddress(widget.id)
        data = chr(RETURNTYPE) + "000000000000000000"
        buff = self.Xbee.buildXbeeTransmitData(address, data)

        self.writebuff = bytearray(buff)
        self.writelen = len(self.writebuff)
 
        await self.connectWrite()
        await asyncio.sleep(1)
        await self.connectRead()

        # find the message we need, it's a specific API response from the receiver
        self.message = await self.parseReturnData(self.readlen, self.readbuff, 87)
        print ("self.message Rx Query ", self.message)

        # save the mac address
        self.macAddress = widget.id

        if not self.message:   # generally don't get it on the first try, just let user try again...
           self.working_text.text = "Failed, try again, third retry looks for Protothrottle"
           self.retries = self.retries + 1
           await asyncio.sleep(0.75)
           self.working_text.text = ""
           return

        if self.message[3] == 129:     # got a valid one, extract the data and build the display
           self.displayMainWidgetScreen(widget, self.message)
       
##
## Read and Write Serial Port to send/receive messages from Xbee Dongle
##

    # send message to Xbee
    async def connectWrite(self):
        self.connection.bulkTransfer(self.writeEndpoint, self.writebuff, self.writelen, USB_WRITE_TIMEOUT_MILLIS)

    # recieve message from Xbee
    async def connectRead(self):
        self.readbuff = bytearray(DEFAULT_READ_BUFFER_SIZE)
        self.readlen  = self.connection.bulkTransfer(self.readEndpoint, self.readbuff, DEFAULT_READ_BUFFER_SIZE, USB_READ_TIMEOUT_MILLIS)

    # Set the readbuffer size externally
    async def connectLargeRead(self, size):
        self.readbuff = bytearray(size)
        self.readlen  = self.connection.bulkTransfer(self.readEndpoint, self.readbuff, size, USB_READ_TIMEOUT_MILLIS)


##
## Parse data and make a list of Node Discovery return messages
## Use this data to build list of buttons for screen display
##

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
        return self.nodeData

##
## Assume we are talking to a protothrottle, send it MRBUS messages 
## to get slot configs. If we get data back, it's a protothrottle
##

    async def getProtothrottle(self):
        self.protomessages = await self.queryProtothrottle()

        if len(self.protomessages) != 0:
           self.working_text.text = ""
           self.displayProtothrottleScreen(self.protomessages)
        else:
           self.retries = 0
           self.working_text.text = "No Protothrottle Found..."
           await asyncio.sleep(.25)
           self.working_text.text = ""

##
## Send MRBUS requests and accumulate responses
##

    async def queryProtothrottle(self):

        slotindex = 128

        lad = slotindex & 0x00ff
        had = (slotindex & 0xff00) >> 8

        xbeeFrame = self.Xbee.xbeeBroadCastRequest(48, 154, [ord('R'), lad, had, 12])
        self.writebuff = bytearray(xbeeFrame)
        self.writelen = len(self.writebuff)

        await self.connectWrite()
        await asyncio.sleep(.1)
        await self.connectRead()

        print ("look for PT, check return data ")

        if self.readbuff[0] == 0:
           return []

        self.working_text.text = "Retrieve Slot Data from Protothrottle"

        messages = []
        msgsave = []
        slotindex = 128

        MAXSLOTS = 10    # maximum number of slots we can retrieve?  Should be 20 but gets 'stuck' if we ask for more.

        i = 0

        while True:

            lad = slotindex & 0x00ff
            had = (slotindex & 0xff00) >> 8

            xbeeFrame = self.Xbee.xbeeBroadCastRequest(48, 154, [ord('R'), lad, had, 12])
            self.writebuff = bytearray(xbeeFrame)
            self.writelen = len(self.writebuff)

            await self.connectWrite()
            await asyncio.sleep(.1)
            await self.connectRead()

            # parse out the data the PT sends back
            msg = self.Xbee.getPacket(self.readbuff)

            if msg == None:
               continue

            if len(msg) < 28:
               continue

            if msgsave == msg:
               continue

            i += 1

            self.working_text.text = "Get offset " + str(slotindex)

            print (i, msg, slotindex, len(msg))

            msgsave = msg
            messages.append(msg)
            slotindex = slotindex + 128

            if slotindex > (128*MAXSLOTS):
               self.working_text.text = ""
               return messages      


##
## Parse return data looking for 16 bit return and Receiver return data
##

    async def parseReturnData(self, size, data, msgcode):
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

        if len(messages) <= 0: 
           return []

        for msg in messages:
            if len(msg) > 20:
               if msg[3] == 129 and msg[9] == msgcode:   # must be 16 bit return packet and a 'W' in the message to be valid
                  return msg

        return []

##
## Android open serial port, will fail if no Dongle detected
##

    def setupAndroidSerialPort(self):
        # Android Specific
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

        self.connection = self.usbmanager.openDevice(self.device)
        self.interface = self.device.getInterface(0)
        self.readEndpoint = self.interface.getEndpoint(0)
        self.writeEndpoint = self.interface.getEndpoint(1)

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

##
## check for permission from the user and wait if required
## NOTE: This will hang here if you choose 'no' when it asks you for permission
## The only way out is to end the program
##

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

##
##
## Display Protothrottle Screen
##
##

    def displayProtothrottleScreen(self, message):
        MARGINTOP = 2
        LNUMWIDTH = 64
        SNUMWIDTH = 42

        scan_content = toga.Box(style=Pack(direction=COLUMN, margin_left=6))

        # Ascii ID and Mac at top of display
        idlabel  = toga.Label(self.buttonDict[self.macAddress], style=Pack(flex=1, color="#000000", align_items=CENTER, font_size=32))
        maclabel = toga.Label(self.macAddress, style=Pack(flex=1, color="#000000", align_items=CENTER, font_size=12))
        boxrowA  = toga.Box(children=[idlabel], style=Pack(direction=ROW, align_items=END, margin_top=4))
        boxrowB  = toga.Box(children=[maclabel], style=Pack(direction=ROW, align_items=END, margin_top=2))

        scan_content.add(boxrowA)
        scan_content.add(boxrowB)

        blank  = toga.Label("   ")
        scan_content.add(blank)

        self.pt_text = Label("", style=Pack(font_size=12, color="#000000"))
        scan_content.add(self.pt_text)

        msave = []
        slot = 0

        for m in message:
            if m != []:
               la = m[16]
               lh = m[17] << 8
               adr = lh | la                       # first two bytes are the locomotive address, go ahead and print that 

               if m[7:] == msave[7:]:                      # toss any duplicates
                  continue

               msave = m

               p0 = f"{adr:4d}"

               idS = "S:"+str(slot)+":"+p0
               idL = "L:"+str(slot)+":"+p0
               idE = "E:"+str(slot)+":"+p0

               slot = slot + 1

               ptlabel = toga.Label(p0, style=Pack(width=100, color="#000000", align_items=END, font_size=28))
               load = Button("Load", id=idL, on_press=self.loadSlot, style=Pack(width=80, height=50, margin_top=5, background_color="#cccccc", color="#000000", font_size=10))
               save = Button("Save", id=idS, on_press=self.saveSlot, style=Pack(width=80, height=50, margin_top=5, background_color="#cccccc", color="#000000", font_size=10))
               edit = Button("Edit", id=idE, on_press=self.editSlot, style=Pack(width=80, height=50, margin_top=5, background_color="#cccccc", color="#000000", font_size=10))
               boxrow = toga.Box(children=[ptlabel, load, save, edit], style=Pack(direction=ROW, align_items=END, margin_top=4))
               scan_content.add(boxrow)

               boxrow = toga.Box(children=[blank, toga.Divider(), blank], style=Pack(direction=ROW, align_items=END))
               scan_content.add(boxrow)

        scan = Button(
            'Scan',
            on_press=self.displayMainWindow,
            style=Pack(width=120, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=12)
        )

        loadAll = Button(
            'Load All',
            on_press=self.displayMainWindow,
            style=Pack(width=120, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=12)
        )

        saveAll = Button(
            'Save All',
            on_press=self.displayMainWindow,
            style=Pack(width=120, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=12)
        )

        boxrow = toga.Box(children=[scan, loadAll, saveAll], style=Pack(direction=ROW, align_items=CENTER, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        self.scroller = toga.ScrollContainer(content=scan_content, style=Pack(direction=COLUMN, align_items=CENTER))
        self.main_window.content = self.scroller
        self.main_window.show()

##
## load slot data from app memory (disk), then send to PT slot
##

    async def loadSlot(self, id):

        s = id.id.split(":")
        slot = "Slot: "+ s[1] + " - " + s[2]
        self.sid = int(s[1])

        fileChose = Intent(Intent.ACTION_GET_CONTENT)
        fileChose.addCategory(Intent.CATEGORY_OPENABLE)
        fileChose.setType("*/*")

        results = await self._impl.intent_result(Intent.createChooser(fileChose, "Choose a file"))

        if True: #try:
           data = results['resultData'].getData()
           context = self._impl.native
           bytesJarray = bytes((context.getContentResolver().openInputStream(data).readAllBytes()))

           await self.sendSlotData(self.sid, list(bytesJarray))

#        except:
#           self.working_text.text = "Load Canceled"
#           await asyncio.sleep(.2)

        self.working_text.text = ""



##
## Save slot data to internal Documents Folder
##

    async def saveSlot(self, id):
        s = id.id.split(":")
        slot = "Slot: "+ s[1] + " - " + s[2]
        self.sid = int(s[1])
        filename = s[2] + ".pts"   # Protothrottle single slot config

        slotdata = await self.getSlotData(self.sid+1)
        datarecord = bytearray(slotdata)

        intent = Intent(Intent.ACTION_CREATE_DOCUMENT)
        intent.addCategory(Intent.CATEGORY_OPENABLE)
#         intent.setType("text/plain")  # Or desired MIME type
        intent.setType("*/*")  # desired MIME type
        intent.putExtra(Intent.EXTRA_TITLE, filename)
        
        results = await self.app._impl.intent_result(intent)

        try:
            if results['resultCode'] == Activity.RESULT_OK:
               uri = results['resultData'].getData()
               context = self._impl.native
               content_resolver = context.getContentResolver()
               output_stream = content_resolver.openOutputStream(uri)
               output_stream.write(datarecord)
               output_stream.close()
        except:
            pass

##
## Redisplay all slots on protothrottle window
##

    def backtoProtothrottle(self, id):
        self.displayProtothrottleScreen(self.protomessages)

##
## Send already collected data to a PT slot
##


    async def sendSlotData(self, slot, data):
        MAXRETRIES = 30
        slotindex = slot*128
        i = 0

        while i < 52:
            lad = slotindex & 0x00ff
            had = (slotindex & 0xff00) >> 8

            datalist = [ord('W'), lad, had]
            for j in range(0,12):
                try:
                   datalist.append(data[i])
                except:
                   i = 65

                i = i + 1

            xbeeFrame = self.Xbee.xbeeBroadCastRequest(48, 154, datalist)

            self.writebuff = bytearray(xbeeFrame)
            self.writelen = len(self.writebuff)

            await self.connectWrite()
            await asyncio.sleep(.1)

            retries = 0
            packetvalid = False

            # Read back data from PT to see if it 'took'

            for x in range(0, MAXRETRIES):
                xbeeFrame = self.Xbee.xbeeBroadCastRequest(48, 154, [ord('R'), lad, had, 12])
                self.writebuff = bytearray(xbeeFrame)
                self.writelen = len(self.writebuff)

                await self.connectWrite()
                await asyncio.sleep(.1)
                await self.connectRead()

                msg = self.Xbee.getPacket(self.readbuff)
                print ("---------- offset", slotindex, "retry ", x, "total bytes ", i)
                print ("WR data ", datalist[3:])
                print ("RD data ", msg[16:])
                
                # readback - if compare is true, break and move on to next 12 bytes
                if datalist[3:] == msg[16:]:
                   print ("MATCH")
                   packetvalid = True
                   break
                else:
                   print ("FAILED MATCH")

            if packetvalid:
               slotindex = slotindex + 12   # only increment if read/write matches


##
## Query the PT for the full data record return as list
##

    async def getSlotData(self, sid):
        slotindex = sid*128
        datarecord = [] 
        msgsave = []
        i = 0

        while True:
            lad = slotindex & 0x00ff
            had = (slotindex & 0xff00) >> 8

            xbeeFrame = self.Xbee.xbeeBroadCastRequest(48, 154, [ord('R'), lad, had, 12])
            self.writebuff = bytearray(xbeeFrame)
            self.writelen = len(self.writebuff)

            await self.connectWrite()
            await asyncio.sleep(.1)
            await self.connectRead()

            msg = self.Xbee.getPacket(self.readbuff)

            if msg == None:          # got nothing, try again
               continue

            if len(msg) < 28:        # truncated, try again
               continue

            if msg == msgsave:       # duplicate, try again
               continue

            msgsave = msg

            self.working_text.text = "Read PT memory " + str(slotindex)
            print (slotindex, msg, len(msg))

            for j in range(16, len(msg)-1):         # trim off the header info and the checksum from the xbee return message
               datarecord.append(msg[j])

            slotindex = slotindex + 12

            i = i + 1
            if i > 6:
               break

        self.working_text.text = ""
        return datarecord



    def editSlot(self, id):
        scan_content = toga.Box(style=Pack(direction=COLUMN, margin_left=6))

    def handle_focus(self, widget):
        native_view = widget._impl
        # Set the background to null to remove the default line.
        native_view.set_background(None)


##
###  Main Receiver Configure Screen
##

    def displayMainWidgetScreen(self, button, message):
        MARGINTOP = 2
        LNUMWIDTH = 64
        SNUMWIDTH = 42

        scan_content = toga.Box(style=Pack(direction=COLUMN, margin_left=6))

        # Ascii ID and Mac at top of display
        btn      = toga.Button(text="Prg", on_press=self.change_xbeeAddr, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        idlabel  = toga.TextInput(id=XBEA, value=self.buttonDict[button.id], style=Pack(flex=1, color="#000000", align_items=CENTER, font_size=32))
        maclabel = toga.Label(button.id, style=Pack(flex=1, color="#000000", align_items=CENTER, font_size=12))
        boxrowA  = toga.Box(children=[idlabel, btn], style=Pack(direction=ROW, align_items=END, margin_top=4))
        boxrowB  = toga.Box(children=[maclabel], style=Pack(direction=ROW, align_items=END, margin_top=2))

        scan_content.add(boxrowA)
        scan_content.add(boxrowB)

        ########################################################################  Build Receiver Main Screen

        adr = adprot[message[11]]   # pull value from received message, PT Main Address

        # Render PT address on the screen
        btn    = toga.Button(id=PTID, text="Prg", on_press = self.change_ptidaddr, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Protothrottle ID", style=Pack(width=265, align_items=END, font_size=18))
        entry  = toga.TextInput(id=PTIDV, on_change=self.change_ptidaddr, value=adr, style=Pack(text_align=RIGHT, height=45, justify_content="center", width=SNUMWIDTH, margin_bottom=2, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry, btn], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        ######################################################################## PT Base Address

        addrbase = str(message[10]) # PT base returned from receiver

        # Render PT base
        btn    = toga.Button(id=BASE, text="Prg", on_press = self.change_ptidbase, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Base ID", style=Pack(width=265, align_items=END, font_size=18))
        entry  = toga.NumberInput(id=BASEV, value=addrbase, style=Pack(text_align=RIGHT, flex=1, height=45, width=SNUMWIDTH, margin_bottom=2, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry, btn], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        ######################################################################## Loco Address, the address on the PT that the receiver responds to

        locoaddr = message[12]
        ch = message[13] << 8
        locoaddr = locoaddr | ch     # 16 bit loco address, this is the address that matches the PT address

        btn    = toga.Button(id=ADDR, text="Prg", on_press = self.change_locoAddr, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Loco Address", style=Pack(width=244, align_items=END, font_size=18))
        entry  = toga.NumberInput(id=ADDRV, value=locoaddr, min=0, max=9999, style=Pack(text_align=RIGHT, justify_content="start", height=48, width=LNUMWIDTH, margin_bottom=2, font_size=18, background_color="#eeeeee", color="#000000"))
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

        btn0   = toga.Button(id=COND, text=consist, on_press = self.change_ConsistMode, style=Pack(width=80, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=14))
        btn1   = toga.Button(id=CONS, text="Prg", on_press = self.change_ConsistAddr, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Consist Address", style=Pack(width=164, align_items=END, font_size=18))
        entry  = toga.NumberInput(id=CONDV, text_align=RIGHT, value=consistaddr, min=0, max=9999, style=Pack(text_align=RIGHT, flex=1, height=48, width=LNUMWIDTH, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, btn0, entry, btn1], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        # ?? DCC address and passthrough, only latest firmware supports this

        
        btn    = toga.Button(id=DECO, text="Prg", on_press = self.change_DCCAddress, style=Pack(width=55, height=55, margin_top=10, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("DCC Addr", style=Pack(width=160, align_items=END, font_size=18))
        passth = toga.Switch("Fixed", id=DCCM, value=False, on_change=self.change_DCCMode)
        entry  = toga.NumberInput(id=DCCA, value=3, min=0, max=9999, style=Pack(text_align=RIGHT, flex=1, height=48, width=LNUMWIDTH, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, passth, entry, btn], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        wdog = chr(message[11])   # pull watchdog value from received message

        # WatchDog
        btn    = toga.Button(id=WDOG, text="Prg", on_press = self.change_WatchDog, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Watch Dog", style=Pack(width=265, align_items=END, font_size=18))
        entry  = toga.TextInput(id=WDOGV, value=wdog, style=Pack(text_align=RIGHT, height=45, justify_content="center", width=SNUMWIDTH, margin_bottom=2, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry, btn], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        outxfn = message[35] & 0x7f  # X function code
        outx   = (message[35] & 0x80) >> 7

        # output X
        btn    = toga.Button(id=OUTX, text="Prg", on_press = self.change_OutputX, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Output X", style=Pack(width=220, align_items=END, font_size=18))
        entry0 = toga.TextInput(id=OUTXF, value=outxfn, style=Pack(text_align=RIGHT, height=45, width=SNUMWIDTH, margin_bottom=2, font_size=18, background_color="#eeeeee", color="#000000"))
        entry1 = toga.TextInput(id=OUTXS, value=outx, style=Pack(text_align=RIGHT, height=45, width=SNUMWIDTH, margin_bottom=2, margin_left=4, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry0, entry1, btn], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        outyfn = message[36] & 0x7f
        outy   = (message[36] & 0x80) >> 7

        # output Y
        btn    = toga.Button(id=OUTY, text="Prg", on_press = self.change_OutputY, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Output Y", style=Pack(width=220, align_items=END, font_size=18))
        entry0 = toga.TextInput(id=OUTYF, value=outyfn, style=Pack(text_align=RIGHT, height=45, width=SNUMWIDTH, margin_bottom=2, font_size=18, background_color="#eeeeee", color="#000000"))
        entry1 = toga.TextInput(id=OUTYS, value=outy, style=Pack(text_align=RIGHT, height=45, width=SNUMWIDTH, margin_bottom=2, margin_left=4, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry0, entry1, btn], style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        boxrow = toga.Box(style=Pack(direction=ROW, align_items=END, margin_top=MARGINTOP, height=40))
        scan_content.add(boxrow)

        self.buttonSave = button

        scan = Button(
            'Scan',
            on_press=self.displayMainWindow,
            style=Pack(width=92, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=10)
        )

        physical = Button(
            'Physical',
            on_press=self.callServoScreen,
            style=Pack(width=92, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=10)
        )

        notches = Button(
            'Notch',
            on_press=self.callNotchesScreen,
            style=Pack(width=92, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=10)
        )

        throttle = Button(
            'Throttle',
            on_press=self.callThrottleScreen,
            style=Pack(width=92, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=10)
        )

        boxrow = toga.Box(children=[scan, physical, notches, throttle], style=Pack(direction=ROW, align_items=CENTER, margin_top=MARGINTOP))
        scan_content.add(boxrow)

        self.scroller = toga.ScrollContainer(content=scan_content, style=Pack(direction=COLUMN, align_items=CENTER))
        self.main_window.content = self.scroller
        self.main_window.show()

    ##
    #### Support routines for screen above
    ##

    async def change_xbeeAddr(self, widget):
        nodeid = str(self.app.widgets[XBEA].value)
        data = self.Xbee.xbeeTransmitRemoteCommand(self.Xbee.buildAddress(self.macAddress), 'N', 'I', nodeid)    # set node id
        self.writebuff = bytearray(data)
        self.writelen = len(self.writebuff)
        await self.connectWrite()

        data = self.Xbee.xbeeTransmitRemoteCommand(self.Xbee.buildAddress(self.macAddress), 'A', 'C', '')        # apply changes
        self.writebuff = bytearray(data)
        self.writelen = len(self.writebuff)
        await self.connectWrite()

        data = self.Xbee.xbeeTransmitRemoteCommand(self.Xbee.buildAddress(self.macAddress), 'W', 'R', '')        # write to eeprom
        self.writebuff = bytearray(data)
        self.writelen = len(self.writebuff)
        await self.connectWrite()

    async def change_ptidaddr(self, widget):
        ptidaddr = str(self.app.widgets[PTIDV].value)
        data = chr(SETPROTOADDRESS) + ptiaddr + '234567890123456789'
        await self.sendDataBuffer(data)

    async def change_ptidbase(self, widget):
        ptidbase = str(self.app.widgets[BASEV].value)
        p = int(ptidbase)
        data = chr(SETBASEADDRESS) + chr(p) + '34567890123456789'
        await self.sendDataBuffer(data)

    async def change_locoAddr(self, widget):
        locoaddr = str(self.app.widgets[ADDRV].value)
        locoaddr = "0000" + locoaddr
        locoaddr = locoaddr[-4:]
        data     = chr(SETLOCOADDRESS) + locoaddr[0] + locoaddr[1] + locoaddr[2] + locoaddr[3] + '567890123456789'
        await self.sendDataBuffer(data)

    async def change_ConsistAddr(self, widget):
        consistaddr = str(self.app.widgets[CONDV].value)
        consistaddr = "0000" + consistaddr
        consistaddr = consistaddr[-4:]
        data        = chr(SETCONSISTADDRESS) + consistaddr[0] + consistaddr[1] + consistaddr[2] + consistaddr[3] + '567890123456789'
        await self.sendDataBuffer(data)

    async def change_ConsistMode(self, widget):
        consistdir = str(self.app.widgets[COND].text)
        cd = 0
        if consistdir == 'OFF':
           self.app.widgets[COND].text = 'FWD'
           cd = 1

        if consistdir == 'FWD':
           self.app.widgets[COND].text = 'REV'
           cd = 2

        if consistdir == 'REV':
           self.app.widgets[COND].text = 'OFF'
           cd = 0

        data = chr(SETCONSISTDIRECTION) + chr(cd) + '234567890123456789'
        await self.sendDataBuffer(data)

    async def change_DCCMode(self, widget):
        dccmode = str(self.app.widgets[DCCM].value)
        if dccmode == True:
           dcm = 0
        else:
           dcm = 1
        data = chr(SETDCCPASSTHRU) + chr(cd) + '234567890123456789'
        await self.sendDataBuffer(data)

    async def change_DCCAddress(self, widget):
        dccaddr = str(self.app.widgets[ADDRV].value)
        dccaddr = "0000" + dccaddr
        dccaddr = dccaddr[-4:]
        data     = chr(SETDCCADDRESS) + dccaddr[0] + dccaddr[1] + dccaddr[2] + dccaddr[3] + '567890123456789'
        await self.sendDataBuffer(data)

    async def change_WatchDog(self, widget):
        wdog = int(self.app.widgets[WDOGV].value)
        dat  = chr(SETTIMEOUT) + chr(wdv) + '345678901201234567'
        await self.sendDataBuffer(data)

    async def change_OutputX(self, widget):
        outFunc  = int(self.app.widgets[OUTXF].value)
        outValue = int(self.app.widgets[OUTXS].value)
        data = chr(SETOUTPUTSMODE) + chr(1) + chr(outFunc) + chr(outValue) + '5678901201234567'
        await self.sendDataBuffer(data)

    async def change_OutputY(self, widget):
        outFunc  = int(self.app.widgets[OUTYF].value)
        outValue = int(self.app.widgets[OUTYS].value)
        data = chr(SETOUTPUTSMODE) + chr(0) + chr(outFunc) + chr(outValue) + '5678901201234567'
        await self.sendDataBuffer(data)


    ####################################################

    async def sendDataBuffer(self, data):
        buff = self.Xbee.buildXbeeTransmitData(self.Xbee.buildAddress(self.macAddress), data)
        self.writebuff = bytearray(buff)
        self.writelen = len(self.writebuff)
        await self.connectWrite()

    ####################################################


    def sendPrgCommand(self, value):
        pass

    def callThrottleScreen(self, widget):
        self.protothrottleSimulation()

    def callMainWidgetWindow(self, widget):
        self.displayMainWidgetScreen(widget, self.message)

##
########################################################
##
    async def callServoScreen(self, widget):
        retries = 0
        while retries < 2:
           data = chr(GETPHYSICS) + "000000000000000000"
           buff = self.Xbee.buildXbeeTransmitData(self.Xbee.buildAddress(self.macAddress), data)

           self.writebuff = bytearray(buff)
           self.writelen = len(self.writebuff)
 
           await self.connectWrite()
           await asyncio.sleep(1)
           await self.connectRead()

           self.pysmessage = await self.parseReturnData(len(self.readbuff), self.readbuff, 80)

           if self.pysmessage != []:
              self.displayServoScreen(self.buttonSave, self.message, self.pysmessage)
              return
           else:
              retries = retries + 1

        return


##
#############################################################
##
    async def callPhysicsScreen(self, widget):
        self.displayPhysicsScreen(self.buttonSave, self.message)



##
############################################################
##
    async def callNotchesScreen(self, widget):
        print ("callNotchesScreen")
        retries = 0
        while retries < 3:
           data = chr(RETURNNOTCHES) + "000000000000000000"
           buff = self.Xbee.buildXbeeTransmitData(self.Xbee.buildAddress(self.macAddress), data)

           self.writebuff = bytearray(buff)
           self.writelen = len(self.writebuff)
 
           await self.connectWrite()
           await asyncio.sleep(1)
           await self.connectRead()

           self.notches = await self.parseReturnData(len(self.readbuff), self.readbuff, 78)

           s = ""
           for c in self.notches:
               s = s + hex(c) + " "
     
           print ("notch data return ", s)

           if self.notches != []:
              print ("displayNotchesScreen")
              self.displayNotchesScreen(self.buttonSave, self.notches)
              return
           else:
              retries = retries + 1
        return


##
########################################################################
### Servo Configure Screen
##

    def displayServoScreen(self, button, message, pymessage):
        MARGINTOP = 2
        LNUMWIDTH = 64
        SNUMWIDTH = 42

        scan_content = toga.Box(style=Pack(direction=COLUMN, margin_left=6))

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
        mode   = toga.Button(id=SVRM, text="ESC", on_press = self.sendPrgCommand, style=Pack(width=90, height=55, background_color="#bbbbbb", color="#000000", font_size=12))
        boxrow = toga.Box(children=[desc, mode], style=Pack(direction=ROW, align_items=END, margin_top=20))
        scan_content.add(boxrow)

        ############################################################# 

        boxrow = toga.Box(children=[blank, toga.Divider(), blank], style=Pack(direction=COLUMN, margin_top=20))
        scan_content.add(boxrow)

        ############################################################# Servo 0 Config

        svrr = message[32]      # Reverse switch servo 0
        checked = False
        if (int(svrr) & 0x01) == 1:
           checked = True

        desc   = toga.Label("Servo 0", style=Pack(width=270, align_items=END, font_size=18))
        rev    = toga.Switch("Reverse", id=SV0R, value=checked, on_change=self.handleServo0)
        boxrow = toga.Box(children=[desc, rev], style=Pack(direction=ROW, align_items=END, margin_top=8))
        scan_content.add(boxrow)

        # Servo zero always follows the throttle, there is no function code

        svlo0 = message[17]        # servo 0 low limit
        ch    = message[18] << 8
        svlo0 = svlo0 | ch

        desc   = toga.Label("     Low Limit", style=Pack(width=244, align_items=END, font_size=12))
        entry0 = toga.NumberInput(id=SV0LV, on_change=self.handleServo0, min=0, max=1000, value=svlo0, style=Pack(text_align=RIGHT, flex=1, height=48, width=LNUMWIDTH, font_size=18, background_color="#eeeeee", color="#000000"))
        btn    = toga.Button(id=SV0LP, text="Prg", on_press = self.handleServo0, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        boxrow = toga.Box(children=[desc, entry0, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        desc   = toga.Label(" ", style=Pack(width=20, align_items=END, font_size=18))
        adj0   = toga.Slider(id=SV0LVS, value=svlo0, min=0, max=1000, on_change=self.handleServo0, style=Pack(width=320, height=20))
        boxrow = toga.Box(children=[desc, adj0], style=Pack(direction=ROW, align_items=END))
        scan_content.add(boxrow)

        svhi0 = message[19]
        ch    = message[20] << 8          # 11,12
        svhi0 = svhi0 | ch

        btn    = toga.Button(id=SV0HP, text="Prg", on_press = self.sendPrgCommand, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("     High Limit", style=Pack(width=244, align_items=END, font_size=12))
        entry1 = toga.NumberInput(id='SV0HV', on_change=self.handleServo0, min=0, max=9999, value=svhi0, style=Pack(text_align=RIGHT, flex=1, height=48, width=LNUMWIDTH, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry1, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        desc   = toga.Label(" ", style=Pack(width=20, align_items=END, font_size=18))
        adj0   = toga.Slider(id='SV0HVS', value=svhi0, min=0, max=1000, on_change=self.handleServo0, style=Pack(width=320, height=20))
        boxrow = toga.Box(children=[desc, adj0], style=Pack(direction=ROW, align_items=END))
        scan_content.add(boxrow)

        ############################################################# 

        boxrow = toga.Box(children=[blank, toga.Divider(), blank], style=Pack(direction=COLUMN, margin_top=20))
        scan_content.add(boxrow)

        ############################################################# Servo 1 Config
        checked = False
        if (int(svrr) & 0x02) == 2:
           checked = True

        desc   = toga.Label("Servo 1", style=Pack(width=270, align_items=END, font_size=18))
        rev    = toga.Switch("Reverse", id=SV1R, value=checked, on_change=self.handleServo1)
        boxrow = toga.Box(children=[desc, rev], style=Pack(direction=ROW, align_items=END, margin_top=8))
        scan_content.add(boxrow)

        sv1func = message[30]      # servo 1 function code

        btn    = toga.Button(id=SV1FCP, text="Prg", on_press = self.handleServo1, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("     Function Code", style=Pack(width=260, align_items=END, font_size=12))
        func   = toga.NumberInput(id=SV1FC, value=sv1func, on_change=self.handleServo1, min=0, max=99, style=Pack(text_align=RIGHT, flex=1, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, func, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        svlo1 = message[21]        # servo 1 low limit
        ch    = message[22] << 8
        svlo1 = svlo1 | ch

        desc   = toga.Label("     Low Limit", style=Pack(width=244, align_items=END, font_size=12))
        entry0 = toga.NumberInput(id=SV1LV, value=svlo1, on_change=self.handleServo1, min=0, max=1000, style=Pack(text_align=RIGHT, flex=1, height=48, width=LNUMWIDTH, font_size=18, background_color="#eeeeee", color="#000000"))
        btn    = toga.Button(id=SV1LP, text="Prg", on_press = self.handleServo1, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        boxrow = toga.Box(children=[desc, entry0, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        desc   = toga.Label(" ", style=Pack(width=20, align_items=END, font_size=18))
        adj0   = toga.Slider(id=SV1LVS, value=svlo1, min=0, max=1000, on_change=self.handleServo1, style=Pack(width=320, height=20))
        boxrow = toga.Box(children=[desc, adj0], style=Pack(direction=ROW, align_items=END))
        scan_content.add(boxrow)

        svhi1 = message[23]
        ch    = message[24] << 8   # servo 1 high limit
        svhi1 = svhi1 | ch

        btn    = toga.Button(id=SV1HP, text="Prg", on_press = self.handleServo1, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("     High Limit", style=Pack(width=244, align_items=END, font_size=12))
        entry1  = toga.NumberInput(id=SV1HV, value=svhi1, on_change=self.handleServo1, min=0, max=9999, style=Pack(text_align=RIGHT, flex=1, height=48, width=LNUMWIDTH, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry1, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        desc   = toga.Label(" ", style=Pack(width=20, align_items=END, font_size=18))
        adj0   = toga.Slider(id=SV1HVS, value=svhi1, min=0, max=1000, on_change=self.handleServo1, style=Pack(width=320, height=20))
        boxrow = toga.Box(children=[desc, adj0], style=Pack(direction=ROW, align_items=END))
        scan_content.add(boxrow)

        ############################################################# 

        boxrow = toga.Box(children=[blank, toga.Divider(), blank], style=Pack(direction=COLUMN, margin_top=20))
        scan_content.add(boxrow)

        ############################################################# Servo 2 Config
        checked = False
        if (int(svrr) & 0x04) == 4:
           checked = True

        desc   = toga.Label("Servo 2", style=Pack(width=270, align_items=END, font_size=18))
        rev    = toga.Switch("Reverse", id=SV2R, value=checked, on_change=self.handleServo2)
        boxrow = toga.Box(children=[desc, rev], style=Pack(direction=ROW, align_items=END, margin_top=8))
        scan_content.add(boxrow)

        sv2func = message[31]   # Servo 2 function code

        btn    = toga.Button(id=SV2FCP, text="Prg", on_press = self.handleServo2, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("     Function Code", style=Pack(width=260, align_items=END, font_size=12))
        func   = toga.NumberInput(id=SV2FC, value=sv2func, on_change=self.handleServo2, min=0, max=99, style=Pack(text_align=RIGHT, flex=1, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, func, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        svlo2 = message[25]               # Servo 2 low limit
        ch    = message[26] << 8
        svlo2 = svlo2 | ch

        desc   = toga.Label("     Low Limit", style=Pack(width=244, align_items=END, font_size=12))
        entry0 = toga.NumberInput(id=SV2LV, value=svlo2, on_change=self.handleServo2, min=0, max=1000, style=Pack(text_align=RIGHT, flex=1, height=48, width=LNUMWIDTH, font_size=18, background_color="#eeeeee", color="#000000"))
        btn    = toga.Button(id=SV2LP, text="Prg", on_press = self.handleServo2, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        boxrow = toga.Box(children=[desc, entry0, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        desc   = toga.Label(" ", style=Pack(width=20, align_items=END, font_size=18))
        adj0   = toga.Slider(id=SV2LVS, value=svlo2, min=0, max=1000, on_change=self.handleServo2, style=Pack(width=320, height=20))
        boxrow = toga.Box(children=[desc, adj0], style=Pack(direction=ROW, align_items=END))
        scan_content.add(boxrow)

        svhi2 = message[27]               # Servo 2 high limit
        ch    = message[28] << 8
        svhi2 = svhi2 | ch

        btn    = toga.Button(id=SV2HP, text="Prg", on_press = self.handleServo2, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("     High Limit", style=Pack(width=244, align_items=END, font_size=12))
        entry1  = toga.NumberInput(id=SV2HV, value=svhi2, on_change=self.handleServo2, min=0, max=9999, style=Pack(text_align=RIGHT, flex=1, height=48, width=LNUMWIDTH, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, entry1, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        desc   = toga.Label(" ", style=Pack(width=20, align_items=END, font_size=18))
        adj0   = toga.Slider(id=SV2HVS, value=svhi2, min=0, max=1000, on_change=self.handleServo2, style=Pack(width=320, height=20))
        boxrow = toga.Box(children=[desc, adj0], style=Pack(direction=ROW, align_items=END))
        scan_content.add(boxrow)

        ##################
        boxrow = toga.Box(children=[blank, toga.Divider(), blank], style=Pack(direction=COLUMN, margin_top=20))
        scan_content.add(boxrow)

        ###
        #### Must get physics data here ######################
        ##

        br0 = pymessage[10]    # Brake rate
        br1 = pymessage[11]
        brate = (br1<<8) | br0

        btn    = toga.Button(id=BRAT, text="Prg", on_press = self.handle_brakeRate, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Brake Rate", style=Pack(width=260, align_items=END, font_size=16))
        func   = toga.NumberInput(id=BRATV, value=brate, min=0, max=99, style=Pack(text_align=RIGHT, flex=1, height=48, width=64, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, func, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        fncode = pymessage[16]   # Brake Function Code

        btn    = toga.Button(id=BFNC, text="Prg", on_press = self.handle_brakeFuncCode, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Brake Rate FnCode", style=Pack(width=260, align_items=END, font_size=16))
        func   = toga.NumberInput(id=BFNCV, value=fncode, min=0, max=99, style=Pack(text_align=RIGHT, flex=1, height=48, width=64, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, func, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        ac0 = pymessage[12]
        ac1 = pymessage[13]
        acceleration = (ac1<<8) | ac0  # Acceleration Value

        btn    = toga.Button(id=ACCL, text="Prg", on_press = self.handle_acceleration, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Acceleration", style=Pack(width=260, align_items=END, font_size=16))
        func   = toga.NumberInput(id=ACCLV, value=acceleration, min=0, max=99, style=Pack(text_align=RIGHT, flex=1, height=48, width=64, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, func, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        dc0 = pymessage[14]
        dc1 = pymessage[15]
        deceleration = (dc1<<8) | dc0  # Deceleration Value

        btn    = toga.Button(id=DECL, text="Prg", on_press = self.handle_deceleration, style=Pack(width=55, height=55, margin_top=6, background_color="#bbbbbb", color="#000000", font_size=12))
        desc   = toga.Label("Deceleration", style=Pack(width=260, align_items=END, font_size=16))
        func   = toga.NumberInput(id=DECLV, value=deceleration, min=0, max=99, style=Pack(text_align=RIGHT, flex=1, height=48, width=64, font_size=18, background_color="#eeeeee", color="#000000"))
        boxrow = toga.Box(children=[desc, func, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        boxrow = toga.Box(children=[blank, toga.Divider(), blank], style=Pack(direction=COLUMN, margin_top=20, margin_bottom=20))
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

    ##
    ### Set data routines
    ##

    async def handle_brakeRate(self, widget):
        brakerate = str(self.app.widgets[BRATEV].value)
        s = "000" + brakerate
        s = s[-3:]
        data = chr(SETBRAKERATE) + s[2] + s[1] + s[0] + '5678901201234567'
        await self.sendDataBuffer(data)

    async def handle_brakeFuncCode(self, widget):
        pass

    async def handle_acceleration(self, widget):
        pass

    async def handle_deceleration(self, widget):
        pass

        
    async def handleServo0(self):
        if self.app.widgets[SV0R].value:
           rev = "1"
        else:
           rev = "0"
        fc  = "00"
        l   = "0000" + str(self.app.widgets[SV0LV].value)
        low = l[-4:]
        h   = "0000" + str(self.app.widgets[SV0HV].value)
        hi  = h[-4:]
        print (rev, fc, low, hi)
        await self.setServoData(0, rev, fc, low, hi)

    async def handleServo1(self):
        if self.app.widgets[SV1R].value:
           rev = "1"
        else:
           rev = "0"
        f   = "00" + str(self.app.widgets[SV1FC].value)
        fc  = f[-2:]
        l   = "0000" + str(self.app.widgets[SV1LV].value)
        low = l[-4:]
        h   = "0000" + str(self.app.widgets[SV1HV].value)
        hi  = h[-4:]
        await self.setServoData(1, rev, fc, low, hi)

    async def handleServo2(self):
        if self.app.widgets[SV2R].value:
           rev = "1"
        else:
           rev = "0"
        f   = "00" + str(self.app.widgets[SV2FC].value)
        fc  = f[-2:]
        l   = "0000" + str(self.app.widgets[SV2LV].value)
        low = l[-4:]
        h   = "0000" + str(self.app.widgets[SV2HV].value)
        hi  = h[-4:]
        await self.setServoData(2, rev, fc, low, hi)

    async def setServoData(self, num, rev, func, low, hi):
        data = chr(SETSERVOCONFIG) + str(num) + hi[0] + hi[1] + hi[2] + hi[3] + low[0] + low[1] + low[2] + low[3] + rev + func[0] + func[1] + '3456789'
        buff = self.Xbee.buildXbeeTransmitData(self.Xbee.buildAddress(self.macAddress), data)
        print ("write buffer ", buff)
        self.writebuff = bytearray(buff)
        self.writelen = len(self.writebuff)
        await self.connectWrite()

##
#####  Notches Screen
##

    def displayNotchesScreen(self, button, message):
        MARGINTOP = 2
        LNUMWIDTH = 64
        SNUMWIDTH = 42

        scan_content = toga.Box(style=Pack(direction=COLUMN, margin_left=6))

        # Ascii ID and Mac at top of display
        idlabel  = toga.Label(self.buttonDict[button.id], style=Pack(flex=1, color="#000000", align_items=CENTER, font_size=32))
        maclabel = toga.Label(button.id, style=Pack(flex=1, color="#000000", align_items=CENTER, font_size=12))
        boxrowA  = toga.Box(children=[idlabel], style=Pack(direction=ROW, align_items=END, margin_top=4))
        boxrowB  = toga.Box(children=[maclabel], style=Pack(direction=ROW, align_items=END, margin_top=2))

        scan_content.add(boxrowA)
        scan_content.add(boxrowB)

        title1 = toga.Label("In Low", style=Pack(margin_left=120, margin_top=10))
        title2 = toga.Label("In High", style=Pack(margin_left=17))
        title3 = toga.Label("Output", style=Pack(margin_left=15))
        boxrowB = toga.Box(children=[title1, title2, title3], style=Pack(direction=ROW, align_items=END, margin_top=2))
        scan_content.add(boxrowB)

        inlow  = message[11]
        inhigh = message[12]
        output = message[13]

        desc   = toga.Label("Notch 1", style=Pack(width=120, align_items=END, font_size=16))
        ntinl  = toga.NumberInput(id=NTINL1, value=inlow, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        ntinh  = toga.NumberInput(id=NTINH1, value=inhigh, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        ntout  = toga.NumberInput(id=NTOUT1, value=output, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        btn    = toga.Button(id=NTPRG1, text="Prg", on_press = self.handle_notchChange, style=Pack(width=55, height=55, margin_top=6, margin_right=5, background_color="#bbbbbb", color="#000000", font_size=12))
        boxrow = toga.Box(children=[desc, ntinl, ntinh, ntout, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        inlow  = message[14]
        inhigh = message[15]
        output = message[16]

        desc   = toga.Label("Notch 2", style=Pack(width=120, align_items=END, font_size=16))
        ntinl  = toga.NumberInput(id=NTINL2, value=inlow, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        ntinh  = toga.NumberInput(id=NTINH2, value=inhigh, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        ntout  = toga.NumberInput(id=NTOUT2, value=output, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        btn    = toga.Button(id=NTPRG2, text="Prg", on_press = self.handle_notchChange, style=Pack(width=55, height=55, margin_top=6, margin_right=5, background_color="#bbbbbb", color="#000000", font_size=12))
        boxrow = toga.Box(children=[desc, ntinl, ntinh, ntout, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        inlow  = message[17]
        inhigh = message[18]
        output = message[19]

        desc   = toga.Label("Notch 3", style=Pack(width=120, align_items=END, font_size=16))
        ntinl  = toga.NumberInput(id=NTINL3, value=inlow, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        ntinh  = toga.NumberInput(id=NTINH3, value=inhigh, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        ntout  = toga.NumberInput(id=NTOUT3, value=output, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        btn    = toga.Button(id=NTPRG3, text="Prg", on_press = self.handle_notchChange, style=Pack(width=55, height=55, margin_top=6, margin_right=5, background_color="#bbbbbb", color="#000000", font_size=12))
        boxrow = toga.Box(children=[desc, ntinl, ntinh, ntout, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        inlow  = message[20]
        inhigh = message[21]
        output = message[22]

        desc   = toga.Label("Notch 4", style=Pack(width=120, align_items=END, font_size=16))
        ntinl  = toga.NumberInput(id=NTINL4, value=inlow, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        ntinh  = toga.NumberInput(id=NTINH4, value=inhigh, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        ntout  = toga.NumberInput(id=NTOUT4, value=output, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        btn    = toga.Button(id=NTPRG4, text="Prg", on_press = self.handle_notchChange, style=Pack(width=55, height=55, margin_top=6, margin_right=5, background_color="#bbbbbb", color="#000000", font_size=12))
        boxrow = toga.Box(children=[desc, ntinl, ntinh, ntout, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        inlow  = message[23]
        inhigh = message[24]
        output = message[25]

        desc   = toga.Label("Notch 5", style=Pack(width=120, align_items=END, font_size=16))
        ntinl  = toga.NumberInput(id=NTINL5, value=inlow, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        ntinh  = toga.NumberInput(id=NTINH5, value=inhigh, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        ntout  = toga.NumberInput(id=NTOUT5, value=output, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        btn    = toga.Button(id=NTPRG5, text="Prg", on_press = self.handle_notchChange, style=Pack(width=55, height=55, margin_top=6, margin_right=5, background_color="#bbbbbb", color="#000000", font_size=12))
        boxrow = toga.Box(children=[desc, ntinl, ntinh, ntout, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        inlow  = message[26]
        inhigh = message[27]
        output = message[28]

        desc   = toga.Label("Notch 6", style=Pack(width=120, align_items=END, font_size=16))
        ntinl  = toga.NumberInput(id=NTINL6, value=inlow, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        ntinh  = toga.NumberInput(id=NTINH6, value=inhigh, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        ntout  = toga.NumberInput(id=NTOUT6, value=output, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        btn    = toga.Button(id=NTPRG6, text="Prg", on_press = self.handle_notchChange, style=Pack(width=55, height=55, margin_top=6, margin_right=5, background_color="#bbbbbb", color="#000000", font_size=12))
        boxrow = toga.Box(children=[desc, ntinl, ntinh, ntout, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        inlow  = message[29]
        inhigh = message[30]
        output = message[31]

        desc   = toga.Label("Notch 7", style=Pack(width=120, align_items=END, font_size=16))
        ntinl  = toga.NumberInput(id=NTINL7, value=inlow, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        ntinh  = toga.NumberInput(id=NTINH7, value=inhigh, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        ntout  = toga.NumberInput(id=NTOUT7, value=output, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        btn    = toga.Button(id=NTPRG7, text="Prg", on_press = self.handle_notchChange, style=Pack(width=55, height=55, margin_top=6, margin_right=5, background_color="#bbbbbb", color="#000000", font_size=12))
        boxrow = toga.Box(children=[desc, ntinl, ntinh, ntout, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
        scan_content.add(boxrow)

        inlow  = message[32]
        inhigh = message[33]
        output = message[34]

        desc   = toga.Label("Notch 8", style=Pack(width=120, align_items=END, font_size=16))
        ntinl  = toga.NumberInput(id=NTINL8, value=inlow, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        ntinh  = toga.NumberInput(id=NTINH8, value=inhigh, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        ntout  = toga.NumberInput(id=NTOUT8, value=output, min=0, max=199, style=Pack(text_align=RIGHT, margin_right=10, height=48, width=48, font_size=18, background_color="#eeeeee", color="#000000"))
        btn    = toga.Button(id=NTPRG8, text="Prg", on_press = self.handle_notchChange, style=Pack(width=55, height=55, margin_top=6, margin_right=5, background_color="#bbbbbb", color="#000000", font_size=12))
        boxrow = toga.Box(children=[desc, ntinl, ntinh, ntout, btn], style=Pack(direction=ROW, align_items=END, margin_top=1))
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



    async def handle_notchChange(self, widget):
        pass



##
### PT Simulation screen
##

    def protothrottleSimulation(self):

        MARGINTOP = 20
        LNUMWIDTH = 64
        SNUMWIDTH = 42

        scan_content = toga.Box(style=Pack(direction=COLUMN, margin_left=6))

        blank  = toga.Label("   ", style=Pack(margin=10))

        self.locoAddr = '0000'

        self.loco = toga.NumberInput(value=self.locoAddr, style=Pack(width=120, text_align="center", background_color="#ffffff", font_size=32, margin=2))
        box  = toga.Box(children=[self.loco], style=Pack(direction=ROW, background_color="#000000", margin_left=140, margin_top=30))
        scan_content.add(box)

        boxrow = toga.Box(children=[blank, toga.Divider(), blank], style=Pack(direction=COLUMN, margin_top=20, margin_bottom=20))
        scan_content.add(boxrow)

        notches = toga.Label("8      7      6      5      4      3      2      1      Idle", style=Pack(text_align="justify", width=360, font_size=12, margin_left=28))
        boxrow = toga.Box(children=[notches], style=Pack(direction=ROW, align_items=CENTER, margin_left=10))
        scan_content.add(boxrow)

        adj0   = toga.Slider(value=8, min=0, max=8, tick_count=8, on_change=self.handleThrottle, style=Pack(width=360, height=50))
        boxrow = toga.Box(children=[adj0], style=Pack(direction=ROW, align_items=CENTER, margin_left=10))
        scan_content.add(boxrow)

        aux  = toga.Button(id="AUX", text="AUX", on_press = self.handleAux, style=Pack(width=75, height=55, margin_top=2, margin_right=5, background_color="#bbbbbb", color="#000000", font_size=12))
        bln  = toga.Label(" ", style=Pack(width=140, margin_left=20))
        horn = toga.Button(id="HORN", text="HORN", on_press=self.handleHorn, style=Pack(width=75, height=55, margin_top=2, margin_right=5, background_color="#bbbbbb", color="#000000", font_size=12))
        boxrow = toga.Box(children=[aux, bln, horn], style=Pack(direction=ROW, margin_top=4, margin_left=30))
        scan_content.add(boxrow)

        reverser = toga.Label("Rev          N           Fwd", style=Pack(text_align="justify", width=260, font_size=12, margin_left=68, margin_top=20))
        boxrow = toga.Box(children=[reverser], style=Pack(direction=ROW, align_items=CENTER, margin_left=100))
        scan_content.add(boxrow)

        bell    = toga.Button(id="BELL", text="BELL", on_press = self.handleBell, style=Pack(width=75, height=55, margin_top=6, margin_right=10, background_color="#bbbbbb", color="#000000", font_size=12))
        reverse = toga.Slider(value=8, min=0, max=8, tick_count=3, on_change=self.handleReverse, style=Pack(width=180, height=50, margin_left=40))
        boxrow  = toga.Box(children=[bell, reverse], style=Pack(direction=ROW, align_items=CENTER, margin_top=2, margin_left=30))
        scan_content.add(boxrow)

        braker = toga.Label("Brake", style=Pack(text_align="justify", width=160, font_size=12))
        boxrow = toga.Box(children=[braker], style=Pack(direction=ROW, align_items=CENTER, margin_left=100, margin_top=20))
        scan_content.add(boxrow)

        brake = toga.Slider(value=0, min=0, max=16, on_change=self.handleBrakeLever, style=Pack(width=220, height=50))
        brfnc  = toga.NumberInput(id="BRFNC", value=11, on_change=self.setBrakeFuncCode, style=Pack(margin_left=20, width=48, height=48, font_size=18))
        boxrow = toga.Box(children=[brake, brfnc], style=Pack(direction=ROW, align_items=CENTER, margin_left=20))
        scan_content.add(boxrow)

        Afnc  = toga.Button(id="A", text="A", on_press=self.handleAfunc, style=Pack(width=35, height=55, margin_top=2, margin_right=5, background_color="#bbbbbb", color="#000000", font_size=12))
        Acode = toga.NumberInput(id="Acode", value=11, on_change=self.setACode, style=Pack(margin_left=20, width=48, height=48, font_size=18))
        bln   = toga.Label(" ", style=Pack(width=140, margin_left=20))
        Bfnc  = toga.Button(id="B", text="B", on_press=self.handleBfunc, style=Pack(width=35, height=55, margin_top=2, margin_right=5, background_color="#bbbbbb", color="#000000", font_size=12))
        Bcode = toga.NumberInput(id="Bcode", value=11, on_change=self.setBCode, style=Pack(margin_left=20, width=48, height=48, font_size=18))

        boxrow = toga.Box(children=[Afnc, bln, Bfnc], style=Pack(direction=ROW, margin_top=4, margin_left=30))
        scan_content.add(boxrow)


        self.number_input = toga.NumberInput(style=Pack(padding=10))   # dummy input to undo focus of loco number input
        self.number_input.style.visibility = HIDDEN
        scan_content.add(self.number_input)

        self.scan = Button(
            'Scan',
            on_press=self.displayMainWindow,
            style=Pack(width=120, height=60, margin_top=6, background_color="#cccccc", color="#000000", font_size=12)
        )

        boxrow = toga.Box(children=[self.scan], style=Pack(direction=ROW, align_items=CENTER, margin_top=10, margin_left=140))
        scan_content.add(boxrow)

        self.scroller = toga.ScrollContainer(content=scan_content, style=Pack(direction=COLUMN, align_items=CENTER, background_color="#eeeeee"))
        self.main_window.content = self.scroller
        self.main_window.show()



    def handleAfunc(self, widget):
        pass

    def handleBfunc(self, widget):
        pass

    def setACode(self, widget):
        pass

    def setBCode(self, widget):
        pass

    def setBrakeFuncCode(self, widget):
        pass

    def confirmInput(self, widget):
        self.number_input.focus()
        pass

    def handleThrottle(self, widget):
        self.number_input.focus()
        pass

    def handleReverse(self, widget):
        self.number_input.focus()
        pass

    def handleBrakeLever(self, widget):
        self.number_input.focus()
        pass

    def handleAux(self, widget):
        self.number_input.focus()
        pass

    def handleHorn(self, widget):
        self.number_input.focus()
        pass

    def handleBell(self, widget):
        self.number_input.focus()
        pass



def main():
    return PTApp()