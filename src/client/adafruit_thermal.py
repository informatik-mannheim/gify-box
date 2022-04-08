"""
Python Library for the Adafruit Thermal Printer.
This library is intended to be used with a Raspberry PI and
a full fledged serial interface. It does not perform handling
of pins but relies on the underlying serial library.
"""

##
#  Thermal printer ~C~ Python library for the
#
#  An Arduino library for the Adafruit Thermal Printer:
#
#  https://www.adafruit.com/product/597
#
#  These printers use TTL serial to communicate.  One pin (5V or 3.3V) is
#  required to issue data to the printer.  A second pin can OPTIONALLY be
#  used to poll the paper status, but not all printers support this, and
#  the output on this pin is 5V which may be damaging to some MCUs.
#
#  Adafruit invests time and resources providing this open source code.
#  Please support Adafruit and open-source hardware by purchasing products
#  from Adafruit!
#
#  @section author Author
#
#  Written by Limor Fried/Ladyada for Adafruit Industries, with
#  contributions from the open source community.  Originally based on
#  Thermal library from bildr.org
#
#  @section license License
#
#  MIT license, all text above must be included in any redistribution.
#
#  Ported to Python and the Raspberry PI by Thomas Smits
#
#  See https://github.com/adafruit/Adafruit-Thermal-Printer-Library
#  for the original code.
#
# pip3 install qrcode[pil]
# pip3 install imageio
# pip3 install pyserial

import time
import serial
import qrcode


