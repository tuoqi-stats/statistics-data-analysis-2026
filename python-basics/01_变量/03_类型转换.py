# -*- coding: utf-8 -*-
"""
================ 03 类型转换 ================

【本文件学什么】
  1. 为什么需要类型转换（"3" + 4 会炸）
  2. int() / float() / str() / bool() 四大转换函数
  3. ⚠️ 各类型的转换陷阱（本文件重点）
  4. 隐式转换：int 和 float 一起运算会发生什么

【怎么运行】
  在 VSCode 里打开本文件，直接点右上角 ▶ 运行；
  或在终端执行：
      python 03_类型转换.py

【预计输出】
  会依次看到 6 个分节的结果，每行 print 的结果都在代码上方用注释写明了。
  ⚠️ 本文件用 try/except 安全地演示"会报错的转换"，所以不会真的中断程序。
  文件末尾会打印"小结"。
"""


# ===== 1. 为什么需要类型转换 =====

# Python 是"强类型"语言：不同类型之间不会偷偷帮你转换。
# 下面这行如果执行会直接报错：
#   print("3" + 4)      ← TypeError: can only concatenate str (not "int") to str
# 因为 "3" 是字符串、4 是整数，字符串的 + 是"拼接"，不能拼一个整数进去。

# 💡 生活类比：把"文字"和"数字"混着算，就像把苹果和扳手相加，得先说清楚怎么算。
#   解决方式就是**显式转换**：明确告诉 Python 你要当哪一种类型来用。

print(f"  字符串拼接：{'3' + '4'}（两个字符串相加 = 拼接）")

# 预期输出：字符串拼接：34（两个字符串相加 = 拼接）
print(f"  数字相加：{3 + 4}")

# 预期输出：数字相加：7
print("--- 1. 为什么需要类型转换结束 ---")


# ===== 2. int()：转成整数 =====

# ===== 2.1 从 float 转 int：是截断不是四舍五入 =====
# ⚠️⚠️ 这是最高频的坑之一！
print(f"  int(3.9) = {int(3.9)}")

# 预期输出：int(3.9) = 3   ← 不是 4！
print(f"  int(3.1) = {int(3.1)}")

# 预期输出：int(3.1) = 3
print(f"  int(-3.9) = {int(-3.9)}")

# 预期输出：int(-3.9) = -3  ← 也是向 0 截断，不是 -4
# ✅ 结论：int() 对小数是"砍掉小数部分"，往 0 的方向取整。
#   想要四舍五入请用 round()，想要向下取整请用 math.floor()。

# ===== 2.2 从 str 转 int：字符串必须"长得像整数" =====
print(f"  int('123') = {int('123')}")

# 预期输出：int('123') = 123
print(f"  int(' 123 ') = {int(' 123 ')}（首尾空格会被自动忽略）")

# 预期输出：int(' 123 ') = 123（首尾空格会被自动忽略）
print(f"  int('-50') = {int('-50')}")

# 预期输出：int('-50') = -50

# ⚠️ 陷阱 1：带小数点的字符串，int() 直接报 ValueError！
#   int("3.5")   ← ValueError: invalid literal for int() with base 10: '3.5'
# 💡 正确姿势：先 float() 再 int()，即 int(float("3.5")) = 3
try:
    int("3.5")
except ValueError as e:
    print(f"  int('3.5') 报错了：{type(e).__name__}")

# 预期输出：int('3.5') 报错了：ValueError
print(f"  正确姿势：int(float('3.5')) = {int(float('3.5'))}")

# 预期输出：正确姿势：int(float('3.5')) = 3

# ⚠️ 陷阱 2：空字符串、字母、混杂内容都不能转
for bad in ["", "abc", "12a"]:
    try:
        int(bad)
    except ValueError:
        # 用 repr() 显示原始字符串，能看到引号和不可见的空白
        print(f"  int({bad!r}) 报错 ValueError")

# 预期输出：int('') 报错 ValueError
# 预期输出：int('abc') 报错 ValueError
# 预期输出：int('12a') 报错 ValueError

