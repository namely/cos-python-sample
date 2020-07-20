from write_handler_impl.service import run
import os

PORT = os.environ.get("APP_PORT") or "9011"

if __name__ == '__main__':
    run(PORT)
