# sma.py

import csv
import datetime
import math
import sys
from collections import defaultdict
from dataclasses import dataclass

import matplotlib.pyplot as plt

weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

@dataclass
class Solution:
    date: datetime.date
    time_taken: int

    def ordinal(self) -> int:
        return self.date.toordinal()

    def week(self) -> int:
        return int(self.ordinal() / len(weekdays))

    def weekday(self) -> int:
        return self.date.weekday()

@dataclass
class Streak:
    start: Solution
    length: int = 1

def sma(window_size):
    smas_by_day = defaultdict(list)
    data_points = []
    for _ in range(max_week - min_week + 1):
        data_points.append([math.nan] * len(weekdays))
    for day, solutions in solutions_by_day.items():
        window = []
        for solution in solutions:
            window.append(solution.time_taken)
            if len(window) == window_size:
                sma = sum(window)/window_size
                smas_by_day[day].append(sma)
                data_points[solution.week() - min_week][day] = sma
                window.pop(0)

    plt.rcParams["figure.dpi"] = 240
    fig = plt.figure()
    fig.suptitle(f"Daily NYT Crossword Solve Times\n{window_size}-Day Moving Average")
    ax = fig.add_subplot()
    ax.plot(range(0, max_week - min_week + 1), data_points, label=weekdays)
    fig.legend(loc="upper right",fontsize="xx-small")
    ax.set_xlabel("Week")
    ax.set_ylabel("Seconds")
    ax.set_xlim(0, max_week - min_week + 1)
    ax.set_ylim(0, 3000)
    fig.savefig(f"sma{window_size}.png")

    return smas_by_day

def format_rank(solution: Solution, rank, recent):
    prefix = "\033[31;1m" if solution == recent else ""
    suffix = "\033[0m"    if solution == recent else ""
    return prefix + \
           f"#{(rank + 1): >3}: {solution.date.strftime('%d/%m/%y')} @ {solution.time_taken}s" + \
           suffix

reader = csv.reader(sys.stdin)

solutions: list[Solution] = []

streaks: list[Streak] = []
for datum in reader:
    date = datetime.date.fromisoformat(datum[0])
    time_taken = int(datum[1])
    solution = Solution(date, time_taken)
    solutions.append(solution)
    if len(streaks) > 0:
        most_recent = streaks[-1]

        if most_recent.start.ordinal() + most_recent.length == solution.ordinal():
            most_recent.length += 1
        else:
            streaks.append(Streak(solution))
    else:
        streaks.append(Streak(solution))

recent = solutions[-1]

solutions.sort(key=lambda d: d.date)
min_week = solutions[0].week()
max_week = solutions[-1].week()

solutions_by_day: dict[int, list[Solution]] = defaultdict(list)
for solution in solutions:
    solutions_by_day[solution.weekday()].append(solution)

print("Streaks")
print("=======")
for streak in sorted(streaks, key=lambda x: x.length, reverse=True)[:3]:
    print(f"From {streak.start.date.strftime('%d/%m/%y')} for {streak.length} day(s)")
print()

grid = []
for _ in range(len(weekdays)):
    grid.append([])
for i, day in enumerate(weekdays):
    days_solutions = solutions_by_day[i][:]
    recent = days_solutions[-1]
    days_solutions.sort(key=lambda s: s.time_taken)
    recent_rank = days_solutions.index(recent)
    grid[i].append(day + "		")
    grid[i].append("=====		")
    if recent_rank > 2:
        for j in range(0, 2):
            grid[i].append(format_rank(days_solutions[j], j, recent))
        grid[i].append("...		")
    for j in range(max(recent_rank - 2, 0),
                   min(recent_rank + 3, len(days_solutions))):
        grid[i].append(format_rank(days_solutions[j], j, recent))
    grid[i].append("...		")
    if recent_rank <= 2:
        grid[i].append("		")
        grid[i].append("		")
        grid[i].append("		")
        grid[i].append("		")
        grid[i].append("		")

print("Daily Stats")
print("===========")
max_len = max(len(grid[day]) for day in range(len(grid)))
for j in range(max_len):
    print("      | ", end="")
    for i in range(len(weekdays)):
        if j < len(grid[i]):
            print(grid[i][j], end="	")
    print()
print()

smas = {}
for window_size in sys.argv[1:]:
    window_size = int(window_size)
    smas[window_size] = sma(window_size)

print("SMA Stats")
print("=========")
for window_size in smas:
    print(f"SMA{window_size}", end=" | ")
    for i in range(len(weekdays)):
        print(f"{smas[window_size][i][-1]: >20.2f}s	", end="")
    print()

