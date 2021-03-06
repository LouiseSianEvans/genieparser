#!/bin/env python
import unittest
from unittest.mock import Mock
from ats.topology import Device

from genie.metaparser.util.exceptions import SchemaEmptyParserError,\
                                       SchemaMissingKeyError
from genie.libs.parser.ios.show_platform import ShowVersion,\
                                       Dir,\
                                       ShowRedundancy,\
                                       ShowInventory,\
                                       ShowBootvar, \
                                       ShowProcessesCpuSorted



class test_show_version(unittest.TestCase):

    dev1 = Device(name='empty')
    dev_iosv = Device(name='iosv')
    empty_output = {'execute.return_value': ''}
    semi_empty_output = {'execute.return_value': '''\
        ROM: Bootstrap program is IOSv
    '''}

    golden_parsed_output_iosv = {
        "version": {
            "last_reload_reason": "Unknown reason",
            "hostname": "N95_1",
            "os": "IOSv",
            "version_short": "15.6",
            "number_of_intfs": {
               "Gigabit Ethernet": "6"
            },
            "version": "15.6(3)M2",
            "rtr_type": "IOSv",
            "chassis_sn": "9K66Z7TOKAACDEQA24N7S",
            "chassis": "IOSv",
            "image_id": "VIOS-ADVENTERPRISEK9-M",
            "processor_type": "revision 1.0",
            "platform": "IOSv",
            "image_type": "production image",
            "main_mem": "435457",
            "mem_size": {
               "non-volatile configuration": "256"
            },
            "system_image": "flash0:/vios-adventerprisek9-m",
            "curr_config_register": "0x0",
            "rom": "Bootstrap program is IOSv",
            "uptime": "1 day, 16 hours, 42 minutes"
        }
    }

    golden_output_iosv = {'execute.return_value': '''\
        Cisco IOS Software, IOSv Software (VIOS-ADVENTERPRISEK9-M), Version 15.6(3)M2, RELEASE SOFTWARE (fc2)
        Technical Support: http://www.cisco.com/techsupport
        Copyright (c) 1986-2017 by Cisco Systems, Inc.
        Compiled Wed 29-Mar-17 14:05 by prod_rel_team


        ROM: Bootstrap program is IOSv

        N95_1 uptime is 1 day, 16 hours, 42 minutes
        System returned to ROM by reload
        System image file is "flash0:/vios-adventerprisek9-m"
        Last reload reason: Unknown reason



        This product contains cryptographic features and is subject to United
        States and local country laws governing import, export, transfer and
        use. Delivery of Cisco cryptographic products does not imply
        third-party authority to import, export, distribute or use encryption.
        Importers, exporters, distributors and users are responsible for
        compliance with U.S. and local country laws. By using this product you
        agree to comply with applicable laws and regulations. If you are unable
        to comply with U.S. and local laws, return this product immediately.

        A summary of U.S. laws governing Cisco cryptographic products may be found at:
        http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

        If you require further assistance please contact us by sending email to
        export@cisco.com.

        Cisco IOSv (revision 1.0) with  with 435457K/87040K bytes of memory.
        Processor board ID 9K66Z7TOKAACDEQA24N7S
        6 Gigabit Ethernet interfaces
        DRAM configuration is 72 bits wide with parity disabled.
        256K bytes of non-volatile configuration memory.
        2097152K bytes of ATA System CompactFlash 0 (Read/Write)
        0K bytes of ATA CompactFlash 1 (Read/Write)
        0K bytes of ATA CompactFlash 2 (Read/Write)
        10080K bytes of ATA CompactFlash 3 (Read/Write)



        Configuration register is 0x0'''
    }

    golden_parsed_output_ios = {
        'version': {'bootldr': 'C3750E Boot Loader (C3750X-HBOOT-M) Version '
                            '15.2(3r)E, RELEASE SOFTWARE (fc1)',
                    'chassis': 'WS-C3750X-24P',
                    'chassis_sn': 'FDO2028F1WK',
                    'curr_config_register': '0xF',
                    'hostname': 'R5',
                    'image_id': 'C3750E-UNIVERSALK9-M',
                    'image_type': 'production image',
                    'last_reload_reason': 'power-on',
                    'license_level': 'ipservices',
                    'license_type': 'Permanent',
                    'main_mem': '262144',
                    'mem_size': {'flash-simulated non-volatile configuration': '512'},
                    'next_reload_license_level': 'ipservices',
                    'number_of_intfs': {'Gigabit Ethernet': '28',
                                        'Ten Gigabit Ethernet': '2',
                                        'Virtual Ethernet': '2'},
                    'os': 'C3750E boot loader',
                    'platform': 'C3750E',
                    'processor_type': 'PowerPC405',
                    'rom': 'Bootstrap program is C3750E boot loader',
                    'rtr_type': 'WS-C3750X-24P',
                    'system_image': 'flash:c3750e-universalk9-mz',
                    'system_restarted_at': '12:22:21 PDT Mon Sep 10 2018',
                    'uptime': '9 weeks, 4 days, 2 hours, 3 minutes',
                    'version': '12.2(55)SE8',
                    'version_short': '12.2'
        }
    }

    golden_output_ios = {'execute.return_value': '''\
        Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(55)SE8, RELEASE SOFTWARE (fc2)
        Technical Support: http://www.cisco.com/techsupport
        Copyright (c) 1986-2013 by Cisco Systems, Inc.
        Compiled Wed 26-Jun-13 09:56 by prod_rel_team
        Image text-base: 0x00003000, data-base: 0x02800000

        ROM: Bootstrap program is C3750E boot loader
        BOOTLDR: C3750E Boot Loader (C3750X-HBOOT-M) Version 15.2(3r)E, RELEASE SOFTWARE (fc1)

        R5 uptime is 9 weeks, 4 days, 2 hours, 3 minutes
        System returned to ROM by power-on
        System restarted at 12:22:21 PDT Mon Sep 10 2018
        System image file is "flash:c3750e-universalk9-mz"


        This product contains cryptographic features and is subject to United
        States and local country laws governing import, export, transfer and
        use. Delivery of Cisco cryptographic products does not imply
        third-party authority to import, export, distribute or use encryption.
        Importers, exporters, distributors and users are responsible for
        compliance with U.S. and local country laws. By using this product you
        agree to comply with applicable laws and regulations. If you are unable
        to comply with U.S. and local laws, return this product immediately.

        A summary of U.S. laws governing Cisco cryptographic products may be found at:
        http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

        If you require further assistance please contact us by sending email to
        export@cisco.com.

        License Level: ipservices
        License Type: Permanent
        Next reload license Level: ipservices

        cisco WS-C3750X-24P (PowerPC405) processor (revision W0) with 262144K bytes of memory.
        Processor board ID FDO2028F1WK
        Last reset from power-on
        2 Virtual Ethernet interfaces
        1 FastEthernet interface
        28 Gigabit Ethernet interfaces
        2 Ten Gigabit Ethernet interfaces
        The password-recovery mechanism is enabled.

        512K bytes of flash-simulated non-volatile configuration memory.
        Base ethernet MAC Address       : 84:3D:C6:38:B9:80
        Motherboard assembly number     : 73-15476-04
        Motherboard serial number       : FDO202907UH
        Model revision number           : W0
        Motherboard revision number     : B0
        Model number                    : WS-C3750X-24P-L
        Daughterboard assembly number   : 800-32727-03
        Daughterboard serial number     : FDO202823P8
        System serial number            : FDO2028F1WK
        Top Assembly Part Number        : 800-38990-01
        Top Assembly Revision Number    : F0
        Version ID                      : V07
        CLEI Code Number                : CMMPP00DRB
        Hardware Board Revision Number  : 0x05


        Switch Ports Model              SW Version            SW Image                 
        ------ ----- -----              ----------            ----------               
        *    1 30    WS-C3750X-24P      12.2(55)SE8           C3750E-UNIVERSALK9-M     


        Configuration register is 0xF

    '''
    }


    def test_empty(self):
        self.dev1 = Mock(**self.empty_output)
        version_obj = ShowVersion(device=self.dev1)
        with self.assertRaises(AttributeError):
            parsered_output = version_obj.parse()

    def test_semi_empty(self):
        self.dev1 = Mock(**self.semi_empty_output)
        version_obj = ShowVersion(device=self.dev1)
        with self.assertRaises(KeyError):
            parsed_output = version_obj.parse()

    def test_golden_iosv(self):
        self.maxDiff = None
        self.dev_iosv = Mock(**self.golden_output_iosv)
        version_obj = ShowVersion(device=self.dev_iosv)
        parsed_output = version_obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output_iosv)

    def test_golden_ios(self):
        self.maxDiff = None
        self.dev_iosv = Mock(**self.golden_output_ios)
        version_obj = ShowVersion(device=self.dev_iosv)
        parsed_output = version_obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output_ios)


