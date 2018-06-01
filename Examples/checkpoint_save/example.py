import os
import time
import glob


def get_timestamp():
    import datetime
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


class CheckPoint(object):
    def __init__(self, prefix='', dill=False):
        self._cp_prefix = prefix
        if dill:
            import dill as p_tool
        else:
            import pickle as p_tool
        self._cp_p_tool = p_tool
        self._cp_state = {}
        self._cp_fn = get_timestamp()
        self.update_cp('_cp_fn', self._cp_fn)
        self._cp_intro = ''
        self.update_cp('_cp_intro', self._cp_intro)

    def update_cp(self, key, value):
        self._cp_state.update({key: value})

    def save_cp(self):
        with open(self._cp_prefix + 'checkpoint_' +
                  self._cp_fn + '.cp', 'wb') as f:
            self._cp_p_tool.dump(self._cp_state, f)

    def restore_cp(self):
        cp_files = glob.glob(self._cp_prefix + 'checkpoint_????????_??????.cp')
        cp_files = sorted(cp_files, reverse=True)
        if cp_files:
            print('Found {} checkpoint files.'.format(len(cp_files)))
            action = input('Select action ([n]ew/[r]estore/[c]lear): ')
            if action == 'n' or action == 'new':
                return False
            elif action == 'r' or action == 'restore':
                print('All checkpoint files:')
                for idx, file in enumerate(cp_files):
                    with open(file, 'rb') as f:
                        cp = self._cp_p_tool.load(f)
                    if '_cp_intro' in cp:
                        print('[{}] {} ({})'.format(idx, file, cp['_cp_intro']))
                    else:
                        print('[{}] {}'.format(idx, file))
                index = int(input('Input the index of the file[{}-{}]: '.
                                  format(0, len(cp_files) - 1)))
                if index > len(cp_files) or index < 0:
                    print('Index out of range!')
                    return False
                with open(cp_files[index], 'rb') as f:
                    self._cp_state.update(self._cp_p_tool.load(f))
                self.__dict__.update(self._cp_state)
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

    def clear_cp(self):
        if os.path.exists(self._cp_prefix + 'checkpoint_' +
                          self._cp_fn + '.cp'):
            os.remove(self._cp_prefix + 'checkpoint_' + self._cp_fn + '.cp')


class Project(CheckPoint):
    def __init__(self):
        super(Project, self).__init__()
        self._cp_intro = 'Project'
        self.update_cp('_cp_intro', self._cp_intro)
        self.setup()

    def setup(self):
        if not self.restore_cp():
            self.count = 0
            self.update_cp('count', self.count)

    def run(self):
        while self.count < 100:
            time.sleep(0.1)
            self.count += 1
            print('count {}'.format(self.count))
            self.update_cp('count', self.count)
            self.save_cp()
        self.close()

    def close(self):
        self.clear_cp()


def main():
    Project().run()


if __name__ == '__main__':
    main()
