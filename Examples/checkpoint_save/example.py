import os
import pickle
import time


class CheckPoint(object):
    def __init__(self):
        self._state = {}

    def update(self, key, value):
        self._state.update({key: value})

    def save(self):
        with open('checkpoint.pkl', 'wb') as f:
            pickle.dump(self._state, f)

    def restore(self):
        if os.path.exists('checkpoint.pkl'):
            cmd = input('Restore checkpoint? [y/n]: ')
            if cmd in 'y' or cmd in 'Y':
                with open('checkpoint.pkl', 'rb') as f:
                    self._state = pickle.load(f)
                self.__dict__.update(self._state)
                return True
            else:
                self.clear()
        return False

    def clear(self):
        if os.path.exists('checkpoint.pkl'):
            os.remove('checkpoint.pkl')


class Project(CheckPoint):
    def __init__(self):
        super(Project, self).__init__()
        self.setup()

    def setup(self):
        if not self.restore():
            self.count = 0
            self.update('count', self.count)

    def run(self):
        while self.count < 100:
            time.sleep(0.1)
            self.count += 1
            print('count {}'.format(self.count))
            self.update('count', self.count)
            self.save()
        self.close()

    def close(self):
        self.clear()


def main():
    Project().run()


if __name__ == '__main__':
    main()
