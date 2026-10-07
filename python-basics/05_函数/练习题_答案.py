"""
================ 练习题 · 参考答案（10 题） ================

【怎么用】
  先自己做 练习题.py，写完了再来对答案。
  本文件是"可以直接运行"的完整版，运行后会打印每题的结果。

【运行】
      python 练习题_答案.py

【预计输出】
  每题结果都有 "题 X" 的前缀，方便对照。最后打印解题要点小结。
"""

print("========== 练习题参考答案 ==========\n")


# ========== 题 1：定义与调用 ==========
# 要点：def 定义、括号调用、参数接收。

def welcome(name):
    # 用 f-string 拼接字符串，把 name 嵌进去
    print(f"    欢迎 {name} 学习 Python！")

print("【题 1】定义与调用")
welcome("小明")
# 预期输出：欢迎 小明 学习 Python！
print()


# ========== 题 2：默认参数 ==========
# 要点：有默认值的参数必须放在必填参数后面。

def power(base, exp=2):
    # ** 是幂运算符
    return base ** exp

print("【题 2】默认参数")
print(f"    power(5) = {power(5)}      ← exp 用默认值 2")

# 预期输出：power(5) = 25      ← exp 用默认值 2
print(f"    power(2, 10) = {power(2, 10)}  ← exp 传 10")

# 预期输出：power(2, 10) = 1024  ← exp 传 10
print()


# ========== 题 3：关键字参数 ==========
# 要点：用 参数名=值 调用，顺序随意、可读性好。

def make_tag(text, tag="p", upper=False):
    # 先按要求决定是否转大写
    content = text.upper() if upper else text
    # 用 f-string 拼出标签
    return f"<{tag}>{content}</{tag}>"

print("【题 3】关键字参数")
# 故意打乱顺序写关键字参数，结果依然正确
print(f"    {make_tag(text='hello', tag='h1', upper=True)}")

# 预期输出：<h1>HELLO</h1>
print(f"    {make_tag('你好', upper=False)}")

# 预期输出：<p>你好</p>
print()


# ========== 题 4：⚠️ 默认参数陷阱 ==========
# 要点：默认值绝不能用可变对象（[] / {} / set()），改用 None + 内部判断。

def add_log(message, logs=None):
    # 关键：只有当调用者没传 logs 时，才创建一个新列表
    if logs is None:
        logs = []
    logs.append(message)
    return logs

print("【题 4】默认参数陷阱（修复版）")
print(f"    add_log('第一次') = {add_log('第一次')}")

# 预期输出：add_log('第一次') = ['第一次']
print(f"    add_log('第二次') = {add_log('第二次')}")

# 预期输出：add_log('第二次') = ['第二次']   ← 独立的新列表，没有累积
print(f"    add_log('第三次') = {add_log('第三次')}")

# 预期输出：add_log('第三次') = ['第三次']
print("    ✅ 三次调用互不影响，说明修复成功")
print()


# ========== 题 5：*args 可变参数 ==========
# 要点：*args 收集成元组；注意空输入的边界处理，避免除以 0。

def average(*nums):
    # 空输入直接返回 0，防止 ZeroDivisionError
    if not nums:
        return 0
    return sum(nums) / len(nums)

print("【题 5】*args 可变参数")
print(f"    average(80, 90, 100) = {average(80, 90, 100)}")

# 预期输出：average(80, 90, 100) = 90.0
print(f"    average() = {average()}")

# 预期输出：average() = 0
print()


# ========== 题 6：**kwargs 可变参数 ==========
# 要点：**kwargs 收集成字典；用列表收集片段再 join，效率比不断 + 字符串高。

def build_query(**params):
    # 收集每个 "键=值" 片段
    parts = []
    for key, value in params.items():
        # 值可能不是字符串，统一用 str() 转换
        parts.append(f"{key}={value}")
    # 用 & 把片段连起来
    return "&".join(parts)

print("【题 6】**kwargs 可变参数")
print(f"    {build_query(name='tom', age=18, city='beijing')}")

# 预期输出：name=tom&age=18&city=beijing

# 一个参数都不传时，返回空字符串
print(f"    build_query() = '{build_query()}'")

# 预期输出：build_query() = ''
print()


