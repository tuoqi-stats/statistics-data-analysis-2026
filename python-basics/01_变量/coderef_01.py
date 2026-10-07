# -*- coding: utf-8 -*-
"""
================ coderef_01 · 全章自检脚本 ================

【这个文件是干什么的】
  它不教你新知识，而是把本章 7 个示例文件里那些"容易被记错"的结论，
  用 assert 逐条验证一遍。全部通过会打印 "全部 PASS"。

  你学完本章后可以运行它，确认自己对结论的理解没有偏差；
  也可以把它当成"第 1 章的答案清单"来读。

【怎么运行】
  在 VSCode 里打开本文件，直接点右上角 ▶ 运行；
  或在终端执行：
      python coderef_01.py

【预计输出】
  一串 [PASS] 行，最后是 "全部 PASS"，程序正常结束（退出码 0）。
  如果哪条断言不成立，会抛 AssertionError 并显示具体是哪一条。
"""

print("========== 第 01 章 · 变量 · 结论自检 ==========\n")

passed = 0


def check(desc, condition):
    """打印一条自检结果；condition 为 False 时立刻中断并报出这条。"""
    global passed
    assert condition, f"❌ 自检失败：{desc}"
    passed += 1
    print(f"  [PASS] {desc}")


# ===== 1. 变量是标签：赋值即引用 =====

# b = a 不复制数据，两个名字指向同一个对象
tag_a = [1, 2, 3]
tag_b = tag_a
check("b = a 之后 a is b 为 True（同一个对象，没复制）", tag_a is tag_b)
tag_b.append(4)
check("通过 b 修改，a 也跟着变（共享同一个列表）", tag_a == [1, 2, 3, 4])

# 想要真的副本必须显式复制
copy_a = [1, 2, 3]
copy_b = copy_a[:]
check("切片 [:] 得到的是新对象（is 为 False）", copy_a is not copy_b)
copy_b.append(99)
check("切片副本后，改 b 不影响 a", copy_a == [1, 2, 3])


# ===== 2. 五大数据类型的名字 =====

check("42 的类型名是 int", type(42).__name__ == "int")
check("4.56 的类型名是 float", type(4.56).__name__ == "float")
check("\"你好\" 的类型名是 str", type("你好").__name__ == "str")
check("True 的类型名是 bool", type(True).__name__ == "bool")
check("None 的类型名是 NoneType", type(None).__name__ == "NoneType")
# bool 是 int 的子类，所以 isinstance(True, int) 也为 True
check("isinstance(True, int) 为 True（bool 是 int 的子类）", isinstance(True, int))


# ===== 3. 浮点数不精确 =====

check("0.1 + 0.2 == 0.3 为 False（浮点数不精确）", not ((0.1 + 0.2) == 0.3))
check("0.1 + 0.2 的 repr 是 0.30000000000000004",
      repr(0.1 + 0.2) == "0.30000000000000004")
check("round(0.1 + 0.2, 2) == 0.3 为 True", round(0.1 + 0.2, 2) == 0.3)


# ===== 4. 类型转换：int() 是截断，不是四舍五入 =====

check("int(3.9) == 3（截断）", int(3.9) == 3)
check("int(3.1) == 3（截断）", int(3.1) == 3)
check("int(-3.9) == -3（向 0 截断，不是 -4）", int(-3.9) == -3)
check("int(3.9) != round(3.9)，说明截断不等于四舍五入", int(3.9) != round(3.9))
check("int('42') + 8 == 50", int("42") + 8 == 50)
check("int(' 123 ') == 123（首尾空格自动忽略）", int(" 123 ") == 123)
check("int(float('3.5')) == 3（两步走的正确姿势）", int(float("3.5")) == 3)

# int("3.5") 必须报 ValueError，这是本章重点陷阱
try:
    int("3.5")
    raise AssertionError("❌ int('3.5') 竟然没报错")
except ValueError:
    check("int('3.5') 抛 ValueError", True)
# 💡 实测彩蛋：全角数字能被 int() 转成功
check("int('３') == 3（全角数字居然能转，实测如此）", int("３") == 3)


# ===== 5. bool() 的真假判断 =====

check("bool('') 为 False（空字符串）", bool("") is False)
check("bool(' ') 为 True（含一个空格，非空即真）", bool(" ") is True)
check("bool('0') 为 True（非空字符串，最易错）", bool("0") is True)
check("bool('False') 为 True（非空字符串，内容不算数）", bool("False") is True)
check("bool(0) 为 False", bool(0) is False)
check("bool(0.0) 为 False", bool(0.0) is False)
check("bool(-1) 为 True（负数也是真）", bool(-1) is True)
check("bool(None) 为 False", bool(None) is False)
check("bool([]) 为 False（空列表）", bool([]) is False)
check("bool([0]) 为 True（非空列表即真）", bool([0]) is True)


# ===== 6. str() 永不报错 + str 与 int 不能自动相加 =====

check("str(123) == '123'", str(123) == "123")
check("str(3.14) == '3.14'", str(3.14) == "3.14")
check("str(True) == 'True'", str(True) == "True")
check("str(None) == 'None'", str(None) == "None")

