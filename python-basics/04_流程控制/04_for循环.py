# -*- coding: utf-8 -*-
"""
============================================================
本文件学什么：for 循环 + range()，遍历字符串、列表、字典
------------------------------------------------------------
运行方式：
    在 VSCode 中打开本文件，按 Ctrl+F5 运行；
    或在终端执行：python 04_for循环.py

预计输出：
    range 生成的各种数列、遍历字符串的每个字符、遍历列表和字典的结果、
    enumerate 带编号的输出等。脚本瞬间结束。
============================================================
"""

# ===== 1. for 循环的基本结构 =====
# 💡 生活类比：点名 —— 老师拿着名单，从头到尾把每个名字念一遍。
#    "把名单里的每个元素，依次取出来做同一件事"，就是 for 循环。
# 语法：
#     for 变量 in 可迭代对象:
#         循环体（每取到一个元素就执行一次）

for fruit in ["苹果", "香蕉", "橘子"]:
    # 预期输出：我喜欢吃 苹果 / 我喜欢吃 香蕉 / 我喜欢吃 橘子
    print("我喜欢吃", fruit)

# 💡 for 比 while 省心：不用自己写计数器、不用担心忘记 i += 1 造成的死循环。
# ⚠️ 但 for 也是靠缩进划分代码块的，冒号和缩进都不能少。


# ===== 2. range() 生成数字序列 =====
# ⚠️ 最重要的规则：range 是"左闭右开" —— 包含起点，不包含终点！

# range(n)：从 0 到 n-1，共 n 个数
nums = list(range(5))
# 预期输出：range(5) -> [0, 1, 2, 3, 4]
print("range(5) ->", nums)

# range(a, b)：从 a 到 b-1
nums2 = list(range(2, 7))
# 预期输出：range(2, 7) -> [2, 3, 4, 5, 6]
print("range(2, 7) ->", nums2)

# range(a, b, step)：带步长
nums3 = list(range(1, 10, 2))
# 预期输出：range(1, 10, 2) -> [1, 3, 5, 7, 9]
print("range(1, 10, 2) ->", nums3)

# 负数步长：倒着数
nums4 = list(range(5, 0, -1))
# 预期输出：range(5, 0, -1) -> [5, 4, 3, 2, 1]
print("range(5, 0, -1) ->", nums4)

# 💡 记忆口诀：起点包括，终点不包括，步长可正可负。


# ===== 3. for + range 的常见用法 =====
# 用法一：重复固定次数（不需要用到数字本身，用 _ 表示"不用这个变量"）
for _ in range(3):
    # 预期输出：打卡 3 次
    print("打卡")

# 用法二：用序号做计算
total = 0
for i in range(1, 101):
    total += i
# 预期输出：1~100 求和： 5050
print("1~100 求和：", total)

# 用法三：生成九九乘法表的一行（第九章）
line = []
for i in range(1, 10):
    line.append(f"9x{i}={9 * i}")
# 预期输出：9 的乘法表： ['9x1=9', '9x2=18', ..., '9x9=81']
print("9 的乘法表：", line)


# ===== 4. 遍历字符串 =====
# 💡 字符串就是一串字符，可以像列表一样挨个取出来。

word = "Python"
for ch in word:
    # 预期输出：P y t h o n（每个字符单独一行）
    print(ch)

# 统计字符串里字母 o 出现的次数
sentence = "hello world"
o_count = 0
for ch in sentence:
    if ch == "o":
        o_count += 1
# 预期输出：'hello world' 里有 2 个 o
print("'hello world' 里有", o_count, "个 o")

# 字符串反转（方法一：从后往前取）
reversed_word = ""
for ch in "abcde":
    reversed_word = ch + reversed_word   # 每次把新字符放到最前面
# 预期输出：反转结果： edcba
print("反转结果：", reversed_word)


# ===== 5. 遍历列表 =====
# 遍历列表的三种方式，各有适用场景。

scores = [88, 92, 75, 60]

# 方式一：直接取值（最常用，只需要元素时用它）
for s in scores:
    # 预期输出：分数： 88 / 92 / 75 / 60
    print("分数：", s)

# 方式二：用索引取值（既要元素，又要改列表时用它）
for idx in range(len(scores)):
    # 预期输出：第 0 个分数是 88 / 第 1 个分数是 92 ...
    print("第", idx, "个分数是", scores[idx])

# 方式三：enumerate 同时拿到索引和值（最 Pythonic，推荐）
for idx, s in enumerate(scores):
    # 预期输出：序号 1: 88 / 序号 2: 92 / 序号 3: 75 / 序号 4: 60
    print("序号", idx + 1, ":", s)

# 💡 enumerate 还可以指定起始编号：enumerate(scores, start=1)


# ===== 6. 遍历字典 =====
# 字典由"键: 值"组成，遍历时默认拿到的是"键"。

person = {"name": "小明", "age": 18, "city": "北京"}

# 默认遍历键
for key in person:
    # 预期输出：键： name / 键： age / 键： city
    print("键：", key)

# .values() 遍历值
for value in person.values():
    # 预期输出：值： 小明 / 值： 18 / 值： 北京
    print("值：", value)

# .items() 同时拿到键和值（最常用）
for key, value in person.items():
    # 预期输出：name = 小明 / age = 18 / city = 北京
    print(key, "=", value)

# ⚠️ 字典在 Python 3.7+ 是有序的（按插入顺序），但不要依赖顺序做业务逻辑。


# ===== 7. 遍历时做统计：综合小例子 =====
# 统计各科平均分、最高分

grades = {"语文": 85, "数学": 92, "英语": 78, "体育": 95}

grade_total = 0
best_subject = ""
best_score = -1          # 初始值设成比所有分数都小

for subject, score in grades.items():
    grade_total += score
    if score > best_score:
        best_score = score
        best_subject = subject

avg = grade_total / len(grades)
# 预期输出：平均分： 87.5
print("平均分：", avg)
# 预期输出：最高分科目： 体育 (95 分)
print("最高分科目：", best_subject, f"({best_score} 分)")


# ===== 8. for 与 while 怎么选 =====
# 💡 一句话原则：
#    - 知道要循环几次 / 要遍历一个容器  -> 用 for
#    - 不知道要循环几次，靠条件决定      -> 用 while
#    例如"把这个列表里的每个数平方"用 for；"一直除到商为 0"用 while。

squares = []
for v in [1, 2, 3, 4]:
    squares.append(v ** 2)
# 预期输出：平方结果： [1, 4, 9, 16]
print("平方结果：", squares)


# ---------- 小结 ----------
# 1. for 变量 in 可迭代对象: —— 挨个取出元素，取完自动结束，不会死循环。
# 2. range 是左闭右开：range(5) 是 0~4；range(1,10,2) 是 1,3,5,7,9。
# 3. 遍历列表：只要元素用直接遍历，要索引用 range(len())，两者都要用 enumerate。
# 4. 遍历字典：直接 for 拿键，.values() 拿值，.items() 同时拿键值（推荐）。
# 5. 已知次数用 for，未知次数用 while。
print("\n[04] for 循环 学习完成 ✅")
