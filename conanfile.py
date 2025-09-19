# Copyright (c) 2024 Huawei Technologies Co., Ltd.
# openUBMC is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import json
import stat
import importlib
import sys

from conanbase import ConanBase, copy, os


required_conan_version = ">=1.60.0"


class AppConan(ConanBase):

    def build(self):
        pass

    def cp_kvm_padding_image(self):
        copy(
            self, "*.jpeg", 
            src=os.path.join(self.source_folder, "vendor/Huawei/BMCSoC/hi1711/kvm_padding_image"), 
            dst=os.path.join(self.package_folder, "opt/bmc/soc/kvm")
        )

    def cp_vce_dft_data(self):
        copy(
            self, "*.dat", 
            src=os.path.join(self.source_folder, "vendor/Huawei/BMCSoC/hi1711/vce_dft_data"), 
            dst=os.path.join(self.package_folder, "opt/bmc/apps/remote_console/dft_data")
        )

    def cp_frame_logrotate_conf(self):
        copy(
            self, "frame", 
            src=os.path.join(self.source_folder, "vendor/Huawei/BMCSoC/hi1711/logrotate_config"), 
            dst=os.path.join(self.package_folder, "etc/logrotate.d")
        )

    def cp_nginx_logrotate_conf(self):
        copy(
            self, "nginx", 
            src=os.path.join(self.source_folder, "vendor/Huawei/BMCSoC/hi1711/logrotate_config"), 
            dst=os.path.join(self.package_folder, "etc/logrotate.d")
        )

    def get_board_path(self):
        server_dirs = os.listdir("./vendor/Huawei/Server")
        for server in server_dirs:
            board_dir_temp = os.path.join("./vendor/Huawei/Server", server, str(self.options.board_name))
            if os.path.isdir(board_dir_temp):
                return board_dir_temp
        return ""

    # 拷贝产品定制化schema文件，实现产品差异化装备定制
    def cp_product_schema(self):
        board_dir = self.get_board_path()
        # 产品差异化schema文件定义在vendor/Huawei/Server/xxx/{product}/schema路径下
        schema_path = os.path.join(self.source_folder, board_dir, "schema")
        if os.path.exists(schema_path):
            copy(
                self, "*.json", 
                src=schema_path, 
                dst=os.path.join(self.package_folder, "opt/bmc/profile_schema/product")
            )

    def cp_include_vendor(self):
        if str(self.options.board_name) == "common":
            copy(
                self, "*", 
                src=os.path.join(self.source_folder, "./vendor"), 
                dst=os.path.join(self.package_folder, "include/vendor")
            )

    def get_event_json(self):
        event_json = {}
        mapping_bmc = {
            "common": "iBMC",
            "openUBMC": "openUBMC",
            "S920H20": "iBMC",
            "S920X20": "iBMC"
        }
        event_json_path = "vendor/event_def.json"
        if os.path.isfile(event_json_path):
            with open(event_json_path, "r") as f:
                event_content = f.read()
            event_oem_content = event_content.replace("{BMC}", mapping_bmc.get(str(self.options.board_name), "BMC"))
            event_json = json.loads(event_oem_content)
            self.validate_event_json(event_json, event_json_path)
        return event_json

    def validate_event_json(self, json_obj, path):
        id_def_set = set()
        for item in json_obj.get("EventDefinition", []):
            if item["EventKeyId"] in id_def_set:
                raise ValueError(f'{path} EventDefinition存在重复的EventId {item["EventKeyId"]}')
            else:
                id_def_set.add(item["EventKeyId"])

        id_des_set = set()
        for item in json_obj.get("EventDescription", []):
            if item["EventKeyId"] in id_des_set:
                raise ValueError(f'{path} EventDescription存在重复的EventId {item["EventKeyId"]}')
            else:
                id_des_set.add(item["EventKeyId"])
            if item["EventKeyId"] not in id_def_set:
                raise ValueError(f'{path} EventDescription存在未定义的EventId {item["EventKeyId"]}')

    def cp_product_event_json(self, event_json):
        board_json = {}
        if event_json:
            bord_dir = self.get_board_path()
            events = []
            events_path = os.path.join(bord_dir, "event/eventDefList.txt")
            if os.path.isfile(events_path):
                with open(events_path, "r") as f:
                    lines = f.readlines()
                events = [line.strip() for line in lines]
            filterd_definitions = [
                item
                for item in event_json.get("EventDefinition", [])
                if item["EventKeyId"] in events
            ]
            filterd_descriptions = [
                item
                for item in event_json.get("EventDescription", [])
                if item["EventKeyId"] in events
            ]
            board_json = {
                "Version": event_json.get("Version", ""),
                "EventDefinition": filterd_definitions,
                "EventDescription": filterd_descriptions
            }
            filterd_json = json.dumps(board_json, ensure_ascii=False)
            filterd_json_path = os.path.join(bord_dir, "event_def.json")
            with os.fdopen(os.open(filterd_json_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
                                   stat.S_IWUSR | stat.S_IRUSR), "w") as f:
                f.write(filterd_json)
            copy(
                self, "event_def.json", 
                src=os.path.join(self.source_folder, bord_dir), 
                dst=os.path.join(self.package_folder, "opt/bmc/conf")
            )

            sys.path.append(os.getcwd())
            registry_py = importlib.import_module("registry")
            registry = getattr(registry_py, "Registry")
            filterd_json_path = os.path.join(bord_dir, "ibmcevents.json")
            registry_obj = registry(board_json, filterd_json_path)
            registry_obj.gen()
            copy(
                self, "ibmcevents.json", 
                src=os.path.join(self.source_folder, bord_dir), 
                dst=os.path.join(self.package_folder, "opt/bmc/apps/event")
            )

    def package(self):
        os.chdir(self.source_folder)
        self.cp_kvm_padding_image()
        self.cp_vce_dft_data()
        self.cp_frame_logrotate_conf()
        self.cp_nginx_logrotate_conf()
        event_json = self.get_event_json()
        self.cp_include_vendor()

        if os.path.isfile(os.path.join(self.source_folder, "dist/permissions.ini")):
            copy(
                self, "permissions.ini", 
                src=os.path.join(self.source_folder, "dist"), 
                dst=self.package_folder
            )
        
        # common为公共特性包, 不包含产品sr, 其他上层定制组件引入该common包进行定制化
        if str(self.options.board_name) == "common":
            return

        file_dir = "default"
        board_dir = self.get_board_path()
        if not board_dir:
            print(f"invalid board_name: {self.options.board_name}")
            return

        for root, dirs, files in os.walk(board_dir):
            for name in files:
                if name == "profile.txt":
                    file_dir = os.path.join(root, name)
                if name == "metrics.json":
                    copy(
                        self, "metrics.json", 
                        src=os.path.join(self.source_folder, root), 
                        dst=os.path.join(self.package_folder, "opt/bmc/metric")
                    )
        if "default" == file_dir:
            print("no file profile.txt")
            return

        with open(file_dir) as fp:
            for line in fp:
                line = line.replace("\n", "")
                line = line.replace(" ", "")
                if 0 == len(line):
                    continue
                index = len(line) - 1
                while line[index] != "/":
                    index = index - 1
                file_root = "./vendor/" + line[0:index]
                file_name = line[index + 1:len(line)]
                _, ext = os.path.splitext(file_name)
                copy(
                    self, file_name, 
                    src=os.path.join(self.source_folder, file_root), 
                    dst=os.path.join(self.package_folder, "opt/bmc", ext[1:])
                )

        # 拷贝产品定制化schema文件
        self.cp_product_schema()
        self.cp_product_event_json(event_json)
