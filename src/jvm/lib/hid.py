# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

__all__ = ('HID',)


class HID:

    @property
    def processor_ids(self):
        from . import wmi
        client = wmi.WmiClient()
        query  = client.execute_query("SELECT ProcessorId "
                                      "FROM Win32_Processor")
        result = [wmi.WmiObject(item) for item in query]
        return [wobj.get_wmi_attribute("ProcessorId") for wobj in result]

    @property
    def bios_id(self):
        from . import wmi
        client = wmi.WmiClient()
        query  = client.execute_query("SELECT Manufacturer, SerialNumber "
                                      "FROM Win32_BIOS")
        result = [wmi.WmiObject(item) for item in query]
        return (result[0].get_wmi_attribute("Manufacturer") + ":" +
                result[0].get_wmi_attribute("SerialNumber"))

    @property
    def motherboard_id(self):
        from . import wmi
        client = wmi.WmiClient()
        query  = client.execute_query("SELECT SerialNumber "
                                      "FROM Win32_BaseBoard")
        result = [wmi.WmiObject(item) for item in query]
        return result[0].get_wmi_attribute("SerialNumber")

    @property
    def mac_addresses(self):
        from . import wmi
        client = wmi.WmiClient()
        query  = client.execute_query("SELECT IPEnabled, MACAddress "
                                      "FROM Win32_NetworkAdapterConfiguration")
        result = [wmi.WmiObject(item) for item in query]
        return [wobj.get_wmi_attribute("MACAddress") for wobj in result
                if wobj.get_wmi_attribute("IPEnabled")]

    @property
    def devices_serial_numbers(self):
        from . import wmi
        client = wmi.WmiClient()
        query  = client.execute_query("SELECT SerialNumber "
                                      "FROM Win32_PhysicalMedia")
        result = [wmi.WmiObject(item) for item in query]
        return [str(wobj.get_wmi_attribute("SerialNumber")) for wobj in result]
