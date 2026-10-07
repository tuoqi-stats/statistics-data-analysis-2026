"""
================ 06 递归 ================

【本文件学什么】
  1. 什么是递归：函数自己调用自己
  2. 递归的两个必备要素：终止条件 + 向终止条件靠近
  3. 经典案例：阶乘、斐波那契数列
  4. 递归深度限制 sys.getrecursionlimit / sys.setrecursionlimit
  5. ⚠️ 忘记终止条件 → RecursionError（用 try/except 安全演示）
  6. 递归 vs 循环：什么时候该用递归

【怎么运行】
      python 06_递归.py

【预计输出】
  依次看到 6 个分节结果。第 5 节会触发一次被捕获的 RecursionError，
  程序不会崩溃，会正常打印出异常信息并继续往下走。
"""

import sys


# ===== 1. 什么是递归：自己调用自己 =====

# 递归的日常类比：俄罗斯套娃 —— 想打开最小的那个，得先打开外面一层，
# 而"打开一层"这件事，本身又是同一套动作。
# 再比如：查字典时，解释里又出现不懂的词，就去查那个词，如此往复，
# 直到查到一个你已经懂的词为止（那个"懂的词"就是终止条件）。

def count_down(n):
    """从 n 倒数到 1。"""
    # 终止条件：到了 0 就停，不再递归
    if n <= 0:
        print("    发射！")
        return            # return 结束这一层

    # 先打印当前数字
    print(f"    {n}")

    # 再让函数调用自己，但参数变小了（n-1），朝终止条件靠近
    count_down(n - 1)

count_down(3)

# 预期输出：
#     3
#     2
#     1
#     发射！
print("--- 1. 递归概念结束 ---")


# ===== 2. 阶乘：递归的经典入门 =====

# 数学定义：n! = n × (n-1)!，且 0! = 1
# 翻译成代码：
#   终止条件：0! = 1
#   递推关系：n! = n * (n-1)!
def factorial(n):
    """计算 n 的阶乘（递归版）。"""
    # 终止条件
    if n == 0:
        return 1

    # 递归调用：把问题"变小一号"再交给同一个函数
    return n * factorial(n - 1)

# 逐个验证：0!、1!、5!
for i in (0, 1, 3, 5):
    print(f"    {i}! = {factorial(i)}")

# 预期输出：
#     0! = 1
#     1! = 1
#     3! = 6
#     5! = 120


# 递归的"展开—回归"过程，用 5! 举例（心里走一遍）：
#   factorial(5) = 5 * factorial(4)
#                = 5 * (4 * factorial(3))
#                = 5 * (4 * (3 * factorial(2)))
#                = 5 * (4 * (3 * (2 * factorial(1))))
#                = 5 * (4 * (3 * (2 * 1)))          ← 走到终止条件 1
#                = 120                               ← 一层层算回来（回归）
print("    5! 的展开过程：5*4*3*2*1 = 120")
print("--- 2. 阶乘结束 ---")


# ===== 3. 斐波那契数列 =====

# 定义：F(0)=0, F(1)=1, 从 F(2) 开始，每项等于前两项之和：1,1,2,3,5,8,13,21...
def fib(n):
    """返回斐波那契数列的第 n 项（递归版）。"""
    # 两个终止条件：n 为 0 或 1 时直接返回
    if n == 0:
        return 0
    if n == 1:
        return 1

    # 递推关系：F(n) = F(n-1) + F(n-2)
    return fib(n - 1) + fib(n - 2)

# 打印前 10 项（0~9）
fib_list = [fib(i) for i in range(10)]
print(f"    斐波那契前 10 项: {fib_list}")

# 预期输出：斐波那契前 10 项: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# ⚠️ 性能提醒：上面的递归写法虽然优雅，但存在大量重复计算！
#    算 fib(35) 会调用自己上千万次，非常慢。
#    下面用循环版对比一下，同样的结果但快得多。
def fib_fast(n):
    """返回斐波那契数列的第 n 项（循环版，效率高）。"""
    # 处理边界情况
    if n < 2:
        return n

    # 用两个变量滚动保存前两项
    a, b = 0, 1
    for _ in range(n - 1):
        # 同时更新前两项：新的 a 是旧的 b，新的 b 是旧的 a+b
        a, b = b, a + b
    return b

print(f"    循环版 fib_fast(9) = {fib_fast(9)}（和递归版结果一致）")

# 预期输出：循环版 fib_fast(9) = 34（和递归版结果一致）
print("    ⚠️ 递归版 fib(35) 很慢，循环版 fib_fast(35) 瞬间完成 —— 这叫重复计算问题")
print("--- 3. 斐波那契结束 ---")


