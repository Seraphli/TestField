import random
import numpy as np
import matplotlib.pyplot as plt

N = 10
EPSILON = 0.01
Q_TARGET = 1 / N


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


class StatDataSet(object):
    def __init__(self, m=100 * N):
        self.m = m
        self.n = np.zeros(N, dtype=np.uint32)
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
    def __init__(self, m=5000):
        super(DataSet, self).__init__(m)
        self._stat = StatDataSet()
        self.accept = True

    def add(self, data):
        self._stat.update(data)
        self.accept = self.should_accept(data)
        if self.accept:
            self.update(data)

    def should_accept(self, data):
        if self._size < self.m:
            return True
        if self.accept:
            self.x_set, self.y_set = self.x_y_set
            self._rx = self.rx()
            self._ry = self.ry(self._rx)
        if data in self.x_set:
            if random.random() < self._rx:
                return True
        if data in self.y_set:
            if random.random() < self._ry:
                return True
        return False

    def rx(self):
        l = []
        x, y = self.x_y_set
        for i in range(N):
            _l = self.p[i] * np.sum(self._stat.p[list(y - {i})]) / \
                 self.denominator(i, x)
            l.append(_l)
        _e = EPSILON * 10
        return min(1 - _e, max(0 + _e, max(l) + _e))

    def ry(self, rx):
        l = []
        x, y = self.x_y_set
        for i in range(N):
            _l = rx * self.p[i] * np.sum(self._stat.p[list(x - {i})]) / \
                 self.denominator(i, y)
            l.append(_l)
        _e = EPSILON * 10
        return max(0 + _e, min(1 - _e, min(l) - _e))

    def denominator(self, i, s):
        d = self._stat.p[i] * (1 - self.p[i]) - self.p[i] * np.sum(
            self._stat.p[list(s - {i})])
        if d == 0:
            d += 1e-5
        return d

    @property
    def x_y_set(self):
        _p = self.p
        x = set()
        y = set()
        for i in range(N):
            if Q_TARGET > _p[i]:
                x.add(i)
            else:
                y.add(i)
        return x, y


def demo():
    g = Generator()
    d = DataSet(5000)
    loss = []
    for _ in range(500000):
        d.add(next(g))
        if d.is_full:
            _loss = np.sqrt(np.sum(np.power(d.p - np.ones(N) * Q_TARGET, 2)))
            loss.append(_loss)
            if _loss < 0.001 or _ > 15000:
                print(f'q: {d.p}')
                print(f'index: {_}')
                plt.figure()
                plt.plot(loss)
                plt.savefig('loss.png')
                plt.close()
                import pickle
                with open('loss.pkl', 'wb') as f:
                    pickle.dump(loss, f)
                break


if __name__ == '__main__':
    demo()
