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
        base_url + "/api/auth",
        json={
            "Username": username,
            "Password": password
        }
    )
    if res.status_code != 200:
        log.error("get jwt query get error",
                  base_url=base_url,
                  username=username,
                  status_code=res.status_code)
        raise AttributeError("get jwt query get error")
    try:
        res_json = res.json()
    except Exception as e:
        log.error("get jwt query get json result error",
                  base_url=base_url,
                  username=username,
                  err=type(e),
                  err_msg=str(e),
                  exc_info=True,
                  stack_info=True)
        raise e
    else:
        jwt = res_json.get("jwt")
        if jwt:
            return jwt
        else:
            log.error("get jwt query has no field jwt",
                      base_url=base_url,
                      username=username,
                      res_json=res_json)
            raise AttributeError("get jwt query has no field jwt")


def get_swarm_id(base_url: str, jwt: str, endpoint: int) -> str:
    """获取端点的SwarmID.

    Args:
        base_url (str): portainer的根地址
        jwt (str): 访问jwt
        endpoint (int): 端点ID

    Raises:
        AttributeError: get swarm id query get error
        e: get swarm id query get json result error
        AttributeError: endpint not swarm

    Returns:
        str: Swarm ID
    """
    res = rq.get(f"{base_url}/api/endpoints/{endpoint}/docker/swarm",
                 headers=rq.structures.CaseInsensitiveDict({"Authorization": "Bearer " + jwt}))
    if res.status_code != 200:
        log.error("get swarm id query get error",
                  base_url=base_url,
                  endpoint=endpoint,
                  status_code=res.status_code)
        raise AttributeError("get swarm id query get error")
    try:
        res_json = res.json()
    except Exception as e:
        log.error("get swarm id query get json result error", endpoint=endpoint, err=type(e), err_msg=str(e), exc_info=True, stack_info=True)
        raise e
    else:
        swarm_id = res_json.get("ID")
        if swarm_id:
            return swarm_id
        else:
            raise AttributeError("endpint not swarm")