class AdafruitThermal:
    """
    Class for the communication with the Adafruit Thermal Printer.
    """

    CHARSET_USA = 0  # American character set
    CHARSET_FRANCE = 1  # French character set
    CHARSET_GERMANY = 2  # German character set
    CHARSET_UK = 3  # UK character set
    CHARSET_DENMARK1 = 4  # Danish character set 1
    CHARSET_SWEDEN = 5  # Swedish character set
    CHARSET_ITALY = 6  # Italian character set
    CHARSET_SPAIN1 = 7  # Spanish character set 1
    CHARSET_JAPAN = 8  # Japanese character set
    CHARSET_NORWAY = 9  # Norwegian character set
    CHARSET_DENMARK2 = 10  # Danish character set 2
    CHARSET_SPAIN2 = 11  # Spanish character set 2
    CHARSET_LATINAMERICA = 12  # Latin American character set
    CHARSET_KOREA = 13  # Korean character set
    CHARSET_SLOVENIA = 14  # Slovenian character set
    CHARSET_CROATIA = 14  # Croatian character set
    CHARSET_CHINA = 15  # Chinese character set

    # Character code tables used with ESC t n
    CODEPAGE_CP437 = 0  # USA, Standard Europe character code table
    CODEPAGE_KATAKANA = 1  # Katakana (Japanese) character code table
    CODEPAGE_CP850 = 2  # Multilingual character code table
    CODEPAGE_CP860 = 3  # Portuguese character code table
    CODEPAGE_CP863 = 4  # Canadian-French character code table
    CODEPAGE_CP865 = 5  # Nordic character code table
    CODEPAGE_WCP1251 = 6  # Cyrillic character code table
    CODEPAGE_CP866 = 7  # Cyrillic #2 character code table
    CODEPAGE_MIK = 8  # Cyrillic/Bulgarian character code table
    CODEPAGE_CP755 = 9  # East Europe, Latvian 2 character code table
    CODEPAGE_IRAN = 10  # Iran 1 character code table
    CODEPAGE_CP862 = 15  # Hebrew character code table
    CODEPAGE_WCP1252 = 16  # Latin 1 character code table
    CODEPAGE_WCP1253 = 17  # Greek character code table
    CODEPAGE_CP852 = 18  # Latin 2 character code table
    CODEPAGE_CP858 = 19  # Multilingual Latin 1 + Euro character code table
    CODEPAGE_IRAN2 = 20  # Iran 2 character code table
    CODEPAGE_LATVIAN = 21  # Latvian character code table
    CODEPAGE_CP864 = 22  # Arabic character code table
    CODEPAGE_ISO_8859_1 = 23  # West Europe character code table
    CODEPAGE_CP737 = 24  # Greek character code table
    CODEPAGE_WCP1257 = 25  # Baltic character code table
    CODEPAGE_THAI = 26  # Thai character code table
    CODEPAGE_CP720 = 27  # Arabic character code table
    CODEPAGE_CP855 = 28  # Cyrillic character code table
    CODEPAGE_CP857 = 29  # Turkish character code table
    CODEPAGE_WCP1250 = 30  # Central Europe character code table
    CODEPAGE_CP775 = 31  # Baltic character code table
    CODEPAGE_WCP1254 = 32  # Turkish character code table
    CODEPAGE_WCP1255 = 33  # Hebrew character code table
    CODEPAGE_WCP1256 = 34  # Arabic character code table
    CODEPAGE_WCP1258 = 35  # Vietnam character code table
    CODEPAGE_ISO_8859_2 = 36  # Latin 2 character code table
    CODEPAGE_ISO_8859_3 = 37  # Latin 3 character code table
    CODEPAGE_ISO_8859_4 = 38  # Baltic character code table
    CODEPAGE_ISO_8859_5 = 39  # Cyrillic character code table
    CODEPAGE_ISO_8859_6 = 40  # Arabic character code table
    CODEPAGE_ISO_8859_7 = 41  # Greek character code table
    CODEPAGE_ISO_8859_8 = 42  # Hebrew character code table
    CODEPAGE_ISO_8859_9 = 43  # Turkish character code table
    CODEPAGE_ISO_8859_15 = 44  # Latin 3 character code table
    CODEPAGE_THAI2 = 45  # Thai 2 character code page
    CODEPAGE_CP856 = 46  # Hebrew character code page
    CODEPAGE_CP874 = 47  # Thai character code page

    BARCODE_UPC_A = 0  # UPC-A barcode system. 11-12 char */
    BARCODE_UPC_E = 1  # UPC-E barcode system. 11-12 char */
    BARCODE_EAN13 = 2  # EAN13 (JAN13) barcode system. 12-13 char */
    BARCODE_EAN8 = 3  # EAN8 (JAN8) barcode system. 7-8 char */
    BARCODE_CODE39 = 4  # CODE39 barcode system. 1<=num of chars */
    BARCODE_ITF = 5  # ITF barcode system. 1<=num of chars, must be an even number */
    BARCODE_CODABAR = 6  # CODABAR barcode system. 1<=num<=255 */
    BARCODE_CODE93 = 7  # CODE93 barcode system. 1<=num<=255 */
    BARCODE_CODE128 = 8  # CODE128 barcode system. 2<=num<=255 */

    ASCII_TAB = '\t'  # Horizontal tab
    ASCII_LF = '\n'  # Line feed
    ASCII_FF = '\f'  # Form feed
    ASCII_CR = '\r'  # Carriage return
    ASCII_DC2 = 18  # Device control 2
    ASCII_ESC = 27  # Escape
    ASCII_FS = 28  # Field separator
    ASCII_GS = 29  # Group separator

    FONT_MASK = (1 << 0)  # Select character font A or B
    INVERSE_MASK = (1 << 1)  # Turn on/off white/black reverse printing mode. No in 268 (see inverseOn())
    UPDOWN_MASK = (1 << 2)  # Turn on/off upside-down printing mode
    BOLD_MASK = (1 << 3)  # Turn on/off bold printing mode
    DOUBLE_HEIGHT_MASK = (1 << 4)  # Turn on/off double-height printing mode
    DOUBLE_WIDTH_MASK = (1 << 5)  # Turn on/off double-width printing mode
    STRIKE_MASK = (1 << 6)  # Turn on/off deleteline mode

    def __init__(self, port="/dev/serial0", baudrate=19200):
        """
        Create a new instance.
        :param port: the device the serial port is attached to. Defaults to '/dev/serial0'
        :param baudrate: the baud rate of the printer, defaults to 19200
        """

        self._print_mode = 0
        self._prev_byte = 0  # Last character issued to printer
        self._column = 0  # Last horizontal column printed
        self._max_column = 0  # Page width (output 'wraps' at this point)
        self._char_height = 0  # Height of characters, in 'dots'
        self._line_spacing = 0  # Inter-line spacing (not line height) in dots
        self._barcode_height = 0  # Barcode height in dots, not including text
        self._max_chunk_height = 0
        self._dtr_pin = 500  # DTR handshaking pin (experimental)
        self._firmware = 0  # Firmware version
        self._dtr_enabled = False  # True if DTR pin set & printer initialized
        self._resume_time = 0  # Wait until micros() exceeds this before sending byte
        self._dot_print_time = 0  # Time to print a single dot line, in microseconds
        self._dot_feed_time = 0  # Time to feed a single dot line, in microseconds
        self._port = port

        if port is not None:
            self._ser = serial.Serial(port, baudrate)  # open serial port
        else:
            self._ser = None

        # Because there's no flow control between the printer and Arduino,
        # special care must be taken to a  def overrunning the printer's buffer.
        # Serial output is throttled based on serial speed as well as an estimate
        # of the device's print and feed rates (relatively slow, being bound to
        # moving parts and physical reality).  After an operation is issued to
        # the printer (e.g. bitmap print), a timeout is set before which any
        # other printer operations will be suspended.  This is generally more
        # efficient than using delay() in that it allows the parent code to
        # continue with other duties (e.g. receiving or decoding an image)
        # while the printer physically completes the task.
        #
        # Number of microseconds to issue one byte to the printer. 11 bits
        # (not 8) to accommodate idle, start and stop bits.  Idle time might
        # be unnecessary, but erring on side of caution here.
        #
        self._byte_time = (((11 * 1000000) + (baudrate / 2)) / baudrate)

    def __del__(self):
        if self._ser is not None:
            self._ser.close()

    @staticmethod
    def __delay(msecs):
        """
        Wait for at least the given amount of time (in milliseconds).
        :param msecs: time in milliseconds to wait
        """
        time.sleep(msecs / 1000)

    @staticmethod
    def __micros():
        """
        Read the internal clock with microsecond precision.
        :return: internal clock value in microseconds
        """
        return time.clock_gettime_ns(time.CLOCK_REALTIME) / 1000

    def printer_init(self, dtr):
        """
        Initialize the printer.

        :param dtr: pin for the DTR (Data Terminal Ready) signal
        """
        self._dtr_enabled = False
        self._dtr_pin = dtr

    def timeout_set(self, x):
        """
        Sets the estimated completion time for a just-issued task.
        :param x: the timeout
        """
        if not self._dtr_enabled:
            self._resume_time = self.__micros() + x

    def timeout_wait(self):
        """
        Waits (if necessary) for the prior task to complete.
        """
        if self._dtr_enabled:
            while (self.__micros() - self._resume_time) < 0:
                if False:
                    break  # TODO: Check for printer status here
        else:
            while (self.__micros() - self._resume_time) < 0:
                pass

    def set_times(self, p, f):
        """
        This method sets the times (in microseconds) for the
        paper to advance one vertical 'dot' when printing and when feeding.
        For example, in the default initialized state, normal-sized text is
        24 dots tall and the line spacing is 30 dots, so the time for one
        line to be issued is approximately 24 * print time + 6 * feed time.
        The default print and feed times are based on a random test unit,
        but as stated above your reality may be influenced by many factors.
        This lets you tweak the timing to a excessive delays and/or
        overrunning the printer buffer.

        Printer performance may vary based on the power supply voltage,
        thickness of paper, phase of the moon and other seemingly random
        variables.
        :param p: time (in milliseconds) to print one dot
        :param f: time (in milliseconds) to feed one dot
        :return:
        """
        self._dot_print_time = p
        self._dot_feed_time = f

    def _send_to_printer(self, b):
        """
        Write one byte to the printer. It is the low level function
        that eventually sends the data out.
        :param b: the byte (as string or int) to print
        """
        if type(b) == str:
            c = ord(b[0])
        else:
            c = b

        raw = c.to_bytes(1, byteorder='big', signed=False)

        if self._ser is not None:
            self._ser.write(raw)
        else:
            print(raw)

    def _read_from_printer(self):
        """
        Read a byte from the printer.
        :return: the byte as int value
        """
        if self._ser is not None:
            val = self._ser.read(1)
        else:
            val = b'\xff'

        return int.from_bytes(val, byteorder='big', signed=False)

    def available(self):
        """
        Checks if the printer is ready to receive more data.
        :return: True if the printer is ready, otherwise False
        """
        if self._ser is not None:
            return self._ser.dtr
        else:
            return True

    def write(self, *bts):
        """
        Writes an arbitrary number of bytes to the printer.
        The function calculates the wait time based on
        the data written
        :param bts: bytes to be written
        """
        self.timeout_wait()

        for byte in bts:
            self._send_to_printer(byte)

        self.timeout_set(len(bts) * self._byte_time)

    # The underlying method for all high-level printing (e.g. println()).
    def _write_char_to_printer(self, c):
        """
        Write a single character to the printer.
        :param c: the character (as int value)
        """

        if c != 13:  # Strip carriage returns
            self.timeout_wait()
            self._send_to_printer(c)
            d = self._byte_time
            if (c == '\n') or (self._column == self._max_column):  # If newline or wrap
                if self._prev_byte == '\n':
                    d += ((self._char_height + self._line_spacing) * self._dot_feed_time)  # Feed line
                else:
                    d += ((self._char_height * self._dot_print_time) +
                          (self._line_spacing * self._dot_feed_time))  # Text line

                self._column = 0
                c = '\n'  # Treat wrap as newline on next pass
            else:
                self._column = self._column + 1

            self.timeout_set(d)
            self._prev_byte = c

    def begin(self, version=268):
        """
        Begin communication with the printer.
        :param version: firmware version
        """
        self._firmware = version

        # The printer can't start receiving data immediately upon power up --
        # it needs a moment to cold boot and initialize.  Allow at least 1/2
        # sec of uptime before printer can receive data.
        self.timeout_set(500000)

        self.wake()
        self.reset()

        self.set_heat_config(11, 120, 40)

        # Enable DTR pin if requested
        if self._dtr_pin < 255:
            # TODO: How to handle on RaspBerry?
            self.write(self.ASCII_GS, 'a', (1 << 5))
            self._dtr_enabled = True

        self._dot_print_time = 30000  # See comments near top of file for
        self._dot_feed_time = 2100  # an explanation of these values.
        self._max_chunk_height = 255

    def reset(self):
        """
        Reset printer to default state.
        """
        self.write(self.ASCII_ESC, '@')  # Init command
        self._prev_byte = '\n'  # Treat as if prior line is blank
        self._column = 0
        self._max_column = 32
        self._char_height = 24
        self._line_spacing = 6
        self._barcode_height = 50

        if self._firmware >= 264:
            # Configure tab stops on recent printers
            self.write(self.ASCII_ESC, 'D')  # Set tab stops...
            self.write(4, 8, 12, 16)  # ...every 4 columns,
            self.write(20, 24, 28, 0)  # 0 marks end-of-list.

    def set_default(self):
        """
        Reset text formatting parameters.
        """
        self.online()
        self.justify('L')
        self.inverse_off()
        self.double_height_off()
        self.set_line_height(30)
        self.bold_off()
        self.underline_off()
        self.set_barcode_height(50)
        self.set_size('s')
        self.set_charset(0)
        self.set_code_page(0)

    def test_page(self):
        """
        Print a test page.
        """
        self.write(self.ASCII_DC2, 'T')
        self.timeout_set(
            self._dot_print_time * 24 * 26 +  # 26 lines w/text (ea. 24 dots high)
            self._dot_feed_time *
            (6 * 26 + 30))  # 26 text lines (feed 6 dots) + blank line

    def set_barcode_height(self, val=50):  # Default is 50
        """
        Sets the height of the barcode.
        :param val: the height of the barcode in pixel
        """
        if val < 1:
            val = 1

        self._barcode_height = val
        self.write(self.ASCII_GS, 'h', val)

    # === Character commands ===

    def _adjust_char_values(self, print_mode):
        """
        Adjust the internal settings based on the print mode.
        :param print_mode: print mode
        """

        if print_mode & self.FONT_MASK != 0:
            # FontB
            self._char_height = 17
            char_width = 9
        else:
            # FontA
            self._char_height = 24
            char_width = 12

        # Double Width Mode
        if print_mode & self.DOUBLE_WIDTH_MASK != 0:
            self._max_column /= 2
            char_width *= 2

        # Double Height Mode
        if print_mode & self.DOUBLE_HEIGHT_MASK != 0:
            self._char_height *= 2

        self._max_column = (384 / char_width)

    def _set_print_mode(self, mask):
        """
        Set the print mode.
        :param mask: bit mask with the print settings
        """
        self._print_mode |= mask
        self._write_print_mode()
        self._adjust_char_values(self._print_mode)
        # charHeight = (printMode & DOUBLE_HEIGHT_MASK) ? 48 : 24
        # maxColumn = (printMode & DOUBLE_WIDTH_MASK) ? 16 : 32

    def _unset_print_mode(self, mask):
        """
        Removes a bit from the print mode mask.
        :param mask: the mask with the bit to be removed
        """
        self._print_mode &= ~mask
        self._write_print_mode()
        self._adjust_char_values(self._print_mode)
        # charHeight = (printMode & DOUBLE_HEIGHT_MASK) ? 48 : 24
        # maxColumn = (printMode & DOUBLE_WIDTH_MASK) ? 16 : 32

    def _write_print_mode(self):
        """
        Sends the current print mode to the pringter
        """
        self.write(self.ASCII_ESC, '!', self._print_mode)

    def normal(self):
        """
        Resets the print mode to normal.
        """
        self._print_mode = 0
        self._write_print_mode()

    def inverse_on(self):
        """
        Turn on inverse printing (white text on black).
        """
        if self._firmware >= 268:
            self.write(self.ASCII_GS, 'B', 1)
        else:
            self._set_print_mode(self.INVERSE_MASK)

    def inverse_off(self):
        """
        Trun off inverse printing.
        """
        if self._firmware >= 268:
            self.write(self.ASCII_GS, 'B', 0)
        else:
            self._unset_print_mode(self.INVERSE_MASK)

    def upside_down_on(self):
        """
        Turn printing upside down on.
        """
        if self._firmware >= 268:
            self.write(self.ASCII_ESC, '{', 1)
        else:
            self._set_print_mode(self.UPDOWN_MASK)

    def upside_down_off(self):
        """
          Turn printing upside down off.
          """
        if self._firmware >= 268:
            self.write(self.ASCII_ESC, '{', 0)
        else:
            self._unset_print_mode(self.UPDOWN_MASK)

    def double_height_on(self):
        """
        Turn printing with double height on.
        """
        self._set_print_mode(self.DOUBLE_HEIGHT_MASK)

    def double_height_off(self):
        """
        Turn printing with double height off.
        """
        self._unset_print_mode(self.DOUBLE_HEIGHT_MASK)

    def double_width_on(self):
        """
        Turn printing with double width on.
        """
        self._set_print_mode(self.DOUBLE_WIDTH_MASK)

    def double_width_off(self):
        """
        Turn printing with double width off.
        """
        self._unset_print_mode(self.DOUBLE_WIDTH_MASK)

    def strike_on(self):
        """
        Turn printing with strike-out width on.
        """
        self._set_print_mode(self.STRIKE_MASK)

    def strike_off(self):
        """
        Turn printing with strike-out width off.
        """
        self._unset_print_mode(self.STRIKE_MASK)

    def bold_on(self):
        """
        Turn bold printing on.
        """
        self._set_print_mode(self.BOLD_MASK)

    def bold_off(self):
        """
        Turn bold printing off.
        """
        self._unset_print_mode(self.BOLD_MASK)

    def justify(self, value):
        """
        Justify the text in printout.
        :param value: the justification as string. 'L' = left, 'R' = right, 'C' = center
        """
        pos = 0
        upper = value.upper()

        if upper == 'L':
            pos = 0
        elif upper == 'C':
            pos = 1
        elif upper == 'R':
            pos = 2

        self.write(self.ASCII_ESC, 'a', pos)

    def feed(self, x=1):
        """
        Feeds by the specified number of lines.
        :param x: number of lines to feed
        """
        if self._firmware >= 264:
            self.write(self.ASCII_ESC, 'd', x)
            self.timeout_set(self._dot_feed_time * self._char_height)
            self._prev_byte = '\n'
            self._column = 0
        else:
            while x > 0:
                self.write('\n')  # Feed manually old firmware feeds excess lines
                x -= 1

    def feed_rows(self, rows):
        """
        Feeds by the specified number of individual pixel rows.
        :param rows: the pixel rows to feed
        """
        self.write(self.ASCII_ESC, 'J', rows)
        self.timeout_set(rows * self._dot_feed_time)
        self._prev_byte = '\n'
        self._column = 0

    def flush(self):
        """
        Flush all data and print it.
        """
        self.write(self.ASCII_FF)

    def set_size(self, value='S'):
        """
        Set the size of the font. The default is small ('S')
        :param value: size as string. 'L' = large, 'M' = medium, 'S' = small
        """
        upper = value.upper()

        if upper == 'M':  # Medium: double height
            # size = 0x01
            # charHeight = 48
            # maxColumn = 32
            self.double_height_on()
            self.double_width_off()
        elif upper == 'L':  # Large: double width and height
            # size = 0x11
            # charHeight = 48
            # maxColumn = 16
            self.double_height_on()
            self.double_width_on()
        else:  # Small: standard width and height
            # size = 0x00
            # charHeight = 24
            # maxColumn = 32
            self.double_width_off()
            self.double_height_off()
        # writeBytes(ASCII_GS, '!', size)
        # prevByte = '\n' # Setting the size adds a linefeed

    def set_heat_config(self, dots=11, heat_time=120, interval=40):
        """
        Control the heating configuration of the printer.
        More heating dots = more peak current, but faster printing speed.
        More heating time = darker print, but slower printing speed and
        possibly paper 'stiction'. More heating interval = clearer print,
        but slower printing speed.

        :param dots: max heating dots" 0-255; max number of thermal print
            head elements that will fire simultaneously. Units = 8 dots
            (minus 1). Printer default is 7 (64 dots, or 1/6 of 384-dot width),
            this code sets it to 11 (96 dots, or 1/4 of width).
        :param heat_time: heating time" 3-255; duration that heating dots
            are fired. Units = 10 us.  Printer default is 80 (800 us),
            this code sets it to value passed (default 120, or 1.2 ms --
            a little longer than the default because we've increased the
            max heating dots).
        :param interval: heating interval" 0-255; recovery time between
            groups of heating dots on line possibly a function of power supply.
            Units = 10 us.  Printer default is 2 (20 us), this code sets it to
            40 (throttled back due to 2A supply).
        """
        self.write(self.ASCII_ESC, '7')  # Esc 7 (print settings)
        self.write(dots, heat_time, interval)  # Heating dots, heat time, heat interval

    def set_print_density(self, density=10, break_time=2):
        """
        Set the printing density.
        :param density: density
        :param break_time: time to break
        :return:
        """
        self.write(self.ASCII_DC2, '#', (density << 5) | break_time)

    def underline_on(self, weight=1):
        """
        Turns underline on. Underlines of different weights can be produced.
        :param weight: the weight of the line.
            0 - no underline
            1 - normal underline
            2 - thick underline
        """
        if weight > 2:
            weight = 2
            self.write(self.ASCII_ESC, '-', weight)

    def underline_off(self):
        """
        Turns underline off.
        """
        self.write(self.ASCII_ESC, '-', 0)

    def print_bitmap(self, w, h, bitmap):
        """
        Print a bitmap image.
        :param w: width of the image
        :param h: height of the image
        :param bitmap: the bitmap as an array of
            grayscale values in the range of 0-255
        """
        row_bytes = (w + 7) // 8  # Round up to next byte boundary

        if row_bytes >= 48:
            row_bytes_clipped = 48
        else:
            row_bytes_clipped = row_bytes  # 384 pixels max width

        # Est. max rows to write at once, assuming 256 byte printer buffer.
        if self._dtr_enabled:
            chunk_height_limit = 255  # Buffer doesn't matter, handshake!
        else:
            chunk_height_limit = 256 // row_bytes_clipped
            if chunk_height_limit > self._max_chunk_height:
                chunk_height_limit = self._max_chunk_height
            elif chunk_height_limit < 1:
                chunk_height_limit = 1

        row_start = 0
        i = 0
        while row_start < h:
            # Issue up to chunkHeightLimit rows at a time:
            chunk_height = h - row_start
            if chunk_height > chunk_height_limit:
                chunk_height = chunk_height_limit

            self.write(self.ASCII_DC2, '*', chunk_height, row_bytes_clipped)

            y = 0
            while y < chunk_height:
                x = 0
                while x < row_bytes_clipped:
                    self.timeout_wait()
                    self._send_to_printer(int(bitmap[i]))
                    x += 1
                    i += 1

                y += 1

            i += row_bytes - row_bytes_clipped

            self.timeout_set(chunk_height * self._dot_print_time)

            row_start += chunk_height_limit

        self._prev_byte = '\n'

    def offline(self):
        """
        Take the printer offline. Print commands sent after this will be
        ignored until 'online' is called.
        """
        self.write(self.ASCII_ESC, '=', 0)

    def online(self):
        """
        Take the printer back online. Subsequent print commands will be obeyed.
        """
        self.write(self.ASCII_ESC, '=', 1)

    def sleep(self):
        """
        Put the printer into a low-energy state immediately.
        """
        self.sleep_after(1)  # Can't be 0, that means 'don't sleep'

    #
    def sleep_after(self, seconds):
        """
        Put the printer into a low-energy state after the given number of seconds.
        :param seconds: seconds to wait before printer goes to sleep.
        """
        if self._firmware >= 264:
            self.write(self.ASCII_ESC, '8', seconds, seconds >> 8)
        else:
            self.write(self.ASCII_ESC, '8', seconds)

    def wake(self):
        """
        Wake the printer from a low-energy state.
        """
        self.timeout_set(0)  # Reset timeout counter
        self.write(255)  # Wake

        if self._firmware >= 264:
            self.__delay(50)
            self.write(self.ASCII_ESC, '8', 0, 0)  # Sleep off (important!)
        else:
            # Datasheet recommends a 50 mS delay before issuing further commands,
            # but in practice this alone isn't sufficient (e.g. text size/style
            # commands may still be misinterpreted on wake).  A slightly longer
            # delay, interspersed with NUL chars (no-ops) seems to help.
            i = 0
            while i < 10:
                self.write(0)
                self.timeout_set(10000)
                i += 1

    def has_paper(self):
        """
        Check the status of the paper using the printer's self reporting
        ability. Returns true for paper, false for no paper.
        Might not work on all printers!
        :return: True if paper is available, otherwise False
        """
        if self._firmware >= 264:
            self.write(self.ASCII_ESC, 'v', 0)
        else:
            self.write(self.ASCII_GS, 'r', 0)

        status = -1
        i = 0
        while i < 10:
            if self.available():
                status = self._read_from_printer()
                break

            self.__delay(100)
            i = i + 1

        return not (status & 0b00000100)

    def set_line_height(self, val=30):
        """
        Set the height of a line.
        :param val: the height of the line in pixel
        """
        if val < 24:
            val = 24
        self._line_spacing = val - 24

        # The printer doesn't take into account the current text height
        # when setting line height, making this more akin to inter-line
        # spacing.  Default line spacing is 30 (char height of 24, line
        # spacing of 6).
        self.write(self.ASCII_ESC, '3', val)

    def set_max_chunk_height(self, val=256):
        """
        Set the maximum height of a chunk.
        :param val: the maximum height
        """
        self._max_chunk_height = val

    # These commands work only on printers w/recent firmware ------------------

    def set_charset(self, val=0):
        """
        Alters some chars in ASCII 0x23-0x7E range see datasheet
        :param val: the value to be sent to the printer
        """
        if val > 1:
            val = 15
        self.write(self.ASCII_ESC, 'R', val)

    #
    def set_code_page(self, val=0):
        """
        Selects alt symbols for 'upper' ASCII values 0x80-0xFF.
        :param val: the codepage. See CODEPAGE_* constants
        """
        if val > 47:
            val = 47
        self.write(self.ASCII_ESC, 't', val)

    def tab(self):
        """
        Performs a vertical tab step.
        """
        self.write(self.ASCII_TAB)
        self._column = (self._column + 4) & 0b11111100

    def set_font(self, font='A'):
        """
        Selects the font for the printout.
        :param font: the font to be selected. Possible values 'A' and 'B'
        """
        upper = font.upper()
        if upper == 'B':
            self._set_print_mode(self.FONT_MASK)
        elif upper == 'A':
            self._unset_print_mode(self.FONT_MASK)
        else:
            self._unset_print_mode(self.FONT_MASK)

    def set_char_spacing(self, spacing=0):
        """
        Sets the spacing between chars.
        :param spacing: the spacing in pixels.
        """
        self.write(self.ASCII_ESC, ' ', spacing)

    # High-level methods

    def print(self, text):
        """
        Prints the given text to the printer.
        :param text: the text to be printed.
        """
        for c in text:
            self._write_char_to_printer(c)
            pass

    def println(self, text=''):
        """
        Prints the given text and ends it with a newline.
        :param text: the text to be printed.
        """
        self.print(text)
        self.print("\n")

    def print_qr_code(self, text):
        """
        Prints an QR code with the given text.
        :param text: the text to be encoded in the QR code
        """
        qr = qrcode.make(text)
        img = qr.get_image()
        width = img.width
        height = img.height
        raw = list(img.im)
        self.print_bitmap(width, height, raw)

    def print_barcode(self, text, barcode_type):
        """
        Prints a barcode.
        :param text: text to be encoded in the barcode
        :param barcode_type: the type of the barcode according BARCODE_* constants
        """
        self.feed(1)  # Recent firmware can't print barcode w/o feed first???
        if self._firmware >= 264:
            barcode_type += 65

        self.write(self.ASCII_GS, 'H', 2)  # Print label below barcode
        self.write(self.ASCII_GS, 'w', 3)  # Barcode width 3 (0.375/1.0mm thin/thick)
        self.write(self.ASCII_GS, 'k', barcode_type)  # Barcode type (listed in .h file)

        length = len(text)

        if self._firmware >= 264:
            if length > 255:
                length = 255

            self.write(length)  # Write length byte

            i = 0
            while i < length:
                self.write(text[i])  # Write string sans NUL
                i = i + 1
        else:
            i = 0
            while i < length:
                self.write(text[i])
                i = i + 1
            self.write(0)

        self.timeout_set((self._barcode_height + 40) * self._dot_print_time)
        self._prev_byte = '\n'