class test_dir(unittest.TestCase):
    dev1 = Device(name='empty')
    dev_iosv = Device(name='iosv')
    empty_output = {'execute.return_value': ''}
    semi_empty_output = {'execute.return_value': '''\
        Directory of flash:/
    '''
    }

    golden_parsed_output_iosv = {
        "dir": {
            "flash0:/": {
               "files": {
                    "e1000_bia.txt": {
                         "last_modified_date": "Oct 17 2018 18:57:18 +00:00",
                         "index": "269",
                         "size": "119",
                         "permissions": "-rw-"
                    },
                    "config": {
                         "last_modified_date": "Oct 14 2013 00:00:00 +00:00",
                         "index": "264",
                         "size": "0",
                         "permissions": "drw-"
                    },
                    "nvram": {
                         "last_modified_date": "Oct 17 2018 18:57:10 +00:00",
                         "index": "268",
                         "size": "524288",
                         "permissions": "-rw-"
                    },
                    "boot": {
                         "last_modified_date": "Jan 30 2013 00:00:00 +00:00",
                         "index": "1",
                         "size": "0",
                         "permissions": "drw-"
                    },
                    "vios-adventerprisek9-m": {
                         "last_modified_date": "Mar 29 2017 00:00:00 +00:00",
                         "index": "267",
                         "size": "147988420",
                         "permissions": "-rw-"
                    }
               },
               "bytes_total": "2142715904",
               "bytes_free": "1989595136"
            },
            "dir": "flash0:/"
        }
    }

    golden_output_iosv = {'execute.return_value': '''\
        Directory of flash0:/

            1  drw-           0  Jan 30 2013 00:00:00 +00:00  boot
          264  drw-           0  Oct 14 2013 00:00:00 +00:00  config
          267  -rw-   147988420  Mar 29 2017 00:00:00 +00:00  vios-adventerprisek9-m
          268  -rw-      524288  Oct 17 2018 18:57:10 +00:00  nvram
          269  -rw-         119  Oct 17 2018 18:57:18 +00:00  e1000_bia.txt

        2142715904 bytes total (1989595136 bytes free)
    '''
    }

    def test_empty(self):
        self.dev1 = Mock(**self.empty_output)
        dir_obj = Dir(device=self.dev1)
        with self.assertRaises(SchemaEmptyParserError):
            parsered_output = dir_obj.parse()

    def test_semi_empty(self):
        self.dev1 = Mock(**self.semi_empty_output)
        dir_obj = Dir(device=self.dev1)
        with self.assertRaises(SchemaMissingKeyError):
            parsed_output = dir_obj.parse()

    def test_golden_iosv(self):
        self.maxDiff = None
        self.dev_iosv = Mock(**self.golden_output_iosv)
        dir_obj = Dir(device=self.dev_iosv)
        parsed_output = dir_obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output_iosv)


