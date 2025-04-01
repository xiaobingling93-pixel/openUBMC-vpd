# 类定义说明

```
"SmcDfxInfo": {
       "properties": {
           "Chip": {
               "usage": [
                   "CSR"
               ],
               "baseType": "String"
           },
           "Offset": {
               "usage": [
                   "CSR"
               ],
               "baseType": "U32"
           },
           "Size": {
               "usage": [
                   "CSR"
               ],
               "baseType": "U8"
           },
           "Period": {
               "usage": [
                   "CSR"
               ],
               "baseType": "U32"
           },
           "SmcVersion": {
               "usage": [
                   "CSR"
               ],
               "baseType": "U32"
           },
           "Config": {
               "baseType": "Dictionary",
               "usage": [
                   "CSR"
               ],
               "$ref": "types.json#/defs/DfxConfigDict"
           },
           "Mapping": {
               "baseType": "Dictionary",
               "usage": [
                   "CSR"
               ],
               "$ref": "types.json#/defs/MappingDict"
           },
           "Context": {
               "baseType": "Dictionary",
               "usage": [
                   "CSR"
               ],
               "$ref": "types.json#/defs/ContextDict"
           }
       }

{
    "defs": {
        "ConfigByteDict": {
            "key": {
                "baseType": "String"
            },
            "value": {
                "baseType": "U8"
            }
        },
        "DfxConfigDict": {
            "key": {
                "baseType": "String"
            },
            "value": {
                "baseType": "Dictionary",
                "$ref": "#/defs/ConfigByteDict"
            }
        },
        "MappingStruct": {
            "Value": {
                "baseType": "String"
            }
        },
        "MappingDict": {
            "key": {
                "baseType": "String"
            },
            "value": {
                "baseType": "Struct",
                "$ref": "#/defs/MappingStruct"
            }
        },
        "ContextDict": {
            "key": {
                "baseType": "String"
            },
            "value": {
                "baseType": "String"
            }
        }
    }
}

```

- Chip：引用的Smc Chip对象
- Offset：SmcDfxInfo的偏移地址（opcode），一般为7424
- Size：SmcDfxInfo的长度
- Period：读取周期
- SmcVersion：支持的Smc最低版本，用于版本检测
- Config：SmcDfxInfo中每个字节与对应硬件信号的对应关系，可通过mask按照单字节或者bit位进行对应
- Mapping：Scanner与硬件信号的对应关系，通过配置表达式获取值，硬件信号名称为Config中的名称
- Context：预留扩展字段，当前1U风扇板 MCU版本号有使用该字段，其他未使用

### SmcDfxInfo定义规则

规则1）SMC（CPLD/MCU）版本号需要在最前面几个字节呈现（如CPLD占用1个字节，MCU占用3字节）；
规则2）DFX寄存器按照压缩方式存储，寄存器中间不做预留，如果后续SMC新增功能，需要末尾追加，不能修改已经定义的寄存器空间；
规则3）返回的寄存器空间，需要支持SMC检测的所有硬件信息（该组件的所有告警、电源、时钟、在位、传感器读数等）。

### CSR配置示例

