from RPi import GPIO
import tm1637
import time

SPICLK = 11
SPIMOSI = 10
SPIMISO = 9
SPICS = 8
ADC_PIN0 = 0
ADC_PIN1 = 1
ADC_PIN2 = 2
class Ad_Converter:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SPICLK, GPIO.OUT)
        GPIO.setup(SPIMOSI, GPIO.OUT)
        GPIO.setup(SPIMISO, GPIO.IN)
        GPIO.setup(SPICS, GPIO.OUT)
        
    def __del__(self):
        GPIO.cleanup()
    # MCP3208からSPI通信で12ビットのデジタル値を取得。0から7の8チャンネル使用可
    def readadc(self,adcnum, clockpin, mosipin, misopin, cspin):
        if adcnum > 7 or adcnum < 0:
            return -1
        GPIO.output(cspin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
        GPIO.output(cspin, GPIO.LOW)
    
        commandout = adcnum
        commandout |= 0x18  # スタートビット＋シングルエンドビット
        commandout <<= 3    # LSBから8ビット目を送信するようにする
        for i in range(5):
            # LSBから数えて8ビット目から4ビット目までを送信
            if commandout & 0x80:
                GPIO.output(mosipin, GPIO.HIGH)
            else:
                GPIO.output(mosipin, GPIO.LOW)
            commandout <<= 1
            GPIO.output(clockpin, GPIO.HIGH)
            GPIO.output(clockpin, GPIO.LOW)
        adcout = 0
        # 13ビット読む（ヌルビット＋12ビットデータ）
        for i in range(13):
            GPIO.output(clockpin, GPIO.HIGH)
            GPIO.output(clockpin, GPIO.LOW)
            adcout <<= 1
            if i>0 and GPIO.input(misopin)==GPIO.HIGH:
                adcout |= 0x1
        GPIO.output(cspin, GPIO.HIGH)
        return adcout
    def read_all(self):
        return [self.readadc(i,SPICLK,SPIMOSI,SPIMISO,SPICS)for i in [ADC_PIN0,ADC_PIN1,ADC_PIN2]]
    def main(self):
        tm = tm1637.TM1637(clk=21, dio=20)
        try:
            while 1:
                for i in [ADC_PIN0,ADC_PIN1,ADC_PIN2]:
                    a=self.readadc(i,SPICLK,SPIMOSI,SPIMISO,SPICS)
                    tm.number(a)
                    time.sleep(1)
        except KeyboardInterrupt:
            return
def main():
    Ad_Converter().main()
if __name__=="__main__":
    main()