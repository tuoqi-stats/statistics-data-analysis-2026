# -*- coding: utf-8 -*-
"""
06_常见陷阱.py —— 浮点精度、整数除法、链式比较、真值判断、共享引用

【本文件学什么】
  1. 浮点精度陷阱：0.1 + 0.2 != 0.3，以及两种正确做法
  2. 除法与取整的坑：/ 得 float、// 是向下取整、% 的负数结果
  3. 链式比较：1 < x < 10 等价于 1 < x and x < 10，且中间量只求值一次
  4. 真值判断：哪些值是假、bool("0") 为什么是 True
  5. 共享引用：x = y = [] 的坑，以及正确写法

【运行方式】
  在 VSCode 终端里执行：  python 06_常见陷阱.py

【预计输出】
  每个陷阱的"错误现象 + 正确做法"对比，1 秒内跑完，无需任何输入。
"""

# -*- coding: utf-8 -*-
# 上面这行是编码声明，保证中文在 Windows 终端里能正常显示，不用管它。

import decimal          # 用于精确小数的标准库
import math             # 用于 math.isclose

# ===== 1. 陷阱一：浮点精度 =====
# 原因：计算机用二进制存小数，0.1 和 0.2 都没法用二进制精确表示，
#       累加后会产生一个极小的误差（约 5.5e-17）。
# 类比：十进制里 1/3 = 0.333... 也写不完，二进制里 0.1 写不完，一个道理。

print("---------- 1. 浮点精度陷阱 ----------")

a, b = 0.1, 0.2

# 预期输出：0.1 + 0.2 = 0.30000000000000004
print("0.1 + 0.2 =", a + b)

# ⚠️ 直接比较会得到 False！
# 预期输出：0.1 + 0.2 == 0.3 → False
print("0.1 + 0.2 == 0.3 →", a + b == 0.3)

# 看看差了多少：是一个非常小的数
# 预期输出：差了多少：(0.1 + 0.2) - 0.3 = 5.551115123125783e-17
print("差了多少：(0.1 + 0.2) - 0.3 =", (a + b) - 0.3)

# 更多例子
# 预期输出：0.1 * 3 = 0.30000000000000004
print("0.1 * 3 =", 0.1 * 3)
# 预期输出：1.0 - 0.9 = 0.09999999999999998
print("1.0 - 0.9 =", 1.0 - 0.9)
# 预期输出：0.3 - 0.1 = 0.19999999999999998
print("0.3 - 0.1 =", 0.3 - 0.1)

print("---- 正确做法 1：round() 四舍五入到指定小数位 ----")

# round(值, 位数)：把两边都转到 2 位小数后再比较
# 预期输出：round(0.1 + 0.2, 2) = 0.3
print("round(0.1 + 0.2, 2) =", round(a + b, 2))
# 预期输出：round 后比较 → True
print("round 后比较 →", round(a + b, 2) == round(0.3, 2))

print("---- 正确做法 2：math.isclose() 判断是否足够接近 ----")

# math.isclose(x, y)：在允许的误差范围内就算相等，最推荐
# 预期输出：math.isclose(0.1 + 0.2, 0.3) → True
print("math.isclose(0.1 + 0.2, 0.3) →", math.isclose(a + b, 0.3))

# 也可以自定义容差
# 预期输出：isclose 且容差 1e-9 → True
print("isclose 且容差 1e-9 →", math.isclose(a + b, 0.3, abs_tol=1e-9))

print("---- 正确做法 3：decimal 做精确十进制运算（涉及钱务必用）----")

# Decimal 接收字符串，能精确表示 0.1 和 0.2
d1 = decimal.Decimal("0.1")
d2 = decimal.Decimal("0.2")
# 预期输出：Decimal 相加：0.3
print("Decimal 相加：", d1 + d2)
# 预期输出：Decimal 比较 → True
print("Decimal 比较 →", d1 + d2 == decimal.Decimal("0.3"))

# ⚠️ 注意：Decimal 一定要传字符串！传 float 已经把误差带进去了
# 预期输出：传 float 的 Decimal：0.1000000000000000055511151231257827021181583404541015625
print("传 float 的 Decimal：", decimal.Decimal(0.1))
# 预期输出：传 str 的 Decimal：0.1
print("传 str 的 Decimal：", decimal.Decimal("0.1"))

# 实用场景：金额计算
price_d = decimal.Decimal("19.99")
cnt_d = decimal.Decimal("3")
# 预期输出：19.99 * 3 = 59.97
print("19.99 * 3 =", price_d * cnt_d)
# 对比 float 的结果（本次运算恰好打印成 59.97，但只要金额位数变化就会出现长尾巴）
# 预期输出：19.99 * 3（float）= 59.97
print("19.99 * 3（float）=", 19.99 * 3)
# 换一个金额立刻看到尾巴
# 预期输出：0.7 * 3（float）= 2.0999999999999996
print("0.7 * 3（float）=", 0.7 * 3)

