import random
import numpy as np

EPSILON = 0.01
Q_TARGET = 0.5


class Generator(object):
    def __init__(self, p=0.8):
        self.p = p

    def __next__(self):
        if random.random() < self.p:
            return 0
        else:
            return 1


class StatDataSet(object):
    def __init__(self, m=1000):
        self.m = m
        self.z_n = 0
        self._next_idx = 0
        self._size = 0
        self._data = np.zeros(self.m)

    @property
    def p(self):
        return self.z_n / self._size

    def update(self, data):
        self._next_idx = (self._next_idx + 1) % self.m
        original = self._data[self._next_idx]
        self._data[self._next_idx] = data

        if self._size == self.m:
            if data == 0:
                if original == 1:
                    self.z_n += 1
            else:
                if original == 0:
                    self.z_n -= 1
        else:
            if data == 0:
                self.z_n += 1
        self._size = min((self._size + 1), self.m)


class DataSet(object):
    def __init__(self, m=5000):
        self.m = m
        self.z_n = 0
        self.q = 0
        self._next_idx = 0
        self._size = 0
        self._data = np.zeros(self.m)
        self._stat = StatDataSet()

    def insert(self, data):
        self._next_idx = (self._next_idx + 1) % self.m
        original = self._data[self._next_idx]
        self._data[self._next_idx] = data

        if self._size == self.m:
            if data == 0:
                if original == 1:
                    self.z_n += 1
            else:
                if original == 0:
                    self.z_n -= 1
        else:
            if data == 0:
                self.z_n += 1
        self._size = min((self._size + 1), self.m)
        self.q = self.z_n / self._size

    def add(self, data):
        self._stat.update(data)
        if self.should_accept(data):
            self.insert(data)

    def should_accept(self, data):
        if self._size < self.m:
            return True
        y_l = EPSILON / self.func_q()
        y_r = (1 - EPSILON) / self.func_q()
        y = random.uniform(max(0.1, y_l + EPSILON * 0.1),
                           min(0.9, y_r - EPSILON * 0.1))
        if Q_TARGET > self.q:
            x = self.func_q() * y + EPSILON
        else:
            x = self.func_q() * y - EPSILON
        print(f'x: {x}, y: {y}')
        if data == 0:
            if random.random() < x:
                return True
        else:
            if random.random() < y:
                return True
        return False

    def func_q(self):
        return (1 - self._stat.p) / self._stat.p * self.q / (1 - self.q)


def demo():
    g = Generator()
    d = DataSet(5000)
    for _ in range(500000):
        d.add(next(g))
        print(f'q: {d.q}')


if __name__ == '__main__':
    demo()
