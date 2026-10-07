"""
================ 03 可变参数 *args 与 **kwargs ================

【本文件学什么】
  1. *args  ：收集任意多个"位置参数"，打包成一个元组
  2. **kwargs：收集任意多个"关键字参数"，打包成一个字典
  3. 两者同时使用时的顺序规则
  4. 拆包：把列表 / 字典拆开传给函数（* 和 ** 在调用处的用法）

【怎么运行】
      python 03_可变参数.py

【预计输出】
  依次看到 5 个分节结果，最后打印小结。
"""


# ===== 1. *args：收集多余的位置参数 =====

# 参数前加一个星号 *，表示"把多出来的位置参数都收进来"，收成一个元组 tuple。
# 名字里的 args 只是约定俗成，写成 *numbers 也可以，关键在那个星号。
def sum_all(*args):
    # 打印一下 args 的类型和内容，看清楚它到底是什么
    print(f"    args 的类型: {type(args).__name__}")
    print(f"    args 的内容: {args}")

    # 因为 args 是元组，可以直接用 sum() 求和
    total = sum(args)
    return total

# 传 3 个参数
print(f"  sum_all(1, 2, 3) = {sum_all(1, 2, 3)}")

# 预期输出：
#     args 的类型: tuple
#     args 的内容: (1, 2, 3)
#   sum_all(1, 2, 3) = 6

# 传 5 个参数，照样可以
print(f"  sum_all(10, 20, 30, 40, 50) = {sum_all(10, 20, 30, 40, 50)}")

# 预期输出：
#     args 的类型: tuple
#     args 的内容: (10, 20, 30, 40, 50)
#   sum_all(10, 20, 30, 40, 50) = 150

# ✅ 结论：一个参数都不传时，args 是空元组 ()
print(f"  sum_all() = {sum_all()}")

# 预期输出：
#     args 的类型: tuple
#     args 的内容: ()
#   sum_all() = 0
print("--- 1. *args 结束 ---")


# ===== 2. *args 与其他参数配合 =====

# 模式：普通参数在前，*args 在后。
# 调用时前面的参数被普通参数吃掉，剩下的全部装进 args。
def show_team(leader, *members):
    print(f"    队长: {leader}")
    print(f"    队员数量: {len(members)}")
    # 用 ", ".join(...) 把元组里的名字拼成字符串
    print(f"    队员列表: {', '.join(members)}")

# "张三" 给 leader，后面三个都进 members
show_team("张三", "李四", "王五", "赵六")

# 预期输出：
#     队长: 张三
#     队员数量: 3
#     队员列表: 李四, 王五, 赵六

# 也可以一个队员都没有
show_team("独狼")

# 预期输出：
#     队长: 独狼
#     队员数量: 0
#     队员列表: 
print("--- 2. *args 配合普通参数结束 ---")


# ===== 3. **kwargs：收集多余的关键字参数 =====

# 参数前加两个星号 **，表示"把多出来的关键字参数都收进来"，收成一个字典 dict。
def print_info(**kwargs):
    print(f"    kwargs 的类型: {type(kwargs).__name__}")
    print(f"    kwargs 的内容: {kwargs}")

    # 遍历字典：.items() 同时拿到键和值
    for key, value in kwargs.items():
        print(f"      {key} = {value}")

# 传一堆 名字=值 形式的参数
print_info(name="小明", age=18, city="上海")

# 预期输出：
#     kwargs 的类型: dict
#     kwargs 的内容: {'name': '小明', 'age': 18, 'city': '上海'}
#       name = 小明
#       age = 18
#       city = 上海

# 不传任何关键字参数时，kwargs 是空字典 {}
print_info()

# 预期输出：
#     kwargs 的类型: dict
#     kwargs 的内容: {}
print("--- 3. **kwargs 结束 ---")


# ===== 4. 四种参数同时出现时的顺序 =====

# 完整顺序：普通参数 → *args → 有默认值的参数 → **kwargs
# （实际写代码时很少四个都用上，但面试常考这个顺序。）
def mixed(a, b, *args, sep="-", **kwargs):
    print(f"    a = {a}, b = {b}")
    print(f"    args = {args}")
    print(f"    sep = {sep}")
    print(f"    kwargs = {kwargs}")

# 1, 2 被 a、b 吃掉；3, 4, 5 进 args；sep 被关键字指定；剩下的进 kwargs
mixed(1, 2, 3, 4, 5, sep="|", x=100, y=200)

# 预期输出：
#     a = 1, b = 2
#     args = (3, 4, 5)
#     sep = |
#     kwargs = {'x': 100, 'y': 200}

# sep 不传时使用默认值 "-"
mixed(1, 2)

# 预期输出：
#     a = 1, b = 2
#     args = ()
#     sep = -
#     kwargs = {}
print("--- 4. 参数顺序结束 ---")


# ===== 5. 拆包：反过来把容器"打开"传进去 =====

# 在"调用"时也可以写 * 和 **，作用是把容器拆成一个个参数。
def multiply(a, b, c):
    return a * b * c

# 有一个列表，刚好三个元素
nums = [2, 3, 4]

# ❌ 直接传列表会把它当成一个参数，报 TypeError（参数个数不匹配）
# print(multiply(nums))

# ✅ 在列表前加 *，相当于写 multiply(2, 3, 4)
print(f"  multiply(*[2, 3, 4]) = {multiply(*nums)}")

# 预期输出：multiply(*[2, 3, 4]) = 24


# 字典的拆包同理，用 ** 把它拆成 参数名=值
def describe(name, age):
    return f"{name} 今年 {age} 岁"

person = {"name": "小红", "age": 20}

# ✅ **person 相当于 describe(name="小红", age=20)
print(f"  describe(**person) = {describe(**person)}")

# 预期输出：describe(**person) = 小红 今年 20 岁

# 💡 拆包最常见的实战场景：把自己收到的 *args / **kwargs 原样转发给另一个函数
def wrapper(*args, **kwargs):
    # 把收到的所有参数原封不动传给 multiply
    result = multiply(*args, **kwargs)
    return result

print(f"  wrapper(2, 3, 4) = {wrapper(2, 3, 4)}")

# 预期输出：wrapper(2, 3, 4) = 24
print("--- 5. 拆包结束 ---")


# ---------- 小结 ----------
# 1. *args    → 收集多余位置参数，得到元组 tuple；调用处写 * 可拆开列表/元组
# 2. **kwargs → 收集多余关键字参数，得到字典 dict；调用处写 ** 可拆开字典
# 3. 记忆口诀 → 一个星号对元组（按位置），两个星号对字典（按名字）
# 4. 参数顺序 → 普通参数 → *args → 默认值参数 → **kwargs
# 5. 拆包用途 → 让函数可以"无损"转发参数，是装饰器（后续章节）的基础
