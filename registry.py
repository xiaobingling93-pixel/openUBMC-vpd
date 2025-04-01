# Copyright (c) 2024 Huawei Technologies Co., Ltd.
# openUBMC is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
import os
import json
import stat
from collections import OrderedDict


class EvtInformation():
    def __init__(self):
        self.event_id = ''
        self.name = ''
        self.msg = ''
        self.severity = ''
        self.resolution = ''
        self.event_code = ''
        self.event_type = 0
        self.effect = ''
        self.cause = ''
        self.event_desc = ''


class Registry:
    def __init__(self, event_datas_dict, json_path):
        self.event_datas_dict = event_datas_dict
        self.json_path = json_path
    
    # 获取严重等级字符串
    @staticmethod
    def get_severity_string(evt_type, severity_level):
        severity_str = ['OK', 'Warning', 'Critical']
        severity_index = int(severity_level)
        evt_type_index = int(evt_type)
        # 事件类型 0:系统事件(包括SEL和事件) 1:维护事件 2:运行事件 3:装备事件
        # 系统事件(故障事件}和装备事件级别 0:ok-OK 1:minor-Warning 2:major-Warning 3:critical-Critical
        # 维护事件、运行事件级别 0:info-OK 1:warning-Warning 2:error-Critical
        if (evt_type_index == 0 or evt_type_index == 3) and severity_index > 1:
            severity_index = severity_index - 1
        return severity_str[int(severity_index)]
    
    # 获取参数信息
    @staticmethod
    def get_msg_args_info(msg_fmt_str):
        args_array = []

        if msg_fmt_str == "":
            return (0, args_array)
        
        for i in range(1, 100):
            cur_index_str = '%%%d' % (i)
            if msg_fmt_str.find(cur_index_str) == -1:
                return (i - 1, args_array)
            args_array.append('string')
        return (0, args_array)

    @staticmethod
    def generate_record_item(event):
        evt_registry_item = OrderedDict()
        msg = event.msg
        if msg != "":
            msg = msg.replace('@#AB;', ' ')
            msg = msg.strip()
        else:
            msg = None
        resolution = event.resolution
        if resolution != "":
            resolution = resolution.replace('@#AB;', ' ')
            resolution = resolution.strip()
        else:
            resolution = None
        effect = event.effect
        if effect != "":
            effect = effect.replace('@#AB;', ' ')
            effect = effect.strip()
        else:
            effect = None
        cause = event.cause
        if cause != "":
            cause = cause.replace('@#AB;', ' ')
            cause = cause.strip()
        else:
            cause = None
        evt_registry_item['Description'] = None
        evt_registry_item['Message'] = msg
        evt_registry_item['Severity'] = Registry.get_severity_string(event.event_type, event.severity)
        (evt_registry_item['NumberOfArgs'], evt_registry_item['ParamTypes']) = Registry.get_msg_args_info(msg)
        evt_registry_item['Resolution'] = resolution

        evt_oem_item = OrderedDict()
        evt_huawei_item = OrderedDict()

        evt_huawei_item['@odata.type'] = '#HwBMCEvent.v1_0_0.HwBMCEvent'
        evt_huawei_item['EventId'] = event.event_code
        evt_huawei_item['EventName'] = event.name
        evt_huawei_item['EventEffect'] = effect
        evt_huawei_item['EventCause'] = cause

        evt_oem_item['Huawei'] = evt_huawei_item
        evt_registry_item['Oem'] = evt_oem_item

        return evt_registry_item

    @staticmethod
    def get_redfish_event():
        event = OrderedDict()
        event_item = OrderedDict()
        event_list = {
            'ResourceUpdated': 'Resource updated.',
            'ResourceStatusChanged': 'Resource status changed.',
            'ResourceAdded': 'Resource added.',
            'ResourceRemoved': 'Resource removed.'
        }
        for key, value in event_list.items():
            event_item['Description'] = value
            event_item['Message'] = value
            event_item['Severity'] = 'OK'
            (event_item['NumberOfArgs'], event_item['ParamTypes']) = Registry.get_msg_args_info("")
            event_item['Resolution'] = None

            evt_oem_item = OrderedDict()
            evt_huawei_item = OrderedDict()

            evt_huawei_item['@odata.type'] = '#HwBMCEvent.v1_0_0.HwBMCEvent'
            evt_huawei_item['EventId'] = None
            evt_huawei_item['EventName'] = None
            evt_huawei_item['EventEffect'] = None
            evt_huawei_item['EventCause'] = None
            evt_oem_item['Huawei'] = evt_huawei_item
            event_item['Oem'] = evt_oem_item
            event[key] = event_item
        return event
    
    @staticmethod
    def get_event_registry_dict(event_dict):
        event_registry_dict = OrderedDict()
        redfish_event = Registry.get_redfish_event()
        event_registry_dict = redfish_event
        event = EvtInformation()
        event_definition = event_dict['EventDefinition']
        event_desc = event_dict['EventDescription']
        i = 0
        while i < len(event_definition):
            event.event_id = event_definition[i]['EventKeyId']
            event.name = event_definition[i]['EventName']
            event.severity = event_definition[i]['SeverityId']
            event.event_code = event_definition[i]['EventCode']
            event.event_type = event_definition[i]['EventType']

            for item in event_desc:
                if item['EventKeyId'] == event.event_id:
                    event.msg = item['Description']['En']
                    event.resolution = item['Suggestion']['En']
                    event.effect = item['Influence']['En']
                    event.cause = item['Cause']['En']
                    break

            record_item = Registry.generate_record_item(event)
            event_registry_dict[event.name] = record_item
            i += 1
        
        return event_registry_dict

    @staticmethod
    def get_dict(path):
        with open(path, 'r') as file:
            event_dict = json.safe_load(file)
        return event_dict

    def save_file(self, event_registry_dict):
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        modes = stat.S_IWUSR | stat.S_IRUSR
        with os.fdopen(os.open(self.json_path, flags, modes), 'w+') as handle:
            str_data = json.dumps(event_registry_dict)
            handle.write(str_data)
    
    def gen(self):
        event_registry_dict = Registry.get_event_registry_dict(self.event_datas_dict)
        self.save_file(event_registry_dict)