import log
import time
import numpy as np


class CMDTYPE:
    CONNECT = 1
    BTNS = 2


class RETURN_CODES:
    SUCCESS = 255


class BixelButtons(object):
    def __init__(self):
        self._clear_btns()
        self._btns_pressed = None
        self.last_btns_pressed = None
        self.btn_int_high = None
        self.btn_int_low = None

    def _clear_btns(self):
        self.btns =  [[0 for y in range(16)] for x in range(16)]

    def update(self, btns):
        result = np.zeros([16, 16])
        for i in range(16):
            low = np.unpackbits(np.array(btns[i*2], dtype=np.uint8))
            high = np.unpackbits(np.array(btns[(i*2)+1], dtype=np.uint8))
            result[i] = np.concatenate([high, low], axis=0)

        self.btns = np.rot90(result, 1)

        self._btns_pressed = tuple(map(tuple, np.transpose(self.btns.nonzero())))
        self._gen_btn_interrupts()
        self.last_btns_pressed = self._btns_pressed
        return self.btns


    def _gen_btn_interrupts(self):
        self.btn_int_high = self.btn_int_low = tuple()
        if self.last_btns_pressed is None:
            return

        self.btn_int_high = set(self._btns_pressed) - set(self.last_btns_pressed)
        self.btn_int_low = set(self.last_btns_pressed) - set(self._btns_pressed)

    def int_high(self):
        return self.btn_int_high

    def int_low(self):
        return self.btn_int_low

    def pressed(self):
        return self._btns_pressed

    def get(self, x, y):
        return self.btns[x][y]


