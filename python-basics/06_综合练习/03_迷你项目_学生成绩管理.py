# -*- coding: utf-8 -*-
"""
本文件学什么：
    迷你项目一 —— 学生成绩管理系统。
    这是把前 5 章知识"组装成一个小软件"的示范：
        ① 变量    —— 用字典统一保存一个学生的信息
        ② 运算符  —— 比较、算术、成员判断
        ③ 表达式  —— 条件表达式定等级、推导式做筛选、f-string 格式化
        ④ 流程控制 —— for 遍历、if/elif/else 分支
        ⑤ 函数    —— 每个功能封装成一个函数，main() 负责串起来

运行方式：
    在 VSCode 里打开本文件，点右上角 ▶ 运行，
    或在终端执行：python 03_迷你项目_学生成绩管理.py

预计输出：
    一份完整的成绩报表，包含：全体学生明细表、班级统计
    （人数/平均分/最高分/最低分/及格率）、等级分布、前三名排行榜。
    全程 1 秒内结束，不需要任何输入。

重要说明：
    本项目的数据全部【硬编码】写在 STUDENTS 列表里，
    没有使用 input()，所以运行起来"唰"地一下就结束了。
    想练手的话，直接改 STUDENTS 里的数据即可，代码不用动。
"""

# ============================================================
# 一、模拟数据（硬编码，不用 input）
# ============================================================
# 每个学生是一个字典：name 姓名，scores 三科成绩
# 语文 chinese / 数学 math / 英语 english
STUDENTS = [
    {"name": "李明",   "chinese": 88, "math": 92, "english": 76},
    {"name": "王小雨", "chinese": 95, "math": 98, "english": 91},
    {"name": "张一",   "chinese": 62, "math": 55, "english": 70},
    {"name": "诸葛亮", "chinese": 100, "math": 100, "english": 99},
    {"name": "赵敏",   "chinese": 73, "math": 68, "english": 80},
    {"name": "陈浩",   "chinese": 45, "math": 58, "english": 52},
    {"name": "刘芳",   "chinese": 84, "math": 79, "english": 87},
    {"name": "孙悦",   "chinese": 91, "math": 85, "english": 93},
]

SUBJECTS = ["chinese", "math", "english"]
SUBJECT_CN = {"chinese": "语文", "math": "数学", "english": "英语"}

# 分隔线常量，用字符串乘法做，改一处全局生效
LINE = "=" * 62
THIN = "-" * 62


# ============================================================
# 二、工具函数：基础计算
# ============================================================

def total_score(student):
    """计算一个学生的总分。用生成器表达式一次求和，简洁又快。"""
    return sum(student[subject] for subject in SUBJECTS)


def average_score(student):
    """计算一个学生的平均分，保留 1 位小数。"""
    return round(total_score(student) / len(SUBJECTS), 1)


def get_level(avg):
    """
    根据平均分返回等级。
    这里用【条件表达式】写成一行，等价于下面被注释掉的 if/elif/else。
    """
    return "A" if avg >= 90 else ("B" if avg >= 80 else ("C" if avg >= 60 else "D"))
    # if avg >= 90:
    #     return "A"
    # elif avg >= 80:
    #     return "B"
    # elif avg >= 60:
    #     return "C"
    # else:
    #     return "D"


def is_pass(avg):
    """判断是否及格：平均分 >= 60 分。"""
    return avg >= 60


# ============================================================
# 三、工具函数：班级级统计
# ============================================================

def class_average(students):
    """班级平均分（所有人平均分的再平均）。"""
    if not students:
        return 0.0
    return round(sum(average_score(s) for s in students) / len(students), 1)


def top_student(students, subject=None):
    """
    找出分数最高的学生。
    subject=None 时按【总分】比；传了科目名就按那一科比。
    """
    if not students:
        return None
    if subject is None:
        return max(students, key=total_score)
    return max(students, key=lambda s: s[subject])


def lowest_student(students):
    """找出平均分最低的学生。"""
    if not students:
        return None
    return min(students, key=average_score)


def pass_rate(students):
    """及格率，返回百分比数值（保留 1 位小数）。"""
    if not students:
        return 0.0
    passed = [s for s in students if is_pass(average_score(s))]   # 推导式筛选
    return round(len(passed) / len(students) * 100, 1)


def level_distribution(students):
    """
    统计各等级人数，返回 {"A": 2, "B": 3, ...} 这样的字典。
    用字典推导式 + list.count 一次生成。
    """
    levels = [get_level(average_score(s)) for s in students]
    return {lv: levels.count(lv) for lv in ["A", "B", "C", "D"]}


def rank_students(students):
    """按总分从高到低排序，返回新列表（不改动原列表）。"""
    return sorted(students, key=total_score, reverse=True)