# 💡 有意思的例外（实测）：int() 能识别 Unicode 的"数字字符"，全角数字也能转成功
#   所以下面这行不会报错，反而打印出 3 —— Python 比想象中宽容一点点
print(f"  int('３') = {int('３')}   ← 全角数字居然也能转（实测）")

# 预期输出：int('３') = 3   ← 全角数字居然也能转（实测）
print("--- 2. int() 结束 ---")


# ===== 3. float()：转成小数 =====

# float() 比 int() "宽容"，因为它能接受带小数点的字符串。
print(f"  float('3.14') = {float('3.14')}")

# 预期输出：float('3.14') = 3.14
print(f"  float('3') = {float('3')}")

# 预期输出：float('3') = 3.0
print(f"  float(3) = {float(3)}，类型 {type(float(3)).__name__}")

# 预期输出：float(3) = 3.0，类型 float
print(f"  float('1e3') = {float('1e3')}（科学计数法字符串也认识）")

# 预期输出：float('1e3') = 1000.0（科学计数法字符串也认识）
print(f"  float('-0.5') = {float('-0.5')}")

# 预期输出：float('-0.5') = -0.5
print(f"  float('inf') = {float('inf')}（inf 表示无穷大）")

# 预期输出：float('inf') = inf（inf 表示无穷大）

# ⚠️ 陷阱：float() 同样不能转空串、字母、带多余内容的东西
try:
    float("3.1.4")
except ValueError as e:
    print(f"  float('3.1.4') 报错了：{type(e).__name__}")

# 预期输出：float('3.1.4') 报错了：ValueError
print("--- 3. float() 结束 ---")


# ===== 4. str()：转成字符串 =====

# str() 几乎"什么都能转"，永远不会报错，是最安全的转换。
print(f"  str(123) = {str(123)!r}（注意外面有引号，说明是字符串）")

# 预期输出：str(123) = '123'（注意外面有引号，说明是字符串）
print(f"  str(3.14) = {str(3.14)!r}")

# 预期输出：str(3.14) = '3.14'
print(f"  str(True) = {str(True)!r}")

# 预期输出：str(True) = 'True'
print(f"  str(None) = {str(None)!r}")

# 预期输出：str(None) = 'None'
print(f"  str([1, 2, 3]) = {str([1, 2, 3])!r}")

# 预期输出：str([1, 2, 3]) = '[1, 2, 3]'

# 💡 实际用途：把数字拼进文字里
# ⚠️ 注意：不用 str() 直接拼数字会报错（见第 1 节）。
#   当然更推荐 f-string，因为它自动帮你转了。
n = 100
print(f"  用 str() 拼接：{'最高分是 ' + str(n) + ' 分'}")

# 预期输出：用 str() 拼接：最高分是 100 分
print(f"  用 f-string 更省事：{'最高分是 ' + f'{n}' + ' 分'}")

# 预期输出：用 f-string 更省事：最高分是 100 分
print("--- 4. str() 结束 ---")


# ===== 5. bool()：转成布尔值（判断"真值"） =====

# bool() 的规则：**看这个东西"空不空"**。
#   空 / 零 → False；非空 / 非零 → True
# 记住口诀：⚠️ "空和零为假，其余为真"。

# ===== 5.1 数字：0 是假，其他都真 =====
print(f"  bool(0) = {bool(0)}")

# 预期输出：bool(0) = False
print(f"  bool(1) = {bool(1)}")

# 预期输出：bool(1) = True
print(f"  bool(-1) = {bool(-1)}")

# 预期输出：bool(-1) = True   ← 负数也是真！
print(f"  bool(0.0) = {bool(0.0)}")

# 预期输出：bool(0.0) = False
print(f"  bool(0.0001) = {bool(0.0001)}")

# 预期输出：bool(0.0001) = True

# ===== 5.2 字符串：空串是假，其他都真 =====
print(f"  bool('') = {bool('')}")

# 预期输出：bool('') = False
print(f"  bool(' ') = {bool(' ')}")

# 预期输出：bool(' ') = True   ← 含一个空格，非空即真！
print(f"  bool('0') = {bool('0')}")

# 预期输出：bool('0') = True   ← ⚠️⚠️ 最容易错的！字符串 '0' 是**非空字符串**，为真
print(f"  bool('False') = {bool('False')}")

