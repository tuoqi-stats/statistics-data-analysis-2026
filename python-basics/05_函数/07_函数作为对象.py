"""
================ 07 函数作为对象 ================

【本文件学什么】
  1. 函数是"一等公民"：可以赋值给变量、放进容器、当参数传、当返回值
  2. 把函数赋值给变量
  3. 把函数作为参数传给另一个函数（高阶函数）
  4. 把函数作为返回值（返回函数的函数）
  5. lambda 初识：匿名函数，适合一行能写完的小逻辑
  6. 内置高阶函数初识：map / filter / sorted(key=...)

【怎么运行】
      python 07_函数作为对象.py

【预计输出】
  依次看到 6 个分节结果，最后打印小结。
"""


# ===== 1. 函数是"一等公民" =====

# 在 Python 里，函数和数字、字符串一样，都是"对象"，可以自由传递。
# 这一点是理解 map / filter / 装饰器 / 回调函数的基础。
def shout(text):
    """把文本转成大写并加上感叹号。"""
    return text.upper() + "!"

# 函数自带一些属性，证明它就是个普通对象
print(f"    函数名: {shout.__name__}")
print(f"    函数类型: {type(shout).__name__}")

# 预期输出：
#     函数名: shout
#     函数类型: function
print("--- 1. 函数是对象结束 ---")


# ===== 2. 把函数赋值给变量 =====

# ⚠️ 关键区别：写 shout 得到的是"函数对象本身"，写 shout() 才是"调用并拿结果"。
# 赋值时千万不要加括号！
alias = shout          # 把函数对象赋给另一个名字，没有调用
print(f"    shout('hello') 调用结果: {shout('hello')}")

# 预期输出：shout('hello') 调用结果: HELLO!

# alias 指向同一个函数，用起来完全一样
print(f"    alias('world') 调用结果: {alias('world')}")

# 预期输出：alias('world') 调用结果: WORLD!

# 两个名字指向的是同一个函数对象
print(f"    alias is shout → {alias is shout}")

# 预期输出：alias is shout → True

# 也可以把函数放进列表 / 字典，按名字调用
actions = {"打招呼": shout}
print(f"    从字典里取出函数并调用: {actions['打招呼']('字典调用')}")

# 预期输出：从字典里取出函数并调用: 字典调用!

# 💡 常见错误：不小心多写了括号
#    a = shout     ← a 是函数，a() 才能得到结果
#    a = shout()   ← 这里就已经调用了一次，a 得到的是返回值字符串，a() 会报错
print("--- 2. 函数赋值给变量结束 ---")


# ===== 3. 把函数作为参数传递（高阶函数） =====

# 接收函数作为参数的函数，叫"高阶函数"。这类函数把"做什么"交给调用者决定。
def apply_twice(func, value):
    """对 value 连续应用两次 func。"""
    # 第一次应用，结果再应用一次
    return func(func(value))

# 传一个"加 1"的函数进去
def add_one(x):
    return x + 1

print(f"    apply_twice(add_one, 5) = {apply_twice(add_one, 5)}")

# 预期输出：apply_twice(add_one, 5) = 7   （5 → 6 → 7）

# 换个函数传进去，行为完全不同 —— 这就是把"逻辑"作为参数的价值
def double(x):
    return x * 2

print(f"    apply_twice(double, 5) = {apply_twice(double, 5)}")

# 预期输出：apply_twice(double, 5) = 20   （5 → 10 → 20）

# 再比如：让一个函数接收"比较规则"
def pick(a, b, rule):
    """按 rule 决定返回 a 还是 b。"""
    # rule(a, b) 返回 True 就选 a，否则选 b
    return a if rule(a, b) else b

def bigger(x, y):
    return x > y

print(f"    pick(3, 9, bigger) = {pick(3, 9, bigger)}")

# 预期输出：pick(3, 9, bigger) = 9
print("--- 3. 函数作为参数结束 ---")


# ===== 4. 把函数作为返回值 =====

# 函数里可以定义并返回另一个函数，外层函数像一个"函数工厂"。
def make_multiplier(n):
    """返回一个"把输入乘以 n"的新函数。"""
    def multiplier(x):
        # 这里用到了外层的变量 n，这就是"闭包"
        return x * n
    # 返回的是内层函数对象（不加括号！）
    return multiplier

# 工厂生产两个不同的函数
times_3 = make_multiplier(3)
times_10 = make_multiplier(10)

print(f"    make_multiplier(3) 造出的函数: times_3(7) = {times_3(7)}")

