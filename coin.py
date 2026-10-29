# -*- coding: utf-8 -*-
"""第 6 次课 Step1：凑硬币 —— 贪心 vs 动态规划。

面额 [1, 5, 11]，目标 15。
检查点：贪心 5 枚（11+1+1+1+1），动规 3 枚（5+5+5）。
"""

COINS = [1, 5, 11]
AMOUNT = 15


def coin_greedy(coins, amount):
    """每步取不超过余额的最大面额，拿完不回头。返回 (枚数, 组合)。"""
    used = []
    rest = amount
    for coin in sorted(coins, reverse=True):
        k = rest // coin          # 这一步能拿几枚
        if k:
            used.extend([coin] * k)
            rest -= coin * k
    return len(used), used


def coin_dp(coins, amount):
    """dp[c] = 凑出 c 元的最少枚数 = 1 + min(dp[c - coin])。

    顺带记录 choice[c]（最后一枚用的面额），用于回溯出组合。
    返回 (最少枚数, 组合, dp 表)。
    """
    inf = float("inf")
    dp = [0] + [inf] * amount
    choice = [0] * (amount + 1)
    for c in range(1, amount + 1):
        for coin in coins:
            if coin <= c and dp[c - coin] + 1 < dp[c]:
                dp[c] = dp[c - coin] + 1
                choice[c] = coin
    if dp[amount] == inf:
        return inf, [], dp
    used, c = [], amount
    while c > 0:                  # 从 dp[15] 顺着 choice 倒着找回每一枚
        used.append(choice[c])
        c -= choice[c]
    return int(dp[amount]), used, dp


def main():
    n_greedy, used_greedy = coin_greedy(COINS, AMOUNT)
    n_dp, used_dp, dp = coin_dp(COINS, AMOUNT)

    print(f"面额 {COINS}，目标 {AMOUNT} 元")
    print(f"贪心：{n_greedy} 枚  ->  {' + '.join(map(str, used_greedy))} = {sum(used_greedy)}")
    print(f"动规：{n_dp} 枚  ->  {' + '.join(map(str, used_dp))} = {sum(used_dp)}")

    print("\n动规 dp 表（dp[c] = 凑出 c 元的最少枚数）：")
    print("  c   : " + " ".join(f"{c: >3}" for c in range(AMOUNT + 1)))
    print("dp[c] : " + " ".join(f"{v: >3}" if v != float('inf') else "  ∞" for v in dp))
    print(f"\n检查点：贪心 {n_greedy} 枚 vs 动规 {n_dp} 枚 -> "
          + ("通过" if (n_greedy, n_dp) == (5, 3) else "不通过"))


if __name__ == "__main__":
    main()
