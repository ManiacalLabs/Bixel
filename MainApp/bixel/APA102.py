from . driver_base import DriverBase, ChannelOrder
from . import log
import spidev


class APA102(DriverBase):
    """Base driver for controling SPI devices on systems like the Raspberry Pi and BeagleBone"""

    def __init__(self, pixels, c_order=ChannelOrder.GRB, dev="/dev/spidev0.0", SPISpeed=12):

        super().__init__(pixels, c_order=c_order)

        self.dev = dev
        self._spiSpeed = SPISpeed

        a, b = -1, -1
        d = self.dev.replace("/dev/spidev", "")
        s = d.split('.')
        if len(s) == 2:
            a = int(s[0])
            b = int(s[1])

        if a < 0 or b < 0:
            error = "When using py-spidev, the given device must be in the format /dev/spidev*.*"
            log.error(error)
            raise ValueError(error)

        self._bootstrapSPIDev()
        import spidev
        self.spi = spidev.SpiDev()
        self.spi.open(a, b)
        self.spi.max_speed_hz = int(self._spiSpeed * 1000000.0)
        log.info('py-spidev speed @ %.1f MHz',
                    (float(self.spi.max_speed_hz) / 1000000.0))

        self.gamma = [int(pow(float(i) / 255.0, 2.5) * 255.0 + 0.5) for i in range(256)]

        # APA102/SK9822 requires latch bytes at the end)
        # Many thanks to this article for combined APA102/SK9822 protocol
        # https://cpldcpu.com/2016/12/13/sk9822-a-clone-of-the-apa102/
        self._start_frame = 4  # start frame is [0, 0, 0, 0]
        self._pixel_bytes = self.numLEDs * 4  # 4 byte frames [bright, r, g, b]
        self._pixel_stop = self._start_frame + self._pixel_bytes
        self._reset_frame = 4  # for SK9822 [0, 0, 0, 0]
        self._end_frame = (num // 2) + 1
        self._packet_size = (self._start_frame + self._pixel_bytes +  self._reset_frame + self._end_frame)
        self._packet = [0] * self._packet_size

        self.set_device_brightness(0xFF)  # required to setup _packet

    def _bootstrapSPIDev(self):
        import os.path
        import sys
        try:
            import spidev
        except:
            error = "Unable to import spidev. Please install. pip install spidev"
            log.error(error)
            raise ImportError(error)

        if not os.path.exists(self.dev):
            error = "Cannot find SPI device. Please see https://github.com/maniacallabs/bibliopixel/wiki/SPI-Setup for details."
            log.error(error)
            raise IOError(error)

        # permissions check
        try:
            open(self.dev)
        except IOError as e:
            if e.errno == 13:
                error = "Cannot find SPI device. Please see https://github.com/maniacallabs/bibliopixel/wiki/SPI-Setup for details."
                log.error(error)
                raise IOError(error)
            else:
                raise e

    def _sendData(self):
        self.spi.xfer2(self._packet)

    def set_device_brightness(self, val):
        """
        APA102 & SK9822 support on chip brightness control allowing greater color depth.
        APA102 superimposes a 440Hz PWM on the 19kHz base PWM to control brightness.
        SK9822 uses a base 4.7kHz PWM but controls brightness with a variable current source.
        Because of this SK9822 will have much less flicker at lower levels.
        Either way, this option is better and faster than scaling in BiblioPixel
        """
        self._chipset_brightness = (val >> 3)  # bitshift to scale from 8 bit to 5
        self._brightness_list = [0xE0 + self._chipset_brightness] * self.numLEDs
        self._packet[self._start_frame + 0:self._pixel_stop:4] = self._brightness_list

    def setMasterBrightness(self, brightness):
        self.set_device_brightness(brightness)
        return True

    def _fixData(self, data):
        for a, b in enumerate(self.c_order):
            self._buf[a:self.numLEDs * 3:3] = [self.gamma[v] for v in data[b::3]]
        self._packet[self._start_frame + 1:self._pixel_stop:4] = self._buf[0::3]
        self._packet[self._start_frame + 2:self._pixel_stop:4] = self._buf[1::3]
        self._packet[self._start_frame + 3:self._pixel_stop:4] = self._buf[2::3]

    def _update(self, data):
        self._fixData(data)
        self._sendData()


# class DriverAPA102(DriverSPIBase):
#     """Main driver for APA102 based LED strips on devices like the Raspberry Pi and BeagleBone"""

#     def __init__(self, num, c_order=ChannelOrder.RGB, use_py_spi=True, dev="/dev/spidev0.0", SPISpeed=2):
#         super(DriverAPA102, self).__init__(num, c_order=c_order,
#                                            use_py_spi=use_py_spi, dev=dev, SPISpeed=SPISpeed)

#         # APA102 requires latch bytes at the end
#         self._latchBytes = (int(num / 64.0) + 1)

#     def _fixData(self, data):
#         gamma = self.gamma
#         self._buf[:] = [0] * self.bufByteCount
#         for a, b in enumerate(self.c_order):
#             self._buf[a:self.numLEDs * 3:3] = [gamma[v] for v in data[b::3]]

#         newBuf = [0xFF] * (self.bufByteCount + self.numLEDs)
#         newBuf[1::4] = self._buf[0::3]
#         newBuf[2::4] = self._buf[1::3]
#         newBuf[3::4] = self._buf[2::3]
#         self._buf[:] = [0, 0, 0, 0] + newBuf
#         self._buf.extend([0xFF, 0, 0, 0] * self._latchBytes)



# class APA102(SPIBase):
#     """Driver for APA102/SK9822 based LED strips on devices like
#     the Raspberry Pi and BeagleBone
#     Provides the same parameters as
#     :py:class:`bibliopixel.drivers.SPI.SPIBase`
#     """

#     def __init__(self, num, gamma=gamma.APA102, **kwargs):
#         super().__init__(num, gamma=gamma, **kwargs)

#         # APA102/SK9822 requires latch bytes at the end)
#         # Many thanks to this article for combined APA102/SK9822 protocol
#         # https://cpldcpu.com/2016/12/13/sk9822-a-clone-of-the-apa102/
#         self._start_frame = 4  # start frame is [0, 0, 0, 0]
#         self._pixel_bytes = self.numLEDs * 4  # 4 byte frames [bright, r, g, b]
#         self._pixel_stop = self._start_frame + self._pixel_bytes
#         self._reset_frame = 4  # for SK9822 [0, 0, 0, 0]
#         self._end_frame = (num // 2) + 1
#         self._packet = self.maker.bytes(self._start_frame + self._pixel_bytes +
#                                         self._reset_frame + self._end_frame)

#         self.set_device_brightness(0xFF)  # required to setup _packet

#     def set_device_brightness(self, val):
#         """
#         APA102 & SK9822 support on chip brightness control allowing greater color depth.
#         APA102 superimposes a 440Hz PWM on the 19kHz base PWM to control brightness.
#         SK9822 uses a base 4.7kHz PWM but controls brightness with a variable current source.
#         Because of this SK9822 will have much less flicker at lower levels.
#         Either way, this option is better and faster than scaling in BiblioPixel
#         """
#         self._chipset_brightness = (val >> 3)  # bitshift to scale from 8 bit to 5
#         self._brightness_list = [0xE0 + self._chipset_brightness] * self.numLEDs
#         self._packet[self._start_frame + 0:self._pixel_stop:4] = self._brightness_list

#     def _compute_packet(self):
#         self._render()
#         self._packet[self._start_frame + 1:self._pixel_stop:4] = self._buf[0::3]
#         self._packet[self._start_frame + 2:self._pixel_stop:4] = self._buf[1::3]
#         self._packet[self._start_frame + 3:self._pixel_stop:4] = self._buf[2::3]