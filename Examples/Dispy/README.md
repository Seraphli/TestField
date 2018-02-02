# Dispy Example

An example of how to use dispy for cluster computing.

## Node

Node represent a computer in the cluster.
It can be a computer in the local network.

For every node you use, you have to install the requirement
similar to the client you used. `virtualenv` is recommended.

Dispy can be run as deamon mode, but I recommend to use `tmux`.

Run `dispynode.py --clean -i IP --ext_ip_addr IP` to start a node.

For example:

`dispynode.py --clean -i 192.168.0.100 --ext_ip_addr 192.168.0.100`

Or you may use `python node_start_script.py` to start a node.

**Notice**: Do not directly run script in Pycharm.
Node may not be reachable due to some problem.

## Client

Client represent a computer which will request for computing resource.

`example.py` provide an example for using dispy.
