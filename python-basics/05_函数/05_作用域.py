"""
================ 05 作用域 ================

【本文件学什么】
  1. 局部作用域（Local）：函数内部定义的变量，外面看不见
  2. 全局作用域（Global）：模块最外层定义的变量
  3. LEGB 查找规则：Local → Enclosing → Global → Built-in
  4. global 关键字：在函数内修改全局变量（以及为什么不推荐滥用）
  5. nonlocal 关键字：在内层函数修改外层函数的变量（闭包初识）

【怎么运行】
      python 05_作用域.py

【预计输出】
  依次看到 6 个分节结果，最后打印小结。
"""


# ===== 1. 局部变量：只在函数内部存活 =====

def local_demo():
    # local_var 在函数内部创建，属于"局部变量"
    local_var = "我是局部变量"
    print(f"    函数内部可以访问: {local_var}")

local_demo()

# 预期输出：函数内部可以访问: 我是局部变量

# ⚠️ 函数执行完毕后，局部变量就被销毁了，外面访问会报 NameError。
# 下面这行如果取消注释就会崩：
#     NameError: name 'local_var' is not defined
# print(local_var)
print("  函数执行完后，local_var 已经不存在了（外面访问会报 NameError）")
print("--- 1. 局部变量结束 ---")


# ===== 2. 全局变量：模块最外层定义，到处能"读" =====

# 在函数外面（顶层）定义的变量是"全局变量"
global_counter = 100

def read_global():
    # 函数内"读取"全局变量是可以的，不需要任何声明
    print(f"    函数内读取全局变量: global_counter = {global_counter}")

read_global()

# 预期输出：函数内读取全局变量: global_counter = 100

# ⚠️ 但"读取"和"修改"是两码事。看下面这个函数：
def shadow_global():
    # 这里看似在"修改"，其实是 Python 创建了一个新的局部变量，
    # 它只是把全局的同名变量"遮住"了（这叫变量遮蔽 / shadowing）
    global_counter = 999
    print(f"    函数内的 global_counter = {global_counter}（这是局部变量！）")

print(f"  调用前，全局的 global_counter = {global_counter}")

# 预期输出：调用前，全局的 global_counter = 100

shadow_global()

# 预期输出：函数内的 global_counter = 999（这是局部变量！）

# 全局变量纹丝不动 —— 这是新手最容易困惑的地方
print(f"  调用后，全局的 global_counter = {global_counter}（没变！）")

# 预期输出：调用后，全局的 global_counter = 100（没变！）
print("--- 2. 全局变量结束 ---")


# ===== 3. LEGB 规则：Python 到底去哪找变量？ =====

# L (Local)     → 当前函数内部
# E (Enclosing) → 外层嵌套函数（闭包）
# G (Global)    → 模块最外层
# B (Built-in)  → Python 内置（如 len、print、sum）

# 先定义一个全局的 tag，用来观察查找顺序
tag = "全局 tag"

def legb_demo():
    # 函数内又定义了一个同名的 tag
    tag = "局部 tag"
    # Python 从 Local 开始找，找到就用，所以打印的是"局部 tag"
    print(f"    legb_demo 里看到的是: {tag}（命中 L 层）")

legb_demo()

# 预期输出：legb_demo 里看到的是: 局部 tag（命中 L 层）

# 没被局部遮蔽的地方，看到的就是全局的
print(f"  函数外面看到的是: {tag}（命中 G 层）")

# 预期输出：函数外面看到的是: 全局 tag（命中 G 层）

# B 层（内置）示例：len、sum 这些名字你没定义过，Python 在 Built-in 层找到了
# 下面这行如果没定义 len 也没用内置的，就会报 NameError
print(f"  内置函数 len('abc') = {len('abc')}（命中 B 层）")

# 预期输出：内置函数 len('abc') = 3（命中 B 层）
print("--- 3. LEGB 规则结束 ---")


# ===== 4. global：真的想改全局变量时 =====

# 在函数内用 global 声明后，赋值操作才会作用到全局变量上。
app_name = "我的程序"

def rename_app():
    # 声明：我要修改的是"全局的" app_name，不是新建局部变量
    global app_name
    app_name = "改名后的程序"

print(f"  改名前的全局 app_name = {app_name}")

# 预期输出：改名前的全局 app_name = 我的程序

rename_app()

# 这次真的变了
print(f"  改名后的全局 app_name = {app_name}")

# 预期输出：改名后的全局 app_name = 改名后的程序


