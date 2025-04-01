# vpd 重要产品数据（vital product data）

硬件PSR、硬件CSR、机型相关的软件配置、北向接口映射、白牌定制等信息

# 代码仓目录结构说明
详细目录结构树如下所示，其中关键路径总结如下。
## 1、整机硬件配置
【路径】./vendor/Huawei/Server/Kunpeng/BM320/PSR （以BM320为例）
【解读】与整机硬件强相关的配置，比如调速策略。天池机型来自挂耳eeprom，开发早期BMC软件携带，待硬件独立发布后，BMC删除。（BMC删除原因之一：在多个机型共包发布时，BMC不易做兼容）
## 2、整机类配置（非PSR配置）
【路径】./vendor/Huawei/Server/Kunpeng/BM320/platform （以BM320为例）
【解读】与整机相关的、且又不适合由硬件PSR承载的配置，比如是否支持SNMP、过热掉电后是否自动上电。
## 3、特定产业专用组件配置信息
【路径】./vendor/Huawei/Server/Kunpeng/Nic/Lom
【解读】鲲鹏产业专用的组件配置信息
## 4、华为服务器通用组件配置信息
【路径】./vendor/Huawei/Nic/hi1822
【解读】华为公司服务器通用组件配置信息
## 5、天池组件配置信息
【路径】./vendor/Huawei/TianChi、./vendor/Huawei/TianChi/BCU、./vendor/Huawei/TianChi/BCU/BC82AMDV-3732
【解读】天池组件配置信息，所有机型通用配置

## 6、Scanner扫描周期配置原则
【注意事项】Scanner扫描周期配置原则，必须按照如下分类进行配置，如果新增的Scanner不在已有分类，则需要subPC评审刷新分类才能添加。
(1)、BCU和EXU的PowerGood告警，周期为100ms
(2)、影响业务类的离散电压，周期为400ms
(3)、影响业务类的时钟告警，周期为400ms
(4)、影响业务类的CPU故障告警，周期为400ms
(5)、业务关键状态：系统复位，上电超时，异常掉电，ThermTrip，周期为400ms
(6)、故障诊断的故障检测，周期为1s
(7)、硬盘类状态扫描，周期为5s
(8)、不影响业务的硬件状态，周期为5s
(9)、热插拔部件在位状态，周期为2s
(10)、非热插拔部件在位扫描，周期为8s
(11)、门限类温度扫描，周期为1s
(12)、门限类电压扫描，周期为3s
(13)、纽扣电池扫描，周期为10s
(14)、风扇转速扫描，周期为1s
(15)、RTC时间同步，周期为6s
(16)、按钮交互类，比如UID按钮，周期为1s
(17)、风扇、电源总功耗扫描，周期为1s
(18)、光模块温度，周期为10s，连续12次失败认为异常
(19)、面板电源按钮，周期为200ms

## 7、SmcDfxInfo配置说明
[SmcDfxInfo配置说明](SmcDfxInfo配置说明.md)

```shell
# vpd代码仓目录结构规划
├── CHANGELOG.md
├── Makefile
├── build.py
├── conanfile.py
├── conaninfo.py
├── mds
├── dist
│   └── permissions.ini
└── vendor                  # 厂家信息：服务器厂家、组件厂家等
    ├── Aspeed
    │   └── bmc_soc
    │       ├── ast2500
    │       └── ast2600
    ├── Huawei
    │   ├── BMCSoC
    │   │   └── hi1711                  # 承载与BMC SoC相关的配置信息
    │   ├── Nic
    │   │   ├── hi1822
    │   │   ├── hi1823
    │   │   ├── sd5902l
    │   │   └── virtual
    │   ├── Raid
    │   ├── Server
    │   │   ├── Ascend
    │   │   ├── Kunpeng
    │   │   │   ├── BM320
    │   │   │   │   ├── PSR             # 整机硬件配置：与整机硬件强相关的配置，比如调速策略。天池机型来自挂耳eeprom，开发早期BMC软件携带，待硬件独立发布后，BMC删除。（BMC删除原因之一：在多个机型共包发布时，BMC不易做兼容）
    │   │   │   │   ├── platform        # 整机类配置（非PSR配置）：与整机相关的、且又不适合由硬件PSR承载的配置，比如是否支持SNMP。
    │   │   │   │   ├── profile.txt     # 承载本机型需要的SR文件
    │   │   │   │   ├── redfish         # Redfish配置，包含自动生成代码、数据映射等
    │   │   │   │   ├── schema          # 产品的装备定制化存在差异性配置时（默认值、属性），在此目录定义差异化的schema文件，构建时会综合profile_schema仓的文件生成新配置
    │   │   │   │   └── web_backend     # WEB后台配置，包含自动生成代码、数据映射等
    │   │   │   └── Nic                 # 本产业用板卡
    │   │   │       └── Lom
    │   │   ├── Pangea
    │   │   ├── TCE
    │   │   └── public
    │   ├── Ssd
    │   └── TianChi
    │       ├── ACU
    │       ├── BCU
    │       │   ├── BC82AMDV-3230
    │       │   │   ├── default         # BMC包携带
    │       │   │   └── manufacture     # 生产烧录，原则与BMC包携带保持一致，只是归档生产周期相对BMC版本发布较慢
    │       │   └── BC82AMDV-3732
    │       │       ├── default         # BMC包携带
    │       │       └── manufacture     # 生产烧录，原则与BMC包携带保持一致，只是归档生产周期相对BMC版本发布较慢
    │       ├── CLU
    │       ├── EXU
    │       ├── IEU
    │       ├── IOU
    │       ├── MEU
    │       ├── PSU
    │       ├── SEU
    │       ├── STU
    │       ├── UBC
    │       └── UBM
    ├── Intel
    │   ├── Nic
    │   │   ├── cx5
    │   │   └── cx6
    │   └── Raid
    ├── Mellanox
    └── Nvidia
        └── Nic
            └── cx6-dx
```

