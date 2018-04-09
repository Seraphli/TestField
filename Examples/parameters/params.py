class Param(object):
    """Parameter"""

    def __init__(self):
        self.total = -1
        self.step = 0

    def val(self):
        self.step += 1
        return


class ConstantParam(Param):
    """Constant parameter"""

    def __init__(self, c):
        super(ConstantParam, self).__init__()
        self.c = c

    def val(self):
        super(ConstantParam, self).val()
        return self.c


class LinearAnnealParam(Param):
    """Linear anneal parameter"""

    def __init__(self, initial, final, total):
        super(LinearAnnealParam, self).__init__()
        self.initial = initial
        self.final = final
        self.total = total
        self.max = max(initial, final)
        self.min = min(initial, final)
        self.decay = (self.final - self.initial) / self.total

    def val(self):
        super(LinearAnnealParam, self).val()
        return max(self.min,
                   min(self.max,
                       self.initial + self.decay * self.step))


class MultiStageParam(Param):
    def __init__(self, l_params):
        """Use list of parameter for multistage calculation

        Args:
            l_params (list of Param): List of parameter
        """
        super(MultiStageParam, self).__init__()
        self.l_params = l_params
        self.skip = 0
        self.index = 0

    def val(self):
        super(MultiStageParam, self).val()
        if self.l_params[self.index].total != -1 \
                and self.index < len(self.l_params) - 1 \
                and self.step - self.skip > self.l_params[self.index].total:
            self.skip += self.l_params[self.index].total
            self.index += 1
        return self.l_params[self.index].val()
