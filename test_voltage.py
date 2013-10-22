#!/env/pyhton
#GPIB Tets program for HP3455A and 6624A
#Evan Salazar (Visgence Inc)

from PySide import QtCore,QtNetwork
import time
import sys
import numpy as np
import pylab as pl
import serial
def convNum(line):

    numStr = ""
    for c in line:
        if c.encode('hex') != '00':
            numStr += c

    numStr = numStr.rstrip()
    numStr = numStr.strip(" ")
    numstr = numStr.replace('\0','')
    return float(numStr)



if __name__ == "__main__":
    
    serial = serial.Serial(port='COM20',baudrate=9600)

    s = QtNetwork.QTcpSocket()

    s.connectToHost('192.168.11.84',1234)
    s.waitForConnected()

    s.write("++addr 1\n")
    s.write("++auto 0\n")
    s.write("++addr\n")
    s.waitForReadyRead()
    
    print str(s.readLine()).rstrip()

    x = np.arange(1.93,2.13,.01)
    y = []
    sensor = []

    for i in x:
        s.write("++addr 5\n")
        s.write("vset 1,%f\n" % (i))
        s.write("++addr 1\n")
        #time.sleep(.1)

        s.write("++trg\n")
        s.write("++read\n")
        s.waitForReadyRead()
        num = convNum(s.readLine())
        serial.flushInput()
        serial.read()
        serial.readline()
        num2 = convNum(serial.readline()) /1000.00
        print str(num) + " " + str(num2)
        y.append(num)
        sensor.append(num2)
        #time.sleep(.1)
    
    s.disconnectFromHost()

    y = np.array(x)
    sensor = np.array(sensor)

    pl.plot(y,y,color='r')
    pl.plot(y,sensor)
    #pl.plot(x,y-sensor)
    pl.show()
