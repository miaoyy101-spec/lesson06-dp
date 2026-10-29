# -*- coding: utf-8 -*-
"""第 6 次课 Step2：0-1 背包（限重 1000g，至多装满）。

检查点：最优重要度 315，组合 睡袋 + 食物 + 水具（350+400+250=1000g）。
说明：指南表格的“重要度”列为空，本题取值见 ITEMS，睡袋+食物+水具合计 315；
      若教师给定其它重要度，只改 ITEMS 即可，算法不变。
"""

ITEMS = [                      # (名字, 重量 g, 重要度)
    ("帐篷", 300, 90),
    ("炉具", 200, 60),
    ("睡袋", 350, 105),
    ("食物", 400, 120),
    ("水具", 250, 90),
]
CAPACITY = 1000
PRINT_STEP = 100               # 表按 1g 计算，打印时每 100g 取一档


def knapsack(items, capacity):
    """0-1 背包（至多装满）。

    dp[i][c] = 只考虑前 i 件、限重 c 时的最大重要度
             = max(不带第 i 件, 带第 i 件)
    返回 (dp 表, 选中物品列表)。
    """
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, v = items[i - 1][1], items[i - 1][2]
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]                    # 不带第 i 件
            if c >= w:                                  # 带第 i 件
                dp[i][c] = max(dp[i][c], dp[i - 1][c - w] + v)

    chosen, c = [], capacity                            # 从右下角回溯
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:                    # 说明第 i 件被带上了
            chosen.append(items[i - 1])
            c -= items[i - 1][1]
    return dp, chosen[::-1]


def knapsack_must(items, capacity, must_name):
    """带“必投项目”约束的 0-1 背包：must_name 这件必须带上。

    做法：先把它强制扣掉（重量减、重要度先记上），
    剩下的物品在剩余容量上照常做 0-1 背包。
    """
    must = next(it for it in items if it[0] == must_name)
    rest_items = [it for it in items if it[0] != must_name]
    if must[1] > capacity:
        return None, []
    _, chosen = knapsack(rest_items, capacity - must[1])
    return must[2] + sum(it[2] for it in chosen), [must] + chosen


def report(title, dp, chosen, capacity):
    total_weight = sum(it[1] for it in chosen)
    total_value = sum(it[2] for it in chosen)
    print(f"\n【{title}】容量 {capacity}g")
    print(f"最优重要度：{total_value}")
    print("组合：" + " + ".join(f"{it[0]}({it[1]}g/{it[2]})" for it in chosen)
          + f"  总重 {total_weight}g")
    print("dp 表最后一行（每 100g 一档）：")
    for c in range(0, capacity + 1, PRINT_STEP):
        print(f"  c={c:>4}g : {dp[len(dp) - 1][c]}")
    print("回溯路径（从右下角往上走，值变了 = 带了这件）：")
    c = capacity
    for i in range(len(dp) - 1, 0, -1):
        w = ITEMS[i - 1][1]
        if dp[i][c] != dp[i - 1][c]:
            print(f"  dp[{i}][{c}]={dp[i][c]} != dp[{i - 1}][{c}]={dp[i - 1][c]}"
                  f" -> 带上 {ITEMS[i - 1][0]}，容量 {c} -> {c - w}")
            c -= w
    return total_value


def brute_force(items, capacity):
    """对照验证：枚举全部 2^n 种带/不带组合（n=5 只有 32 种），返回最优值。"""
    from itertools import combinations
    best = 0
    for r in range(len(items) + 1):
        for combo in combinations(items, r):
            if sum(it[1] for it in combo) <= capacity:
                best = max(best, sum(it[2] for it in combo))
    return best


def main():
    dp, chosen = knapsack(ITEMS, CAPACITY)
    value = report("Step2 背包 1000g", dp, chosen, CAPACITY)
    ok = value == 315 and {it[0] for it in chosen} == {"睡袋", "食物", "水具"}
    print("\n检查点：" + ("315 且组合为 睡袋/食物/水具 -> 通过" if ok else "不通过"))
    print(f"暴力枚举核对（2^5 种组合）：{brute_force(ITEMS, 1000)}  与 dp 结果一致"
          f" -> {'是' if brute_force(ITEMS, 1000) == value else '否'}")

    # 自主实践①：预算改成 800g，与 1000g 对比
    dp800, chosen800 = knapsack(ITEMS, 800)
    report("自主实践① 预算 800g", dp800, chosen800, 800)

    # 自主实践②：加“必投项目”约束（帐篷必须带上）
    v_must, chosen_must = knapsack_must(ITEMS, CAPACITY, "帐篷")
    print(f"\n【自主实践② 必投：帐篷】容量 {CAPACITY}g")
    print(f"最优重要度：{v_must}")
    print("组合：" + " + ".join(f"{it[0]}({it[1]}g/{it[2]})" for it in chosen_must)
          + f"  总重 {sum(it[1] for it in chosen_must)}g")
    print(f"对照：不加约束时 315（睡袋+食物+水具，恰好 1000g），强制带帐篷后 {v_must}，"
          f"少了 {315 - v_must}：帐篷 90 顶替了睡袋 105，"
          f"剩下的 700g 也再装不回原组合（睡袋+食物+水具要 1000g）。")


if __name__ == "__main__":
    main()
