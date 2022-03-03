import sys
import time
import csv
# import spidev
# import RPi.GPIO as GPIO
import random
import json
import urllib.request
# import os
import datetime

# def setup(spi):
#     spi.open(0, 0)
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(17,GPIO.OUT)
#     GPIO.setup(27,GPIO.OUT)
#     GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
#     GPIO.output(17,GPIO.LOW)
#     GPIO.output(27,GPIO.LOW)

def demo(t_init, n_times):
    # print(os.environ['CSV_FILENAME'])
    # filename = os.environ['CSV_FILENAME']
    filename = sys.argv[1]
    with open('/home/pi/radee-2018/public/csv/' + filename + '.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        delta_t = 0
        # for i in range(n_times):
        while delta_t < int(sys.argv[2]):
            time.sleep(0.1)
            volt = round(random.gauss(20, 50) + random.gauss(350, 10))
            delta_t = round((time.time() - t_init), 2)
            dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # delta_t = time.time()
            writer.writerow([dt, volt])
            # print(d)
            # print([volt, dt, delta_t])
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
            time.sleep(0.1)


# def measurement(spi, t_init, n_times, ws):
#     filename = sys.argv[1]
#     with open('../public/data/' + filename + '.csv', 'a') as f:
#         writer = csv.writer(f, lineterminator='\n')
#         for i in range(n_times):
#             # GPIO.wait_for_edge(18,GPIO.RISING)
#             time.sleep(0.1)
#             # GPIO.output(27,GPIO.HIGH)
#             # SPI通信：値の読み出し
#             # tmp = spi.xfer2([0x68, 0x00])
#             # volt = ((tmp[0] << 8) + tmp[1]) & 0x3ff
#             volt = round(random.gauss(400, 10))
#             delta_t = round((time.time() - t_init), 2)
#             # CSV書き出し
#             writer.writerow([volt, delta_t])
#             # デバッグ用
#             print([volt, delta_t])
#             # GPIO.output(27,GPIO.LOW)
#             time.sleep(0.1)
#             # GPIO.output(17,GPIO.HIGH)
#             # time.sleep(0.0005)
#             # GPIO.output(17,GPIO.LOW)

# def termination(spi):
#     spi.close()
#     GPIO.cleanup()

if __name__ == '__main__':
    print("----- Let's Start Our Measurement! -----")
    url = 'http://radee.local:3000/data'
    headers = {
        'Content-Type': 'application/json',
    }
    time.sleep(1)
    t_init = time.time()
    # spi = 0
    try:
        # setup(spi)
        # measurement(spi, t_init, 100, ws)
        demo(t_init, 100)
    except KeyboardInterrupt:
        # termination(spi)
        print('----- Terminated with Keyboard Interruption. -----')
    # except:
    #     # termination(spi)
    #     print('----- Terminated with ERROR. -----')
    finally:
        # termination(spi)
        print('----- Terminated completely. -----')
        req2 = urllib.request.Request(url)
        try:
            with urllib.request.urlopen(req2) as res2:
                body = res2.read()
        except urllib.error.HTTPError as err2:
            print(err2.code)
        except urllib.error.URLError as err2:
            print(err2.reason)
