# -*- coding: utf-8 -*-
"""
03_逻辑运算符.py —— 本章第 3 个示例文件

本节学什么：
    1. 三个逻辑运算符：and（与）、or（或）、not（非）
    2. 真值表：谁和谁组合出什么结果
    3. ⭐ 短路求值：and 遇到假就停，or 遇到真就停（本节最重要）
    4. ⭐ 逻辑运算符返回的其实是"操作数本身"，不一定都是 True/False
    5. 哪些值算"假"（falsy），哪些值算"真"（truthy）
    6. 用逻辑运算符做"兜底赋值"和"安全取值"的实用写法

运行方式（在 VSCode 终端里）：
    python 03_逻辑运算符.py

预计输出：
    若干行 True / False / 数字 / 字符串，共 86 行左右，
    全程无报错、无等待输入。

阅读方法：
    "短路求值"和"返回操作数本身"这两节可能要多读两遍，
    先运行看输出，再回来读原理，效果最好。
"""

# ============================================================
# ===== 一、and：两个都为真，结果才为真 =====
# ============================================================
#
#   真值表（A and B）：
#   A       B       A and B
#   ------  ------  --------
#   True    True    True     ← 只有这一种情况为 True
#   True    False   False
#   False   True    False
#   False   False   False
#
# 💡 生活类比：and 就像"两个条件都得满足"。
#    "带伞 and 戴帽子"才出门 → 少带一样就不出门。

print("===== 一、and =====")

print(True and True)      # 预期输出：True
print(True and False)     # 预期输出：False
print(False and True)     # 预期输出：False
print(False and False)    # 预期输出：False

# 实际场景：判断一个人是否"既成年又有票"
age, has_ticket = 20, True
print(age >= 18 and has_ticket)     # 预期输出：True

age, has_ticket = 16, True
print(age >= 18 and has_ticket)     # 预期输出：False  （年龄不够）


# ============================================================
# ===== 二、or：只要有一个为真，结果就为真 =====
# ============================================================
#
#   真值表（A or B）：
#   A       B       A or B
#   ------  ------  --------
#   True    True    True
#   True    False   True
#   False   True    True
#   False   False   False    ← 只有这一种情况为 False
#
# 💡 生活类比：or 就像"满足其中一个就行"。
#    "带现金 or 带手机" → 有一样就能付款。

print("\n===== 二、or =====")

print(True or True)       # 预期输出：True
print(True or False)      # 预期输出：True
print(False or True)      # 预期输出：True
print(False or False)     # 预期输出：False

# 实际场景：判断是否"周末或节假日"
is_weekend, is_holiday = False, True
print(is_weekend or is_holiday)     # 预期输出：True   （今天放假）

is_weekend, is_holiday = False, False
print(is_weekend or is_holiday)     # 预期输出：False  （今天要上班）


# ============================================================
# ===== 三、not：把结果反过来 =====
# ============================================================
# not 是"取反"，真变假、假变真。它只作用于一个值。
#
#   A       not A
#   ------  -------
#   True    False
#   False   True

print("\n===== 三、not =====")

print(not True)           # 预期输出：False
print(not False)          # 预期输出：True

# 实际场景：判断"不为空"、"没有过期"
is_empty = False
print(not is_empty)       # 预期输出：True   （不空）

# 双重否定 = 肯定（not not True 就是 True）
print(not not True)       # 预期输出：True

# 💡 not 的优先级比 and / or 都高：not a and b 相当于 (not a) and b
a, b = False, True
print(not a and b)        # 预期输出：True   （(not False) and True = True）


# ============================================================
# ===== 四、⭐ 短路求值：and 和 or 的"偷懒"特性 =====
# ============================================================
# 这是本节最重要的知识点！
#
#   and：从左往右算，只要碰到一个"假"，立刻停下，返回那个假值。
#        因为无论右边是什么，结果都注定是假，所以右边根本不用算。
#
#   or：从左往右算，只要碰到一个"真"，立刻停下，返回那个真值。
#        因为无论右边是什么，结果都注定是真，所以右边也不用算。
#
# 💡 生活类比：相亲时说"有房 and 有车"。
#    一见面发现对方没房，后面的"有车"根本不用问了，直接否掉。
#    这就是短路——省时间，而且能避免不必要的麻烦。

