"""
gcd 関数の Validation テスト
期待値と実際の出力を体系的に比較する
"""
import math

def gcd(a: int, b: int) -> int:
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError(f"整数を指定してください: a={a!r}, b={b!r}")
    if a == 0 and b == 0:
        raise ValueError("gcd(0, 0) は未定義です")
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


# ─────────────────────────────────────────────
# テストケース定義
# ─────────────────────────────────────────────

CASES = [
    # カテゴリ, a, b, 期待値, 根拠コメント
    # ── 課題指定ケース ──
    ("課題指定",  52,   28,    4,  "52=4×13, 28=4×7"),
    ("課題指定", 108,   18,   18,  "18は108の約数"),

    # ── 一般的な正の整数 ──
    ("正の整数",  48,   18,    6,  "48=6×8, 18=6×3"),
    ("正の整数", 100,   75,   25,  "100=25×4, 75=25×3"),
    ("正の整数",  36,   48,   12,  "順序逆でも同じ"),
    ("正の整数",   7,   13,    1,  "互いに素"),
    ("正の整数", 360,  252,   36,  "大きい数"),
    ("正の整数", 1000000, 999999, 1, "連続整数は互いに素"),

    # ── 負の数 ──
    ("負の数",  -52,   28,    4,  "負×正: |a|で処理"),
    ("負の数",   52,  -28,    4,  "正×負"),
    ("負の数",  -52,  -28,    4,  "両方負"),
    ("負の数", -108,  -18,   18,  "両方負・整除"),
    ("負の数",  -7,   13,    1,  "互いに素・片方負"),

    # ── 0 を含む ──
    ("ゼロ含む",   0,   28,   28,  "P4: gcd(0,b)=b"),
    ("ゼロ含む",  52,    0,   52,  "P4: gcd(a,0)=a"),
    ("ゼロ含む",   0,    1,    1,  "gcd(0,1)=1"),
    ("ゼロ含む",   0, -18,   18,  "gcd(0,負)=|負|"),

    # ── 1 を含む ──
    ("1含む",     1,   28,    1,  "P5: gcd(1,b)=1"),
    ("1含む",    52,    1,    1,  "P5: gcd(a,1)=1"),
    ("1含む",     1,    1,    1,  "P6: gcd(1,1)=1"),
    ("1含む",    -1,   28,    1,  "負の1"),

    # ── 同じ数 ──
    ("等値",     28,   28,   28,  "P6: gcd(a,a)=|a|"),
    ("等値",    -52,  -52,   52,  "P6: 両方負"),
    ("等値",      5,    5,    5,  "自明"),

    # ── 片方が倍数 ──
    ("整除",    108,   18,   18,  "108=18×6"),
    ("整除",     28,    7,    7,  "28=7×4"),
    ("整除",    100,   10,   10,  "100=10×10"),

    # ── 素数ペア ──
    ("素数",     17,   13,    1,  "互いに素な素数"),
    ("素数",     97,   89,    1,  "大きな素数同士"),
]

EXCEPTION_CASES = [
    ("例外",  0,   0, ValueError, "gcd(0,0)は未定義"),
    ("例外", 3.5, 2,  TypeError,  "浮動小数点"),
    ("例外",  3,  "a", TypeError, "文字列"),
]

# ─────────────────────────────────────────────
# 実行・検証
# ─────────────────────────────────────────────

def run_validation():
    COL = {"課題指定": 0, "正の整数": 0, "負の数": 0,
           "ゼロ含む": 0, "1含む": 0, "等値": 0, "整除": 0, "素数": 0}
    pass_count = fail_count = 0

    print("=" * 74)
    print("  gcd 関数 Validation レポート")
    print("=" * 74)

    current_cat = None
    for cat, a, b, expected, note in CASES:
        actual   = gcd(a, b)
        oracle   = math.gcd(abs(a), abs(b))  # Python標準ライブラリを正解オラクルに
        ok_impl  = actual == expected
        ok_oracle = actual == oracle
        ok = ok_impl and ok_oracle

        if cat != current_cat:
            current_cat = cat
            print(f"\n  【{cat}】")
            print(f"  {'a':>10}  {'b':>10}  {'期待値':>6}  {'実際':>6}  {'標準':>6}  {'結果':^6}  備考")
            print(f"  {'─'*66}")

        mark = "✓" if ok else "✗ FAIL"
        if ok:
            pass_count += 1
        else:
            fail_count += 1

        print(f"  {a:>10}  {b:>10}  {expected:>6}  {actual:>6}  {oracle:>6}  {mark:^6}  {note}")

    # 例外ケース
    print(f"\n  【例外処理】")
    print(f"  {'a':>8}  {'b':>8}  {'期待例外':<14}  {'結果':^6}  備考")
    print(f"  {'─'*54}")
    for cat, a, b, exc_type, note in EXCEPTION_CASES:
        try:
            gcd(a, b)
            mark = "✗ FAIL"
            fail_count += 1
        except exc_type:
            mark = "✓"
            pass_count += 1
        except Exception:
            mark = "✗ FAIL"
            fail_count += 1
        print(f"  {str(a):>8}  {str(b):>8}  {exc_type.__name__:<14}  {mark:^6}  {note}")

    # サマリー
    total = pass_count + fail_count
    print(f"\n{'=' * 74}")
    print(f"  結果: {pass_count}/{total} 通過  |  {'全テスト通過 ✓' if fail_count == 0 else f'失敗 {fail_count} 件 ✗'}")
    print(f"{'=' * 74}")

    # 性質の検証
    print("\n  【数学的性質の検証】")
    print(f"  {'─'*54}")
    props = [
        ("P2 可換性",  lambda: gcd(52,28) == gcd(28,52)),
        ("P4 零元(右)", lambda: gcd(52, 0) == 52),
        ("P4 零元(左)", lambda: gcd(0, 28) == 28),
        ("P5 単位元",  lambda: gcd(52, 1) == 1),
        ("P6 冪等性",  lambda: gcd(52, 52) == 52),
        ("P7 負の対称性", lambda: gcd(-52, 28) == gcd(52, -28) == gcd(52, 28)),
        ("P10 互除法", lambda: gcd(52, 28) == gcd(28, 52 % 28)),
        ("P11 スカラー倍", lambda: gcd(52*3, 28*3) == 3 * gcd(52, 28)),
    ]
    for name, fn in props:
        ok = fn()
        print(f"  {name:<16}  {'✓ 成立' if ok else '✗ 不成立'}")
    print(f"  {'─'*54}")

if __name__ == "__main__":
    run_validation()