```
"SmcDfxInfo_EXU": {
      "Chip": "#/Smc_ExpBoardSMC",
      "Offset": 7424,
      "Size": 51,
      "Period": 200,
      "SmcVersion": 108,
      "Config": {
        "1": {"cpld_ver": 255},
        "2": {"temp_lm75_front_low": 255},
        "3": {"temp_lm75_front_high": 255},
        "4": {"temp_lm75_right_low": 255},
        "5": {"temp_lm75_right_high": 255},
        "6": {"temp_lm75_left_low": 255},
        "7": {"temp_lm75_left_high": 255},
        "8": {"adc_fan_2_high": 255},
        "9": {"adc_fan_1_low": 255},
        "10": {"bmc_adc_vcc_12v0_1_low": 255},
        "11": {"bmc_adc_vcc_12v0_1_high": 255},
        "12": {"bmc_adc_vcc_12v0_2_low": 255},
        "13": {"bmc_adc_vcc_12v0_2_high": 255},
        "14": {"bmc_adc_vcc_12v0_3_low": 255},
        "15": {"bmc_adc_vcc_12v0_3_high": 255},
        "16": {"bmc_adc_stby_3v3_low": 255},
        "17": {"bmc_adc_stby_3v3_high": 255},
        "18": {"bmc_adc_vcc_5v0_low": 255},
        "19": {"bmc_adc_vcc_5v0_high": 255},
        "20": {"bmc_adc_stby_5v0_low": 255},
        "21": {"bmc_adc_stby_5v0_high": 255},
        "32": {"status_power_sensor": 8,"status_lm75": 4,"status_adc": 2},
        "34": {"prsnt_lci_n": 2,"prsnt_rci_n": 1},
        "35": {"bmc_rst_event": 4,"uid_button_event": 2,"fp_power_button_event": 1},
        "36": {"nic1_prsnt": 1},
        "37": {"nic2_prsnt": 1},
        "38": {"m2_power_cable_prsnt": 64,"prsnt_baseboard": 32,"prsnt_tpcm": 16,"prsnt_fan_board": 8,"prsnt_inner_hdd": 4,"prsnt_psu_hdd": 2,"prsnt_front_hdd": 1},
        "39": {"bbu_prsnt": 1},
        "40": {"sys_all_pwrgd_reg": 1},
        "41": {"sys_power_on_flash": 1},
        "42": {"vcc_time_out": 8,"vcc_power_fail": 4},
        "43": {"code_power_time_out": 255},
        "44": {"code_power_fail": 255},
        "45": {"clk_50m_loss_status": 1},
        "46": {"clk_100m_loss_status": 1},
        "47": {"link_nic1_port": 15},
        "48": {"link_nic2_port": 15},
        "49": {"over_temp_12v_3": 4,"over_temp_12v_2": 2,"over_temp_12v_1": 1},
        "50": {"pmbus_cpld_alert1": 16,"pg_ip_ps_1": 8,"pg_ps_1": 4,"bmc_efusev_ps_1": 2,"psu1_cpld_prsnt": 1},
        "51": {"pmbus_cpld_alert2": 16,"pg_ip_ps_2": 8,"pg_ps_2": 4,"bmc_efusev_ps_2": 2,"psu2_cpld_prsnt": 1}
      },
      "Mapping": {
        "Scanner_SerdesLom1Pres": {"Value": "expr($nic1_prsnt)"},
        "Scanner_SerdesLom2Pres": {"Value": "expr($nic2_prsnt)"},
        "Scanner_Psu1OPOKStatus": {"Value": "expr($pg_ps_1)"},
        "Scanner_Psu2OPOKStatus": {"Value": "expr($pg_ps_2)"},
        "Scanner_PS1Pres": {"Value": "expr($psu1_cpld_prsnt)"},
        "Scanner_PS2Pres": {"Value": "expr($psu2_cpld_prsnt)"},
        "Scanner_UIDButtonEvent": {"Value": "expr($uid_button_event)"},
        "Scanner_PowerGd": {"Value": "expr($sys_all_pwrgd_reg)"},
        "Scanner_PowerGdFlash": {"Value": "expr($sys_power_on_flash)"},
        "Scanner_CLU_1": {"Value": "expr($prsnt_fan_board)"},
        "Scanner_FanPwrSensorStatus": {"Value": "expr($status_power_sensor)"},
        "Scanner_Fan_Pwr": {"Value": "expr($adc_fan_2_high + ($adc_fan_1_low << 8))"},
        "Scanner_SEU_1": {"Value": "expr($prsnt_front_hdd)"},
        "Scanner_SEU_2": {"Value": "expr($prsnt_psu_hdd)"},
        "Scanner_PowerBtnEvt": {"Value": "expr($fp_power_button_event)"},
        "Scanner_100M1ClockFailMntr": {"Value": "expr($clk_100m_loss_status)"},
        "Scanner_50M1ClockFailMntr": {"Value": "expr($clk_50m_loss_status)"},
        "Scanner_PowerOnTimeout": {"Value": "expr($vcc_time_out)"},
        "Scanner_PwrOkSigDrop": {"Value": "expr($vcc_power_fail)"},
        "Scanner_Nic1Lm75": {"Value": "expr($temp_lm75_right_low + ($temp_lm75_right_high << 8))"},
        "Scanner_Nic2Lm75": {"Value": "expr($temp_lm75_left_low + ($temp_lm75_left_high << 8))"},
        "Scanner_PSULm75": {"Value": "expr($temp_lm75_front_low + ($temp_lm75_front_high << 8))"},
        "Scanner_ExpMos1TempHigh": {"Value": "expr($over_temp_12v_1)"},
        "Scanner_ExpMos2TempHigh": {"Value": "expr($over_temp_12v_2)"},
        "Scanner_ExpMos3TempHigh": {"Value": "expr($over_temp_12v_3)"},
        "Scanner_RightEar": {"Value": "expr($prsnt_rci_n)"},
        "Scanner_LeftEar": {"Value": "expr($prsnt_lci_n)"},
        "Scanner_ECUSys12V1": {"Value": "expr($bmc_adc_vcc_12v0_1_low + ($bmc_adc_vcc_12v0_1_high << 8))"},
        "Scanner_ECUSys12V2": {"Value": "expr($bmc_adc_vcc_12v0_2_low + ($bmc_adc_vcc_12v0_2_high << 8))"},
        "Scanner_ECUSys12V3": {"Value": "expr($bmc_adc_vcc_12v0_3_low + ($bmc_adc_vcc_12v0_3_high << 8))"},
        "Scanner_ECUSys3V1": {"Value": "expr($bmc_adc_stby_3v3_low + ($bmc_adc_stby_3v3_high << 8))"},
        "Scanner_ECUSys5V1": {"Value": "expr($bmc_adc_vcc_5v0_low + ($bmc_adc_vcc_5v0_high << 8))"},
        "Scanner_ECUSys5V2": {"Value": "expr($bmc_adc_stby_5v0_low + ($bmc_adc_stby_5v0_high << 8))"},
        "Scanner_CpuBrdPresenceMntr": {"Value": "expr($prsnt_baseboard)"},
        "Scanner_FanCableMntr": {"Value": "expr($prsnt_fan_board)"},
        "Scanner_EXUPwrOnTimeOut": {"Value": "expr($code_power_time_out)"},
        "Scanner_EXUPwrSigDrop": {"Value": "expr($code_power_fail)"}
      }
    }

```

