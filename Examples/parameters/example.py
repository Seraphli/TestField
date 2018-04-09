from params import LinearAnnealParam, MultiStageParam


def main():
    test = MultiStageParam([
        LinearAnnealParam(1, 1, 10),
        LinearAnnealParam(1, 0.0001, 50)
    ])
    for i in range(70):
        print(i, test.val())


if __name__ == '__main__':
    main()
