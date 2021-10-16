# Copyright (c) 2004-2021 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

__all__ = ('WmiObject', 'WmiClient')


class WmiObject:

    def __init__(self, com_object):
        super().__init__()
        self._properties = None
        self._values     = {}
        self._com_object = com_object

    @property
    def properties(self):
        if self._properties is None:
            self._properties = self._com_object.Properties_
        return self._properties

    def get_wmi_attribute(self, attr):
        if attr not in self._values:
            self._values[attr] = self.properties.Item(attr).Value
        return self._values[attr]

    def get_path(self):
        return self._com_object.Path_.Path


class WmiClient:

    def __init__(self, namespace=r"root\cimv2"):
        super().__init__()
        from comtypes import CoInitializeEx
        # CoInitialize is per-thread, but comtypes only calls it once on module load.
        # We don't know if it was called for the current thread so we call it again
        # to make sure:
        CoInitializeEx()
        self._namespace  = namespace
        self._com_client = self._get_client(namespace)

    @staticmethod
    def _get_client(namespace):
        import comtypes.client
        comtypes.client.gen_dir               = None
        comtypes.client._generate.__verbose__ = False
        from comtypes        import CoGetObject
        from comtypes.client import GetModule
        wmi_module = GetModule(["{565783C6-CB41-11D1-8B02-00600806D9B6}", 1, 2])
        client = CoGetObject(r"winmgmts:{}".format(namespace),
                             interface=wmi_module.ISWbemServicesEx)
        return client

    def execute_query(self, query):
        from _ctypes import COMError
        from sys     import version_info
        results = self._com_client.ExecQuery(query)
        count = 0
        try:
            count = results.Count
        except COMError:
            pass
        for idx in (range(count) if version_info[0] >= 3 else xrange(count)):
            yield results.ItemIndex(idx)

    def execute_event_query(self, query):
        from _ctypes import COMError
        from sys     import version_info
        results = self._com_client.ExecNotificationQuery(query)
        count = 0
        try:
            count = results.Count
        except COMError:
            pass
        for idx in (range(count) if version_info[0] >= 3 else xrange(count)):
            yield results.ItemIndex(idx)