# 预期输出：make_multiplier(3) 造出的函数: times_3(7) = 21
print(f"    make_multiplier(10) 造出的函数: times_10(7) = {times_10(7)}")

# 预期输出：make_multiplier(10) 造出的函数: times_10(7) = 70

# ✅ 结论：同一个函数能记住不同的环境（n=3 或 n=10），各自独立工作。
# 💡 这种"带记忆的函数"是装饰器（进阶内容）的基石。
print("--- 4. 函数作为返回值结束 ---")


# ===== 5. lambda 初识：一行写完的匿名函数 =====

# 语法：lambda 参数列表: 表达式
# 它的"函数体"只能是一个表达式，不能写 if/for 等多行语句。
# 类比：lambda 是"便签纸上的小配方"，临时用一次；def 是"正式菜谱"，可以复用。

# 用 def 写
def add_def(x, y):
    return x + y

# 用 lambda 写，效果完全一样
add_lambda = lambda x, y: x + y

print(f"    def 版:  add_def(2, 3) = {add_def(2, 3)}")
print(f"    lambda 版: add_lambda(2, 3) = {add_lambda(2, 3)}")

# 预期输出：
#     def 版:  add_def(2, 3) = 5
#     lambda 版: add_lambda(2, 3) = 5

# 上面这种"赋值给变量"的写法其实不推荐，Python 官方建议用 def 更好读。
# lambda 真正的用武之地是"当场传一个小函数"，见下面：
numbers = [5, 2, 8, 1, 9]

# 按"原值"排序
print(f"    默认排序: {sorted(numbers)}")

# 预期输出：默认排序: [1, 2, 5, 8, 9]

# 按"相反数"排序，等价于从大到小。用 lambda 当场定义排序依据，不用专门写函数。
print(f"    按相反数排序: {sorted(numbers, key=lambda x: -x)}")

# 预期输出：按相反数排序: [9, 8, 5, 2, 1]

# ✅ lambda 适用场景：一行能写完的小逻辑，且只在这里用一次。
# ⚠️ 不适用场景：逻辑超过一行、需要复用、需要写文档 —— 用 def。
print("--- 5. lambda 初识结束 ---")


# ===== 6. 内置高阶函数初识：map / filter / sorted =====

fruits = ["apple", "banana", "cherry"]

# map(函数, 可迭代对象)：把函数应用到每个元素上，返回一个迭代器
# 这里把每个水果名都变大写
upper_fruits = list(map(lambda s: s.upper(), fruits))
print(f"    map 转大写: {upper_fruits}")

# 预期输出：map 转大写: ['APPLE', 'BANANA', 'CHERRY']

nums = [1, 2, 3, 4, 5, 6, 7, 8]

# filter(函数, 可迭代对象)：保留让函数返回 True 的元素
# 这里保留偶数（x % 2 == 0）
evens = list(filter(lambda x: x % 2 == 0, nums))
print(f"    filter 取偶数: {evens}")

# 预期输出：filter 取偶数: [2, 4, 6, 8]

# sorted 的 key 参数：指定"按什么排序"
people = [
    {"name": "小明", "age": 18},
    {"name": "小红", "age": 22},
    {"name": "小刚", "age": 16},
]

# 按字典里的 age 字段排序（key 接收一个"取出排序依据"的函数）
sorted_people = sorted(people, key=lambda p: p["age"])
names_by_age = [p["name"] for p in sorted_people]
print(f"    按年龄从小到大排序: {names_by_age}")

# 预期输出：按年龄从小到大排序: ['小刚', '小明', '小红']

# ✅ 结论：这些工具的共同点是"接收一个函数来决定行为"。
#    正因为 Python 里函数是对象，才能写出这么灵活的代码。
print("--- 6. 内置高阶函数结束 ---")


# ---------- 小结 ----------
# 1. 一等公民   → 函数可以赋值、进容器、当参数、当返回值
# 2. 赋值注意   → func 是函数对象，func() 是调用；赋值别加括号
# 3. 高阶函数   → 接收函数做参数的函数（apply_twice / pick）
# 4. 返回函数   → "函数工厂"，能造出带不同记忆的函数（闭包）
# 5. lambda     → 匿名函数，只有一行表达式；适合临时传一次的小逻辑
# 6. map/filter/sorted(key=) → 常用内置高阶函数，配合 lambda 非常顺手
# 💡 记住：把"数据"和"操作数据的逻辑"都当作值来传递，代码会灵活很多。
