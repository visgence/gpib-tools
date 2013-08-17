#!/env/pyhton
#GPIB Tets program for HP3455A and 6624A
#Evan Salazar (Visgence Inc)

from PySide import QtCore,QtNetwork
import time
import sys
import numpy as np
import pylab as pl

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
    
    s = QtNetwork.QTcpSocket()

    s.connectToHost('192.168.11.38',1234)
    s.waitForConnected()

    s.write("++addr 22\n")
    s.write("++auto 0\n")
    s.write("++addr\n")
    s.waitForReadyRead()
    
    print str(s.readLine()).rstrip()

    x = np.arange(0,10.1,.1)
    y = []

    for i in x:
        s.write("++addr 5\n")
        s.write("vset 1,%f\n" % (i))
        s.write("++addr 22\n")
        #time.sleep(.1)

        s.write("++trg\n")
        s.write("++read\n")
        s.waitForReadyRead()
        num = convNum(s.readLine())
        print num
        y.append(num)
        #time.sleep(.1)
    
    s.disconnectFromHost()



    pl.plot(x,y,color='r')
    pl.plot(x,x)
    pl.show()
