# -*- coding: utf-8 -*-
"""
============================================================
本文件学什么：循环控制 —— break / continue / else 子句 / pass
------------------------------------------------------------
运行方式：
    在 VSCode 中打开本文件，按 Ctrl+F5 运行；
    或在终端执行：python 05_循环控制.py

预计输出：
    break 提前退出、continue 跳过本次、for...else 与 while...else 的
    两种执行结果（有 break / 无 break 各演示一次）。脚本瞬间结束。
============================================================
"""

# ===== 1. break：立刻跳出整个循环 =====
# 💡 生活类比：吃包子吃到第 3 个发现是坏的，直接放下不吃了 —— 后面的也不看了。
# break 执行后，循环立刻结束，循环体剩余代码和后续迭代都不再执行。

print("--- break 演示 ---")
for i in range(1, 10):
    if i == 4:
        # 预期输出：遇到 4，吃不下啦，退出循环
        print("遇到 4，吃不下啦，退出循环")
        break                      # 整个 for 循环到此结束
    # 预期输出：吃了第 1 个包子 / 第 2 个 / 第 3 个（没有第 4 个）
    print("吃了第", i, "个包子")

# 预期输出：循环之后继续执行
print("循环之后继续执行")


# ===== 2. continue：跳过本次，继续下一次 =====
# 💡 生活类比：发传单，遇到 3 号楼直接跳过，继续发 4 号楼 —— 不结束工作。
# continue 只结束"这一轮"，循环还会继续走下去。

print("\n--- continue 演示 ---")
for floor in range(1, 6):
    if floor == 3:
        # 预期输出：3 楼没人，跳过
        print(floor, "楼没人，跳过")
        continue                   # 跳过本轮剩下的代码
    # 预期输出：给 1 楼发传单 / 2 楼 / 4 楼 / 5 楼（3 楼被跳过）
    print("给", floor, "楼发传单")

# ⚠️ 对比记忆：break 是"整个循环结束"，continue 是"只跳过这一轮"。


# ===== 3. break vs continue 对照实验 =====
# 同一份数据，两种写法，结果完全不同。

print("\n--- 对照实验 ---")
# 用 break：找到第一个就停
found = None
for num in [3, 8, 15, 22, 7]:
    if num % 2 == 0:
        found = num
        break
# 预期输出：break 找到的第一个偶数： 8
print("break 找到的第一个偶数：", found)

# 用 continue：跳过的项不算，把所有偶数都收集起来
evens = []
for num in [3, 8, 15, 22, 7]:
    if num % 2 != 0:
        continue                   # 奇数跳过，不添加
    evens.append(num)
# 预期输出：continue 收集的所有偶数： [8, 22]
print("continue 收集的所有偶数：", evens)


# ===== 4. ⭐ 循环的 else 子句：没被 break 才执行 =====
# 💡 这是 Python 特有的、很容易被忽略的语法：
#    循环正常跑完了（没遇到 break），才执行 else；
#    一旦中途被 break 打断，else 就不执行。
# 💡 类比：找钥匙 —— 把整间房都翻遍了还没找到，才说"确实没有"；
#    要是中途找到了就出门了，就不会说那句话。

print("\n--- for...else：有 break（找到目标） ---")
target = 15
for n in [3, 8, 15, 22]:
    if n == target:
        # 预期输出：找到了 15
        print("找到了", target)
        break
else:
    # 因为有 break，这句不会执行
    print("找遍了都没找到")

print("--- for...else：没有 break（没找到） ---")
target2 = 99
for n in [3, 8, 15, 22]:
    if n == target2:
        print("找到了", target2)
        break
else:
    # 预期输出：没找到 99，列表里没有它
    print("没找到", target2, "，列表里没有它")

# ⚠️ 注意：for 后没写 break 时，循环结束后一定会执行 else，
#    这点和"for 后面直接写普通代码"看起来一样，但配合 break 时行为不同。


# ===== 5. while...else：规则完全一样 =====
# 💡 else 只关心"有没有被 break 打断"，跟 for / while 无关。

print("\n--- while...else：有 break ---")
n = 1
while n <= 10:
    if n * n > 20:
        # 预期输出：第一个平方大于 20 的数是 5
        print("第一个平方大于 20 的数是", n)
        break
    n += 1
else:
    print("循环内没有找到")       # 被 break 了，不执行

print("--- while...else：没有 break ---")
n2 = 1
while n2 <= 3:
    n2 += 1
else:
    # 预期输出：循环正常走完了（n2 = 4）
    print("循环正常走完了（n2 =", str(n2) + "）")

# ✅ 实用场景：判断"是不是质数"就是 for...else 的经典用法。
print("\n--- 实战：判断质数（用 for...else） ---")
def is_prime(num):
    """判断大于 1 的整数是否为质数。"""
    if num < 2:
        return False
    for divisor in range(2, num):
        if num % divisor == 0:
            break                  # 找到因子，说明不是质数
    else:
        return True                # 一次都没 break，说明是质数
    return False

for v in [7, 9, 13, 1]:
    # 预期输出：7 -> 是质数 / 9 -> 不是质数 / 13 -> 是质数 / 1 -> 不是质数
    print(v, "->", "是质数" if is_prime(v) else "不是质数")


# ===== 6. pass：占位符，什么都不做 =====
# 💡 pass 是"空语句"，语法上需要一句代码、但暂时不想写逻辑时用它占位。
#    它不是 break，不会跳出循环。

print("\n--- pass 演示 ---")
for i in range(3):
    if i == 1:
        pass                       # 什么都不做，但语法完整（将来在这里补代码）
    # 预期输出：处理 0 / 处理 1 / 处理 2
    print("处理", i)

# pass 的常见用途：先搭框架，函数体还没想好
def todo_later():
    pass                           # 留个空壳，防止程序报语法错误

# 预期输出：占位函数调用正常，返回 None
print("占位函数调用正常，返回", todo_later())


# ===== 7. 循环控制组合实战：从列表里取前 3 个正数 =====
# 💡 场景：数据里混着负数和 0，只要前 3 个正数，凑够就停。

data = [-5, 3, 0, 7, -2, 12, 8, -9]
positives = []

for value in data:
    if value <= 0:
        continue                   # 非正数直接跳过
    positives.append(value)
    if len(positives) == 3:
        break                      # 凑够 3 个就提前收工

# 预期输出：前 3 个正数： [3, 7, 12]
print("前 3 个正数：", positives)
# 预期输出：一共只看了 6 个数据
print("一共只看了", data.index(12) + 1, "个数据")


# ---------- 小结 ----------
# 1. break：立刻跳出整个循环（后续迭代 + 循环体剩余代码都不执行）。
# 2. continue：只跳过这一轮，循环继续往下走。
# 3. ⭐ for...else / while...else：循环没被 break 才执行 else，被 break 就不执行。
# 4. else 子句最实用的场景是"查找/质数判断"：break 找因子，else 才下结论。
# 5. pass 是占位符，什么都不做，和 break 完全不同。
# 6. 实战技巧：continue 用来过滤数据，break 用来"凑够就走"，能省很多无用计算。
print("\n[05] 循环控制 学习完成 ✅")
