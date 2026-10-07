# -*- coding: utf-8 -*-
"""
本文件学什么：
    迷你项目二 —— 猜数字游戏。
    正常的猜数字游戏要用 input() 让人输入，但那样程序会卡住等输入，
    不适合自动演示。这里的做法是：
        用 random 生成目标数字（固定随机种子，保证每次结果一样），
        用【预设的猜测序列列表】模拟玩家的输入，
        自动把一整局跑完，并打印每一次"大了 / 小了"的过程。

    知识点覆盖：
        ① 变量    —— 记录猜测次数、当前猜测值
        ② 运算符  —— 比较运算符 > < ==、算术、逻辑 and
        ③ 表达式  —— 条件表达式 + f-string 格式化
        ④ 流程控制 —— for 遍历猜测序列、if/elif/else、break
        ⑤ 函数    —— 把比较逻辑、回合执行、结果展示都封装成函数

运行方式：
    在 VSCode 里打开本文件，点右上角 ▶ 运行，
    或在终端执行：python 04_迷你项目_猜数字游戏.py

预计输出：
    三局游戏的完整对战过程：
      第 1 局：目标数 1~100，用二分法（每次砍掉一半范围，最多 7 次必中）
      第 2 局：目标数 1~50，用预设的玩家猜测序列（含超范围输入，演示边界校验）
      第 3 局：目标数 1~30，用"笨办法"从 1 开始一个个猜（演示算法与运气的差别）
    每局结束打印总结，最后打印总战绩。
    全程 1 秒内结束，绝对不会卡住等你输入。

重要说明：
    本文件【没有】任何 input()，也没有可能死循环的 while True。
    想换个目标数字？改 `random.seed(42)` 里的数字即可。
"""

import random

# 把随机种子固定住，这样每次运行生成的"神秘数字"都一样，
# 学习时输出才能复现、方便对照。
random.seed(42)

LINE = "=" * 56
THIN = "-" * 56


# ============================================================
# 一、核心逻辑函数
# ============================================================

def compare(guess, target):
    """
    比较猜测值和目标值，返回 (结果代号, 中文提示)。
    这就是游戏最核心的一行逻辑，单独抽出来方便复用和测试。
    """
    if guess > target:
        return "high", "大了 ↓"
    elif guess < target:
        return "low", "小了 ↑"
    else:
        return "hit", "猜中啦 🎉"


def validate(guess, low, high):
    """
    校验猜测值是否在合法范围内。
    返回 (是否合法, 提示文字)。
    """
    if guess < low or guess > high:
        return False, f"超出范围（应在 {low}~{high} 之间），本次作废"
    return True, ""


def play_round(round_no, target, low, high, guesses=None, strategy_name="",
               max_attempts=None):
    """
    执行一局游戏。

    参数：
        round_no      第几局（用于显示）
        target        本局的目标数字
        low, high     合法猜测范围
        guesses       预设的猜测序列（模拟玩家输入）。
                      传 None 表示"由程序根据每次的反馈实时决定下一次猜什么"，
                      即真正的二分法（见下面 binary_next）。
        strategy_name 策略名称（用于显示）
        max_attempts  最多猜多少次；None 表示不限制
                       （前提是 guesses 有限，或者用了二分法）

    返回：
        (是否成功, 实际有效猜测次数, 用到的猜测列表)
    """
    print()
    print(LINE)
    print(f"第 {round_no} 局 | 范围 {low}~{high} | 策略：{strategy_name}")
    print(LINE)

    attempts = 0          # 真正生效的猜测次数
    used = []             # 记录有效猜测，最后展示
    hit = False           # 是否命中

    # 下面是"猜什么"的来源，分两种情况：
    #   1. guesses 传了列表  -> 用预设序列（模拟真人玩家）
    #   2. guesses 是 None   -> 用二分法生成器，靠反馈实时决定下一次猜什么
    if guesses is not None:
        # ---- 情况 1：预设序列模式 ----
        for guess in guesses:
            if max_attempts is not None and attempts >= max_attempts:
                print(f"  （已达到本局最多 {max_attempts} 次的上限，停止猜测）")
                break

            # 先校验，非法猜测不计入次数
            ok, msg = validate(guess, low, high)
            if not ok:
                print(f"  第 {attempts + 1:>2} 次：猜 {guess:>3}  ->  {msg}")
                continue

            attempts += 1
            used.append(guess)
            result, text = compare(guess, target)
            print(f"  第 {attempts:>2} 次：猜 {guess:>3}  ->  {text}")

            if result == "hit":
                hit = True
                break     # 猜中了就跳出循环，不再继续猜

    else:
        # ---- 情况 2：二分法模式（迭代器 + send 反馈） ----
        guesser = binary_next(low, high)
        try:
            guess = next(guesser)          # 第一次启动，拿到第一个中间值
        except StopIteration:
            guess = None

        while guess is not None:
            if max_attempts is not None and attempts >= max_attempts:
                print(f"  （已达到本局最多 {max_attempts} 次的上限，停止猜测）")
                break

            attempts += 1
            used.append(guess)
            result, text = compare(guess, target)
            print(f"  第 {attempts:>2} 次：猜 {guess:>3}  ->  {text}")

            if result == "hit":
                hit = True
                break

            # 把"大了/小了"的结果送回生成器，让它决定下一次猜哪里
            try:
                guess = guesser.send(result)
            except StopIteration:
                guess = None

    # 本局收尾
    print(THIN)
    if hit:
        print(f"  结果：命中！目标数字就是 {target}，共猜了 {attempts} 次")
        print(f"  过程：{' -> '.join(str(g) for g in used)}")
    else:
        print(f"  结果：猜测次数用完了，还没猜中 😢")
        print(f"  目标数字其实是 {target}，共猜了 {attempts} 次")

    return hit, attempts, used


