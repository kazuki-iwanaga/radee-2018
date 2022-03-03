import sys
import time
import csv
import spidev
import RPi.GPIO as GPIO
import json
import urllib.request
import datetime

def setup(spi):
    spi.open(0, 0)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(19,GPIO.OUT)
    GPIO.setup(26,GPIO.OUT)
    GPIO.setup(13,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.output(19,GPIO.LOW)
    GPIO.output(26,GPIO.LOW)

def measurement(spi, t_init):
    filename = sys.argv[1]
    with open('/home/pi/radee-2018/public/csv/' + filename + '.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        # for i in range(n_times):
        delta_t = 0
        while delta_t < int(sys.argv[2]):
            GPIO.wait_for_edge(13,GPIO.RISING)
            time.sleep(0.0003)
            GPIO.output(26,GPIO.HIGH)
            # SPI通信：値の読み出し
            tmp = spi.xfer2([0x68, 0x00])
            volt = ((tmp[0] << 8) + tmp[1]) & 0x3ff
            delta_t = round((time.time() - t_init), 2)
            dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # CSV書き出し
            writer.writerow([dt, volt])
            # デバッグ用
            # print([volt, delta_t])
            data = {
                'voltage': volt,
                'delta_t': delta_t,
                'datetime': str(dt)
            }
            req = urllib.request.Request(url, json.dumps(data).encode(), headers)
            try:
                with urllib.request.urlopen(req) as res:
                    body = res.read()
            except urllib.error.HTTPError as err:
                print(err.code)
            except urllib.error.URLError as err:
                print(err.reason)
            GPIO.output(26,GPIO.LOW)
            time.sleep(0.0003)
            GPIO.output(19,GPIO.HIGH)
            time.sleep(0.0005)
            GPIO.output(19,GPIO.LOW)

def termination(spi):
    spi.close()
    GPIO.cleanup()

if __name__ == '__main__':
    print("----- Let's Start Our Measurement! -----")
    url = 'http://radee.local:3000/data'
    headers = {
        'Content-Type': 'application/json',
    }
    # time.sleep(1)
    t_init = time.time()
    spi = spidev.SpiDev()
    try:
        setup(spi)
        measurement(spi, t_init)
    # except KeyboardInterrupt:
    #     termination(spi)
    #     print('----- Terminated with Keyboard Interruption. -----')
    # except:
    #     termination(spi)
    #     print('----- Terminated with ERROR. -----')
    finally:
        print('----- Terminating...... -----')
        termination(spi)
        req2 = urllib.request.Request(url)
        try:
            with urllib.request.urlopen(req2) as res2:
                body = res2.read()
        except urllib.error.HTTPError as err2:
            print(err2.code)
        except urllib.error.URLError as err2:
            print(err2.reason)
        print('----- Terminated completely. -----')
        
