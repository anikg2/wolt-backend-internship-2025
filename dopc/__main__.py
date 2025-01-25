from dopc.service import runService
from dopc.helpers import getServicePort
import argparse


if __name__ == "__main__":
    # Adding support for custom port. Defaults to port specified in config.py
    parser = argparse.ArgumentParser()
    default_port = getServicePort()
    parser.add_argument('--port', type=int, help="The port on which the DOPC service will run", default=default_port)
    args = parser.parse_args()

    # Run the DOPC service at the specified/default port
    runService(args.port)