# -*- coding: utf-8 -*-
"""
================ 02 基本数据类型 ================

【本文件学什么】
  1. 用 type() 查看一个值是什么类型
  2. 五种最基础的类型：int / float / str / bool / None
  3. 每种类型长什么样、能做什么、有什么注意点
  4. isinstance()：判断"是不是某类型"
  5. 类型注解写法（x: int = 1）的初识

【怎么运行】
  在 VSCode 里打开本文件，直接点右上角 ▶ 运行；
  或在终端执行：
      python 02_基本数据类型.py

【预计输出】
  会依次看到 7 个分节的结果，每行 print 的结果都在代码上方用注释写明了。
  文件末尾会打印"小结"。
"""


# ===== 1. 用 type() 查看类型 =====

# 💡 变量本身没有类型，**值才有类型**。
#   type(值) 会告诉你这个值是什么类型，返回的是类型对象本身。
#   打印时用 type(x).__name__ 可以直接拿到类型的名字（如 'int'），读起来更清爽。

num = 42
print(f"  42 的类型是：{type(num).__name__}")

# 预期输出：42 的类型是：int

# ✅ 结论：不确定某个值是什么类型时，第一反应就是 type() 一下。
print("--- 1. type() 结束 ---")


# ===== 2. int：整数 =====

# int 表示整数，可以正、可以负、可以很大（Python 整数没有上限）。
count = 10
negative = -7
zero = 0
big = 123456789012345678901234567890

print(f"  count = {count}，类型 {type(count).__name__}")

# 预期输出：count = 10，类型 int
print(f"  negative = {negative}")

# 预期输出：negative = -7
print(f"  zero = {zero}")

# 预期输出：zero = 0
print(f"  超大整数 = {big}（Python 整数不溢出，这是它的优势）")

# 预期输出：超大整数 = 123456789012345678901234567890（Python 整数不溢出，这是它的优势）

# 💡 三种进制写法，值其实都是 255
print(f"  十进制 255      = {255}")
print(f"  二进制 0b11111111 = {0b11111111}")

# 预期输出：二进制 0b11111111 = 255
print(f"  十六进制 0xFF   = {0xFF}")

# 预期输出：十六进制 0xFF   = 255
print("--- 2. int 结束 ---")


# ===== 3. float：小数（浮点数） =====

# float 表示带小数点的数。注意：只要带了小数点，类型就是 float。
price = 9.9
pi = 3.14159
half_from_int = 10.0

print(f"  price = {price}，类型 {type(price).__name__}")

# 预期输出：price = 9.9，类型 float
print(f"  half_from_int = {half_from_int}，类型 {type(half_from_int).__name__}")

# 预期输出：half_from_int = 10.0，类型 float
# 💡 上面这条说明：10 是 int，10.0 是 float，写法差一个点，类型就不同。

# ⚠️ 陷阱一：浮点数不精确
#   计算机用二进制存小数，有些十进制小数表示不精确，这是所有编程语言的通病。
result = 0.1 + 0.2
print(f"  0.1 + 0.2 = {result}")

# 预期输出：0.1 + 0.2 = 0.30000000000000004
print(f"  0.1 + 0.2 == 0.3 吗？ {result == 0.3}")

# 预期输出：0.1 + 0.2 == 0.3 吗？ False
# 💡 需要精确比较小数时，通常用 round() 四舍五入，或改用整数 / Decimal。
print(f"  补救：round(0.1 + 0.2, 2) = {round(result, 2)}")

# 预期输出：补救：round(0.1 + 0.2, 2) = 0.3

# ⚠️ 陷阱二：科学计数法
small = 1.5e-3
print(f"  1.5e-3 = {small}（就是 0.0015）")

# 预期输出：1.5e-3 = 0.0015（就是 0.0015）
print("--- 3. float 结束 ---")


# ===== 4. str：字符串 =====

# str 表示文本，用**单引号 / 双引号 / 三引号**包起来，三者效果基本一样。
s1 = "双引号"
s2 = '单引号'
s3 = """三引号可以
跨多行"""

print(f"  s1 = {s1}，类型 {type(s1).__name__}")

# 预期输出：s1 = 双引号，类型 str
print(f"  s2 = {s2}")

# 预期输出：s2 = 单引号
print(f"  s3 = {s3}")

# 预期输出：s3 = 三引号可以
#                 跨多行
print(f"  s3 的长度 = {len(s3)}")

# 预期输出：s3 的长度 = 9（"三引号可以" 5 个 + 换行符 1 个 + "跨多行" 3 个 = 9）
# 💡 三引号里的换行也占 1 个字符，用 len() 亲自数一数就清楚了。

# ===== 4.1 引号嵌套与转义 =====
# 外面用双引号，里面就能直接放单引号，反之亦然。
quote1 = "他说：'你好'"
print(f"  引号嵌套 1：{quote1}")

# 预期输出：引号嵌套 1：他说：'你好'

# 也可以用反斜杠 \\ 转义
quote2 = "他说：\"你好\""
print(f"  引号嵌套 2（转义）：{quote2}")

# 预期输出：引号嵌套 2（转义）：他说："你好"

# 常见转义字符
print("  换行符 \\n 的效果 →")
print("  第一行\n  第二行")

# 预期输出：换行符 \n 的效果 →
#           第一行
#           第二行
print(f"  制表符 \\t 的效果：[a\tb]")

# 预期输出：制表符 \t 的效果：[a	b]
print(f"  反斜杠 \\\\ 的效果：[\\]")

# 预期输出：反斜杠 \\ 的效果：[\]

