import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--email', required=True)
    parser.add_argument('--user', required=True)
    parser.add_argument('--pass', required=True)
    parser.add_argument('--folder', required=True)
    parser.add_argument('--phone', required=True)

    return parser.parse_args()
def test_work(d):
    s = vars(d)
    for k in s:
        print(f'{k} == {s[k]}')


def main():
    args = parse_args()
    test_work(args)


if __name__ == '__main__':
    main()
