import sys

def main():
    data_path = sys.argv[1]

    # TBD: may want to use a sorted list for faster sorted insertion
    data = {}

    with open(data_path) as f:
        for line in f:
            date, seconds = map(lambda x: x.strip(), line.split(','))
            data[date] = seconds

    for line in sys.stdin:
        date, seconds = map(lambda x: x.strip(), line.split(','))
        data[date] = seconds

    with open(sys.argv[1], 'w') as f:
        for date in sorted(data):
            print(f"{date},{data[date]}", file=f)

if __name__ == '__main__':
    main()

