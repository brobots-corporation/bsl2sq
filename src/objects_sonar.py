import sys
import argparse

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('srcDir', type=str, help='Path to source directory with 1c project.')
    parser.add_argument('parsePrefix', type=str, help='Prefix for subsystems. This subsystems will be parse.')

    return parser

if __name__ == '__main__':
    parser = createParser()
    args = parser.parse_args()
    print(args.srcDir)
    print(args.parsePrefix)

