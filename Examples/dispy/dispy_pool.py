def get_local_ip():
    import socket
    lan_ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                if not ip.startswith("127.")]
               or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close())
                    for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]])
              + ["no IP found"])[0]
    return lan_ip


class DispyPool(object):
    def __init__(self, func, nodes):
        lan_ip = get_local_ip()
        import dispy
        self.func = func
        self.cluster = dispy.JobCluster(func,
                                        ip_addr=lan_ip,
                                        ext_ip_addr=lan_ip,
                                        nodes=nodes)

    def map(self, args):
        results = []
        jobs = []
        for arg in args:
            job = self.cluster.submit(arg)
            jobs.append(job)
        for job in jobs:
            result = job()
            if job.exception is not None:
                print("exception", job.exception)
            if job.stdout != "":
                print("stdout", job.stdout)
            results.append(result)
        return results

    def test_map(self, args):
        results = []
        for arg in args:
            results.append(self.func(arg))
        return results

    def stats(self):
        self.cluster.stats()

    def close(self):
        self.cluster.close()
