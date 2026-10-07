# -*- coding: utf-8 -*-
"""
04_条件表达式.py —— 三元表达式 a if cond else b

【本文件学什么】
  1. 条件表达式的基本语法：值1 if 条件 else 值2
  2. 它和 if-else 语句的等价关系
  3. 嵌套写法（含括号提升可读性）
  4. 求值顺序：条件成立走左边，不成立走右边（只算一边！）
  5. 什么时候用它、什么时候别用

【运行方式】
  在 VSCode 终端里执行：  python 04_条件表达式.py

【预计输出】
  各种条件表达式的取值结果，1 秒内跑完，无需任何输入。
"""

# ===== 1. 基本语法 =====
# 语法：  值1 if 条件 else 值2
# 读法：  如果"条件"成立，整个表达式取"值1"，否则取"值2"
# 类比：  "下雨就带伞，否则带墨镜" →  伞 if 下雨 else 墨镜
#
# ⚠️ else 是必须的！没有 else 的条件表达式是语法错误。
#    下面这行是错的：  "成年" if age >= 18

print("---------- 1. 基本语法 ----------")

age = 20

# 条件 age >= 18 为 True，取左边的值
# 预期输出：年龄 20 → 成年
print(f"年龄 {age} →", "成年" if age >= 18 else "未成年")

age2 = 15
# 条件为 False，取右边的值
# 预期输出：年龄 15 → 未成年
print(f"年龄 {age2} →", "未成年" if age2 < 18 else "成年")

# 值可以是数字
score = 85
# 预期输出：是否及格：1
print("是否及格：", 1 if score >= 60 else 0)


# ===== 2. 等价于 if-else 语句 =====
# 条件表达式就是"能嵌入到别处的 if-else"，用一行代替四行。
# 但注意：if-else 语句是"做事"，条件表达式是"算值"。

print("---------- 2. 与 if-else 语句等价 ----------")

num = 7

# 写法一：if-else 语句（4 行）
if num % 2 == 0:
    result_stmt = "偶数"
else:
    result_stmt = "奇数"

# 写法二：条件表达式（1 行）
result_expr = "偶数" if num % 2 == 0 else "奇数"

# 预期输出：语句写法：奇数
print("语句写法：", result_stmt)
# 预期输出：表达式写法：奇数
print("表达式写法：", result_expr)
# 预期输出：两种写法结果相同 → True
print("两种写法结果相同 →", result_stmt == result_expr)


# ===== 3. 可以直接用在 print() 里 =====
# 这是条件表达式相对 if-else 语句的最大优势：
# 它是一个"值"，所以能塞进任何要值的地方。

print("---------- 3. 当值直接使用 ----------")

temperature = 30

# 预期输出：今天偏热
print("今天偏热" if temperature > 28 else "今天凉爽")

# 放进 f-string 的花括号里
# 预期输出：气温 30℃，体感：热
print(f"气温 {temperature}℃，体感：{'热' if temperature > 28 else '舒适'}")

# 放进列表里
# 预期输出：['甲', '甲', '乙', '乙']
results = ["甲" if i < 2 else "乙" for i in range(4)]
print(results)

# 放进函数调用的参数里
nums = [3, 9, 5]
# 预期输出：最大值：9
print("最大值：", max(nums[0], nums[1] if nums[1] > nums[2] else nums[2]))


# ===== 4. 嵌套条件表达式 =====
# 条件表达式可以嵌套，实现多分支。
# 但嵌套超过 2 层就该改成 if-elif-else 语句了，否则没人看得懂。

print("---------- 4. 嵌套写法 ----------")

point = 92

# 一层：及格 / 不及格
# 预期输出：一层判断：及格
print("一层判断：", "及格" if point >= 60 else "不及格")

# 两层嵌套：注意 else 后面接的是另一个条件表达式
# 条件：>=90 优秀，80~89 良好，其余 加油
# 预期输出：两层嵌套：优秀
level = "优秀" if point >= 90 else ("良好" if point >= 80 else "加油")
print("两层嵌套：", level)

# 同样的逻辑，加括号后一眼看出分组归属
# 预期输出：加括号版本：优秀
level2 = "优秀" if point >= 90 else ("良好" if point >= 80 else "加油")
print("加括号版本：", level2)

# 用 if-elif-else 语句写同样的逻辑，更清楚（推荐 3 分支以上时用）
if point >= 90:
    level3 = "优秀"
elif point >= 80:
    level3 = "良好"
else:
    level3 = "加油"
# 预期输出：if-elif-else 版本：优秀
print("if-elif-else 版本：", level3)

# 三层嵌套对比：不推荐，仅演示语法可行
# 预期输出：四档：A
grade = "A" if point >= 90 else ("B" if point >= 80 else ("C" if point >= 60 else "D"))
print("四档：", grade)
# ⚠️ 超过 2 层嵌套请改用 if-elif-else，可读性优先！


# ===== 5. 求值顺序：只算一边 =====
# 重要特性：条件成立时，只计算左边；不成立时，只计算右边。
# 另一边根本不会被求值。这叫"惰性求值"。

print("---------- 5. 只计算一边 ----------")

# 用一个函数来证明"某一边有没有被算过"
trace = []          # 记录哪些分支被求值过