- Config为对应byte与硬件信号的对应关系，key表示第几个byte，从1开始，1个byte可以存在多个信号或1个信号，通过信号名称与mask掩码对应整字节数据或其中某个bit位的数据
- Config对应关系需与产品对应硬件约定
- Mapping为Scanner与硬件信号的对应关系，key为Scanner名称，Scanner必须位于同一CSR中，"Value"表示为Scanner的值，通过配置表达式从硬件信号获取值；
- 固定第一个字节表示Smc版本号，2段式，高4位为第一段，低4位为第二段，如32表示版本号为2.0
- 如果单板无CPLD，仅有MCU，使用前3个字节表示MCU版本号，例如"\x00\x02\x12"，表示MCU版本号为0.2.18，在Context中配置表达式获取版本号；
- 同一Chip上配置相同的Scanner会进行合并处理，在定义时可以定义在多个SR文件中，需保持定义一致，比如EXU上的PowerGood信号；
- 多个SR中可定义同一个Chip的SmcDfxInfo，将进行合并处理；

### 版本控制

为避免SMC版本/CSR版本/BMC版本之间的不兼容情况，使用版本号配置进行检查，如果检查不兼容，则使用单独查询命令字的方式获取Scanner的值，避免功能异常；

#### 预期最低版本号

- 在SmcDfxInfo配置中通过字段SmcVersion字段进行配置
- CPLD版本号通过`(smc_version >> 4) * 100 + (smc_version & 0xf)`表达式进行计算
- MCU版本号通过`($mcu_ver_major << 16) + ($mcu_ver_minor << 8) + $mcu_ver_build)`表达式进行计算