# ⚠️⚠️ 为什么"尽量避免滥用" global？看这个例子：
total = 0

def add_to_total_bad(n):
    # 这个函数通过修改全局变量来"返回"结果，调用者完全看不出它的副作用！
    global total
    total += n

# 调用它，外界状态被悄悄改变了
add_to_total_bad(5)
add_to_total_bad(10)
print(f"  滥用 global 后 total = {total}（外界状态被悄悄改动）")

# 预期输出：滥用 global 后 total = 15（外界状态被悄悄改动）

# ✅ 推荐的写法：用参数传入、用返回值传出，数据流向一目了然
def add_numbers(values):
    """接收一个列表，返回它们的和。同样的事，但没有任何隐藏副作用。"""
    return sum(values)

result = add_numbers([5, 10])
print(f"  推荐写法得到 result = {result}（从返回值拿到，一目了然）")

# 预期输出：推荐写法得到 result = 15（从返回值拿到，一目了然）

# 滥用 global 的三大危害（重要！）：
#   1. 数据流不可追踪：调用一个函数竟然会改变远处的变量，排查 bug 极痛苦
#   2. 函数不可复用：它依赖外部环境，换个地方用就出错
#   3. 难以测试：必须先把全局环境摆好才能测这个函数
# 💡 原则：只要能通过"参数传入 + 返回值传出"做到，就不要用 global。
print("--- 4. global 结束 ---")


# ===== 5. nonlocal：修改外层嵌套函数的变量 =====

# nonlocal 用于嵌套函数场景：内层函数想修改"外层函数的变量"（不是全局的）。
def outer_counter():
    count = 0            # count 属于 outer_counter 这个"外层函数"的局部变量

    def inner():
        # 声明：我要改的是外层的 count
        nonlocal count
        count += 1
        return count

    # 这里连续调用内层函数，观察 count 是否累加
    print(f"    第 1 次调用 inner(): {inner()}")
    print(f"    第 2 次调用 inner(): {inner()}")
    print(f"    第 3 次调用 inner(): {inner()}")

outer_counter()

# 预期输出：
#     第 1 次调用 inner(): 1
#     第 2 次调用 inner(): 2
#     第 3 次调用 inner(): 3

# 💡 nonlocal 的存在意义：Python 里"闭包"（内层函数记住外层变量）需要它来写"计数器"这类逻辑。
#    如果不用 nonlocal 而直接写 count += 1，会报：
#    UnboundLocalError: cannot access local variable 'count' where it is not associated with a value
print("--- 5. nonlocal 结束 ---")


# ===== 6. 全局变量的"隐藏"现象与命名建议 =====

# ⚠️ 经典报错场景：函数里既有赋值、又想先读取同名全局变量 → UnboundLocalError
size = 10

def tricky():
    # 因为这行赋值，Python 在"编译时"就把 size 判定为局部变量，
    # 于是上一行的 print 在局部里找不到它 → 报错。
    # 下面两行如果取消注释，运行就会崩：
    #     UnboundLocalError: cannot access local variable 'size'
    # print(size)
    # size = 20
    print("    这个函数里的 size 被判定为局部变量，先读后写会报 UnboundLocalError")

tricky()

# 预期输出：这个函数里的 size 被判定为局部变量，先读后写会报 UnboundLocalError

# ✅ 命名建议：全局变量用全大写，一眼区分，减少遮蔽风险
MAX_RETRY = 3
DEFAULT_TIMEOUT = 30

def show_config():
    # 全大写的名字一看就是"全局常量"，不会和局部变量混淆
    print(f"    配置：MAX_RETRY={MAX_RETRY}, DEFAULT_TIMEOUT={DEFAULT_TIMEOUT}")

show_config()

# 预期输出：配置：MAX_RETRY=3, DEFAULT_TIMEOUT=30
print("--- 6. 命名建议结束 ---")


# ---------- 小结 ----------
# 1. 局部变量   → 函数内创建，函数外访问会 NameError
# 2. 全局变量   → 顶层定义，函数内可直接"读"，但不能直接"写"
# 3. LEGB       → Local → Enclosing → Global → Built-in，由内向外找
# 4. global     → 声明后才能修改全局变量；⚠️ 滥用会让数据流不可追踪，尽量别用
# 5. nonlocal   → 修改外层嵌套函数的变量，写闭包/计数器时用
# 6. 命名习惯   → 全局常量用全大写，避免与局部变量撞名
# 💡 黄金原则：优先"参数传入 + 返回值传出"，最后才考虑 global / nonlocal。
