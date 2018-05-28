import os
import time
import glob


def get_timestamp():
    import datetime
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


class CheckPoint(object):
    def __init__(self, dill=False):
        if dill:
            import dill as p_tool
        else:
            import pickle as p_tool
        self._p_tool = p_tool
        self._state = {}
        self._fn = get_timestamp()
        self.update('_fn', self._fn)

    def update(self, key, value):
        self._state.update({key: value})

    def save(self):
        with open('checkpoint_' + self._fn + '.cp', 'wb') as f:
            self._p_tool.dump(self._state, f)

    def restore(self):
        cp_files = glob.glob('checkpoint_????????_??????.cp')
        cp_files = sorted(cp_files, reverse=True)
        if cp_files:
            print('Found {} checkpoint files.'.format(len(cp_files)))
            action = input('Select action ([n]ew/[r]estore/[c]lear): ')
            if action == 'n' or action == 'new':
                return False
            elif action == 'r' or action == 'restore':
                print('All checkpoint files:')
                for idx, file in enumerate(cp_files):
                    print('[{}] {}'.format(idx, file))
                index = int(input('Input the index of the file[{}-{}]: '.
                                  format(0, len(cp_files) - 1)))
                if index > len(cp_files) or index < 0:
                    print('Index out of range!')
                    return False
                with open(cp_files[index], 'rb') as f:
                    self._state = self._p_tool.load(f)
                self.__dict__.update(self._state)
                return True
            elif action == 'c' or action == 'clear':
                cmd = input('WARN: Clear all checkpoints? [y/N]')
                if cmd == 'y' or cmd == 'Y':
                    for file in cp_files:
                        if os.path.exists(file):
                            os.remove(file)
                    print('All checkpoints removed.')
                    return False
                else:
                    return False
            else:
                print('Unrecognized action!')
        return False

    def clear(self):
        if os.path.exists('checkpoint_' + self._fn + '.cp'):
            os.remove('checkpoint_' + self._fn + '.cp')


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
