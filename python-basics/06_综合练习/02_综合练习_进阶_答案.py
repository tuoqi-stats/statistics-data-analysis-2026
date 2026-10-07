# -*- coding: utf-8 -*-
"""
本文件学什么：
    综合练习（进阶篇）参考答案 —— 与 02_综合练习_进阶.py 的 6 道题一一对应。
    重点展示「怎么把多个知识点组合成一个有用的函数」，
    每题保留【思路】注释，方便对照自己的写法。

运行方式：
    在 VSCode 里打开本文件，点右上角 ▶ 运行，
    或在终端执行：python 02_综合练习_进阶_答案.py

预计输出：
    依次打印第 1 题到第 6 题的思路和运行结果，
    包括统计字典、斐波那契数列、推导式结果、排序结果、
    九九乘法表 + 空心菱形、单词统计报表。
    全程 1 秒内结束，不需要任何输入。
"""

print("=" * 60)
print("综合练习（进阶篇）—— 参考答案")
print("=" * 60)
print()


# ============================================================
# 第 1 题：成绩统计函数
#   【思路】
#     一个函数只做一件事：接收列表 -> 返回统计字典。
#     返回字典比返回 5 个变量好用得多，调用方用 key 取就行，
#     以后想加"中位数"也只需要往字典里多塞一个键。
# ============================================================
print("-" * 60)
print("第 1 题：成绩统计函数")
print("-" * 60)
print("【思路】函数接收列表，返回一个统计字典")


def analyze_scores(scores):
    """接收分数列表，返回统计结果字典。"""
    return {
        "count": len(scores),                        # 人数
        "total": sum(scores),                        # 总分
        "average": round(sum(scores) / len(scores), 1),   # 平均分，保留 1 位
        "max": max(scores),                          # 最高分
        "min": min(scores),                          # 最低分
    }


scores = [88, 59, 92, 45, 76, 100, 61]
result = analyze_scores(scores)

print(f"人数：{result['count']}")
print(f"总分：{result['total']}")
print(f"平均分：{result['average']}")
print(f"最高分：{result['max']}")
print(f"最低分：{result['min']}")
print()


# ============================================================
# 第 2 题：递归——斐波那契与递归求和
#   【思路】
#     递归 = 把大问题拆成同样形式的小问题 + 一个能停下来的终止条件。
#     fib 有两个终止条件（n == 0 和 n == 1），因为数列的起点是两数。
#     recursive_sum 只有一个终止条件（n == 0）。
#     注意：递归深度有限（Python 默认约 1000 层），
#           所以 recursive_sum(100) 没问题，但 recursive_sum(10000) 会报错。
# ============================================================
print("-" * 60)
print("第 2 题：递归")
print("-" * 60)
print("【思路】先写终止条件，再把问题拆成更小的同类问题")


def fib(n):
    """返回斐波那契数列第 n 项：0, 1, 1, 2, 3, 5, 8, ..."""
    if n == 0:          # 终止条件 1
        return 0
    if n == 1:          # 终止条件 2
        return 1
    return fib(n - 1) + fib(n - 2)      # 拆成两个更小的问题


def recursive_sum(n):
    """用递归求 1 + 2 + ... + n"""
    if n == 0:          # 终止条件
        return 0
    return n + recursive_sum(n - 1)


fib_list = [fib(i) for i in range(11)]      # 顺便用一下推导式
print(f"fib(0) 到 fib(10) = {fib_list}")
print(f"recursive_sum(100) = {recursive_sum(100)}")

# 演示递归和循环是等价的：用循环算一遍做对照
total = 0
for i in range(1, 101):
    total += i
print(f"用 for 循环对照     = {total}（结果一致）")
print()


# ============================================================
# 第 3 题：推导式综合——筛选、变换、建字典
#   【思路】
#     推导式的通用形状：[表达式 for 变量 in 可迭代对象 if 条件]
#     字典推导式把 [] 换成 {} 并写成 键: 值
#     集合推导式也是 {}，但没有冒号，重复元素自动去重
# ============================================================
print("-" * 60)
print("第 3 题：推导式综合运用")
print("-" * 60)
print("【思路】列表推导式做筛选和变换，字典/集合推导式换一对花括号即可")

names = ["键盘", "鼠标", "显示器", "耳机", "摄像头"]
prices = [199, 89, 1299, 349, 259]

# 1. 筛选：价格 >= 200 的商品名
expensive = [n for n, p in zip(names, prices) if p >= 200]
print(f"价格 >= 200 的商品：{expensive}")

# 2. 变换：全部打 8 折，保留整数
discounted = [round(p * 0.8) for p in prices]
print(f"原价：{prices}")
print(f"8 折：{discounted}")

# 3. 字典推导式：{商品名: 价格}
price_map = {n: p for n, p in zip(names, prices)}
print(f"价格字典：{price_map}")
print(f"查一下显示器的价格：{price_map['显示器']} 元")

# 4. 集合推导式：所有价格的个位数（自动去重）
ones_digits = {p % 10 for p in prices}
print(f"价格个位数集合：{sorted(ones_digits)}")
print()


