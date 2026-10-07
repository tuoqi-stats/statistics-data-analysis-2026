"""
================ 04 返回值 ================

【本文件学什么】
  1. return 单个值
  2. return 多个值（本质是返回一个元组，可用拆包接收）
  3. 没有 return 时，函数返回 None
  4. 提前返回（early return）：用 return 提前结束函数
  5. 多个 return 分支 vs 单一出口的写法对比
  6. ⚠️ return 与 print 的区别

【怎么运行】
      python 04_返回值.py

【预计输出】
  依次看到 6 个分节结果，最后打印小结。
"""


# ===== 1. return 单个值 =====

# return 的作用：① 立刻结束函数 ② 把值交给调用者。
def add(a, b):
    return a + b

# 返回值需要被接收或使用，否则就"丢了"
result = add(3, 5)
print(f"  add(3, 5) 返回: {result}")

# 预期输出：add(3, 5) 返回: 8

# 返回值可以直接参与表达式计算
print(f"  add(3, 5) * 2 = {(add(3, 5)) * 2}")

# 预期输出：add(3, 5) * 2 = 16
print("--- 1. return 单个值结束 ---")


# ===== 2. return 多个值 =====

# 写法上像返回多个值，实际上 Python 把它们打包成一个"元组"返回。
def min_max(numbers):
    """返回列表中的最小值和最大值。"""
    # 这里返回了两个值，中间用逗号隔开
    return min(numbers), max(numbers)

# 方式一：用一个变量接住，得到的是元组
result_tuple = min_max([3, 1, 4, 1, 5, 9, 2, 6])
print(f"  用单个变量接收: {result_tuple}")
print(f"  接收到的类型: {type(result_tuple).__name__}")

# 预期输出：
#   用单个变量接收: (1, 9)
#   接收到的类型: tuple

# 方式二（推荐）：用"拆包"一次拿到两个变量
low, high = min_max([3, 1, 4, 1, 5, 9, 2, 6])
print(f"  用拆包接收: 最小值={low}, 最大值={high}")

# 预期输出：用拆包接收: 最小值=1, 最大值=9

# 拆包时变量个数必须和值的个数一致，否则报 ValueError：
#     too many values to unpack
print("--- 2. return 多个值结束 ---")


# ===== 3. 没有 return 时返回 None =====

def say_hi(name):
    # 这个函数只是打印，没有写 return
    print(f"    say_hi 正在打印: 你好，{name}")

# 调用它，能看到打印效果
returned_value = say_hi("小明")

# 预期输出：say_hi 正在打印: 你好，小明

# ⚠️ 重点：没写 return 的函数，返回值是 None（表示"什么都没有"），不是 0 也不是空字符串
print(f"  函数返回值: {returned_value}")
print(f"  对它做判断: returned_value is None → {returned_value is None}")

# 预期输出：
#   函数返回值: None
#   对它做判断: returned_value is None → True

# 只写 return（后面不跟值）效果一样，也是返回 None
def do_nothing():
    return

print(f"  光写 return 的返回值: {do_nothing()}")

# 预期输出：光写 return 的返回值: None
print("--- 3. 无返回值结束 ---")


# ===== 4. 提前返回：用一个 return 拦住非法输入 =====

# 这种"先处理异常情况，尽早 return"的写法叫"卫语句"，能让代码少一层缩进、更易读。
def divide(a, b):
    # 先检查除数是否为 0，是的话提前返回并告知失败
    if b == 0:
        return None       # 提前结束，下面的代码不再执行
    return a / b          # 正常情况返回商

print(f"  divide(10, 2) = {divide(10, 2)}")

# 预期输出：divide(10, 2) = 5.0
print(f"  divide(10, 0) = {divide(10, 0)}   ← 提前返回 None")

# 预期输出：divide(10, 0) = None   ← 提前返回 None

# ✅ 更推荐的写法：抛异常，让调用者明确知道出错了
def divide_strict(a, b):
    if b == 0:
        # raise 会中断程序，除非调用方用 try/except 接住
        raise ValueError("除数不能为 0")
    return a / b

try:
    print(f"  divide_strict(10, 0) = {divide_strict(10, 0)}")
except ValueError as e:
    # 这里捕获异常，保证程序不会崩
    print(f"  divide_strict(10, 0) 抛出了异常: {e}")

# 预期输出：divide_strict(10, 0) 抛出了异常: 除数不能为 0
print("--- 4. 提前返回结束 ---")


# ===== 5. 多分支 return vs 单一出口 =====

# 写法 A：多个 return 分支，逻辑直观，推荐这种。
def grade_a(score):
    if score >= 90:
        return "优秀"
    elif score >= 80:
        return "良好"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"

# 写法 B：先把结果存到变量，最后统一 return，只有一个出口。
def grade_b(score):
    # 先把 result 设好默认值，避免漏掉某种情况时变量未定义
    if score >= 90:
        result = "优秀"
    elif score >= 80:
        result = "良好"
    elif score >= 60:
        result = "及格"
    else:
        result = "不及格"
    return result

# 两种写法结果完全一致
for s in (95, 85, 70, 40):
    print(f"    {s} 分 → grade_a={grade_a(s)}, grade_b={grade_b(s)}")

# 预期输出：
#     95 分 → grade_a=优秀, grade_b=优秀
#     85 分 → grade_a=良好, grade_b=良好
#     70 分 → grade_a=及格, grade_b=及格
#     40 分 → grade_a=不及格, grade_b=不及格
print("--- 5. 多分支 return 结束 ---")


# ===== 6. ⚠️ return 和 print 的区别（很多人栽在这） =====

def add_and_print(a, b):
    # 这个函数"打印"了结果，但没有"返回"结果
    print(f"    add_and_print 内部打印: {a + b}")

def add_and_return(a, b):
    # 这个函数"返回"了结果，没有打印
    return a + b

print("  【情况一】只有 print，没有 return：")

# 调用后屏幕上有输出，但变量 x 拿到的是 None
x = add_and_print(1, 2)
print(f"    x = {x}   ← 拿到的是 None，无法继续参与计算")

# 预期输出：
#     add_and_print 内部打印: 3
#     x = None   ← 拿到的是 None，无法继续参与计算

print("  【情况二】只有 return，没有 print：")

# 屏幕上没有输出，但 y 拿到了真正的结果 3
y = add_and_return(1, 2)
print(f"    y = {y}   ← 拿到了真正的结果，可以继续计算")

# 预期输出：y = 3   ← 拿到了真正的结果，可以继续计算

# ✅ 结论：print 是"给别人看"，return 是"把结果交出来"。
#         想把结果继续用，就必须 return；只在函数里 print，外面什么都拿不到。
print("    y * 10 =", y * 10, " ← 能参与运算，说明确实拿到了值")

# 预期输出：y * 10 = 30  ← 能参与运算，说明确实拿到了值
print("--- 6. return 与 print 区别结束 ---")


# ---------- 小结 ----------
# 1. return 单值     → 结束函数并交回一个值
# 2. return 多值     → 实际是返回元组，可用 a, b = f() 拆包接收
# 3. 无 return       → 返回值是 None；光写 return 也是 None
# 4. 提前返回        → 用卫语句拦截异常输入，减少嵌套层级
# 5. 多分支 return   → 直观易读，优于"单一出口 + 临时变量"
# 6. ⚠️ print ≠ return → 要拿到结果必须 return，print 只是显示
