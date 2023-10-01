import datetime
import sys
import zoneinfo

import requests

def get_user_credentials():
    uid    = int(sys.argv[1])
    cookie = sys.argv[2]

    return uid, cookie

def get_date_iso():
    if len(sys.argv) > 3:
        year  = int(sys.argv[3])
        month = int(sys.argv[4])
        day   = int(sys.argv[5])
    else:
        ny     = zoneinfo.ZoneInfo("America/New_York")
        now_ny = datetime.datetime.now(tz=ny)

        year  = now_ny.year
        month = now_ny.month
        day   = now_ny.day
        if now_ny.weekday() in (5, 6) and now_ny.hour >= 18:
            # Sat/Sun after 6 PM
            day += 1
        elif now_ny.weekday() in (0, 1, 2, 3, 4) and now_ny.hour >= 22:
            # Mon/Tue/Wed/Thu/Fri after 10 PM
            day += 1

    return '{}-{:02}-{:02}'.format(year, month, day)

def main():
    uid, cookie = get_user_credentials()
    date_iso    = get_date_iso()

    session = requests.Session()
    session.headers.update({'Cookie': cookie })

    puzzle_url = 'https://www.nytimes.com/svc/crosswords/v3/{uid}/puzzles.json'
    puzzle_params = { 'date_start': date_iso, 'date_end': date_iso }
    puzzle_data = session.get(puzzle_url.format(uid=uid),
                              params=puzzle_params).json()['results'][0]

    if puzzle_data['star'] != 'Gold':
        return

    game_url  = 'https://www.nytimes.com/svc/crosswords/v6/game/{id}.json'
    game_data = session.get(game_url.format(id=puzzle_data['puzzle_id'])).json()
    calcs = game_data['calcs']

    if 'secondsSpentSolving' not in calcs:
        return

    seconds = calcs['secondsSpentSolving']
    print(f'{date_iso},{seconds}')

if __name__ == '__main__':
    main()
