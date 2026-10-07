# -*- coding: utf-8 -*-
"""
================ 练习题 · 参考答案（10 题） ================

【怎么用】
  先自己做 练习题.py，写完了再来对答案。
  本文件是"可以直接运行"的完整版，运行后会打印每题的结果。

【运行】
      python 练习题_答案.py

【预计输出】
  每题结果都有 "【题 X】" 的前缀，方便对照。最后打印解题要点小结。
"""

print("========== 练习题参考答案 ==========\n")


# ========== 题 1：变量赋值与命名 ==========
# 要点：snake_case 命名；赋值用 =；重新赋值会覆盖旧值。

my_name = "小明"
my_age = 18
my_height = 1.75

# 第一次打印：年龄 18
print("【题 1】变量赋值与命名")
print(f"    我叫 {my_name}，今年 {my_age} 岁，身高 {my_height} 米")

# 预期输出：我叫 小明，今年 18 岁，身高 1.75 米

# 重新赋值：把标签 my_age 换贴到新对象 20 上
my_age = 20
print(f"    修改后：我叫 {my_name}，今年 {my_age} 岁，身高 {my_height} 米")

# 预期输出：修改后：我叫 小明，今年 20 岁，身高 1.75 米
print()


# ========== 题 2：基本数据类型与 type() ==========
# 要点：type(x).__name__ 返回类型名的字符串。

v1 = 123
v2 = 4.56
v3 = "你好"
v4 = True

print("【题 2】基本数据类型与 type()")
print(f"    123 的类型是 {type(v1).__name__}")

# 预期输出：123 的类型是 int
print(f"    4.56 的类型是 {type(v2).__name__}")

# 预期输出：4.56 的类型是 float
print(f"    '你好' 的类型是 {type(v3).__name__}")

# 预期输出：'你好' 的类型是 str
print(f"    True 的类型是 {type(v4).__name__}")

# 预期输出：True 的类型是 bool
print()


# ========== 题 3：int() 转换与截断 ==========
# 要点：int("42") 可用；int(3.99) 是截断（向 0 取整），不是四舍五入。

print("【题 3】int() 转换与截断")
num_from_str = int("42")
print(f"    int('42') + 8 = {num_from_str + 8}")

# 预期输出：int('42') + 8 = 50
print(f"    int(3.99) = {int(3.99)}   ← 截断，不是四舍五入")

# 预期输出：int(3.99) = 3   ← 截断，不是四舍五入
print(f"    int(-3.99) = {int(-3.99)}   ← 向 0 方向截断")

# 预期输出：int(-3.99) = -3   ← 向 0 方向截断
print()


# ========== 题 4：⚠️ int("3.5") 报错的处理 ==========
# 要点：带小数点的字符串不能直接 int()，要先 float() 再 int()。

print("【题 4】int('3.5') 报错的处理")
try:
    int("3.5")
except ValueError:
    # 捕获到异常后给出友好提示，而不是让程序崩掉
    print("    转换失败：字符串带小数点，需要先转 float")

# 预期输出：转换失败：字符串带小数点，需要先转 float

# 正确姿势：两步走
result = int(float("3.5"))
print(f"    int(float('3.5')) = {result}")

# 预期输出：int(float('3.5')) = 3
print()


# ========== 题 5：bool() 真值判断陷阱 ==========
# 要点：⚠️ 字符串只看"空不空"，完全不看内容。"0"、"False" 都是非空字符串 → True。

empty_str = ""
space_str = " "
zero_str = "0"
false_str = "False"
zero_int = 0
zero_float = 0.0
none_val = None

print("【题 5】bool() 真值判断陷阱")
print(f"    bool('')      = {bool(empty_str)}")

# 预期输出：bool('')      = False
print(f"    bool(' ')     = {bool(space_str)}   ← 有空格，非空即真")

# 预期输出：bool(' ')     = True   ← 有空格，非空即真
print(f"    bool('0')     = {bool(zero_str)}   ← ⚠️ 非空字符串就是真")

# 预期输出：bool('0')     = True   ← ⚠️ 非空字符串就是真
print(f"    bool('False') = {bool(false_str)}   ← ⚠️ 内容写着 False 也没用")

# 预期输出：bool('False') = True   ← ⚠️ 内容写着 False 也没用
print(f"    bool(0)       = {bool(zero_int)}")

# 预期输出：bool(0)       = False
print(f"    bool(0.0)     = {bool(zero_float)}")

# 预期输出：bool(0.0)     = False
print(f"    bool(None)    = {bool(none_val)}")

# 预期输出：bool(None)    = False

# 总结：只有"空串、空容器、数字 0、None"这四类才是 False，其余一律 True。
# ⚠️ 特别注意：字符串的 '0' 和 'False' 都是 True，因为它们不是空字符串。
print()


# ========== 题 6：字符串与数字转换拼接 ==========
# 要点：str + int 会 TypeError；必须用 str() 或 f-string。

score = 95
total = 100

print("【题 6】字符串与数字转换拼接")

# 方式一：str() 手动转换
way1 = "得分：" + str(score) + " / " + str(total)
print(f"    方式一（str 拼接）：{way1}")

