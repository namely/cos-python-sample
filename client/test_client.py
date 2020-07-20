from test.test_api import TestApi
from test.test_handler import TestHandler
from test.test_cos import TestCos

if __name__ == '__main__':
    TestHandler.run()
    TestCos.run()
    # TestApi.run()
