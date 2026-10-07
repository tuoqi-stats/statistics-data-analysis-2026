# -*- coding: utf-8 -*-
"""
================ 04 可变与不可变 ================

【本文件学什么】
  1. 不可变类型：改不了，只能"换一个新的"
  2. 可变类型：可以在原地修改内容
  3. id()：看对象的"身份证号"（内存地址）
  4. is 与 == 的区别（本文件重点）
  5. 小整数缓存与字符串驻留：为什么有的 is 是 True 有的是 False

【怎么运行】
  在 VSCode 里打开本文件，直接点右上角 ▶ 运行；
  或在终端执行：
      python 04_可变与不可变.py

【预计输出】
  会依次看到 6 个分节的结果。
  ⚠️ 注意：id() 输出的具体数字每次运行都不一样，属正常现象，
     你要看的是"两次 id 是否相同"，而不是具体数字是多少。
  文件末尾会打印"小结"。
"""


# ===== 1. 什么是"可变"与"不可变" =====

# 💡 生活类比：
#   不可变类型像"刻好字的石碑"——想改内容，只能重新刻一块新的带走。
#   可变类型像"白板"——笔一擦，内容就在原地变了，白板还是那块白板。
#
# 常见分类（先记住这四类就够用）：
#   不可变：int、float、str、bool、None、tuple
#   可变：  list、dict、set

print("  ---- 不可变类型示例：str ----")
s = "abc"
print(f"  修改前 s = {s}，id = {id(s)}")

# 用 += 拼接后，s 其实指向了一个"新的"字符串对象
s = s + "d"
print(f"  修改后 s = {s}，id = {id(s)}   ← id 变了，说明换了新对象")

# ✅ 结论：字符串不能原地修改，所谓"修改"其实是创建新字符串再重新绑定。

print("  ---- 可变类型示例：list ----")
nums = [1, 2, 3]
print(f"  修改前 nums = {nums}，id = {id(nums)}")

# append 是"就地修改"，会在原对象上追加元素
nums.append(4)
print(f"  修改后 nums = {nums}，id = {id(nums)}   ← id 没变，还是同一个对象")

# ✅ 结论：列表可以原地修改，改完后 id 保持一致。
print("--- 1. 什么是可变与不可变结束 ---")


# ===== 2. id()：对象的身份证号 =====

# id(对象) 返回这个对象在内存中的唯一编号（CPython 里就是内存地址）。
# ⚠️ 一旦对象被回收，这个编号可能被后来者复用，所以不要把它当持久化的标识。

x = 100
y = x
print(f"  x = {x}, id(x) = {id(x)}")
print(f"  y = {y}, id(y) = {id(y)}")
print(f"  x is y ？{x is y}   ← 同一个对象，id 相同")

# ✅ 结论：y = x 只是给同一个对象又贴了一张标签，没有复制数据。
print("--- 2. id() 结束 ---")


# ===== 3. is 与 == 的区别（核心！） =====

# == 比较的是"值是否相等"（内容一样就算）
# is 比较的是"是不是同一个对象"（身份证号相同才算）

list_a = [1, 2, 3]
list_b = [1, 2, 3]
list_c = list_a          # 贴标签，不是复制

print(f"  list_a = {list_a}")
print(f"  list_b = {list_b}（新建的另一个列表）")
print(f"  list_c = {list_c}（list_c 指向 list_a）")
print()

# 值相等：三个列表内容完全一样
print(f"  list_a == list_b ？{list_a == list_b}   ← 内容相等")

# 但 a 和 b 是两个不同的对象
print(f"  list_a is list_b ？{list_a is list_b}   ← 不同的对象")

# c 就是 a 本身
print(f"  list_a is list_c ？{list_a is list_c}   ← 同一个对象")
print()

# ✅ 记忆口诀：
#   == 问"你们长得一样吗？"
#   is 问"你们是同一个人吗？"

# ⚠️ 陷阱：用 is 比较值
print(f"  [1,2,3] == [1,2,3] ？{[1, 2, 3] == [1, 2, 3]}")
print(f"  [1,2,3] is [1,2,3] ？{[1, 2, 3] is [1, 2, 3]}   ← ⚠️ 别用 is 比内容！")
print()

# 💡 那什么时候该用 is？只有一个标准答案：判断 None。
value = None
print(f"  value is None ？{value is None}   ← ✅ 这才是 is 的正确用法")
print(f"  推荐写法：if value is None: ...")
print("--- 3. is 与 == 结束 ---")


# ===== 4. 小整数缓存：为什么 int("256") is int("256") 是 True =====

# 💡 Python 为了省内存，会把 -5 到 256 之间的整数**提前创建好并一直保留**。
#   这叫"小整数缓存"。所以这个范围内的同一个数，每次拿到的是同一个对象。

n1 = int("100")
n2 = int("100")
print(f"  int('100') is int('100') ？{n1 is n2}   ← 100 在缓存区间内，是同一个对象")

# ⚠️ 但 257 超出 -5 ~ 256 的范围，就老老实实每次都新建一个对象
big1 = int("257")
big2 = int("257")
print(f"  int('257') is int('257') ？{big1 is big2}   ← 257 超出缓存区间，是新对象")

# 小整数缓存的下边界也一样
neg_in = int("-5")
neg_in2 = int("-5")
print(f"  int('-5') is int('-5') ？{neg_in is neg_in2}   ← -5 在缓存区间内")

neg_out = int("-6")
neg_out2 = int("-6")
print(f"  int('-6') is int('-6') ？{neg_out is neg_out2}   ← -6 超出缓存区间")

# ✅ 结论：缓存范围是 -5 ~ 256（含两端）。
print()

