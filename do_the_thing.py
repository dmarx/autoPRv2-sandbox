import sys

if __name__ == '__main__':
    args = sys.argv[1:]
    print(len(args))
    for i, a in enumerate(args):
        print(a)
