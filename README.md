This is a "library" to interace with CyberPower networked PDUs in pure Python
without having to install anything external (system libraries, MIBs). To be
honest it's really just a wrapper around a single pysnmp call, the rest is just
comments.

Tested against the PDU15SWHVIEC8FNET. I don't understand SNMP well enough to
know if this would be expected to work on other models. But hey, maybe.

Should support both Python 2 and 3.

# Usage

Press the "select" button on your PDU for 3 seconds, it will show its IP address
on the 7-segment displays.

Then `CyberPowerPdu(ip_addr).set_outlet_on(1, True)` will turn outlet 1 on.
