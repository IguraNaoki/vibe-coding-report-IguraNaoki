"""
ユークリッドの互除法 — デバッグ版
計算途中のステップを可視化する
"""

def gcd_debug(a: int, b: int, verbose: bool = True) -> int:
    """
    反復版 GCD（デバッグ出力付き）

    Args:
        a, b   : 整数（負・0・正すべて可）
        verbose: False にすると通常の gcd と同じ動作

    Returns:
        最大公約数
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError(f"整数を指定してください: a={a!r}, b={b!r}")
    if a == 0 and b == 0:
        raise ValueError("gcd(0, 0) は未定義です")

    original_a, original_b = a, b
    a, b = abs(a), abs(b)

    if verbose:
        width = max(len(str(a)), len(str(b)), 6)
        divider = "─" * (width * 3 + 28)
        print(f"\n┌{'─' * (len(divider) - 2)}┐")
        print(f"│  gcd({original_a}, {original_b}) の計算過程")
        print(f"└{'─' * (len(divider) - 2)}┘")
        if (original_a < 0 or original_b < 0):
            print(f"  ▸ 負の数を絶対値に変換: ({original_a}, {original_b}) → ({a}, {b})")
        print()
        print(f"  {'ステップ':>4}   {'a':>{width}}   {'b':>{width}}   {'a mod b':>{width}}   {'式'}")
        print(f"  {divider}")

    step = 0
    while b:
        remainder = a % b
        if verbose:
            print(f"  {step:>4}     {a:>{width}}   {b:>{width}}   {remainder:>{width}}   "
                  f"{a} = {b} × {a // b} + {remainder}")
        a, b = b, remainder
        step += 1

    if verbose:
        print(f"  {divider}")
        print(f"  {'終了':>4}     {a:>{width}}   {b:>{width}}   {'—':>{width}}   "
              f"b = 0 になったので終了")
        print()
        print(f"  → gcd({original_a}, {original_b}) = {a}  "
              f"（{step} ステップ）")
        print()

    return a


def gcd_recursive_debug(a: int, b: int, _depth: int = 0, _orig=None) -> int:
    """
    再帰版 GCD（デバッグ出力付き）
    呼び出しツリーをインデントで可視化する
    """
    if _depth == 0:
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError(f"整数を指定してください: a={a!r}, b={b!r}")
        if a == 0 and b == 0:
            raise ValueError("gcd(0, 0) は未定義です")
        _orig = (a, b)
        a, b = abs(a), abs(b)
        print(f"\n  再帰版 gcd({_orig[0]}, {_orig[1]}) の呼び出しツリー")
        print()

    indent = "  " + "  " * _depth
    arrow  = "└─" if _depth > 0 else "  "

    if b == 0:
        print(f"{indent}{arrow}gcd({a}, {b})  →  b=0 なので {a} を返す  ✓")
        return a

    remainder = a % b
    print(f"{indent}{arrow}gcd({a}, {b})  →  {a} mod {b} = {remainder}  →  gcd({b}, {remainder}) を呼ぶ")
    result = gcd_recursive_debug(b, remainder, _depth + 1, _orig)

    if _depth == 0:
        print()
        print(f"  → gcd({_orig[0]}, {_orig[1]}) = {result}")
        print()

    return result


# ──────────────────────────────────────────────
# デモ実行
# ──────────────────────────────────────────────

if __name__ == "__main__":
    demo_cases = [
        (48, 18),
        (100, 75),
        (-35, 14),
        (0, 9),
    ]

    print("=" * 55)
    print("  【反復版】ステップ表示")
    print("=" * 55)
    for a, b in demo_cases:
        gcd_debug(a, b)

    print()
    print("=" * 55)
    print("  【再帰版】呼び出しツリー表示")
    print("=" * 55)
    for a, b in demo_cases:
        gcd_recursive_debug(a, b)