class test_show_redundancy(unittest.TestCase):
    dev1 = Device(name='empty')
    dev_iosv = Device(name='iosv')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output_iosv = {
        "red_sys_info": {
        "last_switchover_reason": "unsupported",
        "maint_mode": "Disabled",
        "switchovers_system_experienced": "0",
        "available_system_uptime": "0 minutes",
        "communications": "Down",
        "hw_mode": "Simplex",
        "communications_reason": "Failure",
        "standby_failures": "0"
        },
        "slot": {
            "slot 0": {
               "image_ver": "Cisco IOS Software, IOSv Software (VIOS-ADVENTERPRISEK9-M), Version 15.6(3)M2, RELEASE SOFTWARE (fc2)",
               "uptime_in_curr_state": "1 day, 16 hours, 42 minutes",
               "config_register": "0x0",
               "curr_sw_state": "ACTIVE"
            }
        }
    }

    golden_output_iosv = {'execute.return_value': '''\
        Redundant System Information :
        ------------------------------
               Available system uptime = 0 minutes
        Switchovers system experienced = 0
                      Standby failures = 0
                Last switchover reason = unsupported

                         Hardware Mode = Simplex
                      Maintenance Mode = Disabled
                        Communications = Down      Reason: Failure

        Current Processor Information :
        -------------------------------
                       Active Location = slot 0
                Current Software state = ACTIVE
               Uptime in current state = 1 day, 16 hours, 42 minutes
                         Image Version = Cisco IOS Software, IOSv Software (VIOS-ADVENTERPRISEK9-M), Version 15.6(3)M2, RELEASE SOFTWARE (fc2)
        Technical Support: http://www.cisco.com/techsupport
        Copyright (c) 1986-2017 by Cisco Systems, Inc.
        Compiled Wed 29-Mar-17 14:05 by prod_rel_team
                Configuration register = 0x0

        Peer (slot: 0) information is not available because it is in 'DISABLED' state
    '''
    }

    def test_empty(self):
        self.dev1 = Mock(**self.empty_output)
        redundancy_obj = ShowRedundancy(device=self.dev1)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = redundancy_obj.parse()

    def test_golden_iosv(self):
        self.maxDiff = None
        self.dev_iosv = Mock(**self.golden_output_iosv)
        redundancy_obj = ShowRedundancy(device=self.dev_iosv)
        parsed_output = redundancy_obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output_iosv)


