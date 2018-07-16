import numpy as np


class StatDataSet(object):
    def __init__(self, m, n_class):
        self.m = m
        self.n_class = n_class
        self.n = np.zeros(self.n_class, dtype=np.uint32)
        self._next_idx = 0
        self._size = 0
        self._data = np.zeros(self.m, dtype=np.uint8)

    @property
    def p(self):
        return self.n / self._size

    @property
    def is_full(self):
        return self._size == self.m

    @staticmethod
    def convert_to_index(data):
        return int(data)

    def update(self, data):
        self._next_idx = (self._next_idx + 1) % self.m
        original = self._data[self._next_idx]
        self._data[self._next_idx] = data
        if self.is_full:
            self.n[self.convert_to_index(original)] -= 1
        self.n[self.convert_to_index(data)] += 1
        self._size = min((self._size + 1), self.m)


class DataSet(StatDataSet):
    def __init__(self, m, n_class):
        super(DataSet, self).__init__(m, n_class)
        self._stat = StatDataSet(n_class * 100, n_class)
        self.accept = True

    def add(self, data):
        self._stat.update(data)
        self.accept = self.should_accept(data)
        if self.accept:
            self.update(data)
            return True
        return False

    def should_accept(self, data):
        if self._size < self.m:
            return True
        if self.accept:
            self.x_set, self.y_set = self.x_y_set
        if data in self.x_set:
            if self.mse < 5 / self.m:
                if np.random.random() < 0.5 + self.mse:
                    return True
            else:
                if np.random.random() < 0.99:
                    return True
        if data in self.y_set:
            if self.mse < 5 / self.m:
                if np.random.random() < 0.5 + self.mse:
                    return True
            else:
                if np.random.random() < 0.01:
                    return True
        return False

    @property
    def p_target(self):
        return 1 / self.n_class

    @property
    def x_y_set(self):
        _p = self.p
        x = set()
        y = set()
        for i in range(self.n_class):
            if self.p_target > _p[i]:
                x.add(i)
            else:
                y.add(i)
        return x, y

    @property
    def mse(self):
        return np.sqrt(
            np.sum(np.power(self.p - np.ones(self.n_class) * self.p_target, 2)))


def main():
    import matplotlib.pyplot as plt
    N = 10

    def softmax(x):
        return np.exp(x) / np.sum(np.exp(x))

    class Generator(object):
        def __init__(self):
            self.random = np.random.RandomState(0)
            self.z = self.random.rand(N)
            self.p = softmax(self.z)
            self.dataset = np.arange(10)

        def __next__(self):
            return self.random.choice(self.dataset, p=self.p)

    g = Generator()
    d = DataSet(5000, N)
    loss = []
    for _ in range(500000):
        d.add(next(g))
        if d.is_full:
            loss.append(d.mse)
            if d.mse < 0.0006:
                print(f'q: {d.p}')
                print(f'index: {_}')
                break
    plt.figure()
    plt.plot(loss)
    plt.savefig('loss.png')
    plt.close()


if __name__ == '__main__':
    main()
