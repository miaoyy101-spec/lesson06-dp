# -*- coding: utf-8 -*-
"""第 6 次课 独立研究任务（选做）。

① 回溯法：n-后问题是什么，与动规“穷举”有何不同
② 完全背包（物品可重复）改哪一行
③ 分支限界：一句话 + 比回溯好在哪里
"""

# ---------- ① n-后问题：回溯法 ----------

def n_queens(n):
    """逐行放皇后，放不下就回退一行，统计解的个数与第一个解。"""
    cols, d1, d2 = set(), set(), set()      # 列、主对角线、副对角线占用情况
    pos, first, count = [], None, 0

    def place(row):
        nonlocal count, first
        if row == n:
            count += 1
            if first is None:
                first = pos.copy()
            return
        for col in range(n):
            if col in cols or (row - col) in d1 or (row + col) in d2:
                continue                     # 这个位置被攻击，换下一列
            cols.add(col); d1.add(row - col); d2.add(row + col); pos.append(col)
            place(row + 1)                   # 递归放下行
            cols.remove(col); d1.remove(row - col); d2.remove(row + col); pos.pop()  # 回退
    place(0)
    return count, first


def n_queens_bruteforce_states(n):
    """对照：不放回的全排列穷举，要试 n! 种摆法（8 后 = 40320，12 后 = 4.79 亿）。"""
    import math
    return math.factorial(n)


# ---------- ② 完全背包：只改循环方向 ----------

ITEMS = [("帐篷", 300, 90), ("炉具", 200, 60), ("睡袋", 350, 105),
         ("食物", 400, 120), ("水具", 250, 90)]


def knapsack_01(items, capacity):
    """0-1 背包（一维滚动数组写法）：容量必须从大到小走。"""
    dp = [0] * (capacity + 1)
    for _, w, v in items:
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]


def knapsack_complete(items, capacity):
    """完全背包（物品可重复拿）：只把容量改成从小到大走，其余一行不动。"""
    dp = [0] * (capacity + 1)
    for _, w, v in items:
        for c in range(w, capacity + 1):     # <- 唯一区别：正序，允许同一件被反复用
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]


# ---------- ③ 分支限界：与纯回溯对比搜索结点数 ----------

def dfs_nodes(items, capacity):
    """纯回溯（暴力枚举带/不带），返回搜索结点数。"""
    nodes = 0

    def dfs(i, c, v):
        nonlocal nodes
        nodes += 1
        if i == len(items):
            return v
        best = dfs(i + 1, c, v)              # 不带
        if c >= items[i][1]:
            best = max(best, dfs(i + 1, c - items[i][1], v + items[i][2]))  # 带
        return best
    best = dfs(0, capacity, 0)
    return best, nodes


def bab_nodes(items, capacity):
    """分支限界：先按性价比排序，用“剩余容量全按最高性价比估上界”，
    上界还不如当前最优就整枝剪掉。返回 (最优值, 搜索结点数)。"""
    order = sorted(items, key=lambda it: it[2] / it[1], reverse=True)
    best, nodes = 0, 0

    def bound(i, c, v):
        b = v
        for it in order[i:]:
            if it[1] <= c:
                c -= it[1]
                b += it[2]
            else:
                b += it[2] / it[1] * c       # 装不下就按比例估，作为乐观上界
                break
        return b

    def dfs(i, c, v):
        nonlocal best, nodes
        nodes += 1
        if v > best:
            best = v
        if i == len(items) or bound(i, c, v) <= best:
            return                           # 上界不乐观 -> 剪枝，不再往下搜
        if c >= order[i][1]:
            dfs(i + 1, c - order[i][1], v + order[i][2])
        dfs(i + 1, c, v)
    dfs(0, capacity, 0)
    return best, nodes


def main():
    print("① n-后问题（回溯法）")
    for n in (8, 9, 10):
        count, first = n_queens(n)
        print(f"  n={n}: 解 {count} 个，穷举要试 {n_queens_bruteforce_states(n)} 种排列；"
              f"第一个解（每行皇后所在列）= {first}")

    print("\n② 完全背包 vs 0-1 背包（容量 1000g，物品可重复拿）")
    print(f"  0-1 背包最优：{knapsack_01(ITEMS, 1000)}（每件最多带一次）")
    print(f"  完全背包最优：{knapsack_complete(ITEMS, 1000)}"
          f"（水具 90/250 性价比最高，会被重复拿 4 次 = 360）")

    print("\n③ 分支限界 vs 纯回溯（同一个 1000g 背包）")
    v1, nodes1 = dfs_nodes(ITEMS, 1000)
    v2, nodes2 = bab_nodes(ITEMS, 1000)
    print(f"  纯回溯：最优 {v1}，搜索结点 {nodes1} 个")
    print(f"  分支限界：最优 {v2}，搜索结点 {nodes2} 个 -> 少搜 {nodes1 - nodes2} 个结点")


if __name__ == "__main__":
    main()
