"""01 描述性统计：手工计算 + pandas 验证。

运行方式:
    python 01_descriptive_stats.py
"""

import csv
from pathlib import Path

DATA = Path(__file__).parent.parent / "data" / "sample_scores.csv"


def load_scores(path: Path) -> list[float]:
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return [float(r["score"]) for r in rows]


def mean(xs):
    return sum(xs) / len(xs)


def variance(xs, sample: bool = True):
    n = len(xs)
    m = mean(xs)
    d = sum((x - m) ** 2 for x in xs)
    return d / (n - 1 if sample else n)


def median(xs):
    s = sorted(xs)
    n = len(s)
    mid = n // 2
    if n % 2:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2


if __name__ == "__main__":
    scores = load_scores(DATA)
    print(f"样本量 n        = {len(scores)}")
    print(f"均值 x̄          = {mean(scores):.2f}")
    print(f"中位数          = {median(scores):.2f}")
    print(f"样本方差 s²     = {variance(scores):.2f}")
    print(f"样本标准差 s    = {variance(scores) ** 0.5:.2f}")
    print(f"最小值 = {min(scores)}, 最大值 = {max(scores)}, 极差 = {max(scores) - min(scores)}")