def subject_average(students, subject):
    """某一科的全班平均分。"""
    if not students:
        return 0.0
    return round(sum(s[subject] for s in students) / len(students), 1)


# ============================================================
# 四、打印函数：只负责"显示"，不负责"计算"
# ============================================================

def print_report_header(title):
    """打印一个统一样式的标题。"""
    print(LINE)
    print(title.center(60))
    print(LINE)


def print_student_table(students):
    """打印全体学生成绩明细表。"""
    print()
    print("【全体学生成绩明细】")
    # 表头：< 左对齐，> 右对齐，数字控制宽度
    print(f"{'姓名':<8}{'语文':>6}{'数学':>6}{'英语':>6}{'总分':>6}{'平均分':>8}{'等级':>6}")
    print(THIN)
    for s in students:
        print(
            f"{s['name']:<8}"
            f"{s['chinese']:>6}"
            f"{s['math']:>6}"
            f"{s['english']:>6}"
            f"{total_score(s):>6}"
            f"{average_score(s):>8.1f}"
            f"{get_level(average_score(s)):>6}"
        )
    print(THIN)


def print_class_stats(students):
    """打印班级整体统计。"""
    print()
    print("【班级整体统计】")
    print(f"  班级人数     ：{len(students)} 人")
    print(f"  班级平均分   ：{class_average(students)}")
    print(f"  及格人数     ：{sum(1 for s in students if is_pass(average_score(s)))} 人"
          f"（及格率 {pass_rate(students)}%）")

    for subject in SUBJECTS:
        avg = subject_average(students, subject)
        best = top_student(students, subject)
        print(f"  {SUBJECT_CN[subject]}平均分：{avg:<6}"
              f"（最高分 {best[subject]} 分，由 {best['name']} 取得）")


def print_level_distribution(students):
    """打印等级分布，用 █ 画一个简单的横向条形图。"""
    print()
    print("【等级分布】（A≥90，B≥80，C≥60，D<60）")
    dist = level_distribution(students)
    for level in ["A", "B", "C", "D"]:
        count = dist[level]
        bar = "█" * count                      # 字符串乘法画条形
        percent = round(count / len(students) * 100, 1)
        print(f"  {level} 档：{bar:<10} {count} 人 ({percent}%)")


def print_ranking(students, top_n=3):
    """打印总分排行榜前 N 名。"""
    print()
    print(f"【总分排行榜 Top {top_n}】")
    ranked = rank_students(students)
    medals = ["🥇", "🥈", "🥉"]                # 前三名的奖牌
    for i, s in enumerate(ranked[:top_n]):
        medal = medals[i] if i < len(medals) else f"{i + 1}."
        print(f"  {medal} {s['name']:<8}总分 {total_score(s):>3} 分，"
              f"平均 {average_score(s):>5.1f} 分，等级 {get_level(average_score(s))}")


def print_highlights(students):
    """打印几个亮点：最高分学生、最低分学生、需要关注的学生。"""
    print()
    print("【重点关注】")

    best = top_student(students)
    worst = lowest_student(students)
    print(f"  表现最好：{best['name']}（总分 {total_score(best)} 分，"
          f"平均 {average_score(best)} 分）")
    print(f"  需要加油：{worst['name']}（总分 {total_score(worst)} 分，"
          f"平均 {average_score(worst)} 分）")

    # 用推导式找出所有不及格的同学
    fail_names = [s["name"] for s in students if not is_pass(average_score(s))]
    if fail_names:
        print(f"  不及格名单：{'、'.join(fail_names)}（共 {len(fail_names)} 人）")
    else:
        print("  全班都及格了，太棒了！")


# ============================================================
# 五、主流程：把所有函数串起来
# ============================================================

def main():
    """程序的入口函数，只负责按顺序调用上面写好的各个函数。"""
    print_report_header("学生成绩管理系统")
    print(f"数据来源：代码内硬编码模拟数据（未使用 input，运行瞬间完成）")

    # 1. 明细表
    print_student_table(STUDENTS)

    # 2. 班级统计
    print_class_stats(STUDENTS)

    # 3. 等级分布
    print_level_distribution(STUDENTS)

    # 4. 排行榜
    print_ranking(STUDENTS, top_n=3)

    # 5. 重点关注
    print_highlights(STUDENTS)

    print()
    print(LINE)
    print("报表生成完毕。".center(60))
    print("试试把最上面的 STUDENTS 改成你自己的数据，再运行一次！".center(46))
    print(LINE)


# ============================================================
# 六、程序入口
# ============================================================
# 下面这一行的意思是："只有直接运行本文件时才执行 main()"。
# 如果这个文件被别的文件 import 进去，main() 就不会自动跑。
if __name__ == "__main__":
    main()