class test_show_inventory(unittest.TestCase):
    dev1 = Device(name='empty')
    dev_iosv = Device(name='iosv')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output_iosv = {
        "slot": {
            "1": {
               "rp": {
                    "IOSv": {
                         "descr": "IOSv chassis, Hw Serial#: 9K66Z7TOKAACDEQA24N7S, Hw Revision: 1.0",
                         "name": "IOSv",
                         "pid": "IOSv",
                         "sn": "9K66Z7TOKAACDEQA24N7S",
                         "vid": "1.0"
                    }
               }
            }
        }

    }

    golden_output_iosv = {'execute.return_value': '''\
        NAME: "IOSv", DESCR: "IOSv chassis, Hw Serial#: 9K66Z7TOKAACDEQA24N7S, Hw Revision: 1.0"
        PID: IOSv              , VID: 1.0, SN: 9K66Z7TOKAACDEQA24N7S
    '''
    }

    def test_empty(self):
        self.dev1 = Mock(**self.empty_output)
        inventory_obj = ShowInventory(device=self.dev1)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = inventory_obj.parse()

    def test_golden_iosv(self):
        self.maxDiff = None
        self.dev_iosv = Mock(**self.golden_output_iosv)
        inventory_obj = ShowInventory(device=self.dev_iosv)
        parsed_output = inventory_obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output_iosv)


