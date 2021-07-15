import Telmin
import argparse
import random
import datetime
import tm1637
import nashio
import numpy as np
LA=440
a, aa, b, c, cc, d, dd, e, f, ff, g, gg = np.geomspace(
    LA, LA*2, 12, endpoint=False)
OCTAVE = [(c, "ﾄﾞ"), (cc, "ﾄﾞ#"), (d, "ﾚ"), (dd, "ﾚ#"), (e, "ﾐ"), (f, "ﾌｧ"),
          (ff, "ﾌｧ#"), (g, "ｿ"), (gg, "ｿ#"), (a*2, "ﾗ"), (aa*2, "ﾗ#"), (b*2, "ｼ")]
# print(OCTAVE)


class DisplaySound:
    def __init__(self):
        self.lcd = nashio.LCD()
        self.tm = tm1637.TM1637(clk=21, dio=20)
        parser = argparse.ArgumentParser(description='音楽を鳴らすよ！')
        parser.add_argument(
            "-l", "--rangel",
            default=-2, type=int,
            help="音の範囲の左,マイナスでも可能です。[l,r)のlです。"
        )
        parser.add_argument(
            "-r", "--ranger",
            default=+3, type=int,
            help="音の範囲の右,マイナスでも可能です。[l,r)のrです。"
        )
        parser.add_argument(
            "-d", "--distancemax",
            default=Telmin.DISTANCE_HIGH, type=int,
            help="測る距離のmaxです。100以上は意味ないです(たぶん)"
        )
        parser.add_argument('--excludesharp', action='store_true',
                            help="これを指定すると、sharp付きの音が消えます。")
        self.args = parser.parse_args()

        if self.args.rangel>self.args.ranger:
            raise ValueError("ranger should be larger than rangel.\nrangerはrangelよりも大きくなくてはいけません。")
        if not(0<self.args.distancemax<=100):
            raise ValueError("distancemax should be larger than 0 and smaller than 100.\ndistancemaxは0より大きく、100以下でなければいけません。")

    def __del__(self):
        self.lcd.clear()
        self.lcd.write_string("ｼｭｳﾘｮｳ")
        self.lcd.newline()
        self.lcd.write_string("ｼﾏｼﾀ")
        self.tm.show(" End")

    def make_sound(self, distance: float, base=OCTAVE):
        if distance >= self.args.distancemax:
            self.lcd.clear()
            self.lcd.write_string("ｵﾄﾊ")
            self.lcd.newline()
            self.lcd.write_string("ﾅｯﾃｲﾏｾﾝ")
            now=datetime.datetime.now()
            self.tm.numbers(now.hour,now.minute)
            return 0
        for i, j in zip(range(len(base))[::-1], np.linspace(0, self.args.distancemax, len(base)-1, endpoint=True)):
            if distance < j:
                # self.lcd.write_string("ｹﾞﾝｻﾞｲﾉｵﾄﾊ")
                # self.lcd.newline()
                hz = int(round(base[i][0]))
                self.lcd.clear()
                self.lcd.write_string(f"{hz}Hz")
                self.lcd.newline()
                self.lcd.write_string(base[i][1])
                self.tm.number(hz)
                return hz

    def main(self, octave=OCTAVE):
        if self.args.excludesharp:
            octave = [i for i in OCTAVE if "#" not in i[1]]
        base = []
        for i in range(self.args.rangel, self.args.ranger):
            base += map(lambda x: (x[0]*(2**i), x[1]), octave)
        print(len(base))
        def sound_function(x): return self.make_sound(x, base)
        termin = Telmin.Telmin()
        termin.main(sound_function)


if __name__ == "__main__":
    DisplaySound().main()