# CSR配置说明
## Connector对象配置
分析天池及传统产品，可以按管理维度将组件和板卡划分为几类，不同类型组件的Connector连接器对象配置有一定的差异。以下根据组件类型分别说明。
### 天池标准组件
```json
"Connector_Exu_1": {
    "Bom": "14100513",
    "Slot": 1,
    "Position": 1,
    "Presence": "<=/Scanner_Presence_1.Value",
    "Id": "",
    "AuxId": "",
    "Buses": [
        "I2c_2"
    ],
    "SystemId": 1,
    "SilkText": "exu",
    "IdentifyMode": 3,
    "Type": ""
}
```
主要参数说明：
- `"Bom": "14100513"` 表示下级组件Bom Id。
- `"Type": ""` 描述连接器后端设备的类型（如PCIeSlot，PCIeRiser，NVMe，PSU，BCU，SEU等）
- `"IdentifyMode": 3` 表示下级组件识别方式，3对应下级组件识别方式为天池标准类型组件。
- `"Presence": "<=/Scanner_Presence_1.Value"` 表示Presence状态获取方式，天池标准组件类型需要指定在位状态获取方式，一般通过同步属性语法通过硬件代理读取指定器件寄存器数据，例如SMC。
- `"Id": ""` 表示下级组件Board id，天池标准组件的BoardId通过Chip属性关联的器件对象，调用对应的读写接口获取Eeprom数据中的Board Id信息。无需配置（不生效）。

### BoardId不可读类型组件
```json
"Connector_IdReport_1": {
    "Bom": "14100513",
    "Slot": 1,
    "Position": 1,
    "Presence": 0,
    "Id": "",
    "AuxId": "",
    "Buses": [
        "I2c_2"
    ],
    "SystemId": 1,
    "SilkText": "exu",
    "IdentifyMode": 2,
    "Type": ""
}
```
主要参数说明：
- `"Bom": "14100513"` 表示下级组件Bom Id。
- `"Type": ""` 描述连接器后端设备的类型（如PCIeSlot，PCIeRiser，NVMe，PSU，BCU，SEU等）
- `"IdentifyMode": 2` 表示下级组件识别方式，2对应下级组件识别方式为BoardId不可读（上报）类型组件。
- `"Presence": 0` 表示初始Presence状态，BoardId不可读类型由多样化硬件上报设置，值必须配置为0，否则会导致下级组件无法正确触发自发现逻辑。
- `"Id": ""` 表示下级组件board id，BoardId不可读类型由多样化硬件上报设置，无需配置（不生效）。
- `"AuxId": ""` 表示下级组件aux id，BoardId不可读类型由多样化硬件上报设置，无需配置（不生效）。

### BoardId可读类型组件
```json
"Connector_IdRead_1": {
    "Bom": "14100513",
    "Slot": 1,
    "Position": 1,
    "Presence": "<=/Scanner_Presence_1.Value",
    "Id": "#/Accessor_Id_1.Value",
    "AuxId": "",
    "Buses": [
        "I2c_2"
    ],
    "SystemId": 1,
    "SilkText": "exu",
    "IdentifyMode": 1,
    "Type": ""
}
```
主要参数说明：
- `"Bom": "14100513"` 表示下级组件Bom Id。
- `"Type": ""` 描述连接器后端设备的类型（如PCIeSlot，PCIeRiser，NVMe，PSU，BCU，SEU等）
- `"IdentifyMode": 1` 表示下级组件识别方式，1对应下级组件识别方式为BoardId可读类型组件。
- `"Presence": "<=/Scanner_Presence_1.Value"` 表示Presence状态获取方式，BoardId可读类型需要指定在位状态获取方式，一般通过同步属性语法通过硬件代理读取指定器件寄存器数据。
- `"Id": "#/Accessor_Id_1.Value"` 表示下级组件board id，BoardId可读类型需要指定board id获取方式，一般通过引用属性语法通过硬件代理读取指定器件寄存器数据。
