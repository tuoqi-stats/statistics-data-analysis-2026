# -*- coding: utf-8 -*-
"""
================ 05 常见陷阱 ================

【本文件学什么】
  1. 赋值即引用（最重要的一条）
  2. 多重赋值：a, b = 1, 2 和交换变量
  3. 链式赋值：a = b = c = 0
  4. del 删除变量：删的是"标签"，不是"盒子"
  5. 内存回收（垃圾回收）初识
  6. 其他高频小陷阱

【怎么运行】
  在 VSCode 里打开本文件，直接点右上角 ▶ 运行；
  或在终端执行：
      python 05_常见陷阱.py

【预计输出】
  会依次看到 7 个分节的结果，每行 print 的结果都在代码上方用注释写明了。
  文件末尾会打印"小结"。
"""


# ===== 1. 赋值即引用（本章最重要的一条） =====

# ⚠️ 很多人以为 a = [1, 2, 3] 然后 b = a 是"复制了一份列表"。
#   错！Python 里 = 从不复制数据，它只是"再贴一张标签"。

origin = [1, 2, 3]
alias = origin            # alias 和 origin 指向同一个列表
alias.append(4)           # 通过 alias 修改列表内容

print(f"  origin = {origin}   ← 我们只改过 alias，origin 却也变了")
print(f"  alias  = {alias}")
print(f"  origin is alias ？{origin is alias}   ← 它俩根本是同一个对象")
print()

# ✅ 结论：对可变对象，通过任何一张标签修改，其他标签都会"看到"这个变化。

# 想要独立副本，必须显式复制：
real_copy = origin[:]     # 用切片复制出一个新列表
real_copy.append(999)
print(f"  切片复制后 real_copy = {real_copy}，origin = {origin}")
print(f"  origin is real_copy ？{origin is real_copy}   ← 两个不同对象")
print()

# 💡 不可变类型没这个问题：因为根本改不了，只能重新绑定
s1 = "abc"
s2 = s1
s2 = s2 + "d"             # 这里 s2 换到了新对象，s1 纹丝不动
print(f"  s1 = {s1}，s2 = {s2}   ← 字符串不受影响")
print("--- 1. 赋值即引用结束 ---")


# ===== 2. 多重赋值 =====

# Python 允许一行给多个变量赋值，等号两边用逗号隔开。
# 规则：右边的值会**同时**赋给左边，像并发执行一样。

a, b, c = 1, 2, 3
# 预期输出：a, b, c = 1, 2, 3  →  a=1, b=2, c=3
print(f"  a, b, c = 1, 2, 3  →  a={a}, b={b}, c={c}")

# ⚠️ 陷阱：左右数量必须一致，否则报 ValueError
# 预期输出：x, y = 1, 2, 3 报错：ValueError（左边2个右边3个，数量不匹配）
try:
    x, y = 1, 2, 3
except ValueError as e:
    print(f"  x, y = 1, 2, 3 报错：{type(e).__name__}（左边2个右边3个，数量不匹配）")

# ===== 2.1 交换变量：Python 的招牌写法 =====
# 其他语言要借助临时变量 temp，Python 一行搞定。
left = "左"
right = "右"
# 预期输出：交换前：left=左, right=右
print(f"  交换前：left={left}, right={right}")

left, right = right, left
# 预期输出：交换后：left=右, right=左
print(f"  交换后：left={left}, right={right}")

# 💡 原理：右边 right, left 会先被打包成一个元组 ("右", "左")，再依次拆给左边。

# ===== 2.2 拆包：把序列里的值分给多个变量 =====
point = (10, 20)
px, py = point
# 预期输出：拆包 (10, 20) → px=10, py=20
print(f"  拆包 (10, 20) → px={px}, py={py}")

# 用 * 收集剩余的值
first, *others = [1, 2, 3, 4, 5]
# 预期输出：first, *others = [1,2,3,4,5] → first=1, others=[2, 3, 4, 5]
print(f"  first, *others = [1,2,3,4,5] → first={first}, others={others}")
print("--- 2. 多重赋值结束 ---")


# ===== 3. 链式赋值 =====

# a = b = c = 0 会让三个变量都指向同一个对象。
x = y = z = 0
# 预期输出：x = y = z = 0  →  x=0, y=0, z=0
print(f"  x = y = z = 0  →  x={x}, y={y}, z={z}")

