import sys
from typing import List
from schema_entry import EntryPoint
from .update_service_in_stack import UpdateServiceInStack
from .update_service_by_webhook import UpdateServiceByWebhooks


def main(argv: List[str] = sys.argv[1:]) -> None:
    """服务启动入口.

    设置覆盖顺序`环境变量>命令行参数`>`'-c'指定的配置文件`>`项目启动位置的配置文件`>默认配置.
    """
    root = EntryPoint(name="portainer_deploy_tool", description="在portainer上更新部署镜像")
    root.regist_sub(UpdateServiceInStack)
    root.regist_sub(UpdateServiceByWebhooks)
    root(argv)

    return None


if __name__ == "__main__":
    main(sys.argv[1:])
