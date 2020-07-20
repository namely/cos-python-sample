from test.test_api import TestApi
from test.test_handler import TestHandler
from test.test_cos import TestCos

if __name__ == '__main__':
    TestHandler.run(host="write-handler", port="9011")
    # TestCos.run(host = "host.docker.internal", port = "9000")
    TestCos.run(host = "chiefofstate", port = "9000")
    # TestApi.run(host = "api", port = "9010")
