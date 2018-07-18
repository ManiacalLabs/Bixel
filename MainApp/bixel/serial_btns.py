import time
import traceback
import numpy as np
import serial
import serial.tools.list_ports
from . import log


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

        # self.btns = np.rot90(result, 1)
        self.btns = np.fliplr(result)

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

    def __init__(self, dev="", hardwareID="16C0:0483"):

        self._hardwareID = hardwareID
        self._com = None
        self.dev = dev

        resp = self._connect()
        if resp != RETURN_CODES.SUCCESS:
            raise Exception('Error connecting to button controller: {}'.format(resp))

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
            for port in serial.tools.list_ports.grep(hardwareID):
                BixelButtonSerial.foundDevices.append(port[0])

        return BixelButtonSerial.foundDevices

    @staticmethod
    def _comError():
        error = "There was an unknown error communicating with the device."
        log.error(error)
        raise IOError(error)

    def send_cmd(self, cmd):
        packet = bytearray()
        packet.append(cmd)
        self._com.write(packet)

    def _connect(self):
        try:
            if(self.dev == "" or self.dev is None):
                BixelButtonSerial.findSerialDevices(self._hardwareID)
                if len(BixelButtonSerial.foundDevices) > 0:
                    self.dev = BixelButtonSerial.foundDevices[0]
                else:
                    raise Exception('No devices found and no port name given')

            log.info("Using COM Port: %s", self.dev)

            try:
                self._com = serial.Serial(self.dev, timeout=5)
            except serial.SerialException as e:
                ports = BixelButtonSerial.findSerialDevices(self._hardwareID)
                error = "Invalid port specified. No COM ports available."
                if len(ports) > 0:
                    error = "Invalid port specified. Try using one of: \n" + \
                        "\n".join(ports)
                log.info(error)
                raise Exception(error)

            self.send_cmd(CMDTYPE.CONNECT)

            resp = self._com.read(1)
            if len(resp) == 0:
                BixelButtonSerial._comError()

            return ord(resp)

        except serial.SerialException as e:
            error = "Unable to connect to the device. Please check that it is connected and the correct port is selected."
            log.error(traceback.format_exc())
            log.error(error)
            raise e

    def get(self):
        try:
            self.send_cmd(CMDTYPE.BTNS)
            resp = ord(self._com.read(1))
            if resp != RETURN_CODES.SUCCESS:
                raise Exception('Received {}'.format(resp))
            btns = self._com.read(32)  # read 16 * uint16_t = 32 bytes
            self.buttons.update(btns)
            return self.buttons
        except serial.SerialException:
            log.error("Problem connecting to serial device.")
            return -1