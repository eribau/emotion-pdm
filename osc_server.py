# Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscmethod as osm

IP = "127.0.0.1"
PORT = "6503"

def pitch(p):
    # Will receive message data unpacked in s, x, y
    print("Pitch = ", p)
    pass

def intensity(i):
    print("Intensity = ", i)
    pass

# Start the system.
osc_startup()

# Make server channels to receive packets.
osc_udp_server(IP, PORT, "server")
# osc_udp_server("0.0.0.0", 3724, "anotherserver")

# Associate Python functions with message address patterns, using default
# argument scheme OSCARG_DATAUNPACK.
osc_method("/test/F0", pitch)
osc_method("/test/int", intensity)
# Too, but request the message address pattern before in argscheme

# Periodically call osc4py3 processing method in your event loop.
finished = False
while not finished:
    # …
    try:
        osc_process()
    except KeyboardInterrupt():
        osc_terminate()
        pass
    # …

# Properly close the system.
osc_terminate()