# ========== 题 7：多个返回值 ==========
# 要点：return a, b, c 实际返回元组；调用方拆包接收。

def analyze(numbers):
    # 先算总和与最大值
    total = sum(numbers)
    maximum = max(numbers)
    # 平均值 = 总和 / 个数
    mean = total / len(numbers)
    # 三个值打包返回
    return total, maximum, mean

print("【题 7】多个返回值")
total, maximum, mean = analyze([1, 2, 3, 4])
print(f"    总和={total}, 最大值={maximum}, 平均值={mean}")

# 预期输出：总和=10, 最大值=4, 平均值=2.5

# 也可以用单个变量接住，得到的是元组
result = analyze([1, 2, 3, 4])
print(f"    单变量接收: {result}（类型 {type(result).__name__}）")

# 预期输出：单变量接收: (10, 4, 2.5)（类型 tuple）
print()


# ========== 题 8：作用域与 global ==========
# 要点：① global 声明后才能改全局变量；② 对比两种风格的优劣。

score = 0

def add_score(points):
    # 声明操作的是全局的 score
    global score
    score += points

print("【题 8】作用域与 global")
add_score(10)
add_score(20)
print(f"    两次累加后 score = {score}")

# 预期输出：两次累加后 score = 30

# ② 回答：用"参数传入 + 返回值传出"更好，因为：
#    1. 数据流一目了然 —— 看函数签名就知道需要什么、产出什么；
#    2. 没有隐藏副作用 —— 调用者不会被远处变量的变化"偷袭"；
#    3. 函数可复用、易测试 —— 不依赖外部环境，随时能单独调用验证。
#    而 global 会让"谁改了我的变量"变得难以追查，是 bug 的高发区。
#
#    等价的无副作用写法：
def add_score_better(current, points):
    """传入当前分数和增加量，返回新分数。"""
    return current + points

# 用全局变量接收返回值，效果一样但逻辑清晰
score = add_score_better(score, 5)
print(f"    用推荐写法再加 5 后 score = {score}")

# 预期输出：用推荐写法再加 5 后 score = 35
print()


# ========== 题 9：递归 ==========
# 要点：必须有终止条件，且每次递归都更接近终止条件。

def sum_to(n):
    # 终止条件：n <= 0 时累加结束
    if n <= 0:
        return 0
    # 递推关系：1..n 的和 = n + (1..n-1 的和)
    return n + sum_to(n - 1)

print("【题 9】递归")
print(f"    sum_to(5) = {sum_to(5)}")

# 预期输出：sum_to(5) = 15

# 顺便验证一下：1 到 100 的和 = 5050
print(f"    sum_to(100) = {sum_to(100)}")

# 预期输出：sum_to(100) = 5050
print()


# ========== 题 10：函数作为参数 / lambda ==========
# 要点：lambda 作为 key / filter 的实参，一行表达小逻辑。

nums_list = [3, 7, 1, 9, 4]

print("【题 10】函数作为参数 / lambda")

# ① key=lambda x: -x 表示按"相反数"排序，等价于从大到小
sorted_desc = sorted(nums_list, key=lambda x: -x)
print(f"    从大到小排序: {sorted_desc}")

# 预期输出：从大到小排序: [9, 7, 4, 3, 1]

# ② filter 保留让 lambda 返回 True 的元素，即大于 3 的数
bigger_than_3 = list(filter(lambda x: x > 3, nums_list))
print(f"    大于 3 的数: {bigger_than_3}")

# 预期输出：大于 3 的数: [7, 9, 4]
print()


# ---------- 解题要点小结 ----------
# 题 1  定义要 def + 缩进，调用必须加括号。
# 题 2  默认参数让调用更简单；有默认值的参数写在后面。
# 题 3  关键字参数顺序随意，代码自解释。
# 题 4  ⚠️ 默认值永远别用 [] / {}，用 None + 内部判断。
# 题 5  *args 是元组；注意空输入的边界情况。
# 题 6  **kwargs 是字典；字符串拼接优先用 join。
# 题 7  return 多值 = 返回元组，调用方可以拆包。
# 题 8  global 能用但少用；优先"参数进、返回值出"。
# 题 9  递归两大要素：终止条件 + 逼近终止条件。
# 题 10 lambda 适合一行小逻辑，常配 sorted / map / filter 使用。
