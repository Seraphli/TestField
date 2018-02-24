import threading


class SubmitThread(threading.Thread):
    def __init__(self, cluster, arg, callback, threads, sema):
        super(SubmitThread, self).__init__()
        self.cluster = cluster
        self.arg = arg
        self.callback = callback
        self.threads = threads
        self.sema = sema
        self.daemon = True

    def run(self):
        job = self.cluster.submit(self.arg)
        result = job()
        if job.exception is not None:
            print("exception: {}".format(job.exception))
        if job.stdout != "":
            print("stdout: {}".format(job.stdout))
        self.callback(result=result)
        self.threads.remove(self)
        if self.sema:
            self.sema.release()


def get_local_ip():
    import socket
    lan_ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                if not ip.startswith("127.")]
               or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close())
                    for s in [socket.socket(socket.AF_INET,
                                            socket.SOCK_DGRAM)]][0][1]])
              + ["no IP found"])[0]
    return lan_ip


class DispyPool(object):
    """Use Dispy like mp.pool"""

    def __init__(self, func, nodes, limit=0):
        """Initialize pool object with the function
        
        Args:
            func: function needed to run
            nodes (list): list of str, containing ip addresses
            limit: if given, pool will limit the number of submit.
                This argument won't affect map.
            
        """
        lan_ip = get_local_ip()
        import dispy
        self.func = func
        self.cluster = dispy.JobCluster(func,
                                        ip_addr=lan_ip,
                                        ext_ip_addr=lan_ip,
                                        nodes=nodes)
        self.threads = []
        self.pool_sema = None
        if limit > 0:
            self.pool_sema = threading.Semaphore(limit)

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

    def submit(self, arg, callback=None):
        if callback:
            self.pool_sema.acquire()
            t = SubmitThread(self.cluster, arg, callback,
                             self.threads, self.pool_sema)
            self.threads.append(t)
            t.start()
        else:
            job = self.cluster.submit(arg)
            result = job()
            return result

    def test_submit(self, arg, callback=None):
        if callback:
            result = self.func(arg)
            callback(result)
        else:
            return self.func(arg)

    def join(self):
        self.cluster.wait()
        for t in self.threads:
            t.join()
        self.threads = []

    def close(self):
        self.cluster.close(timeout=0.1, terminate=True)
        for t in self.threads:
            t.join(0.01)
