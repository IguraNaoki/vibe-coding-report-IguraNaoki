"""
gcd_impl.py  —  正しい実装 (gcd) と バグ入り実装 (BuggyGcd)
"""


# ────────────────────────────────────────────
#  正しい実装
# ────────────────────────────────────────────

def gcd(a: int, b: int) -> int:
    """
    ユークリッドの互除法で最大公約数を返す。

    Precondition : a, b ∈ ℤ, (a, b) ≠ (0, 0)
    Postcondition: 戻り値 d > 0, d|a, d|b, ∀e(e|a ∧ e|b → e ≤ d)
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError(f"整数を指定してください: a={a!r}, b={b!r}")
    if a == 0 and b == 0:
        raise ValueError("gcd(0, 0) は未定義です")
    a, b = abs(a), abs(b)          # P7: 負の対称性
    while b: != 0:                       # P10: gcd(a,b) = gcd(b, a mod b)
        a, b = b, a % b
    return a                        # P4: gcd(a,0) = a


# ────────────────────────────────────────────
#  バグ入り実装集  BuggyGcd
#  各メソッドが 1 つのバグを意図的に持つ
# ────────────────────────────────────────────

class BuggyGcd:

    # ── Bug A: 絶対値変換なし ──────────────────
    def no_abs(self, a: int, b: int) -> int:
        """負の数を abs() せずにそのまま計算する。"""
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError
        if a == 0 and b == 0:
            raise ValueError
        # abs() を呼ばないので負の a が残る
        while b:
            a, b = b, a % b
        return a  # a が負になりうる → 非負性 P1 違反

    # ── Bug B: gcd(0,0) ガードなし ────────────
    def no_zero_guard(self, a: int, b: int) -> int:
        """(0, 0) のチェックを省略。b=0 で即 return a=0 を返す。"""
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError
        # ValueError を送出すべきガード節がない
        a, b = abs(a), abs(b)
        while b:
            a, b = b, a % b
        return a  # gcd(0,0) → 0 を返してしまう

    # ── Bug C: 基底ケースの条件が逆 ───────────
    def wrong_base_case(self, a: int, b: int) -> int:
        """終了条件を `a == 0` にしてしまったバグ。"""
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError
        if a == 0 and b == 0:
            raise ValueError
        a, b = abs(a), abs(b)
        # 正しくは `while b:` だが `while a:` にしてしまう
        while a:               # ← Bug: a と b が逆
            a, b = b, a % b
        return b               # ← Bug: 最終的に b を返してしまう (= 0)

    # ── Bug D: 更新順序が逆 ────────────────────
    def swapped_assignment(self, a: int, b: int) -> int:
        """(a, b) = (b, a%b) の右辺順序を間違えたバグ。"""
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError
        if a == 0 and b == 0:
            raise ValueError
        a, b = abs(a), abs(b)
        step = 0
        while b:
            a, b = a % b, b    # ← Bug: b が変わらず a だけ縮む → 無限ループ防止で上限設定
            step += 1
            if step > 200:     # 無限ループ防止（テスト用）
                return -1
        return a

    # ── Bug E: 型チェックなし ──────────────────
    def no_type_check(self, a, b):
        """isinstance チェックを省略。float が混入しても動いてしまう。"""
        # TypeError を送出すべき型チェックがない
        if a == 0 and b == 0:
            raise ValueError
        a, b = abs(a), abs(b)
        while b:
            a, b = b, a % b
        return a  # float のまま計算 → 丸め誤差で誤答の可能性