try:
    "结果：" + 100
    raise AssertionError("❌ str + int 竟然没报错")
except TypeError:
    check("'结果：' + 100 抛 TypeError（不会自动转换）", True)


# ===== 7. == 与 is 的区别 =====

eq_a = [1, 2, 3]
eq_b = [1, 2, 3]
eq_c = eq_a
check("两个内容相同的列表 == 为 True", eq_a == eq_b)
check("两个内容相同的列表 is 为 False（是两个对象）", eq_a is not eq_b)
check("贴标签得到的 c is a 为 True（同一个对象）", eq_a is eq_c)
check("None 判断用 is：[None][0] is None 为 True", [None][0] is None)


# ===== 8. 小整数缓存：范围是 -5 ~ 256 =====

check("int('256') is int('256') 为 True（边界内）", int("256") is int("256"))
check("int('100') is int('100') 为 True（区间内）", int("100") is int("100"))
check("int('257') is int('257') 为 False（超出区间）", int("257") is not int("257"))
check("int('-5') is int('-5') 为 True（下边界内）", int("-5") is int("-5"))
check("int('-6') is int('-6') 为 False（超出下边界）", int("-6") is not int("-6"))

# ⚠️ 稳定的反例：用 int() 转换拿到的值不受"常量合并"影响
check("int('1000') is int('1000') 为 False（稳定反例）",
      int("1000") is not int("1000"))

# ⚠️ 同代码块里的相同字面量会被"常量合并"，所以 is 可能为 True
literal_ns = {}
exec("lit1 = 257\nlit2 = 257\nresult = lit1 is lit2", literal_ns)
check("同代码块 a = 257; b = 257 后 a is b 为 True（常量合并，不是缓存）",
      literal_ns["result"] is True)


# ===== 9. 字符串比较一律用 == =====

# 字面量会被驻留，所以 is 可能是 True —— 但这是实现细节
str1 = "hello"
str2 = "hello"
check("字面量 'hello' is 'hello' 为 True（被驻留，别依赖）", str1 is str2)

# 起个变量名再比较，避免写 "x" is not "y" 这种会引起 SyntaxWarning 的写法
joined = "".join(["hel", "lo"])
literal = "hello"
check("运行时拼接得到的 'hello' is 字面量 'hello' 为 False（不驻留）",
      not (joined is literal))
check("但两者 == 为 True（值永远相等，这才是该依赖的）", joined == literal)


# ===== 10. 多重赋值、链式赋值、del =====

# 多重赋值与一行交换
m_a, m_b, m_c = 1, 2, 3
check("多重赋值 a, b, c = 1, 2, 3 成立", (m_a, m_b, m_c) == (1, 2, 3))
m_a, m_c = m_c, m_a
check("一行交换 a, c = c, a 之后 a=3, c=1", (m_a, m_c) == (3, 1))

# 拆包
p_x, p_y = (100, 200)
check("拆包 (100, 200) → x=100, y=200", (p_x, p_y) == (100, 200))

# 链式赋值 + 可变类型 = 共享
c1 = c2 = []
c1.append("x")
check("链式赋值 c1 = c2 = [] 后 c1 is c2 为 True（共享，危险）", c1 is c2)
check("往 c1 追加后 c2 也变了", c2 == ["x"])

# 分开写就互不影响
d1 = []
d2 = []
d1.append("x")
check("分开写 d1 = []; d2 = [] 后互不影响", d2 == [])

# del 删的是名字，不是数据
keep = "临时数据"
removed = keep
del removed
check("del 一个名字后，别的名字依然能访问到数据", keep == "临时数据")
try:
    removed  # noqa: F821  —— 故意访问已删除的名字
    raise AssertionError("❌ del 之后还能访问？")
except NameError:
    check("del 之后再访问该名字抛 NameError", True)

# 链式赋值 + 不可变类型是安全的
i1 = i2 = 0
i1 = i1 + 1
check("链式赋值给不可变值后再改其中一个，另一个不受影响", i2 == 0)


# ===== 11. 三种进制写法与 True/False 的数值行为 =====

check("二进制 0b11111111 == 255", 0b11111111 == 255)
check("十六进制 0xFF == 255", 0xFF == 255)
check("True + True == 2", True + True == 2)
check("True == 1 且 False == 0", True == 1 and False == 0)
check("1 + 2.5 的结果是 float（隐式类型提升）", isinstance(1 + 2.5, float))
check("10 / 2 的结果是 float 而非 int（除法永远返回小数）",
      isinstance(10 / 2, float) and 10 / 2 == 5.0)
check("10 // 2 的结果是 int（整除）", isinstance(10 // 2, int))


# ===== 自检结束 =====

print(f"\n========== 全部 PASS（共 {passed} 条自检） ==========")
print("说明：以上结论全部由 Python 3.13 实际运行时验证，未依赖任何猜测。")
print("如果你自己写代码时得到不同结果，多半是踩到了某条实现细节的坑 ——")
print("记住一句话：比较值用 ==，判断 None 用 is，其余情况别用 is。")