def left_value():
    trace.append("计算了左边")
    return "左边的值"

def right_value():
    trace.append("计算了右边")
    return "右边的值"

# 先清空记录，条件为 True 时应该只算左边
trace.clear()
picked1 = left_value() if True else right_value()
# 预期输出：取到：左边的值
print("取到：", picked1)
# 预期输出：实际求值的分支：['计算了左边']
print("实际求值的分支：", trace)

# 条件为 False 时只算右边
trace.clear()
picked2 = left_value() if False else right_value()
# 预期输出：取到：右边的值
print("取到：", picked2)
# 预期输出：实际求值的分支：['计算了右边']
print("实际求值的分支：", trace)

# 实用意义：可以放心写"可能出错"的表达式
denominator = 0
# 条件保护了除法：只有分母不为 0 才做除法
# 预期输出：安全求值：无法计算
print("安全求值：", 10 / denominator if denominator != 0 else "无法计算")


# ===== 6. 条件表达式的返回值类型 =====
print("---------- 6. 两边类型可以不同 ----------")

value = 0

# 两边类型不同是允许的，Python 不检查
# 预期输出：值：0 （类型：<class 'int'>）
print("值：", value if value != 0 else 0, "（类型：{}）".format(type(value if value != 0 else 0)))

# 但类型不同会让后续代码难处理，尽量避免
mixed = "无数据" if value == 0 else value
# 预期输出：混合类型结果：无数据
print("混合类型结果：", mixed)
# 预期输出：它的类型：<class 'str'>
print("它的类型：", type(mixed))


# ===== 7. 常见实用场景 =====
print("---------- 7. 实用场景 ----------")

# 场景 1：给默认值（值为空时兜底）
user_input = ""
# 预期输出：用户名：游客
print("用户名：", user_input if user_input else "游客")

# 场景 2：限制取值范围（钳制）
raw = 120
# 预期输出：限制后：100
print("限制后：", 100 if raw > 100 else raw)

# 场景 3：多条件组合
is_weekend = True
is_sunny = False
# 预期输出：今天：宅家
print("今天：", "出游" if (is_weekend and is_sunny) else "宅家")

# 场景 4：给负数加符号显示
profit = -350
# 预期输出：盈亏：亏 350 元
print("盈亏：", f"亏 {-profit} 元" if profit < 0 else f"赚 {profit} 元")

# 场景 5：列表推导式里做筛选标记
numbers = [1, 2, 3, 4, 5]
# 预期输出：奇偶标记：['奇', '偶', '奇', '偶', '奇']
print("奇偶标记：", ["偶" if n % 2 == 0 else "奇" for n in numbers])


# ===== 8. 什么时候别用条件表达式 =====
# ⚠️ 下列情况请老老实实用 if-else 语句：
#   1. 分支里要执行多个操作（赋值、打印、调用函数等）；
#   2. 嵌套超过 2 层；
#   3. 条件本身很长、很复杂；
#   4. 只是为了少写几行（省行数不是目的，可读性才是）。

print("---------- 8. 何时不该用 ----------")

# 反例：分支里要做两件事，硬塞进条件表达式会变成这样（很丑）
x = 5
# 这种写法不推荐：为了副作用而调用函数
# print("正数" if x > 0 else "非正数")

# 正确做法：用 if-else 语句
if x > 0:
    print("x 是正数")          # 预期输出：x 是正数
else:
    print("x 不是正数")


# ===== 9. 陷阱提醒 =====
print("---------- 9. 陷阱提醒 ----------")

# ⚠️ 陷阱 1：忘了 else
# bad = "成年" if age >= 18       # SyntaxError: expected 'else' after 'if' expression

# ⚠️ 陷阱 2：条件写在中间，别和 if-else 语句搞混
# 表达式：  A if 条件 else B     ← 条件在中间，A、B 在两边
# 语句：    if 条件: ... else: ...  ← 条件在最前面

# ⚠️ 陷阱 3：嵌套时 else 的归属要看括号
p = 95
# 不写括号，else 会和最近的 if 配对，容易读错
without_paren = "优" if p >= 90 else "良" if p >= 80 else "差"
# 预期输出：不写括号：优
print("不写括号：", without_paren)

# 加上括号后分组一目了然
with_paren = "优" if p >= 90 else ("良" if p >= 80 else "差")
# 预期输出：加括号：优
print("加括号：", with_paren)
# 预期输出：两种写法结果相同 → True
print("两种写法结果相同 →", without_paren == with_paren)

# ⚠️ 陷阱 4：两个分支都会写，但只有一边被执行，别在分支里做有副作用的操作
# 例如 "记录日志() if ok else None" 这种用法，容易埋坑

# ---------- 小结 ----------
# 1. 语法：值1 if 条件 else 值2（三部分，else 必须有）。
# 2. 它等价于一个能"算出值"的 if-else，所以能放进 print()、f-string、列表里。
# 3. 求值顺序：条件为真只算左边，为假只算右边，另一边完全不求值。
# 4. 嵌套不要超过 2 层，超过就用 if-elif-else 语句，并给嵌套加括号。
# 5. 合适场景：赋默认值、范围钳制、f-string 里做小判断、推导式里做标记。
# 6. 不合适场景：分支里要执行多个操作、条件太复杂、纯粹为了少写行数。