# 预期输出：bool('False') = True   ← ⚠️ 内容写着 False，但它是非空字符串，仍为真
# ✅ 结论：判断字符串真值，只看"长不长为空"，**完全不看内容是什么**。

# ===== 5.3 None 和容器：None 和空容器是假 =====
print(f"  bool(None) = {bool(None)}")

# 预期输出：bool(None) = False
print(f"  bool([]) = {bool([])}（空列表）")

# 预期输出：bool([]) = False（空列表）
print(f"  bool([0]) = {bool([0])}（含一个元素的列表，非空即真）")

# 预期输出：bool([0]) = True（含一个元素的列表，非空即真）
empty_dict = {}
print(f"  bool(空字典) = {bool(empty_dict)}（空字典）")

# 预期输出：bool(空字典) = False（空字典）

# ===== 5.4 实用场景：用真值做判断 =====
# 这是 Python 里非常常见的写法：直接 if 一个变量，不用写 == 0 或 != ""
name = ""
if not name:
    print("  name 为空，提示用户输入（这就是 if not name 的用法）")

# 预期输出：name 为空，提示用户输入（这就是 if not name 的用法）
print("--- 5. bool() 结束 ---")


# ===== 6. 隐式转换：不写转换函数时的自动行为 =====

# ===== 6.1 int 和 float 混算，结果自动变 float =====
# 这叫"隐式转换"或"类型提升"，Python 自动把 int 提升为 float 再算。
result = 1 + 2.5
print(f"  1 + 2.5 = {result}，类型 {type(result).__name__}")

# 预期输出：1 + 2.5 = 3.5，类型 float
print(f"  10 / 2 = {10 / 2}，类型 {type(10 / 2).__name__}")

# 预期输出：10 / 2 = 5.0，类型 float   ← ⚠️ 除法 / 永远返回 float，即使整除！
print(f"  10 // 2 = {10 // 2}，类型 {type(10 // 2).__name__}")

# 预期输出：10 // 2 = 5，类型 int   ← 想得到整数商用 //
print(f"  7 % 2 = {7 % 2}（取余）")

# 预期输出：7 % 2 = 1（取余）

# ===== 6.2 str 和数字不会自动转换 =====
# Python 的原则：宁可报错，也不猜你的意图。
try:
    "结果：" + 100
except TypeError as e:
    print(f"  '结果：' + 100 报错了：{type(e).__name__}（str 和 int 不能自动合并）")

# 预期输出：'结果：' + 100 报错了：TypeError（str 和 int 不能自动合并）
print(f"  str(100) 手动转换后：{'结果：' + str(100)}")

# 预期输出：str(100) 手动转换后：结果：100

# ===== 6.3 bool 参与运算会变成 int =====
print(f"  True + 1 = {True + 1}（True 当作 1）")

# 预期输出：True + 1 = 2（True 当作 1）
print(f"  False + 1 = {False + 1}（False 当作 0）")

# 预期输出：False + 1 = 1（False 当作 0）
print("--- 6. 隐式转换结束 ---")


# ---------- 小结 ----------
print("========== 本节小结 ==========")
print("  1. Python 是强类型：'3' + 4 会报错，必须先显式转换")
print("  2. int(3.9) = 3，是截断不是四舍五入；int('3.5') 会 ValueError")
print("  3. float('3.14') 可用；float(3) = 3.0")
print("  4. str() 什么都能转，最安全")
print("  5. bool() 规则：空和零为假，其余为真；bool('0') 和 bool('False') 都是 True")
print("  6. 隐式转换：int 和 float 混算变 float；/ 永远返回 float")
print("==============================")

# 1. Python 是强类型语言，不同类型不自动混合运算
# 2. int()：小数是截断（int(3.9)==3），字符串必须像整数，"3.5" 会报错
# 3. float()：接受 "3.14"、"1e3" 等；float(3) 得到 3.0
# 4. str()：万能且安全，数字拼字符串必用它或 f-string
# 5. bool()：空和零为假，其余为真；⚠️ bool("0") 是 True（非空字符串）
# 6. 隐式转换：int + float → float；除法 / 结果永远是 float
# 💡 记住一句话：拿不准就用 try 试一下，或者先 type() 看看。
