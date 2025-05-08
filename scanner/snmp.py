from pysnmp.hlapi import (
    getCmd, SnmpEngine, CommunityData,
    UdpTransportTarget, ContextData,
    ObjectType, ObjectIdentity
)

import config

def get_device_info(ip):
    """
    Выполняет SNMP-запрос к устройству для получения описания (sysDescr).
    Возвращает строку описания или None.
    """
    for community in config.SNMP_COMMUNITIES:
        try:
            error_indication, error_status, _, var_binds = next(
                getCmd(
                    SnmpEngine(),
                    CommunityData(community, mpModel=0),  # SNMP v1
                    UdpTransportTarget((ip, 168), timeout=10, retries=0),
                    ContextData(),
                    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))
                )
            )
            if error_indication:
                print(f"[SNMP] Ошибка для {ip}: {error_indication}")
                continue
            elif error_status:
                print(f"[SNMP] Статус ошибки: {error_status.prettyPrint()}")
                continue
            else:
                info = str(var_binds[0][1])
                print(f"[SNMP] {ip} => {info}")
                return info
        except Exception as e:
            print(f"[SNMP] Исключение при опросе {ip}: {e}")
    return None