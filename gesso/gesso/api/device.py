import yaml

from ..util import util

from port import Port

class Device(object):

    def __init__(self, path=None):
        """ The ``Device`` class represents a device.

        Args:
            path (str): path to a model yaml file.
        """
        self.name = None
        self.ports = []

        if path != None:
            model = util.load_yaml_file(path)
            
            # Load name from device model file
            if 'name' in model:
                self.name = model['name']

            # Load ports from device model file
            for port_model in model['ports']:
                port = Port(port_model['number'])

                # Parse port state space:
                # 1. search for 'mode', 'direction', 'voltage' (a) values or (b) lists of values
                # 2. search for 'states' list

                if 'mode' in port_model and 'direction' in port_model and 'voltage' in port_model:
                    state = {}
                    state['mode'] = [port_model['mode']]
                    state['direction'] = [port_model['direction']]
                    state['voltage'] = [port_model['voltage']]
                    port.states.append(state)

                elif 'states' in port_model:
                    for state in port_model['states']:
                        port.states.append(state)
                        #print state['mode']
                        #print state['direction']
                        #print state['voltage']

                self.ports.append(port)

                # Registry URI example:
                # gesso.network/mokogobo/gesso-8.0.0


    # def get_state(self):

    def get_ports(self):
        # TODO: return list of ports
        # TODO: device.ports
        return self.ports

"""
device = Device()
supported_voltages = device.get_ports()[0].get_model().get_voltages()

is_supported_config = device.get_ports()[0].get_model().get_voltages()

----

device.ports.get(number=3)      # Low-level API (for on-device, calls into platform API)
device.ports.get('adc')         # High-level API (for controllers)

----

devices                                # list of available devices
device.ports()                         # list of ports attached to the device
device.ports(3, 4)                     # list of ports attached to the device
device.ports(3, 4).voltage
device.ports(3, 4).get('mode', 'voltage')
device.ports(3, 4).set('mode': 'digital', 'voltage': '5v')

----

device.ports.get('adc').set(adc=844)
    device.ports.get('adc').sample(adc=844)
    single_sample_value = device.ports.get('adc').sample()
        device.ports.get('adc').value(adc=844)
        single_sample_value = device.ports.get('adc').value()
device.ports.get('adc').publish(adc=844)
device.ports.get('adc').publish(voltage=2.4)
device.ports.get('adc').publish(voltage=2.4)
adc_value_stream = device.ports.get('adc').subscribe()

// path_config = assemble(device_001, device_002)

device.ports.get(3).voltage
device.ports.get(3).validate(mode='digital', direction='input', voltage='5v')
device.ports.get(3).configure(mode='digital', direction='input', voltage='5v')

device.ports.get([3,5,8]).validate(mode='digital', voltage='5v')
device.ports.get([3,5,8]).value(mode='digital', voltage='5v')
device.ports.set([3,5,8]).value(mode='digital', voltage='5v')

device.ports(3).voltage
device.ports(3).validate(mode='digital', direction='input', voltage='5v')
device.ports(3).configure(mode='digital', direction='input', voltage='5v')
device.ports([3,4,8]).voltage

device.ports[3].voltage
device.ports[3].validate(mode='digital', direction='input', voltage='5v')
device.ports[3].configure(mode='digital', direction='input', voltage='5v')

??? device.interfaces
system.interfaces                       # .interfaces only for system, not device? device analog is port?
system.interfaces.get('right-motor')    # interface name is specified in path name and yaml interface cfg
system.interfaces.get('robot').controller

Note:
Using the following has a parallel UI in the mobile app (i.e., diff levels of abstraction in zoom levels)
    `device.ports.*`
    `system.interfaces.*`

interfaces = device.get_interfaces()
interfaces['interface-name'].ports
"""
