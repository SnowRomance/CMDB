#### Common
def get_user_dict(filteruser):
    user = {}
    user["id"] = filteruser[0]
    user["password"] = filteruser[1]
    user["username"] = filteruser[4]
    user["email"] = filteruser[7]
    return user


def get_host_dict(filterhost):
    host = {}

    host["id"] = filterhost[0]
    host["ip"] = filterhost[1]
    host["hostname"] = filterhost[2]
    host["group_name"] = filterhost[3]
    host["nick_name"] = filterhost[4]
    host["idc_name"] = filterhost[5]
    host["inner_ip"] = filterhost[6]

    return host