#### 实际Smc版本号

实际的Smc版本号来源有3种方式：

- 通过Context中的表达式获取，如1U 风扇板MCU版本号：
  ```
  "SmcDfxInfo_CLU": {
         "Chip": "#/Smc_FanBoardSMC",
         "Offset": 7424,
         "Size": 55,
         "Period": 2000,
         "SmcVersion": 784,
         "Config": {
              "1": {"mcu_ver_major": 255},
              "2": {"mcu_ver_minor": 255},
              "3": {"mcu_ver_build": 255},
               ...
         },
        "Context": {
                "SmcVersion": "expr(($mcu_ver_major << 16) + ($mcu_ver_minor << 8) + $mcu_ver_build)"
        },
        "Mapping": {
               ...
        }
  }
  ```

Context中的SmcVersion即为实际的MCU版本号

- 通过opcode命令字0x900查询获取
- 通过SmcDfxInfo第一个字节获取

#### 版本号比较

- 来源优先级：通过Context中表达式获取的版本号 > 通过opcode命令字0x900查询获取的版本号 > 通过SmcDfxInfo第一个字节获取的版本号；
- 若实际版本号 >= 预期最低版本号，则检查成功，使用SmcDfxInfo获取Scanner的值，否则检查失败，使用原来的opcode命令字获取值；
- 可通过日志查看版本号比较是否成功，以及是否已启用SmcDfxInfo：
  `cat /var/log/framework.log | grep SmcDfxInfo`

```
检查成功的日志：
1970-01-01 08:00:35.540949 hwproxy NOTICE: smc_dfx_info.lua(208): smc_dfx_info:SmcDfxInfo_EXU_0101, version check success, expect version: 108, version by expr: nil, version by opcode: 109, version by dfx: 109

检查失败的日志：
1970-01-01 00:01:21.828078 hwproxy ERROR: smc_dfx_info.lua(201): stop read smc_dfx_info: SmcDfxInfo_CLU_010103, check smc version failed, expect version: 108, version by expr: nil,version by opcode: 106, version by dfx: 1
```

- 初始配置SmcDfxInfo时SmcVersion应配置为最低支持的CPLD/MCU版本，后续如果有更新SmcDfxInfo配置，增加内容时更新SmcVersion；

#### 版本兼容性关系

将BMC/CPLD（MCU）/CSR版本分为老版本（无SmcDfxInfo）、初始版本（首次更新SmcDfxInfo的版本）、新版本（更新SmcDfxInfo内容后的版本），版本间的兼容关系如下：

| BMC版本 | CPLD/MCU版本 | CSR版本  |Scanner获取值|
|---------|-----------|--------------|---------------|
|老版本|*|*|<mark>忽略SmcDfxInfo配置，使用单独的opcode获取</mark>|
|新版本|老版本|老版本|<mark>无SmcDfxInfo配置，使用单独的opcode获取</mark>|
|新版本|初始版本|老版本|<mark>版本检查失败，忽略SmcDfxInfo配置，使用单独的opcode获取</mark>|
|新版本|新版本|老版本|<mark>版本检查失败，忽略SmcDfxInfo配置，使用单独的opcode获取</mark>|
|新版本|老版本|初始版本|<mark>无SmcDfxInfo配置，使用单独的opcode获取</mark>|
|新版本|初始版本|初始版本|<mark>版本检查成功，使用SmcDfxInfo获取</mark>|
|新版本|新版本|初始版本|<mark>版本检查失败，忽略SmcDfxInfo配置，使用单独的opcode获取</mark>|
|新版本|老版本|新版本|<mark>无SmcDfxInfo配置，使用单独的opcode获取</mark>|
|新版本|初始版本|新版本|<mark>版本检查成功，使用SmcDfxInfo获取</mark>|
|新版本|新版本|新版本|<mark>版本检查成功，使用SmcDfxInfo获取</mark>|