# 预期输出：x is y is z ？True   ← 都是同一个 0
print(f"  x is y is z ？{x is y and y is z}   ← 都是同一个 0")

# ⚠️⚠️ 陷阱：链式赋值 + 可变类型 = 灾难
#   三个变量会共享同一个列表，改一个三个都变！
m = n = k = []
m.append("只往 m 里加")
# 预期输出：m=['只往 m 里加'], n=['只往 m 里加'], k=['只往 m 里加']   ← ⚠️ 三个全变了！
print(f"  m={m}, n={n}, k={k}   ← ⚠️ 三个全变了！")

# 预期输出：m is n ？True   ← 它们是同一个列表
print(f"  m is n ？{m is n}   ← 它们是同一个列表")

# ✅ 结论：链式赋值适合不可变值（0、""、None）；
#   可变对象一定要分开写：m, n, k = [], [], []

m2, n2, k2 = [], [], []
m2.append("只往 m2 里加")
# 预期输出：分开写：m2=['只往 m2 里加'], n2=[], k2=[]   ← ✅ 互不影响
print(f"  分开写：m2={m2}, n2={n2}, k2={k2}   ← ✅ 互不影响")
print("--- 3. 链式赋值结束 ---")


# ===== 4. del：删除的是"标签"，不是"盒子" =====

# del 变量名 会把这张标签撕掉。如果还有别的标签指向同一个对象，对象依然活着。

temp_var = 123
# 预期输出：删除前：temp_var = 123
print(f"  删除前：temp_var = {temp_var}")

del temp_var

# ⚠️ 删除后再访问就会报 NameError
# 预期输出：删除后访问报错：NameError（名字没定义）
try:
    print(temp_var)
except NameError as e:
    print(f"  删除后访问报错：{type(e).__name__}（名字没定义）")

print()

# 关键演示：对象和标签的关系
box = [1, 2, 3]
another_tag = box          # 同一个列表贴了两张标签
del box                    # 撕掉 box 这张标签
# 预期输出：del box 之后，another_tag 依然可用：[1, 2, 3]
print(f"  del box 之后，another_tag 依然可用：{another_tag}")

# ✅ 结论：del 删的是"名字"，不是"数据"。只要还有别的名字指着它，数据就还在。
print()

# del 也能删列表里的元素
items = [1, 2, 3, 4, 5]
del items[0]               # 删下标为 0 的元素
# 预期输出：del items[0] 之后：[2, 3, 4, 5]
print(f"  del items[0] 之后：{items}")
print("--- 4. del 删除变量结束 ---")


# ===== 5. 内存回收（垃圾回收）初识 =====

# Python 用"引用计数"作为主要的回收机制：
#   每个对象都记着"有多少张标签指向我"（引用计数）。
#   当计数变成 0，即没有任何名字指向它时，它就会被自动回收，内存被释放。

# 我们无法直接"看到"回收发生，但可以用 id 复用现象来间接感受：
# 对象被回收后，它占用的内存会被后来的对象复用，导致 id 相同。

# 注意：下面的演示只是"帮你建立直觉"，id 复用不是判断回收是否发生的
# 可靠手段（实现细节），请不要在真实代码里依赖它。

import gc

data = [1, 2, 3, 4, 5]
print(f"  data 的 id = {id(data)}")

del data
# 到这里，[1,2,3,4,5] 已经没有标签指向它了，引用计数归零 → 被回收

# 手动触发一次回收（平常不需要手动调用，这里只为演示）
gc.collect()
print("  已执行 del data 并触发 gc.collect()")
print("  💡 对象在没人引用时会被自动回收，你不需要手动管内存")

# 引用计数无法处理的场景：循环引用，这时靠"分代回收"兜底（进阶内容，了解即可）
cycle_a = []
cycle_b = []
cycle_a.append(cycle_b)    # a 引用 b
cycle_b.append(cycle_a)    # b 引用 a，形成环
del cycle_a, cycle_b
print("  循环引用对象已被删除引用，gc 会负责处理它们（进阶话题）")
print("  ✅ 初学者结论：只管处理好变量的引用关系，内存交给 Python")
print("--- 5. 内存回收结束 ---")


# ===== 6. 其他高频小陷阱 =====

