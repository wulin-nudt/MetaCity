#coding=utf-8

import pty
import os
import select

from mininet.util import (errRun, errFail, Python3, getincrementaldecoder,
                          quietRun, BaseString,encode)

def mkpty():
    #Open a new tty
    master1, slave = pty.openpty()
    slaveName1 = os.ttyname(slave)
    master2, slave = pty.openpty()
    slaveName2 = os.ttyname(slave)


    print ('\nslave device names:', slaveName1, slaveName2)
    return master1, master2

if __name__ == "__main__":

    master1, master2 = mkpty()
    while True:
        #       rl=read list, wait until ready to reading
        #       wl=write list, wait until ready to writing
        #       el=exception list, wait for an "exceptional condition"
        #       timeout = 1s

        rl, wl, el = select.select([master1, master2], [], [], None)
        for device in rl:
            data = os.read(device, 128)
            # data=getincrementaldecoder().decode(data)
            if device == master1:
                print("read from master1: %s,%s" % (len(data), data))
                # os.write(master2, encode(data))
            else:
                pass
                # os.write(master1, encode(data))