# ============================================================
# 第 4 题：可变参数 *args 与自定义排序
#   【思路】
#     *nums 把传进来的所有位置参数打包成一个元组；
#     n=3 写在 *nums 后面，是"关键字参数"，调用时必须写 n=2 这种形式；
#     sorted(..., key=lambda s: sum(s["scores"])) 告诉 Python：
#     排序时不要比较字典本身（没法比），而是比较"总分"这个数字。
# ============================================================
print("-" * 60)
print("第 4 题：*args 可变参数与自定义排序")
print("-" * 60)
print("【思路】*args 收任意个参数；sorted 的 key 告诉它按什么排")


def top_n(*nums, n=3):
    """接收任意个数字，返回最大的 n 个（从大到小）"""
    return sorted(nums, reverse=True)[:n]


def sort_students(students):
    """按总分从高到低给学生们排序"""
    return sorted(students, key=lambda s: sum(s["scores"]), reverse=True)


print(f"top_n(45, 88, 12, 99, 67, 31)          -> {top_n(45, 88, 12, 99, 67, 31)}")
print(f"top_n(45, 88, 12, 99, 67, 31, n=2)     -> {top_n(45, 88, 12, 99, 67, 31, n=2)}")
print()

students = [
    {"name": "小明", "scores": [88, 76, 90]},
    {"name": "小红", "scores": [95, 92, 98]},
    {"name": "小刚", "scores": [60, 72, 65]},
]

print("按总分排名：")
for rank, stu in enumerate(sort_students(students), start=1):
    total = sum(stu["scores"])
    print(f"  第 {rank} 名：{stu['name']}，总分 {total}")
print()


# ============================================================
# 第 5 题：嵌套循环打印图形
#   【思路】
#     九九乘法表：外层控制"行号 b"，内层只从 1 打印到 b，形成下三角。
#     空心菱形：
#       上半部分（含中间那行）共 5 行，第 i 行（i 从 0 开始）
#         左边界在第 (4 - i) 列，右边界在第 (4 + i) 列；
#         只有 j == 左边界 或 j == 右边界 时打印 *，其余打印空格。
#       下半部分把上半部分的第 0~3 行倒序再打印一遍即可。
# ============================================================
print("-" * 60)
print("第 5 题：嵌套循环打印图形")
print("-" * 60)
print("【思路】外层控制行，内层控制列，用条件判断决定这一格打什么")

print("1) 九九乘法表：")
for b in range(1, 10):
    line = ""
    for a in range(1, b + 1):
        line += f"{a}x{b}={a * b:<3}"     # :<3 表示左对齐占 3 个字符宽度
    print(line)
print()

print("2) 空心菱形：")
size = 5          # 上半部分（含中心行）的行数

# 上半部分：i 从 0 到 size-1，行宽递增
for i in range(size):
    left = size - 1 - i
    right = size - 1 + i
    line = ""
    for j in range(size * 2 - 1):         # 一共 9 列
        if j == left or j == right:
            line += "*"
        else:
            line += " "
    print(line)

# 下半部分：把上半部分去掉中心行后倒序打印
for i in range(size - 2, -1, -1):
    left = size - 1 - i
    right = size - 1 + i
    line = ""
    for j in range(size * 2 - 1):
        if j == left or j == right:
            line += "*"
        else:
            line += " "
    print(line)
print()


# ============================================================
# 第 6 题：单词统计小工具（函数组合）
#   【思路】
#     拆成三个小函数，各管一段：
#       count_words  负责"数"      -> 返回字典
#       top_words    负责"排"      -> 返回列表
#       format_report 负责"显示"    -> 只管打印
#     这样每个函数都很短，也容易单独测试。
#     排序技巧：key=lambda item: (-item[1], item[0])
#       次数取负 -> 次数多的排前面（默认是升序）；
#       次数相同时，按单词字母升序。
# ============================================================
print("-" * 60)
print("第 6 题：单词统计小工具")
print("-" * 60)
print("【思路】数词、排序、显示拆成三个小函数，各管一件事")


def count_words(text):
    """统计每个单词出现的次数，返回字典"""
    words = text.lower().split()        # 转小写 + 按空格切开
    word_count = {}
    for w in words:
        word_count[w] = word_count.get(w, 0) + 1     # get 取不到时给默认值 0
    return word_count


def top_words(word_count, n=3):
    """按次数从高到低返回前 n 个 (单词, 次数)"""
    return sorted(word_count.items(), key=lambda item: (-item[1], item[0]))[:n]


def format_report(word_count):
    """打印单词统计报表"""
    print(f"{'单词':<12}{'次数'}")
    print("-" * 20)
    for word, count in sorted(word_count.items(),
                              key=lambda item: (-item[1], item[0])):
        print(f"{word:<12}{count}")


text = (
    "the quick brown fox jumps over the lazy dog "
    "the dog barks and the fox runs away "
    "a quick brown fox is quick"
)

wc = count_words(text)
print(f"一共 {len(wc)} 个不同的单词")
print()

print(f"出现最多的 3 个单词：{top_words(wc, 3)}")
print()

print("完整报表：")
format_report(wc)
print()


print("=" * 60)
print("参考答案结束！")
print("接下来请打开 03_迷你项目_学生成绩管理.py，看看这些知识怎么组合成小软件。")
print("=" * 60)