class BixelButtonSerial(object):
    """Main driver for Serial based LED strips"""
    foundDevices = []
    deviceIDS = {}
    deviceVers = []

    def __init__(self, dev="", hardwareID="16C0:0483"):

        self._hardwareID = hardwareID
        self._com = None
        self.dev = dev

        resp = self._connect()
        if resp != RETURN_CODES.SUCCESS:
            raise Exception('Error connecting to button controller')

        self.buttons = BixelButtons()

    def __exit__(self, type, value, traceback):
        if self._com is not None:
            log.info("Closing connection to: %s", self.dev)
            self._com.close()

    @staticmethod
    def findSerialDevices(hardwareID="16C0:0483"):
        hardwareID = "(?i)" + hardwareID  # forces case insensitive
        if len(BixelButtonSerial.foundDevices) == 0:
            BixelButtonSerial.foundDevices = []
            BixelButtonSerial.deviceIDS = {}
            for port in serial.tools.list_ports.grep(hardwareID):
                id = BixelButtonSerial.getDeviceID(port[0])
                ver = BixelButtonSerial.getDeviceVer(port[0])
                if id >= 0:
                    BixelButtonSerial.deviceIDS[id] = port[0]
                    BixelButtonSerial.foundDevices.append(port[0])
                    BixelButtonSerial.deviceVers.append(ver)

        return BixelButtonSerial.foundDevices

    @staticmethod
    def _printError(error):
        msg = "Unknown error occured."
        if error == RETURN_CODES.ERROR_SIZE:
            msg = "Data packet size incorrect."
        elif error == RETURN_CODES.ERROR_UNSUPPORTED:
            msg = "Unsupported configuration attempted."
        elif error == RETURN_CODES.ERROR_PIXEL_COUNT:
            msg = "Too many pixels specified for device."
        elif error == RETURN_CODES.ERROR_BAD_CMD:
            msg = "Unsupported protocol command. Check your device version."

        log.error("%s: %s", error, msg)
        raise BiblioSerialError(msg)

    @staticmethod
    def _comError():
        error = "There was an unknown error communicating with the device."
        log.error(error)
        raise IOError(error)

    def _connect(self):
        try:
            if(self.dev == "" or self.dev is None):
                BixelButtonSerial.findSerialDevices(self._hardwareID)

                if self.deviceID is not None:
                    if self.deviceID in BixelButtonSerial.deviceIDS:
                        self.dev = BixelButtonSerial.deviceIDS[self.deviceID]
                        self.devVer = 0
                        try:
                            i = BixelButtonSerial.foundDevices.index(self.dev)
                            self.devVer = BixelButtonSerial.deviceVers[i]
                        except:
                            pass
                        log.info("Using COM Port: %s, Device ID: %s, Device Ver: %s",
                                 self.dev, self.deviceID, self.devVer)

                    if self.dev == "" or self.dev is None:
                        error = "Unable to find device with ID: {}".format(
                            self.deviceID)
                        log.error(error)
                        raise ValueError(error)
                elif len(BixelButtonSerial.foundDevices) > 0:
                    self.dev = BixelButtonSerial.foundDevices[0]
                    self.devVer = 0
                    try:
                        i = BixelButtonSerial.foundDevices.index(self.dev)
                        self.devVer = BixelButtonSerial.deviceVers[i]
                    except:
                        pass
                    devID = -1
                    for id in BixelButtonSerial.deviceIDS:
                        if BixelButtonSerial.deviceIDS[id] == self.dev:
                            devID = id

                    log.info("Using COM Port: %s, Device ID: %s, Device Ver: %s",
                             self.dev, devID, self.devVer)

            try:
                self._com = serial.Serial(self.dev, timeout=5)
            except serial.SerialException as e:
                ports = BixelButtonSerial.findSerialDevices(self._hardwareID)
                error = "Invalid port specified. No COM ports available."
                if len(ports) > 0:
                    error = "Invalid port specified. Try using one of: \n" + \
                        "\n".join(ports)
                log.info(error)
                raise BiblioSerialError(error)

            packet = BixelButtonSerial._generateHeader(CMDTYPE.SETUP_DATA, 4)
            packet.append(self._type)  # set strip type
            byteCount = self.bufByteCount
            if self._type in BufferChipsets:
                if self._type == LEDTYPE.APA102 and self.devVer >= 2:
                    pass
                else:
                    self._bufPad = BufferChipsets[self._type](self.numLEDs) * 3
                    byteCount += self._bufPad

            packet.append(byteCount & 0xFF)  # set 1st byte of byteCount
            packet.append(byteCount >> 8)  # set 2nd byte of byteCount
            packet.append(self._SPISpeed)
            self._com.write(packet)

            resp = self._com.read(1)
            if len(resp) == 0:
                BixelButtonSerial._comError()

            return ord(resp)

        except serial.SerialException as e:
            error = "Unable to connect to the device. Please check that it is connected and the correct port is selected."
            log.error(traceback.format_exc())
            log.error(error)
            raise e

    @staticmethod
    def _generateHeader(cmd, size):
        packet = bytearray()
        packet.append(cmd)
        packet.append(size & 0xFF)
        packet.append(size >> 8)
        return packet

    @staticmethod
    def setDeviceID(dev, id):
        if id < 0 or id > 255:
            raise ValueError("ID must be an unsigned byte!")

        try:
            com = serial.Serial(dev, timeout=5)

            packet = BixelButtonSerial._generateHeader(CMDTYPE.SETID, 1)
            packet.append(id)
            com.write(packet)

            resp = com.read(1)
            if len(resp) == 0:
                BixelButtonSerial._comError()
            else:
                if ord(resp) != RETURN_CODES.SUCCESS:
                    BixelButtonSerial._printError(ord(resp))

        except serial.SerialException:
            log.error("Problem connecting to serial device.")
            raise IOError("Problem connecting to serial device.")

    @staticmethod
    def getDeviceID(dev):
        packet = BixelButtonSerial._generateHeader(CMDTYPE.GETID, 0)
        try:
            com = serial.Serial(dev, timeout=5)
            com.write(packet)
            resp = ord(com.read(1))
            return resp
        except serial.SerialException:
            log.error("Problem connecting to serial device.")
            return -1

    @staticmethod
    def getDeviceVer(dev):
        packet = BixelButtonSerial._generateHeader(CMDTYPE.GETVER, 0)
        try:
            com = serial.Serial(dev, timeout=0.5)
            com.write(packet)
            ver = 0
            resp = com.read(1)
            if len(resp) > 0:
                resp = ord(resp)
                if resp == RETURN_CODES.SUCCESS:
                    ver = ord(com.read(1))
            return ver
        except serial.SerialException:
            log.error("Problem connecting to serial device.")
            return 0

    def setMasterBrightness(self, brightness):
        packet = BixelButtonSerial._generateHeader(CMDTYPE.BRIGHTNESS, 1)
        packet.append(brightness)
        self._com.write(packet)
        resp = ord(self._com.read(1))
        if resp != RETURN_CODES.SUCCESS:
            BixelButtonSerial._printError(resp)
            return False
        else:
            return True

    # Push new data to strand
    def _update(self, data):
        count = self.bufByteCount + self._bufPad
        packet = BixelButtonSerial._generateHeader(CMDTYPE.PIXEL_DATA, count)

        self._fixData(data)

        packet.extend(self._buf)
        packet.extend([0] * self._bufPad)
        self._com.write(packet)

        resp = self._com.read(1)
        if len(resp) == 0:
            BixelButtonSerial._comError()
        if ord(resp) != RETURN_CODES.SUCCESS:
            BixelButtonSerial._printError(ord(resp))

        self._com.flushInput()

    def getButtons(self):
        packet = BixelButtonSerial._generateHeader(CMDTYPE.GETBTNS, 0)
        try:
            self._com.write(packet)
            resp = ord(self._com.read(1))
            if resp != RETURN_CODES.SUCCESS:
                BixelButtonSerial._printError(resp)
            btns = self._com.read(32)  # read 16 * uint16_t = 32 bytes
            return self.buttons.update(btns)
        except serial.SerialException:
            log.error("Problem connecting to serial device.")
            return -1