# ===== 4. 递归深度限制 =====

# Python 为了防止无限递归把内存吃爆，给递归层数设了上限。
current_limit = sys.getrecursionlimit()
print(f"    当前递归深度上限: {current_limit}")

# 预期输出：当前递归深度上限: 1000（不同环境可能略有不同）

# 可以用 sys.setrecursionlimit(n) 调整上限。
# ⚠️ 一般不建议随便调大：调太大可能真的把栈撑爆导致程序崩溃（段错误）。
#    只有在确认递归不会无限进行、且确实需要更深时，才适当调整。

def deep_count(n):
    """递归数到 n，用来测试能递归多深。"""
    # 用 % 100000 == 0 只打印里程碑，避免刷屏
    if n % 100000 == 0:
        print(f"    deep_count 已递归到 {n}")
    if n == 0:
        return 0
    return 1 + deep_count(n - 1)

# 先临时把上限调高一点，演示"深一点也能跑"
sys.setrecursionlimit(5000)
print(f"    临时调高上限后，deep_count(3000) = {deep_count(3000)}")

# 预期输出：临时调高上限后，deep_count(3000) = 3000

# 用完记得调回去，避免影响后续代码
sys.setrecursionlimit(current_limit)
print(f"    已恢复上限为: {sys.getrecursionlimit()}")

# 预期输出：已恢复上限为: 1000
print("--- 4. 递归深度限制结束 ---")


# ===== 5. ⚠️ 忘记终止条件 → RecursionError（安全演示） =====

# 下面这个函数故意写错：没有终止条件，参数还越变越大，会一直递归下去。
def broken_recursion(n):
    # ❌ 少了 if n == 0: return 这样的出口
    # 每次调用 n 还加 1，永远不会自然停下来
    return broken_recursion(n + 1)

# ⚠️ 千万不要直接 broken_recursion(0)，会让程序崩溃并打印巨大堆栈。
#    这里用 try/except 把它接住，安全地展示报错信息。
try:
    broken_recursion(0)
except RecursionError as e:
    # 捕获到 RecursionError，说明确实触发了递归深度超限
    print(f"    ✅ 已捕获到 RecursionError: {e}")
    print("    → 原因：函数缺少终止条件，无限递归撞上了递归深度上限")

# 预期输出：
#     ✅ 已捕获到 RecursionError: maximum recursion depth exceeded
#     → 原因：函数缺少终止条件，无限递归撞上了递归深度上限

# 💡 写递归前先问自己两个问题：
#    ① 终止条件是什么？（什么时候不用再递归了）
#    ② 每一次递归调用，有没有让问题离终止条件更近？（n 变小 / 列表变短）
#    两个问题答不上来，就别用递归。
print("--- 5. RecursionError 演示结束 ---")


# ===== 6. 递归 vs 循环：怎么选 =====

# 场景一：问题本身是"层层嵌套"的，用递归写更自然（如目录遍历、树结构）。
def sum_list_recursive(items):
    """递归求列表元素之和，用来展示"把大问题拆成小问题"的思路。"""
    # 终止条件：空列表的和是 0
    if not items:
        return 0
    # 把"求整个列表的和"拆成"第一个元素 + 剩下元素的和"
    return items[0] + sum_list_recursive(items[1:])

# 场景二：简单的重复动作，用循环更直观、更快、更省内存。
def sum_list_loop(items):
    """循环求列表元素之和。"""
    total = 0
    for x in items:
        total += x
    return total

nums = [1, 2, 3, 4, 5]
print(f"    递归求和: {sum_list_recursive(nums)}")
print(f"    循环求和: {sum_list_loop(nums)}")

# 预期输出：
#     递归求和: 15
#     循环求和: 15

# ✅ 选择建议：
#   - 数据是"树/嵌套结构" → 递归（代码短、思路清晰）
#   - 只是简单重复、追求性能 → 循环
#   - 递归层次可能很深 → 循环（避免 RecursionError）
print("--- 6. 递归 vs 循环结束 ---")


# ---------- 小结 ----------
# 1. 递归        → 函数自己调用自己
# 2. 两大要素    → 终止条件 + 每次递归都朝终止条件靠近（缺一不可）
# 3. 阶乘        → n! = n * (n-1)!，0! = 1
# 4. 斐波那契    → F(n) = F(n-1) + F(n-2)，⚠️ 朴素递归有大量重复计算，慢
# 5. 深度限制    → sys.getrecursionlimit() 查看，sys.setrecursionlimit() 调整（谨慎）
# 6. RecursionError → 忘记终止条件的必然结果；用 try/except 可以安全捕获
# 7. 选择        → 嵌套/树结构用递归，简单重复用循环
