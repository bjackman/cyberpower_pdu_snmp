import argparse

from pysnmp.hlapi import (setCmd, SnmpEngine, CommunityData, UdpTransportTarget,
                          ContextData, ObjectType, ObjectIdentity, Integer32)

class CyberPowerPduException(Exception):
    pass

class CyberPowerPdu(object):
    """
    Class to query & control a CyberPower PDU via SNMP.

    Tested on the PDU15SWHVIEC8FNET. I don't understand SNMP well enough to have
    any idea if this would be expected to work on other models.

    This class is basically just a piece of copy-pasted pysnmp code and a
    depository for comments.

    :param host: IP address or hostname of the PDU on the network
    :type host: str
    """

    # Some comments in this class will tell you to run snmptranslate commands
    # and such - for them to work you'll need to install the CPS-MIB. You can do
    # that like this (Ubuntu):
    # sudo apt-get install snmp snmp-mibs-downloader
    # sudo sed -i "s/^mibs/#mibs/" /etc/snmp/snmp.conf
    # wget -O mib.zip https://www.cyberpower.com/uk/en/File/GetFileSampleByDocId?docId=FW-0000008-02
    # mkdir -p ~/.snmp/mibs
    # unzip -d ~/.snmp/mibs mib.zip
    # echo mibs CPS-MIB | sudo tee --append /etc/snmp/snmp.conf

    # See snmptranslate -Td CPS-MIB::ePDUOutletControlOutletCommand
    outlet_state_oids = {
        'immediateOn': 1, 'immediateOff': 2, 'immediateReboot': 3, 'delayedOn': 4,
        'delayedOff': 5, 'delayedReboot': 6, 'cancelPendingCommand': 7, 'outletIdentify': 8
    }

    def __init__(self, host):
        self.host = host

    def set_outlet_on(self, outlet, on):
        """
        Set an outlet on or off

        :param outlet: Which outlet to set the power for (for my model this is
                       in the range 1 through 8)
        :param on: True means turn it on, False means turn it off
        """
        # OK, sorry for this insane code - the pysnmp docs explicitly say you
        # should just copy paste their examples.
        # This is based on the code from here:
        # http://snmplabs.com/pysnmp/examples/hlapi/asyncore/sync/manager/cmdgen/modifying-variables.html

        # The command we would run to power on outlet 1 on the PDU, if we were
        # not masochists is this:
        #
        # snmpset -v 1 -c private $IPADDR CPS-MIB::ePDUOutletControlOutletCommand.1 i immediateOn
        #
        # However to get those human-readable names to work we'd need to
        # download MIBs and tell pysnmp about them. pysnmp + pysmi apparently
        # know how to do this but I tried to point it at the CyberPower MIB file
        # and it failed silently so huffed and gave up.
        #
        # So instead, we're going to do something more akin to this command,
        # which is exactly the same thing but without the human-readable names:
        #
        # snmpset -v 1 -c private $IPADDR .1.3.6.1.4.1.3808.1.1.3.3.3.1.1.4.2 i 1
        #
        # In that command ".1.3.6.1.4.1.3808.1.1.3.3.3.1.1.4.2" is the
        # masochistic name for "CPS-MIB::ePDUOutletControlOutletCommand.1" and
        # "1" is the masochistic name for "immediateOn"
        #
        # I figured out what that command would be by running this:
        # snmptranslate -On CPS-MIB::ePDUOutletControlOutletCommand
        #
        # SnmpEngine and ContextData are just pointless boilerplate required by
        # pysnmp.  Hopefully you can sort of see how the other bits map to the
        # code below (the "i" becaomse "Integer32").

        oid = ObjectIdentity('1.3.6.1.4.1.3808.1.1.3.3.3.1.1.4.{}'.format(outlet))
        target_state = 'immediateOn' if on else 'immediateOff'
        errorIndication, errorStatus, errorIndex, varBinds = next(
            setCmd(SnmpEngine(),
                   CommunityData('private'),
                   UdpTransportTarget(('192.168.106.68', 161)),
                   ContextData(),
                   ObjectType(oid, Integer32(self.outlet_state_oids[target_state]))))

        if errorIndication:
            raise CyberPowerPduException(errorIndication)
        elif errorStatus:
            raise CyberPowerPduException(
                '%s at %s' % (errorStatus.prettyPrint(),
                              errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='Hostname/IP address of PDU')
    parser.add_argument('outlet', help='Outlet to interact with')
    parser.add_argument('on', choices=('on', 'off'))

    args = parser.parse_args()

    CyberPowerPdu(args.host).set_outlet_on(args.outlet, args.on == 'on')
