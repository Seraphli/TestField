import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Example about argparse')
    parser.add_argument('-n', type=int, required=True,
                        help='number of iterations')
    parser.add_argument('--output', type=str, default='Done!',
                        help='phase to output')
    return parser.parse_args()


def main():
    import time
    args = parse_args()
    for _ in range(args.n):
        time.sleep(0.1)
    print(args.output)


if __name__ == '__main__':
    main()
