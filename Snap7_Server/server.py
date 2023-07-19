import snap7
import time

server = snap7.server.Server()
size = 10
tcpport = 5002

globaldata = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte]*size)()
outputs = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte]*size)()
inputs = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte]*size)()

server.register_area(snap7.snap7types.srvAreaPA, 0, outputs)
server.register_area(snap7.snap7types.srvAreaMK, 0, globaldata)
server.register_area(snap7.snap7types.srvAreaPE, 0, inputs)

server.start(tcpport=tcpport)
snap7.util.set_real(outputs, 0, 1.234)      # srvAreaPA
snap7.util.set_real(globaldata, 0, 2.234)   # srvAreaMK
snap7.util.set_real(inputs, 0, 3.234)       # srvAreaPE

while True:
    while True:
        event = server.pick_event()
        if event:
            print(server.event_text(event))
        else:
            break
        time.sleep(.01)
server.stop()
server.destroy()