# ===== 6.1 变量未定义就使用 → NameError =====
# 预期输出：使用未定义变量：NameError
try:
    print(undeclared_var)
except NameError as e:
    print(f"  使用未定义变量：{type(e).__name__}")

# ===== 6.2 大小写拼错 → 实际是"新变量" =====
myScore = 100
# 预期输出：myScore 和 myscore 是两个不同的变量（Python 区分大小写）
try:
    print(myscore)
except NameError:
    print("  myScore 和 myscore 是两个不同的变量（Python 区分大小写）")

# ===== 6.3 中文标点 → 语法错误 =====
# ⚠️ 全角括号、全角引号、全角分号都是新手常见错误：
#   print（"你好"）      ← SyntaxError（用了中文全角括号）
# 预期输出：⚠️ 提醒：代码里的括号 () 、引号 '' "" 、逗号 , 都必须是英文半角
print("  ⚠️ 提醒：代码里的括号 () 、引号 '' \"\" 、逗号 , 都必须是英文半角")

# ===== 6.4 = 和 == 混淆 =====
num = 5
print(f"  num = 5   是赋值（把 5 给 num）")

# 预期输出：num == 5  是判断，结果是 True
print(f"  num == 5  是判断，结果是 {num == 5}")

# ⚠️ 写成 if num = 5: 会直接 SyntaxError，Python 在这点上比 C 语言严格。

# ===== 6.5 变量名遮蔽内置函数 =====
# ⚠️ 用内置名字当变量名，会覆盖内置功能，后面就没法用了。
#   反例：sum = 10 之后，sum([1,2,3]) 就会报错。
# 预期输出：内置函数 sum 正常可用：sum([1, 2, 3]) = 6
print(f"  内置函数 sum 正常可用：sum([1, 2, 3]) = {sum([1, 2, 3])}")
print("--- 6. 其他高频小陷阱结束 ---")


# ===== 7. 陷阱速查：一段对比代码 =====

# 把前面最重要的几个坑集中对比一下，加深印象。

print("  【对比 1】不可变 vs 可变 的共享行为")
p = 10
q = p
q = q + 1
# 预期输出：整数：p=10, q=11   ← 改 q 不影响 p
print(f"    整数：p={p}, q={q}   ← 改 q 不影响 p")

p_list = [10]
q_list = p_list
q_list.append(1)
# 预期输出：列表：p_list=[10, 1], q_list=[10, 1]   ← ⚠️ 改 q_list 影响了 p_list
print(f"    列表：p_list={p_list}, q_list={q_list}   ← ⚠️ 改 q_list 影响了 p_list")
print()

print("  【对比 2】链式赋值 + 可变类型")
e1 = e2 = []
e1.append("x")
# 预期输出：e1=['x'], e2=['x']   ← ⚠️ 共享同一个列表
print(f"    e1={e1}, e2={e2}   ← ⚠️ 共享同一个列表")

e3 = []
e4 = []
e3.append("x")
# 预期输出：e3=['x'], e4=[]   ← ✅ 分开写就互不影响
print(f"    e3={e3}, e4={e4}   ← ✅ 分开写就互不影响")
print("--- 7. 陷阱速查结束 ---")


# ---------- 小结 ----------
print("========== 本节小结 ==========")
print("  1. 赋值即引用：b = a 不复制数据，只是多贴一张标签")
print("  2. 多重赋值 a, b = 1, 2；交换变量 a, b = b, a 一行搞定")
print("  3. 链式赋值 a = b = [] 会让多个变量共享同一个可变对象，危险！")
print("  4. del 删的是名字（标签），不是数据；还有别的标签则数据仍在")
print("  5. 引用计数为 0 时对象自动回收，无需手动管理内存")
print("  6. 常见坑：未定义变量、大小写拼错、中文标点、= 与 ==、遮蔽内置名")
print("==============================")

# 1. 赋值即引用（最高频误解）：b = a 不复制；要副本用 a[:] 或 copy
# 2. 多重赋值：a, b = 1, 2；交换：a, b = b, a
# 3. 链式赋值遇可变对象会共享，务必分开写
# 4. del 删标签不删数据；对象无人引用时自动回收
# 5. 注意 NameError 的三种常见来源：没定义、大小写错、拼写错
# 💡 记住一句话：对可变对象，"赋值"就是"共享"，想独立就得"复制"。