print("\n===== 四、短路求值 =====")

# 用"函数带副作用"来证明短路确实发生了：
# 下面这个函数每次被调用都会打印一行字。
def check(name, value):
    """打印一行说明，并返回传入的 value。用来观察函数有没有被调用。"""
    print(f"  → 正在计算 {name}")
    return value

# and 短路：左边是 False，右边根本没执行（没有出现 "正在计算 B"）
print("\n[and 短路演示]")
result = check("A", False) and check("B", True)
print(result)             # 预期输出：False（且上面只有 A 那一行，没有 B）

# and 不短路：左边是 True，必须继续算右边
print("\n[and 不短路演示]")
result = check("A", True) and check("B", True)
print(result)             # 预期输出：True（A、B 两行都会打印）

# or 短路：左边是 True，右边根本没执行
print("\n[or 短路演示]")
result = check("A", True) or check("B", False)
print(result)             # 预期输出：True（上面只有 A 那一行）

# or 不短路：左边是 False，必须继续算右边
print("\n[or 不短路演示]")
result = check("A", False) or check("B", False)
print(result)             # 预期输出：False（A、B 两行都会打印）

# ✅ 结论：短路求值能省计算、还能防止报错（比如避免除以 0）
numerator, denominator = 10, 0
# 下面的 or 写法：denominator 为 0（假）时就不会去算除法，避免 ZeroDivisionError
print(denominator != 0 and numerator / denominator > 1)   # 预期输出：False（安全，不报错）
# print(numerator / denominator > 1)                      # 这行会直接报 ZeroDivisionError


# ============================================================
# ===== 五、⭐ and / or 返回的是"操作数本身" =====
# ============================================================
# 这一点初学者几乎都会意外：and 和 or 的结果不一定是True/False！
#
#   A and B  →  A 为假就返回 A，否则返回 B      （返回第一个"假"或最后一个值）
#   A or  B  →  A 为真就返回 A，否则返回 B      （返回第一个"真"或最后一个值）
#
# 记忆技巧：and 找"假"（找不到就认最后一个），or 找"真"（找不到也认最后一个）。

print("\n===== 五、返回操作数本身 =====")

# and 系列：左边假就返回左边，左边真就返回右边
print(0 and 100)          # 预期输出：0      （0 是假，返回 0）
print(1 and 100)          # 预期输出：100    （1 是真，返回右边的 100）
print("" and "hello")     # 预期输出：（空行） （空字符串是假，返回空字符串）
print("hi" and "hello")   # 预期输出：hello

# or 系列：左边真就返回左边，左边假就返回右边
print(1 or 100)           # 预期输出：1      （1 是真，返回 1）
print(0 or 100)           # 预期输出：100    （0 是假，返回右边的 100）
print("hi" or "hello")    # 预期输出：hi
print("" or "默认值")      # 预期输出：默认值

# 用 type() 确认返回的确实是操作数本身的类型，不是 bool
print(type(0 and 100))    # 预期输出：<class 'int'>
print(type("" or "默认值"))  # 预期输出：<class 'str'>

# 💡 实用写法 1：兜底默认值（空/假就用后面的）
user_input = ""
name = user_input or "匿名用户"
print(name)               # 预期输出：匿名用户

user_input = "小明"
name = user_input or "匿名用户"
print(name)               # 预期输出：小明

# 💡 实用写法 2：安全取值（真才用后面的）
count = 5
print(count and f"共 {count} 条记录")   # 预期输出：共 5 条记录

count = 0
print(count and f"共 {count} 条记录")   # 预期输出：0     （0 是假，直接返回 0）


