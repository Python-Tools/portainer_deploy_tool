import requests as rq
from pyloggerhelper import log
base_schema_properties = {
    "log_level": {
        "type": "string",
        "title": "l",
        "description": "log等级",
        "enum": ["DEBUG", "INFO", "WARN", "ERROR"],
        "default": "DEBUG"
    },
    "base_url": {
        "type": "string",
        "title": "b",
        "description": "portainer的根url"
    }
}


def get_jwt(base_url: str, username: str, password: str) -> str:
    """获取jwt.

    Args:
        base_url (str): portainer的根地址
        username (str): portainer用户名
        password (str): 用户的密码

    Returns:
        str: jwt的值
    """
    res = rq.post(
        base_url + "/auth",
        json={
            "Username": username,
            "Password": password
        }
    )
    if res.status_code != 200:
        log.error("get jwt query get error", base_url=base_url, username=username, status_code=res.status_code)
        raise AttributeError("get jwt query get error")
    try:
        res_json = res.json()
    except Exception as e:
        log.error("get jwt query get json result error", base_url=base_url, username=username, err=type(e), err_msg=str(e), exc_info=True, stack_info=True)
        raise e
    else:
        jwt = res_json.get("jwt")
        if jwt:
            return jwt
        else:
            log.error("get jwt query has no field jwt", base_url=base_url, username=username, res_json=res_json)
            raise AttributeError("get jwt query has no field jwt")