# ✅ 结论：一般计算用 float；比较用 isclose 或 round；
#          涉及金钱、科学计数用 Decimal。


# ===== 2. 陷阱二：除法与取整 =====
print("---------- 2. 除法与取整陷阱 ----------")

x, y = 7, 2

# / 永远返回浮点数，即使能整除
# 预期输出：7 / 2 = 3.5
print("7 / 2 =", x / y)
# 预期输出：6 / 2 = 3.0
print("6 / 2 =", 6 / 2)
# 预期输出：6 / 2 的类型：<class 'float'>
print("6 / 2 的类型：", type(6 / 2))

# // 是"向下取整"（floor），不是"去掉小数部分"
# 预期输出：7 // 2 = 3
print("7 // 2 =", x // y)
# 预期输出：7.0 // 2 = 3.0
print("7.0 // 2 =", 7.0 // 2)

# ⚠️ 负数时容易踩坑：向下取整取的是更小的那个整数
# 预期输出：-7 // 2 = -4     （不是 -3！）
print("-7 // 2 =", -7 // 2)
# 预期输出：-7 // 2 的真值验证：-7 / 2 = -3.5
print("-7 // 2 的真值验证：-7 / 2 =", -7 / 2)

# 如果想"向零截断"，用 math.trunc 或 int()
# 预期输出：int(-7 / 2) = -3
print("int(-7 / 2) =", int(-7 / 2))
# 预期输出：math.trunc(-7 / 2) = -3
print("math.trunc(-7 / 2) =", math.trunc(-7 / 2))

# % 取余：结果的符号跟着"除数"走（这是 Python 的特点）
# 预期输出：7 % 3 = 1
print("7 % 3 =", 7 % 3)
# 预期输出：-7 % 3 = 2      （不是 -1！）
print("-7 % 3 =", -7 % 3)
# 预期输出：7 % -3 = -2
print("7 % -3 =", 7 % -3)

# 记住这条恒等式，取余结果就永远不会错：
#   a == (a // b) * b + a % b
print("恒等式验证 -7 % 3：", (-7 // 3) * 3 + (-7 % 3), "== -7 →", (-7 // 3) * 3 + (-7 % 3) == -7)

# ✅ 结论：正数场景下 // 和 % 都很直观；遇到负数一定要小心，
#          拿不准就写测试验证恒等式。


# ===== 3. 陷阱三：链式比较 =====
# Python 允许把比较"串起来写"：1 < x < 10
# 它等价于 (1 < x) and (x < 10)，但关键区别是：
# ⚠️ 中间的 x 只会被"求值一次"！

print("---------- 3. 链式比较 ----------")

value = 5

# 预期输出：1 < 5 < 10 → True
print("1 < 5 < 10 →", 1 < value < 10)

# 等价写法，结果一样
# 预期输出：等价于 and → True
print("等价于 and →", 1 < value and value < 10)

# 边界情况：等于边界值也成立（因为是 < 不是 <=）
# 预期输出：1 < 10 < 10 → False
print("1 < 10 < 10 →", 1 < 10 < 10)
# 预期输出：1 <= 10 <= 10 → True
print("1 <= 10 <= 10 →", 1 <= 10 <= 10)

print("---- 关键：中间量只求值一次 ----")

call_count = []       # 用来记录函数被调用了几次

def get_value():
    """每次调用都会记录一次，用来验证求值次数"""
    call_count.append(1)
    return 5

print("---- 方式 A：链式比较 1 < get_value() < 10 ----")
call_count.clear()
# 预期输出：链式比较结果：True
print("链式比较结果：", 1 < get_value() < 10)
# 预期输出：get_value() 被调用了 1 次
print("get_value() 被调用了", len(call_count), "次")

print("---- 方式 B：手写 and 1 < get_value() and get_value() < 10 ----")
call_count.clear()
# 预期输出：and 写法结果：True
print("and 写法结果：", 1 < get_value() and get_value() < 10)
# 预期输出：get_value() 被调用了 2 次
print("get_value() 被调用了", len(call_count), "次")

# ✅ 结论：链式比较不仅短，而且更高效——中间表达式只算一次。
#          这在中间量是"函数调用"或"耗时计算"时非常重要。

print("---- 链式比较的其他形式 ----")

# 连续小于
# 预期输出：1 < 2 < 3 < 4 → True
print("1 < 2 < 3 < 4 →", 1 < 2 < 3 < 4)
# 预期输出：1 < 2 < 2 < 4 → False
print("1 < 2 < 2 < 4 →", 1 < 2 < 2 < 4)

# 混用比较运算符（等价于 1 < 2 and 2 != 3）
# 预期输出：1 < 2 != 3 → True
print("1 < 2 != 3 →", 1 < 2 != 3)

# 判断是否在区间内（很常用）
score = 85
# 预期输出：85 在 [60, 90) 内 → True
print("85 在 [60, 90) 内 →", 60 <= score < 90)

# 也可以和 == 串起来
# 预期输出：1 < 2 == 2 → True
print("1 < 2 == 2 →", 1 < 2 == 2)


# ===== 4. 陷阱四：真值判断 =====
# 在 if / while / and / or / not 甚至 bool() 里，
# Python 会把任何对象"翻译"成 True 或 False。
#
# 为假（falsy）的只有这几类，记住它们就行：
#   False、None、0、0.0、0j、""、[]、()、{}、set()、range(0)
# 其他一切（包括非空容器、非零数字、非空字符串）都为真。

print("---------- 4. 真值判断 ----------")

falsy_values = [False, None, 0, 0.0, 0j, "", [], (), {}, set(), range(0)]
print("---- 为假的值 ----")
for v in falsy_values:
    # 预期输出：每行形如  bool(0) → False ；注意 range(0) 会打印成 range(0, 0)
    print(f"bool({v!r}) →", bool(v))

truthy_values = [True, 1, -1, 0.1, "0", "False", " ", [0], (0,), {"a": 1}, {0}]
print("---- 为真的值 ----")
for v in truthy_values:
    # 预期输出：每行形如  bool('0') → True
    print(f"bool({v!r}) →", bool(v))

print("---- ⚠️ 最容易错的几个 ----")

# ⚠️ 坑 1：字符串 "0" 是"非空字符串"，所以是 True！
# 预期输出：bool("0") → True      （不是 False！）
print('bool("0") →', bool("0"))

# ⚠️ 坑 2：字符串 "False" 也是非空字符串，同样是 True
# 预期输出：bool("False") → True
print('bool("False") →', bool("False"))

# ⚠️ 坑 3：只有一个空格的字符串也是非空
# 预期输出：bool(" ") → True
print('bool(" ") →', bool(" "))

# ⚠️ 坑 4：[0] 是"含有一个元素的列表"，为真；空列表才为假
# 预期输出：bool([0]) → True ；bool([]) → False
print("bool([0]) →", bool([0]), "；bool([]) →", bool([]))

# ⚠️ 坑 5：None 和 0 都不等于 False，但都为假
# 预期输出：None == False → False ；bool(None) → False
print("None == False →", None == False, "；bool(None) →", bool(None))

print("---- 实用写法：用真值判断简化代码 ----")

user_input = ""
# 不推荐：if user_input != "":
# 推荐：直接把值放条件里
# 预期输出：输入为空 → True
print("输入为空 →", not user_input)

items = [1, 2, 3]
# 判断列表非空，直接写 if items: 即可
# 预期输出：列表非空 → True
print("列表非空 →", bool(items))

# 判断变量既不为 None 也有内容
name = "小明"
# 预期输出：name 有效 → True
print("name 有效 →", bool(name))

# ⚠️ 但要注意：数字 0 也是"假"，如果合法的 0 需要被当成有效值，
#    就必须显式判断 `if x is not None:`，不能用真值判断

def get_score():
    return 0     # 0 分是合法值

score_result = get_score()
# 错误做法：把 0 分当成了"没有分数"
print("用真值判断：", "有分数" if score_result else "没分数", "  ← ⚠️ 0 分被误判了")
# 正确做法：显式判断 None
print("用 is not None 判断：", "有分数" if score_result is not None else "没分数", "  ← ✅")

# ✅ 结论：真值判断很简洁，但"0 和空字符串是否为有效值"要提前想清楚。


# ===== 5. 陷阱五：x = y = [] 共享引用 =====
# 可变对象（list / dict / set）赋值时传的是"引用"，不是复制。
# x = y = [] 意味着：x 和 y 指向内存里的"同一个"列表。

print("---------- 5. 共享引用陷阱 ----------")

print("---- 错误示范：x = y = [] ----")
x = y = []              # ⚠️ 两个变量指向同一个列表
x.append("我只想加到 x")

# 预期输出：x = ['我只想加到 x']
print("x =", x)
# ⚠️ 预期输出：y = ['我只想加到 x']    （y 也被改了！）
print("y =", y)

# 用 id() 看内存地址，完全一样
# 预期输出：x 和 y 是同一个对象 → True
print("x 和 y 是同一个对象 →", id(x) == id(y))
# 预期输出：x is y → True
print("x is y →", x is y)

print("---- 正确做法 1：分成两行分别赋值 ----")
p = []
q = []                  # ✅ 各建一个新列表
p.append("只加到 p")

# 预期输出：p = ['只加到 p']
print("p =", p)
# 预期输出：q = []
print("q =", q)
# 预期输出：p 和 q 是同一个对象 → False
print("p 和 q 是同一个对象 →", id(p) == id(q))

print("---- 正确做法 2：先复制再改 ----")
origin = [1, 2, 3]
copied = origin.copy()          # 浅复制，新列表
copied.append(4)

# 预期输出：origin = [1, 2, 3]
print("origin =", origin)
# 预期输出：copied = [1, 2, 3, 4]
print("copied =", copied)

# 也可以用切片复制：[ : ]
copied2 = origin[:]
copied2.append(99)
# 预期输出：origin 仍未变：[1, 2, 3]
print("origin 仍未变：", origin)

print("---- ⚠️ 更隐蔽的坑：*= 和 += ----")
list_a = [1, 2]
list_b = list_a
list_b += [3]           # ⚠️ += 对列表是"原地修改"，所以 list_a 也变了

# 预期输出：list_a = [1, 2, 3]
print("list_a =", list_a)
# 预期输出：list_b = [1, 2, 3]
print("list_b =", list_b)

# 对比：字符串是不可变的，+= 会创建新对象，不会有这个问题
str_a = "ab"
str_b = str_a
str_b += "c"            # 字符串 += 实际是"新建字符串再绑定"
# 预期输出：str_a = ab  （没被改）
print("str_a =", str_a)
# 预期输出：str_b = abc
print("str_b =", str_b)

print("---- ⚠️ 更更隐蔽的坑：默认参数用可变对象 ----")

def add_item_bad(item, container=[]):
    """⚠️ 默认参数在函数定义时只创建一次，所有调用共用同一个列表"""
    container.append(item)
    return container

# 预期输出：第一次：['a']
print("第一次：", add_item_bad("a"))
# 预期输出：第二次：['a', 'b']   ← 上次的结果还在里面！
print("第二次：", add_item_bad("b"))

def add_item_good(item, container=None):
    """✅ 用 None 作为默认值，在函数内部新建列表"""
    if container is None:
        container = []
    container.append(item)
    return container

# 预期输出：第一次：['a']
print("第一次：", add_item_good("a"))
# 预期输出：第二次：['b']
print("第二次：", add_item_good("b"))

print("---- 何时不用担心共享引用 ----")
# 不可变对象（int / float / str / tuple）赋值不会有共享修改问题
m = n = 10
m += 1                  # 整数 += 是"新建对象再绑定"
# 预期输出：m = 11，n = 10
print(f"m = {m}，n = {n}")

# 元组本身不可变，但里面装的列表仍然可以被改（浅拷贝的另一面）
t1 = ([1],)
t2 = t1
t2[0].append(2)
# 预期输出：t1 = ([1, 2],)   ← 改里面的列表，两个变量都"看到"了
print("t1 =", t1)

# ✅ 结论：
#   1. 可变对象用 = 赋值 / 当默认参数 → 一定想清楚是不是要共享。
#   2. 想要独立副本：用 .copy()、切片 [:] 或 copy.deepcopy()。
#   3. 函数默认参数永远不要用 [] / {} / set()，用 None 代替。
#   4. 判断"是不是同一个对象"用 is，判断"值是否相等"用 ==。


# ===== 6. 陷阱速查总表 =====
print("---------- 6. 陷阱速查总表 ----------")
print("1. 0.1 + 0.2 != 0.3       → 用 round / math.isclose / decimal")
print("2. 7 / 2 得 3.5 不是 3     → 要整数用 //")
print("3. -7 // 2 得 -4 不是 -3   → // 是向下取整")
print("4. -7 % 3 得 2 不是 -1     → % 符号随除数")
print("5. 1 < x < 10            → 等价 and，但 x 只求值一次")
print("6. bool('0') 是 True      → 只有空字符串为假")
print("7. x = y = [] 共享列表     → 分成两行写")
print("8. 默认参数用 []          → 改成 None")

# ---------- 小结 ----------
# 1. 浮点数天然有误差；比较用 math.isclose 或 round；钱和科学计算用 Decimal("0.1")。
# 2. / 永远得 float；// 是向下取整（负数会"更小"）；% 的符号跟着除数走。
# 3. 链式比较 1 < x < 10 等价于 1 < x and x < 10，但中间量只求值一次，更高效。
# 4. 为假的就那几类：False / None / 0 / 0.0 / "" / 空容器；bool("0") 是 True。
# 5. 可变对象赋值是"传引用"：x = y = [] 会共享；要独立就分开写或用 .copy()。
# 6. 可变默认参数是经典大坑，永远用 None + 函数内初始化代替。
