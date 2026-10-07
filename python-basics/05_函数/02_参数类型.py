"""
================ 02 参数类型 ================

【本文件学什么】
  1. 位置参数：按顺序一个个传
  2. 默认参数：不传就用默认值
  3. 关键字参数：用 名字=值 的方式传，顺序随意
  4. 参数的定义顺序规则与调用规则
  5. ⚠️⚠️ 重点：默认参数陷阱（def f(x, lst=[])）

【怎么运行】
      python 02_参数类型.py

【预计输出】
  依次看到 6 个分节结果，其中第 6 节会刻意展示"错误现象"和"正确写法"的对比，
  最后打印小结。
"""


# ===== 1. 位置参数：靠"位置"一一对应 =====

# a、b 是位置参数。调用时按从左到右的顺序赋值：第一个实参给 a，第二个给 b。
# 类比：点奶茶时说"中杯、少冰"，店员按顺序理解成"规格、冰量"。
def introduce(name, age):
    print(f"  我叫 {name}，今年 {age} 岁")

# 第一个实参 "小明" 给 name，第二个 18 给 age
introduce("小明", 18)

# 预期输出：我叫 小明，今年 18 岁

# ⚠️ 顺序传错不会报错，但结果就错了 —— 这是位置参数的隐患
introduce(18, "小明")

# 预期输出：我叫 18，今年 小明 岁   ← 逻辑错了但不报错
print("--- 1. 位置参数结束 ---")


# ===== 2. 默认参数：给参数一个"保底值" =====

# 参数写成 参数名=默认值，调用时就可以不传这个参数。
# 有默认值的参数必须放在没有默认值的参数后面！
def greet(name, greeting="你好"):
    # greeting 没传时就用 "你好"
    print(f"  {greeting}，{name}！")

# 只传 name，greeting 使用默认值 "你好"
greet("小明")

# 预期输出：你好，小明！

# 传两个参数，greeting 被覆盖成 "早上好"
greet("小红", "早上好")

# 预期输出：早上好，小红！
print("--- 2. 默认参数结束 ---")


# ===== 3. 关键字参数：用名字指定，顺序随意 =====

# 调用时写 参数名=值，就不用死记参数顺序了，可读性也更好。
def create_profile(name, age, city):
    print(f"  档案：{name} / {age} 岁 / 来自 {city}")

# 用关键字参数，故意打乱顺序，结果依然正确
create_profile(city="北京", age=25, name="小刚")

# 预期输出：档案：小刚 / 25 岁 / 来自 北京
print("--- 3. 关键字参数结束 ---")


# ===== 4. 位置参数和关键字参数混用 =====

# 规则：位置参数必须写在关键字参数前面。
# ✅ 正确写法：先给必需的 name，再用关键字指定 greeting
greet("小美", greeting="晚上好")

# 预期输出：晚上好，小美！

# ⚠️ 下面这行如果取消注释会报 SyntaxError：
#     positional argument follows keyword argument
# greet(greeting="晚上好", "小美")
print("--- 4. 混合使用结束 ---")


# ===== 5. 默认参数 + 关键字参数的实用场景 =====

# 这种"少量必需 + 大量可选"的设计是最常见的函数写法。
def make_coffee(size="中杯", sugar=1, milk=True, ice=False):
    # 根据参数拼出一杯咖啡的描述
    desc = f"{size}咖啡，糖 {sugar} 勺"
    desc += "，加奶" if milk else "，不加奶"
    desc += "，加冰" if ice else "，常温"
    return desc

# 全部用默认值，什么都不传
print(f"  make_coffee() => {make_coffee()}")

# 预期输出：中杯咖啡，糖 1 勺，加奶，常温

# 只想改冰量，其它用默认值，用关键字参数最清晰
print(f"  make_coffee(ice=True) => {make_coffee(ice=True)}")

# 预期输出：中杯咖啡，糖 1 勺，加奶，加冰

# 大杯 + 无糖 + 去奶
print(f"  make_coffee('大杯', sugar=0, milk=False) => {make_coffee('大杯', sugar=0, milk=False)}")

# 预期输出：大杯咖啡，糖 0 勺，不加奶，常温
print("--- 5. 实用场景结束 ---")


# ===== 6. ⚠️⚠️ 默认参数陷阱（本节最重要！） =====

# 【错误示范】把可变对象（列表、字典）当默认值，是非常经典的坑。
# 原因：默认值 [] 在"函数定义时"只被创建一次，之后所有调用共用同一个列表。
def add_item_wrong(item, basket=[]):
    basket.append(item)   # 往这个"共享"列表里追加元素
    return basket

print("  【错误示范】默认值是空列表 []：")
# 第 1 次调用，看起来很正常
print(f"    第 1 次 add_item_wrong('苹果') => {add_item_wrong('苹果')}")

# 预期输出：第 1 次 add_item_wrong('苹果') => ['苹果']

# 第 2 次调用，问题出现了：上一次的"苹果"居然还在！
print(f"    第 2 次 add_item_wrong('香蕉') => {add_item_wrong('香蕉')}")

# 预期输出：第 2 次 add_item_wrong('香蕉') => ['苹果', '香蕉']

# 第 3 次调用继续累积，篮子越来越"脏"
print(f"    第 3 次 add_item_wrong('橙子') => {add_item_wrong('橙子')}")

# 预期输出：第 3 次 add_item_wrong('橙子') => ['苹果', '香蕉', '橙子']
print("  ⚠️ 我们每次都想要一个新篮子，结果却是同一个篮子不断累积！")


# 【正确写法】默认值用 None，在函数内部判断并新建列表。
# None 是不可变对象，不会出现"共享累积"的问题。
def add_item_right(item, basket=None):
    # 只有调用者没传 basket 时，才创建一个全新的空列表
    if basket is None:
        basket = []
    basket.append(item)
    return basket

print("  【正确写法】默认值是 None，函数内部再建新列表：")
# 每次调用都是全新的列表，互不影响
print(f"    第 1 次 add_item_right('苹果') => {add_item_right('苹果')}")

# 预期输出：第 1 次 add_item_right('苹果') => ['苹果']
print(f"    第 2 次 add_item_right('香蕉') => {add_item_right('香蕉')}")

# 预期输出：第 2 次 add_item_right('香蕉') => ['香蕉']
print(f"    第 3 次 add_item_right('橙子') => {add_item_right('橙子')}")

# 预期输出：第 3 次 add_item_right('橙子') => ['橙子']

# 当然，如果你真的想往指定列表里加，也完全支持
my_basket = ["西瓜"]
print(f"    传入自己的篮子 add_item_right('葡萄', my_basket) => {add_item_right('葡萄', my_basket)}")

# 预期输出：传入自己的篮子 add_item_right('葡萄', my_basket) => ['西瓜', '葡萄']

# ✅ 结论：Python 官方建议 —— 默认参数永远不要用 []、{}、set() 这类可变对象，
#          统一写成 None，然后在函数体里判断后再创建。
print("--- 6. 默认参数陷阱结束 ---")


# ---------- 小结 ----------
# 1. 位置参数       → 按顺序对应，顺序错了不报错但结果错
# 2. 默认参数       → 写法 参数名=默认值，必须放在无默认值参数之后
# 3. 关键字参数     → 写法 参数名=值，顺序随意、可读性好
# 4. 混用规则       → 位置参数必须在前，关键字参数在后
# 5. 推荐设计       → 少量必需参数 + 多用默认值，让调用更简单
# 6. ⚠️ 默认参数陷阱 → 绝不用可变对象做默认值，用 None + 内部判断
