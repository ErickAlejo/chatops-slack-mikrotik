from netmiko import ConnectHandler


def first_check_if_command_is_dangerous(command:str) -> bool:
    """ We searching words dangerous in command
    ### Arguments

        command (str) : command to devices for inst: "interface/print something"
    
    ### Return

        None
    """

    # This flag say us if command is dangerous
    flag = False

    list_words_dmg = [
    "/system reset-configuration",
    "/disk format-drive",
    "/system routerboard upgrade",
    "/ip firewall filter remove [find]",
    "/ip route remove [find]",
    "/interface disable [find]",
    "/interface ethernet set [find] disabled=yes",
    "/user remove [find]",
    "/system reboot",
    "/routing bgp peer disable [find]",
    "/routing ospf instance disable [find]",
    '/user set [find] password=""',
    "/ip service set telnet disabled=no",
    "/ip service set ftp disabled=no",
    "/system shutdown",
    "/ip address remove [find]",
    "/system script remove [find]",
    "/system scheduler remove [find]",
    ]

    for damage in list_words_dmg:
        if command in str(damage):
            flag = True
            return True 

    return False

def second_check_if_command_is_dangerous(command_str:str) -> bool:
    """ Second checking to word dangerous in command"""

    flag = False

    dangerous_verbs = [
        "set",
        "delete",
        "remove",
        "disable",
        "enable",
        "reset",
        "override",
        "commit",
        "rollback",
        "shutdown",
        "restart",
        "clear",
        "format",
        "write",
        "flush",
        "apply",
        "reboot",
        "install",
        "upgrade",
        "uninstall"
    ]

    for word in dangerous_verbs:
        if word in command_str:
            return True
        
    return False


def send_command_to_device_mikrotik(ip:str, command:str):
    mikrotik = {
        'device_type': 'mikrotik_routeros',
        'host': ip,
        'username': 'admin',
        'password': 'S0m0s_2021',
    }

    first_check = first_check_if_command_is_dangerous(command)
    second_check = second_check_if_command_is_dangerous(command)

    if first_check != second_check:
        warning = "🟥 Cannot define if command is dangerous "
        return warning
    
    elif first_check is True or second_check is True:
        warning = "🟥 Command Dangerous "
        return warning

    elif first_check is False or second_check is False:    
        mikrotik_connect = ConnectHandler(**mikrotik)
        output = mikrotik_connect.send_command(command, cmd_verify=True, read_timeout=10)
        return output
