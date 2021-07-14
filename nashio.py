import smbus
import time


class LCD:
    def __init__(self):
        self.BUS = smbus.SMBus(1)
        self.ADRESS_ST7032 = 0x3e
        self.REGISTER_SETTING = 0x00
        self.REGISTER_DISPLAY = 0x40
        self.contrast = 32  # 0から63のコントラスト。30から40程度を推奨
        self.CHARS_PER_LINE = 8  # LCDの横方向の文字数
        self.DISPLAY_LINES = 2   # LCDの行数
        self.DISPLAY_CHARS = self.CHARS_PER_LINE*self.DISPLAY_LINES
        self.position = 0
        self.line = 0
        trials = 5
        for i in range(trials):
            try:
                c_lower = (self.contrast & 0xf)
                c_upper = (self.contrast & 0x30) >> 4
                self.BUS.write_i2c_block_data(self.ADRESS_ST7032, self.REGISTER_SETTING, [
                                              0x38, 0x39, 0x14, 0x70 | c_lower, 0x54 | c_upper, 0x6c])
                time.sleep(0.2)
                self.BUS.write_i2c_block_data(
                    self.ADRESS_ST7032, self.REGISTER_SETTING, [0x38, 0x0d, 0x01])
                time.sleep(0.001)
                break
            except IOError:
                if i == trials-1:
                    exit()

    def clear(self,):

        self.position = 0
        self.line = 0
        self.BUS.write_byte_data(
            self.ADRESS_ST7032, self.REGISTER_SETTING, 0x01)
        time.sleep(0.001)

    def newline(self,):
        if self.line == self.DISPLAY_LINES-1:
            self.clear()
        else:
            self.line += 1
            self.position = self.CHARS_PER_LINE*self.line
            self.BUS.write_byte_data(
                self.ADRESS_ST7032, self.REGISTER_SETTING, 0xc0)
            time.sleep(0.001)

    def write_string(self, s: str):
        for c in s:
            self.write_char(ord(c))

    def write_char(self, c: str):
        byte_data = self.check_writable(c)
        if self.position == self.DISPLAY_CHARS:
            self.clear()
        elif self.position == self.CHARS_PER_LINE*(self.line+1):
            self.newline()
        self.BUS.write_byte_data(
            self.ADRESS_ST7032, self.REGISTER_DISPLAY, byte_data)
        self.position += 1

    def check_writable(self, c):
        if c >= 0x06 and c <= 0xff:  # if ascii
            return c
        if ord("｡") <= c <= ord("ﾋﾟ"[1]):  # if hankaku katakana
            return c-ord("｡")+0b10100001
        else:
            return 0x20  # 空白文字


def main():
    lcd = LCD()
    lcd.write_string("ﾗｽﾞﾍﾞﾘｰ")
    lcd.newline()
    lcd.write_string("ﾊﾟｲ")


def nashio():
    lcd = LCD()
    a = input()
    if a:
        lcd.write_string(a)
    else:
        lcd.write_string("ﾅｼｵ ﾀｶｼ")
    # lcd.newline()


if __name__ == "__main__":
    # main()
    nashio()