# ⚠️⚠️ 极其重要的提醒：
#   千万不要写依赖 is 结果的代码！下面两个值虽然都等于 256 或 257，
#   但"是不是同一个对象"是实现细节，不同 Python 版本 / 不同执行环境都可能不同。
#   ✅ 比较数值请永远用 ==。

# ⚠️ 演示一个"看起来矛盾"的现象：两个 1000 明明超出缓存范围，is 竟然还是 True
#   原因：编译时同一个代码块里的相同字面量会被合并成同一个常量对象（常量合并），
#   但这是编译期行为，必须"写死在同一段代码里"才生效。
#   下面故意用 exec 把它包起来，如果直接写一句 print(lit1 is lit2)，
#   Python 编译期就会把整个表达式直接优化成常量 True，演示不出"合并"这回事。
code = "lit1 = 1000\nlit2 = 1000\nresult = lit1 is lit2"
namespace = {}
exec(code, namespace)
print(f"  同一段代码里 1000 is 1000 ？{namespace['result']}   ← 常量合并，不代表数值能用 is 比")

# ✅ 想找一个"稳定"的反例，就让值在运行时才产生（用 int() 转换）
#   257 以上既不受小整数缓存保护，也不会被常量合并，于是老老实实变成两个对象
safe1 = int("1000")
safe2 = int("1000")
print(f"  int('1000') is int('1000') ？{safe1 is safe2}   ← ⚠️ 稳定的反例：False")
print("--- 4. 小整数缓存结束 ---")


# ===== 5. 字符串驻留：为什么相同的字符串有时是同一个对象 =====

# 💡 Python 会把一些"看起来会被反复使用"的字符串放进池子里复用，
#   这叫"字符串驻留"（intern）。常量字符串（写在代码里的字面量）通常都会被驻留，
#   所以同一个字面量的 is 结果往往为 True。

# 用变量间接传递，模拟"运行时"拿到字符串
def identity(s):
    return s

str1 = identity("hello")
str2 = identity("hello")
print(f"  间接得到的 'hello' is 'hello' ？{str1 is str2}   ← 字面量被驻留，是同一个对象")

# ⚠️ 别以为"只有像标识符的字符串才驻留"，带空格的一样是 True（实测如此）
str3 = identity("hello world!")
str4 = identity("hello world!")
print(f"  间接得到的 'hello world!' is 另一个 ？{str3 is str4}   ← 带空格也驻留了")
# ⚠️ 但驻留规则是实现细节，不同版本可能不同，**绝对不要依赖它**。
print()

# ⚠️ 用运算"拼"出来的字符串通常不会自动驻留（实测：join 出来的是新对象）
joined = "".join(["hel", "lo"])
literal = "hello"
print(f"  拼接得到的 'hello' is 字面量 'hello' ？{joined is literal}   ← ⚠️ 运行时拼出来的，没被驻留")
print(f"  但它们的值相等吗？{joined == literal}   ← ✅ 值永远相等，这才是该依赖的")
print()

# ✅ 结论：字符串的 is 结果完全不可靠，比较字符串一律用 ==。

# 💡 如果确实需要强制驻留（极少用），可以用 sys.intern()
import sys
inner1 = sys.intern("".join(["wor", "ld"]))
inner2 = sys.intern("world")
print(f"  sys.intern 强制驻留后 is ？{inner1 is inner2}   ← 强制后才是同一个对象")
print("--- 5. 字符串驻留结束 ---")


# ===== 6. 可变类型带来的"共享"问题（提前预警） =====

# 因为变量是标签，两个标签指向同一个可变对象时，
# 通过任一标签修改，另一个标签看到的内容也会变。

shared_a = [1, 2, 3]
shared_b = shared_a       # 只是贴标签，不是复制
shared_b.append(99)

print(f"  shared_a = {shared_a}")
print(f"  shared_b = {shared_b}")
print(f"  通过 shared_b 修改，shared_a 也变了！{shared_a == shared_b}")
print()

# ✅ 想要真正的副本，要显式复制
copy_a = [1, 2, 3]
copy_b = copy_a[:]        # 切片会创建新列表
copy_b.append(99)
print(f"  copy_a = {copy_a}   ← 没被影响")
print(f"  copy_b = {copy_b}")
print(f"  copy_a is copy_b ？{copy_a is copy_b}   ← 两个不同对象")
print()

# 💡 这个坑在函数传参时特别致命（第 05 章会再讲），先留个印象。
print("--- 6. 可变类型的共享问题结束 ---")


# ---------- 小结 ----------
print("========== 本节小结 ==========")
print("  1. 不可变：int/float/str/bool/None/tuple；可变：list/dict/set")
print("  2. 不可变类型'修改'= 创建新对象（id 变）；可变类型可原地改（id 不变）")
print("  3. == 比值；is 比对象身份（同一个对象）")
print("  4. 小整数缓存范围：-5 ~ 256，区间内 int('100') is int('100') 为 True")
print("  5. 字符串驻留不可依赖，字符串比较一律用 ==")
print("  6. 两个变量指向同一个可变对象时，改一个会影响另一个")
print("==============================")

# 1. 不可变：int / float / str / bool / None / tuple；可变：list / dict / set
# 2. 不可变类型改内容 = 换新对象（id 变）；可变类型可原地改（id 不变）
# 3. == 比较值是否相等；is 比较是否为同一个对象
# 4. 小整数缓存范围 -5 ~ 256；超出范围每次可能新对象
# 5. 字符串驻留是实现细节，不要依赖；比较字符串用 ==
# 6. b = a 是贴标签；需要独立副本要显式复制（如 a[:]、list(a)）
# 💡 记住一句话：要比较"值"用 ==，要判断"是不是同一个"才用 is（通常只用于 None）。