# 预期输出：方式一（str 拼接）：得分：95 / 100

# 方式二：f-string 自动转换（推荐）
way2 = f"得分：{score} / {total}"
print(f"    方式二（f-string）：{way2}")

# 预期输出：方式二（f-string）：得分：95 / 100
print()


# ========== 题 7：赋值即引用 / 复制 ==========
# 要点：b = a 只是贴标签，共享同一个列表；切片 [:] 才创建新对象。

fruits = ["苹果", "香蕉"]
alias = fruits            # 贴标签，不是复制
alias.append("橙子")

print("【题 7】赋值即引用 / 复制")
print(f"    alias 追加后 fruits = {fruits}   ← 被影响了，因为是同一个列表")

# 预期输出：alias 追加后 fruits = ['苹果', '香蕉', '橙子']   ← 被影响了，因为是同一个列表
print(f"    fruits is alias ？{fruits is alias}")

# 预期输出：fruits is alias ？True

# 切片复制：得到一个独立的新列表
copy_fruits = fruits[:]
copy_fruits.append("葡萄")
print(f"    复制后 fruits      = {fruits}   ← 不受影响")

# 预期输出：复制后 fruits      = ['苹果', '香蕉', '橙子']   ← 不受影响
print(f"    复制后 copy_fruits = {copy_fruits}")

# 预期输出：复制后 copy_fruits = ['苹果', '香蕉', '橙子', '葡萄']
print(f"    fruits is copy_fruits ？{fruits is copy_fruits}")

# 预期输出：fruits is copy_fruits ？False
print()


# ========== 题 8：多重赋值与变量交换 ==========
# 要点：a, b, c = 1, 2, 3；交换 a, c = c, a；拆包 px, py = (100, 200)。

print("【题 8】多重赋值与变量交换")

a, b, c = 1, 2, 3
print(f"    赋值后：a={a}, b={b}, c={c}")

# 预期输出：赋值后：a=1, b=2, c=3

a, c = c, a
print(f"    交换 a 和 c 后：a={a}, b={b}, c={c}")

# 预期输出：交换 a 和 c 后：a=3, b=2, c=1

x, y = (100, 200)
print(f"    拆包后：x={x}, y={y}")

# 预期输出：拆包后：x=100, y=200
print()


# ========== 题 9：== 与 is 的区别 ==========
# 要点：== 比"值"，is 比"是不是同一个对象"。

list1 = [1, 2]
list2 = [1, 2]
list3 = list1

print("【题 9】== 与 is 的区别")
print(f"    list1 == list2 ？{list1 == list2}   ← 内容一样，值为 True")

# 预期输出：list1 == list2 ？True   ← 内容一样，值为 True
print(f"    list1 is list2 ？{list1 is list2}   ← 是两个不同的对象")

# 预期输出：list1 is list2 ？False   ← 是两个不同的对象
print(f"    list1 is list3 ？{list1 is list3}   ← list3 就是 list1 本身")

# 预期输出：list1 is list3 ？True   ← list3 就是 list1 本身

# 结论：判断值相等用 ==；判断是不是同一个对象用 is（常用于 is None）。
print()


# ========== 题 10：del 与内存回收理解 ==========
# 要点：del 删的是"名字"；只要还有别的名字引用，对象就不会被回收。

msg = "临时数据"
print("【题 10】del 与内存回收理解")
print(f"    创建 msg = {msg}")

# 预期输出：创建 msg = 临时数据

backup = msg              # 第二张标签指向同一个字符串
del msg                   # 撕掉 msg 这张标签

# msg 这个名字没了，但 backup 还在，所以数据依然可以访问
print(f"    del msg 之后，backup 依然可用 = {backup}")

# 预期输出：del msg 之后，backup 依然可用 = 临时数据

# 验证 msg 真的没了
try:
    print(msg)
except NameError:
    print("    访问 msg 报错 NameError：名字已被 del 删除")

# 预期输出：访问 msg 报错 NameError：名字已被 del 删除

# 回答：del msg 之后，"临时数据"这个字符串还在内存里吗？
#   ✅ 还在。因为 backup 还引用着它，引用计数不为 0，所以不会被回收。
#   如果没有任何变量引用它（引用计数为 0），Python 才会自动回收。
print()


# ========== 解题要点小结 ==========
print("========== 解题要点小结 ==========")
print("  1. 命名用 snake_case，赋值用 =，重新赋值会覆盖旧值")
print("  2. type(x).__name__ 查看类型名")
print("  3. int(小数) 是截断不是四舍五入；int('42') 可以，int('3.5') 报错")
print("  4. 带小数点字符串先 float 再 int：int(float('3.5')) = 3")
print("  5. bool() 只有空串/空容器/0/None 是 False；'0' 和 'False' 都是 True")
print("  6. 字符串拼数字用 str() 或 f-string")
print("  7. b = a 是共享；要独立副本用 a[:]")
print("  8. 多重赋值、一行交换、拆包")
print("  9. == 比值，is 比对象身份")
print(" 10. del 删标签不删数据；无人引用才回收")
print("==================================")
