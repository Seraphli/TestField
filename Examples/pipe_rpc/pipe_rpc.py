import multiprocessing as mp
import uuid


class Handler(object):
    def add(self, x, y):
        return x + y

    def mul(self, x, y):
        return x * y

    def pow(self, x, y):
        return x ** y

    def __call__(self, method, *args, **kwargs):
        return getattr(self, method)(*args, **kwargs)


class RPCServer(mp.Process):
    def __init__(self):
        super(RPCServer, self).__init__()
        self.daemon = True
        self.channel = mp.Pipe(False)
        self.caller = {}
        self.handler = Handler()

    def run(self):
        while True:
            if self.channel[0].poll():
                caller_id, channel = self.channel[0].recv()
                self.caller[caller_id] = channel

            for caller_id in self.caller:
                if self.caller[caller_id][0][0].poll():
                    cmd, args, kwargs = self.caller[caller_id][0][0].recv()
                    ret = self.handler(cmd, *args, **kwargs)
                    self.caller[caller_id][1][1].send(ret)


class Client(object):
    def __init__(self, channel):
        self.caller_id = uuid.uuid4()
        self.channel = [mp.Pipe(False), mp.Pipe(False)]
        channel[1].send((self.caller_id, self.channel))

    def call(self, method, *args, **kwargs):
        self.channel[0][1].send((method, args, kwargs))
        return self.channel[1][0].recv()

    def __getattr__(self, method):
        return lambda *args, **kwargs: self.call(method, *args, **kwargs)


if __name__ == '__main__':
    import time

    server = RPCServer()
    server.start()
    client = Client(server.channel)
    st = time.time()
    for _ in range(10000):
        a = client.add(2, 3)
        b = client.pow(2, 3)
        c = client.mul(5, 2)
    print(time.time() - st)
    st = time.time()
    for _ in range(10000):
        a = 2 + 3
        b = 2 ** 3
        c = 5 * 2
    print(time.time() - st)
