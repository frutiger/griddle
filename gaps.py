from datetime import date, timedelta
import sys

def main():
    data_path = sys.argv[1]

    # TBD: may want to use a sorted list for faster sorted insertion
    data = {}

    with open(data_path) as f:
        for line in f:
            date_str, seconds = map(lambda x: x.strip(), line.split(','))
            data[date.fromisoformat(date_str)] = seconds

    current_date = None
    for input_date in sorted(data):
        if current_date is None:
            current_date = input_date
            continue

        current_date += timedelta(1)
        while current_date != input_date:
            print(current_date)
            current_date += timedelta(1)

if __name__ == '__main__':
    main()

