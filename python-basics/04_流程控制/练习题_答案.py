# -*- coding: utf-8 -*-
"""
============================================================
练习题参考答案（10 道）—— Python 基础语法 · 流程控制
------------------------------------------------------------
运行方式：
    在 VSCode 中打开本文件，按 Ctrl+F5 运行；
    或在终端执行：python 练习题_答案.py

预计输出：
    每题的标准答案输出，例如 "17 是奇数"、"1~100 的和是 5050" 等。
    ⚠️ 所有循环都有明确终止条件，脚本瞬间结束，不会卡死。
============================================================
"""

print("=" * 50)
print("Python 流程控制 · 练习题参考答案")
print("=" * 50)


# ===== 第 1 题：判断奇偶 =====
# 思路：用 % 取余，余数 0 就是偶数。
print("\n--- 第 1 题：判断奇偶 ---")

num = 17
if num % 2 == 0:
    # 预期输出：17 是偶数（本题不会走到这里）
    print(num, "是偶数")
else:
    # 预期输出：17 是奇数
    print(num, "是奇数")

# 💡 也可以写成一行：print(num, "是", "偶数" if num % 2 == 0 else "奇数")


# ===== 第 2 题：成绩等级（多分支） =====
# 思路：从最严格（>= 90）往下排，命中即停。
print("\n--- 第 2 题：成绩等级 ---")

score = 76
if score >= 90:
    level = "A"
elif score >= 80:
    level = "B"
elif score >= 70:
    level = "C"          # 76 命中这里
elif score >= 60:
    level = "D"
else:
    level = "E"

# 预期输出：76 分，等级：C
print(score, "分，等级：", level)


# ===== 第 3 题：用 while 求 1~100 的和 =====
# 思路：计数器 i 从 1 走到 100，每轮累加进 total。
print("\n--- 第 3 题：while 求和 ---")

i = 1
total = 0                # 累加器初值必须是 0
while i <= 100:
    total += i
    i += 1               # ⚠️ 别忘了这一步，否则死循环
# 预期输出：1~100 的和是 5050
print("1~100 的和是", total)


# ===== 第 4 题：用 for 求列表中的最大值 =====
# 思路：假设第一个元素最大，然后逐个挑战擂主。
print("\n--- 第 4 题：for 求最大值 ---")

numbers = [45, 12, 88, 33, 67, 5]
max_value = numbers[0]        # 擂主：先让第一个元素坐上宝座
for n in numbers:
    if n > max_value:
        max_value = n         # 有人更大就换擂主
# 预期输出：列表中的最大值是 88
print("列表中的最大值是", max_value)

# 💡 内置函数 max(numbers) 能直接得到同样的结果，但手动实现能练循环思维。


# ===== 第 5 题：打印乘法表的第 7 行 =====
# 思路：固定被乘数 7，乘数从 1 到 9。
print("\n--- 第 5 题：7 的乘法表 ---")

for j in range(1, 10):
    # 预期输出：7x1=7 / 7x2=14 / ... / 7x9=63（共 9 行）
    print(f"7x{j}={7 * j}")


# ===== 第 6 题：break 找第一个能被 3 和 5 同时整除的数 =====
# 思路：用 and 组合两个条件；找到就 print + break。
print("\n--- 第 6 题：break 找数 ---")

n = 1
while n <= 100:                  # ✅ 有上限，安全
    if n % 3 == 0 and n % 5 == 0:
        # 预期输出：第一个能被 3 和 5 同时整除的数是 15
        print("第一个能被 3 和 5 同时整除的数是", n)
        break                    # 找到就走，不再继续
    n += 1


# ===== 第 7 题：continue 统计奇数 =====
# 思路：偶数直接 continue 跳过，剩下的都是奇数，计数 +1。
print("\n--- 第 7 题：continue 统计奇数 ---")

odd_count = 0
for n in range(1, 21):
    if n % 2 == 0:
        continue                 # 偶数不参与计数
    odd_count += 1
# 预期输出：1~20 中奇数个数： 10
print("1~20 中奇数个数：", odd_count)

# 💡 还有更简洁的写法：len([n for n in range(1, 21) if n % 2 != 0])


# ===== 第 8 题：for...else 判断质数 =====
# 思路：能找出因子就 break（不是质数）；一次都没 break 才进 else（是质数）。
print("\n--- 第 8 题：for...else 判断质数 ---")

num = 29
if num < 2:
    # 预期输出：1 以下的数不是质数（本题不会走到这里）
    print(num, "不是质数")
else:
    for divisor in range(2, num):
        if num % divisor == 0:
            # 找到因子，说明不是质数（本题不会走到这里）
            print(num, "不是质数")
            break
    else:
        # 预期输出：29 是质数（循环从头到尾没被 break）
        print(num, "是质数")


# ===== 第 9 题：嵌套循环打印数字三角形 =====
# 思路：外层 i 控制行数，内层从 1 打印到 i；同一行不换行用 end=" "。
print("\n--- 第 9 题：数字三角形 ---")

for i in range(1, 6):            # 第 1 行到第 5 行
    for j in range(1, i + 1):    # 第 i 行打印 1~i
        # 预期输出：1 / 1 2 / 1 2 3 / 1 2 3 4 / 1 2 3 4 5（共 5 行）
        print(j, end=" ")
    print()                      # 一行结束，换行


# ===== 第 10 题：综合 —— 统计及格人数与平均分 =====
# 思路：遍历字典的 .items()，边累加总分边数及格人数。
print("\n--- 第 10 题：统计及格人数与平均分 ---")

grades = {"语文": 85, "数学": 42, "英语": 78, "物理": 91, "化学": 60}

pass_count = 0          # 计数器：及格人数
grade_total = 0         # 累加器：总分

for subject, g in grades.items():
    grade_total += g
    if g >= 60:
        pass_count += 1

average = round(grade_total / len(grades), 1)

# 预期输出：及格人数： 4
print("及格人数：", pass_count)
# 预期输出：平均分： 71.2
print("平均分：", average)

# 💡 再进一步：可以顺便找出最高分科目
best_subject = ""
best_score = -1
for subject, g in grades.items():
    if g > best_score:
        best_score = g
        best_subject = subject
# 预期输出：最高分科目： 物理（91 分）
print("最高分科目：", best_subject, f"（{best_score} 分）")


print("\n" + "=" * 50)
print("全部参考答案输出完毕 ✅")
print("=" * 50)
