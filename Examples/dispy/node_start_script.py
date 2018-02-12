from dispy_pool import get_local_ip
import os

if __name__ == '__main__':
    # Use all cores in the machine
    # print(os.system("netstat -plan | grep 51348"))
    command = "dispynode.py --clean -i {0} --ext_ip_addr {0}".format(get_local_ip())
    print(command)
    os.system(command)