# ============================================================
# ===== 六、什么算"真"、什么算"假" =====
# ============================================================
# Python 里任何值都能当"真假"用。规则很简单：
#   ❌ 假的（falsy）只有这几种：False、0、0.0、""（空字符串）、[]、()、{}、set()、None
#   ✅ 其他一切，包括负数、非空字符串、"0"、[0]，都算真的（truthy）
#
# 💡 记忆法：**"空"和"零"算假，其他都算真。**

print("\n===== 六、真假值（truthy / falsy） =====")

# 假的例子
print(bool(False))        # 预期输出：False
print(bool(0))            # 预期输出：False
print(bool(0.0))          # 预期输出：False
print(bool(""))           # 预期输出：False  （空字符串）
print(bool([]))           # 预期输出：False  （空列表）
print(bool({}))           # 预期输出：False  （空字典）
print(bool(None))         # 预期输出：False  （表示"什么都没有"）

# 真的例子：注意这些容易误判的
print(bool(-1))           # 预期输出：True   （负数也是真！只有 0 是假）
print(bool("0"))          # 预期输出：True   （字符串 "0" 非空，是真！）
print(bool("False"))      # 预期输出：True   （字符串 "False" 非空，是真！）
print(bool([0]))          # 预期输出：True   （列表里有元素，是真！）
print(bool(" "))          # 预期输出：True   （一个空格也是非空字符串）

# ⚠️ 新手最常见的坑：字符串 "0" 和数字 0 完全不同
if "0":
    print('"0" 在 if 里被认为是真')      # 预期输出：这一行会打印
if 0:
    print("0 在 if 里被认为是真")        # 预期输出：这一行不会打印
print("上面没有打印 '0 在 if 里被认为是真'，说明数字 0 是假")   # 预期输出：这行会打印

# 💡 所以判断"用户有没有输入"时，直接 if user_input: 比 if user_input != "": 更 Python


# ============================================================
# ===== 七、组合使用与优先级 =====
# ============================================================
# 优先级：not > and > or
# 也就是说：先算 not，再算 and，最后算 or。
# ⚠️ 和数学一样，拿不准就加括号，可读性远大于省两个字符。

print("\n===== 七、组合与优先级 =====")

# 用括号表达"是学生，且（年龄小于 12 或大于 60）"
is_student, age = True, 10
print(is_student and (age < 12 or age > 60))    # 预期输出：True

is_student, age = False, 10
print(is_student and (age < 12 or age > 60))    # 预期输出：False

# 不加括号时，and 先算：True or False and False
# 相当于 True or (False and False) = True or False = True
print(True or False and False)                  # 预期输出：True
print((True or False) and False)                # 预期输出：False  （加了括号结果就变了！）

# 典型场景：判断某数是否"不在 1~100 范围内"
n = 150
print(n < 1 or n > 100)     # 预期输出：True
print(not (1 <= n <= 100))  # 预期输出：True   （用 not + 链式比较，表达同样意思）

# ⚠️ 陷阱：不要写 "x == 1 or 2 or 3" 这种想当然的代码！
x = 5
print(x == 1 or 2 or 3)     # 预期输出：2    ← 返回了 2，不是 True/False！
# 原因：先算 x == 1 得 False，然后 False or 2 得 2（看到"真"就停，2 是真），后面的 3 根本没算。
# ✅ 正确写法：x in (1, 2, 3)   —— in 下一节讲
print(x in (1, 2, 3))       # 预期输出：False
x = 2
print(x in (1, 2, 3))       # 预期输出：True


# ---------- 小结 ----------
# 1. and 全真才真；or 有真就真；not 取反；优先级 not > and > or。
# 2. ⭐ 短路求值：and 遇假即停，or 遇真即停，后面的代码根本不会执行。
# 3. ⭐ and/or 返回的是操作数本身，不一定是 True/False，类型也跟着变。
# 4. 兜底赋值：x = 用户输入 or "默认值"；安全取值：x and f"共 {x} 条"。
# 5. 假值只有：False、0、0.0、""、[]、()、{}、set()、None；其余都是真。
# 6. ⚠️ 字符串 "0" 是真，负数也是真，"空和零"才假。
# 7. ⚠️ 别写 x == 1 or 2 or 3，要写 x in (1, 2, 3)。
