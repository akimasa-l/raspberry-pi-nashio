import datetime
import time
import tm1637
tm = tm1637.TM1637(clk=21, dio=20)
F=0b01110001
U=0b00111110
C=0b00111001
K=0b01110110
try:
    while 1:
        now=datetime.datetime.now()
        # print(now.hour,now.minute)
        tm.numbers(now.hour,now.minute)
        time.sleep(10)
        
        tm.write([F,U,C,K])
        time.sleep(10)
except KeyboardInterrupt:
    pass

tm.scroll("FUCK", delay=250)
