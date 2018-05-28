from dispy_pool import get_local_ip
import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="dispy node start script")
    parser.add_argument("-p", "--port", type=int, default=7000)
    return parser.parse_args()


if __name__ == '__main__':
    # Use all cores in the machine
    # print(os.system("netstat -plan | grep 51348"))
    args = parse_args()
    command = "dispynode.py --clean -i {0} --ext_ip_addr {0}" \
              " -p {1}".format(get_local_ip(), args.port)
    print(command)
    os.system(command)
