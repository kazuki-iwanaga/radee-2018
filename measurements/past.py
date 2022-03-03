# /usr/bin/python2
# -*- coding: utf-8 -*-
# Peak Hold型(RPI-Shaper_v03_02), wait_for_edge方式の処理
# GPIO18 ;　入力　割り込み信号を受信
# GPIO17 ;　出力　電荷リセット
# GPIO27 ;  出力　読出処理中フラグ（タイミング調整用）

from __future__ import print_function
import spidev
import RPi.GPIO as GPIO
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import math

# Initailization
h_title = " PH_v02;"+raw_input("Run condition? ")

#SPI通信？
spi = spidev.SpiDev()
#SPI通信先のポート０を指定
#LINUXデバイスファイル？
spi.open(0, 0)

hist_data=[]
n_event=0
n_print=0

#BOARD（ハード的にみてピン番号を直接指定） BCM（ソフト的にピン番号を指定） この２種類
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)

#読み取り(in) )ピン内部に操作可能な内部抵抗がある（pull_up回路、pull_down回路)
GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#多分GNDに接続してる。電位の初期状態
GPIO.output(17,GPIO.LOW)
GPIO.output(27,GPIO.LOW)

#最初の時間取得
time_stamp=time.time()

# Event Loop
while (n_event<500):

#18番の電位が上がるまで待つ
    GPIO.wait_for_edge(18,GPIO.RISING)

#検出器が検出した回数に+1
    n_event = n_event +1
    n_print=n_print +1

#読み出しを待つ
    time.sleep(0.0008)
    GPIO.output(27,GPIO.HIGH)
#0xで続く数字を16進数表す。「データをください」（阻止によって決まっている合言葉）
    resp = spi.xfer2([0x68, 0x00])
#素子からの返り値を配列として入力
#<<8は桁を８bitずらす。そこにresp[1]を足して16bitの値を取得
    value = ((resp[0] << 8) + resp[1]) & 0x3ff
#配列としてデータを追加
    hist_data.append(value)
    
#27の電位をlowにして処理の準備完了
    GPIO.output(27,GPIO.LOW)
    time.sleep(0.0005)
#センサーの初期化
    GPIO.output(17,GPIO.HIGH)
    time.sleep(0.0005)
#センサー受け取りスタート
    GPIO.output(17,GPIO.LOW)

#イベント時刻の記録
    el_time=(time.time()-time_stamp)*1000
#100イベントごとに表示。whileは500回のイベント測る
    if n_print >= 100:
        n_print=0
        print(" n_event=",n_event,end="")
#10は桁数、1は小数点以下の桁数、fはfloatのf
#頭合わせに使える
        print("  Processed at [ms]; {0:10.1f}".format(el_time),end="")
        print("  ADC ={:5.0f}".format(value))
        
# Termination処理
spi.close()
GPIO.cleanup()
mean=np.mean(hist_data)

#統計処理としての分散の計算
variance=np.var(hist_data)

print(" n_event=",n_event)
print(" Mean =",mean)
print(" Sigma=",math.sqrt(variance))
plt.hist(hist_data,bins=100)
plt.xlim(0,1000)
plt.title(h_title)
plt.xlabel('ADC ')
plt.ylabel('Histogram')
plt.savefig('Radon_v05.pdf')