# ===== 4.2 f-string：把变量嵌进字符串 =====
# 字符串前面加 f，里面用 {} 就能塞变量，这是最常用的写法。
who = "小明"
age = 18
print(f"  f-string 写法：{who} 今年 {age} 岁")

# 预期输出：f-string 写法：小明 今年 18 岁

# {} 里还能直接做运算、调格式
print(f"  3 + 5 = {3 + 5}，保留两位小数 {3.14159:.2f}")

# 预期输出：3 + 5 = 8，保留两位小数 3.14
print("--- 4. str 结束 ---")


# ===== 5. bool：布尔值，只有 True / False =====

# bool 只有两个值：True 和 False，注意**首字母必须大写**。
is_student = True
is_teacher = False

print(f"  is_student = {is_student}，类型 {type(is_student).__name__}")

# 预期输出：is_student = True，类型 bool
print(f"  is_teacher = {is_teacher}")

# 预期输出：is_teacher = False

# ⚠️ 陷阱：true / false 小写会报 NameError（它们只是普通名字，没有定义）
#   is_ok = true       ← 报错 NameError: name 'true' is not defined

# 💡 冷知识：bool 其实是 int 的子类型，True 相当于 1，False 相当于 0。
print(f"  True + True = {True + True}")

# 预期输出：True + True = 2
print(f"  True * 10 = {True * 10}")

# 预期输出：True * 10 = 10
print(f"  True == 1 ？{True == 1}；False == 0 ？{False == 0}")

# 预期输出：True == 1 ？True；False == 0 ？True
print("--- 5. bool 结束 ---")


# ===== 6. None：什么都没有 =====

# None 表示"空"、"没有值"，**只有一个值，首字母大写**。
# 类比：填表格时某个格子暂时不填，就是 None。
# 它和 0、""、False 都不一样：那些是"有值"，None 是"没值"。

result = None
print(f"  result = {result}，类型 {type(result).__name__}")

# 预期输出：result = None，类型 NoneType
print(f"  None == None ？{None == None}")

# 预期输出：None == None ？True
# ⚠️ 注意下面这行：f-string 的 {} 里不能再用同一种引号，否则会解析出错。
#   所以这里先把结果算好存进变量，再放进 f-string，这是很实用的绕坑技巧。
none_eq_0 = (None == 0)
none_eq_empty_str = (None == "")
none_eq_false = (None == False)
print(f"  None == 0 ？{none_eq_0}；None == 空字符串 ？{none_eq_empty_str}；None == False ？{none_eq_false}")

# 预期输出：None == 0 ？False；None == 空字符串 ？False；None == False ？False

# 💡 判断一个值是不是 None，规范写法是用 is，而不是 ==
print(f"  result is None ？{result is None}")

# 预期输出：result is None ？True

# ⚠️ 陷阱：None 不是 "" 也不是 0。做数值运算会报错：
#   None + 1      ← TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
print("--- 6. None 结束 ---")


# ===== 7. isinstance() 与类型注解 =====

# ===== 7.1 isinstance(值, 类型)：判断是不是这个类型 =====
# 比 type(x) == int 更推荐，因为它能识别子类。
print(f"  isinstance(10, int) ？{isinstance(10, int)}")

# 预期输出：isinstance(10, int) ？True
print(f"  isinstance(10.0, int) ？{isinstance(10.0, int)}")

# 预期输出：isinstance(10.0, int) ？False
print(f"  isinstance(True, int) ？{isinstance(True, int)}（bool 是 int 的子类）")

# 预期输出：isinstance(True, int) ？True（bool 是 int 的子类）

# 第二个参数可以是"元组的多个类型"，满足一个就为 True
print(f"  isinstance(10, (int, float)) ？{isinstance(10, (int, float))}")

# 预期输出：isinstance(10, (int, float)) ？True

# ===== 7.2 类型注解：写给人和工具的提示 =====
# Python 允许在变量名后加 ": 类型" 做标注。
# ⚠️ 这只是"提示"，Python 运行时**不会强制检查**，写错了也不会报错。
student_name: str = "小明"
student_age: int = 18
print(f"  类型注解写法：{student_name}: {type(student_name).__name__}, "
      f"{student_age}: {type(student_age).__name__}")

# 预期输出：类型注解写法：小明: str, 18: int

# 演示"注解不强制"：标注成 int，实际给了字符串，运行照样通过
fake: int = "我其实是字符串"
print(f"  标注 int 但实际是：{type(fake).__name__}（注解不强制检查）")

# 预期输出：标注 int 但实际是：str（注解不强制检查）
print("--- 7. isinstance 与类型注解结束 ---")


# ---------- 小结 ----------
print("========== 本节小结 ==========")
print("  1. 变量无类型，值才有类型；type(值).__name__ 查看类型名")
print("  2. int 整数（不限大小）/ float 小数 / str 文本 / bool 真假 / None 空")
print("  3. 10 是 int，10.0 是 float，差一个点类型就不同")
print("  4. 0.1 + 0.2 != 0.3，浮点数不精确是通病")
print("  5. True/False/None 首字母必须大写")
print("  6. None 表示没值，判断用 is None")
print("  7. isinstance(x, (int, float)) 判断类型更推荐；类型注解不强制检查")
print("==============================")

# 1. 用 type(x).__name__ 查看类型名，比 type(x) 打印更清爽
# 2. int / float / str / bool / None 是五大基础类型
# 3. 浮点数不精确（0.1 + 0.2 != 0.3）
# 4. True、False、None 首字母大写；bool 是 int 的子类
# 5. None 表示"没有值"，判断时用 is None
# 6. isinstance() 判断类型，类型注解只是提示不强制
# 💡 记住一句话：拿不准类型，就 type() 一下。