# ============================================================
# 二、游戏策略：生成预设的猜测序列
# ============================================================

def binary_next(low, high):
    """
    真正的二分法猜想器：每次都猜当前范围的正中间。

    这是一个【生成器函数】（用 yield 而不是 return）。
    它的特点是：每次被取一个值，就会"暂停"在那里，
    等下一次再取值时，才继续往下执行。

    关键点：它不知道目标数字是多少，只能靠外面把
    "大了 / 小了" 的结果通过 send() 告诉它，
    然后它据此把范围砍掉一半——这才是二分法的精髓。

    1~100 的范围，最多 7 次必然命中（2 的 7 次方是 128）。
    """
    lo, hi = low, high
    while lo <= hi:
        mid = (lo + hi) // 2      # 猜中间值
        feedback = yield mid      # 把 mid 交出去，并等对方把结果送回来

        if feedback == "low":     # 猜小了，目标在右半边
            lo = mid + 1
        elif feedback == "high":  # 猜大了，目标在左半边
            hi = mid - 1
        else:
            return                # 猜中了，结束


def dumb_guesses(low, high):
    """笨办法：从 low 开始一个一个往上猜（最多猜 40 次，避免输出太长）。"""
    return list(range(low, min(high, low + 40) + 1))


def custom_guesses():
    """
    手写一串猜测值（模拟真人玩家随手猜）。
    故意混入两个超出范围的值，用来演示边界校验。
    目标数字是 8，所以最后会猜到它。
    """
    return [25, 50, 999, 12, 0, 5, 9, 7, 8]


# ============================================================
# 三、入口：串起三局不同风格的对战
# ============================================================

def main():
    print(LINE)
    print("猜数字游戏".center(52))
    print("用预设猜测序列模拟玩家，无需输入，自动跑完整局".center(40))
    print(LINE)
    print(f"随机种子已固定为 42，所以每局的目标数字每次都一样，输出可复现。")

    # ---------- 第 1 局：二分法，范围 1~100 ----------
    # guesses=None 表示不用预设序列，改用二分法生成器实时决策
    target1 = random.randint(1, 100)
    hit1, tries1, _ = play_round(
        round_no=1,
        target=target1,
        low=1,
        high=100,
        guesses=None,
        strategy_name="二分法（每次砍掉一半范围）",
    )

    # ---------- 第 2 局：手动预设序列，范围 1~50，含非法输入 ----------
    target2 = random.randint(1, 50)
    hit2, tries2, _ = play_round(
        round_no=2,
        target=target2,
        low=1,
        high=50,
        guesses=custom_guesses(),
        strategy_name="真人式乱猜（预设序列 + 一次超范围输入）",
    )

    # ---------- 第 3 局：笨办法，范围 1~30 ----------
    # 目标数字是 1，所以从 1 开始猜会一次命中；这局用来对比"运气"和"算法"
    target3 = 1
    hit3, tries3, _ = play_round(
        round_no=3,
        target=target3,
        low=1,
        high=30,
        guesses=dumb_guesses(1, 30),
        strategy_name="笨办法（从 1 往上一个个猜）",
    )

    # ---------- 总战绩 ----------
    print()
    print(LINE)
    print("总战绩".center(52))
    print(LINE)

    results = [hit1, hit2, hit3]
    wins = sum(1 for r in results if r)
    print(f"  总局数：3")
    print(f"  获胜局数：{wins}")
    print(f"  第 1 局用了 {tries1} 次（二分法，稳扎稳打）")
    print(f"  第 2 局用了 {tries2} 次（乱猜，效率不稳定）")
    print(f"  第 3 局用了 {tries3} 次（笨办法，全靠运气）")

    # 用条件表达式给出一句评价
    if tries1 <= 7:
        comment = f"二分法只用 {tries1} 次就搞定 1~100，这就是算法的力量！"
    else:
        comment = "这局二分法发挥不太理想，检查一下范围更新逻辑。"
    print()
    print(f"  点评：{comment}")
    print("  结论：范围越大，好算法和笨办法的差距就越明显。")
    print("        1~100 用二分法最多 7 次必中，笨办法最坏要 100 次。")
    print()
    print("试试把 random.seed(42) 改成别的数字，看看目标数字会变成几。")
    print(LINE)


if __name__ == "__main__":
    main()