class test_show_bootvar(unittest.TestCase):
    dev = Device(name='ios')
    dev_iosv = Device(name='iosv')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output_iosv = {
        "active": {
          "boot_variable": "disk0:s72033-adventerprisek9-mz.122-33.SRE0a-ssr-nxos-76k-1,12",
          "configuration_register": "0x2012"
        },
        "next_reload_boot_variable": "disk0:s72033-adventerprisek9-mz.122-33.SRE0a-ssr-nxos-76k-1,12"
    }

    golden_output_iosv = {'execute.return_value': '''\
        BOOT variable = disk0:s72033-adventerprisek9-mz.122-33.SRE0a-ssr-nxos-76k-1,12;
        CONFIG_FILE variable = 
        BOOTLDR variable = 
        Configuration register is 0x2012

        Standby not ready to show bootvar

    '''
    }

    def test_empty(self):
        self.dev = Mock(**self.empty_output)
        platform_obj = ShowBootvar(device=self.dev)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = platform_obj.parse()    

    def test_golden(self):
        self.maxDiff = None
        self.dev_iosv = Mock(**self.golden_output_iosv)
        platform_obj = ShowBootvar(device=self.dev_iosv)
        parsed_output = platform_obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output_iosv)


class test_show_processes_cpu_sorted_CPU(unittest.TestCase):

    dev = Device(name='c3850')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        "five_sec_cpu_total": 13,
         "five_min_cpu": 15,
         "one_min_cpu": 23,
         "five_sec_cpu_interrupts": 0
    }

    golden_output = {'execute.return_value': '''\
        show processes cpu sorted 5min | inc CPU
        CPU utilization for five seconds: 13%/0%; one minute: 23%; five minutes: 15%
    '''
    }

    golden_parsed_output_1 = {
        "sort": {
            1: {
               "invoked": 3321960,
               "usecs": 109,
               "tty": 0,
               "one_min_cpu": 0.54,
               "process": "PIM Process",
               "five_min_cpu": 0.48,
               "runtime": 362874,
               "pid": 368,
               "five_sec_cpu": 1.03
            },
            2: {
               "invoked": 1466728,
               "usecs": 2442,
               "tty": 0,
               "one_min_cpu": 0.87,
               "process": "IOSv e1000",
               "five_min_cpu": 2.77,
               "runtime": 3582279,
               "pid": 84,
               "five_sec_cpu": 0.55
            },
            3: {
               "invoked": 116196,
               "usecs": 976,
               "tty": 0,
               "one_min_cpu": 0.07,
               "process": "OSPF-1 Hello",
               "five_min_cpu": 0.07,
               "runtime": 113457,
               "pid": 412,
               "five_sec_cpu": 0.15
            }
        },
        "five_sec_cpu_total": 4,
        "five_min_cpu": 9,
        "one_min_cpu": 4,
        "nonzero_cpu_processes": [
        "PIM Process",
        "IOSv e1000",
        "OSPF-1 Hello"
        ],
        "five_sec_cpu_interrupts": 0
    }

    golden_output_1 = {'execute.return_value': '''
        CPU utilization for five seconds: 4%/0%; one minute: 4%; five minutes: 9%
         PID Runtime(ms)     Invoked      uSecs   5Sec   1Min   5Min TTY Process 
         368      362874     3321960        109  1.03%  0.54%  0.48%   0 PIM Process      
          84     3582279     1466728       2442  0.55%  0.87%  2.77%   0 IOSv e1000   
          412      113457      116196        976  0.15%  0.07%  0.07%   0 OSPF-1 Hello
    '''}

    def test_empty(self):
        self.dev = Mock(**self.empty_output)
        obj = ShowProcessesCpuSorted(device=self.dev)
        with self.assertRaises(SchemaEmptyParserError):
            parsered_output = obj.parse()

    def test_golden(self):
        self.maxDiff = None
        self.dev = Mock(**self.golden_output)
        obj = ShowProcessesCpuSorted(device=self.dev)
        parsed_output = obj.parse(key_word='CPU', sort_time='5min')
        self.assertEqual(parsed_output, self.golden_parsed_output)

    def test_golden_1(self):
        self.maxDiff = None
        self.dev = Mock(**self.golden_output_1)
        obj = ShowProcessesCpuSorted(device=self.dev)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output_1)


if __name__ == '__main__':
    unittest.main()

