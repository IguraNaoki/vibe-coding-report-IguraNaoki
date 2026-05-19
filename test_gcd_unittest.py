"""
test_gcd_unittest.py  —  unittest 形式 gcd 関数テストスイート

実行方法:
    python -m unittest test_gcd_unittest -v          # 全テスト
    python -m unittest test_gcd_unittest.TestZero -v # クラス単体
    python -m unittest test_gcd_unittest.TestIntentionallyFailing -v  # 失敗ケースのみ
"""

import unittest
import math
from gcd_impl import gcd, BuggyGcd


# ════════════════════════════════════════════════════════════
#  1. 課題指定ケース
# ════════════════════════════════════════════════════════════

class TestAssignmentCases(unittest.TestCase):
    """課題で明示されたテストケース"""

    def test_52_and_28(self):
        self.assertEqual(gcd(52, 28), 4)

    def test_108_and_18(self):
        self.assertEqual(gcd(108, 18), 18)


# ════════════════════════════════════════════════════════════
#  2. 正の整数
# ════════════════════════════════════════════════════════════

class TestPositiveIntegers(unittest.TestCase):

    # subTest を使うと失敗した入力値がエラーメッセージに表示される
    def test_parametrize(self):
        cases = [
            (48,  18,  6),
            (100, 75,  25),
            (36,  48,  12),        # a < b でも可換
            (7,   13,  1),         # 互いに素
            (360, 252, 36),
            (1_000_000, 999_999, 1),  # 連続整数
        ]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(gcd(a, b), expected)

    def test_commutativity(self):
        """P2 可換性: gcd(a, b) == gcd(b, a)"""
        self.assertEqual(gcd(52, 28), gcd(28, 52))

    def test_divisor_property(self):
        """結果が両辺を割り切ること"""
        d = gcd(360, 252)
        self.assertEqual(360 % d, 0)
        self.assertEqual(252 % d, 0)

    def test_matches_stdlib(self):
        """Python 標準ライブラリ math.gcd をオラクルとして照合"""
        cases = [(48, 18), (100, 75), (360, 252), (7, 13)]
        for a, b in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(gcd(a, b), math.gcd(a, b))


# ════════════════════════════════════════════════════════════
#  3. 負の数
# ════════════════════════════════════════════════════════════

class TestNegativeIntegers(unittest.TestCase):

    def test_parametrize(self):
        cases = [
            (-52,  28,  4),
            ( 52, -28,  4),
            (-52, -28,  4),
            (-108, -18, 18),
            (-7,   13,  1),
        ]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(gcd(a, b), expected)

    def test_sign_symmetry(self):
        """P7 負の対称性: gcd(-a, b) == gcd(a, -b) == gcd(a, b)"""
        self.assertEqual(gcd(-52, 28), gcd(52, -28))
        self.assertEqual(gcd(-52, 28), gcd(52,  28))

    def test_both_negative_equals_positive(self):
        self.assertEqual(gcd(-108, -18), gcd(108, 18))


# ════════════════════════════════════════════════════════════
#  4. ゼロを含む
# ════════════════════════════════════════════════════════════

class TestZero(unittest.TestCase):

    def test_zero_left(self):
        """P4: gcd(0, b) == b"""
        self.assertEqual(gcd(0, 28), 28)

    def test_zero_right(self):
        """P4: gcd(a, 0) == a"""
        self.assertEqual(gcd(52, 0), 52)

    def test_zero_and_one(self):
        self.assertEqual(gcd(0, 1), 1)

    def test_zero_and_negative(self):
        self.assertEqual(gcd(0, -18), 18)

    def test_both_zero_raises_value_error(self):
        """gcd(0, 0) は数学的に未定義 → ValueError"""
        with self.assertRaises(ValueError):
            gcd(0, 0)

    def test_both_zero_error_message(self):
        """エラーメッセージに '未定義' が含まれること"""
        with self.assertRaisesRegex(ValueError, "未定義"):
            gcd(0, 0)


# ════════════════════════════════════════════════════════════
#  5. 1 を含む
# ════════════════════════════════════════════════════════════

class TestOne(unittest.TestCase):

    def test_unit_left(self):
        """P5: gcd(1, b) == 1"""
        self.assertEqual(gcd(1, 28), 1)

    def test_unit_right(self):
        """P5: gcd(a, 1) == 1"""
        self.assertEqual(gcd(52, 1), 1)

    def test_one_one(self):
        self.assertEqual(gcd(1, 1), 1)

    def test_negative_one(self):
        self.assertEqual(gcd(-1, 28), 1)


# ════════════════════════════════════════════════════════════
#  6. 数学的性質
# ════════════════════════════════════════════════════════════

class TestMathProperties(unittest.TestCase):

    def test_idempotent(self):
        """P6 冪等性: gcd(a, a) == |a|"""
        self.assertEqual(gcd(28,  28),  28)
        self.assertEqual(gcd(-52, -52), 52)

    def test_scalar_multiple(self):
        """P11 スカラー倍: gcd(k*a, k*b) == k * gcd(a, b)"""
        self.assertEqual(gcd(52 * 3, 28 * 3), 3 * gcd(52, 28))

    def test_associativity(self):
        """P3 結合性: gcd(a, gcd(b, c)) == gcd(gcd(a, b), c)"""
        a, b, c = 52, 28, 18
        self.assertEqual(gcd(a, gcd(b, c)), gcd(gcd(a, b), c))

    def test_euclidean_theorem(self):
        """P10 互除法: gcd(a, b) == gcd(b, a mod b)"""
        a, b = 52, 28
        self.assertEqual(gcd(a, b), gcd(b, a % b))

    def test_bezout_identity(self):
        """P12 ベズーの等式: ∃ s,t ∈ ℤ  s.t.  s*a + t*b == gcd(a, b)"""
        def ext_gcd(a, b):
            if b == 0:
                return a, 1, 0
            g, s, t = ext_gcd(b, a % b)
            return g, t, s - (a // b) * t

        a, b = 52, 28
        d = gcd(a, b)
        _, s, t = ext_gcd(a, b)
        self.assertEqual(s * a + t * b, d)

    def test_result_always_nonnegative(self):
        """P1 非負性: 結果は常に >= 0"""
        cases = [(-52, 28), (52, -28), (-52, -28), (0, 28)]
        for a, b in cases:
            with self.subTest(a=a, b=b):
                self.assertGreaterEqual(gcd(a, b), 0)


# ════════════════════════════════════════════════════════════
#  7. 例外処理
# ════════════════════════════════════════════════════════════

class TestExceptions(unittest.TestCase):

    def test_bool_raises_type_error(self):
        """bool は int のサブクラスだが明示的に弾く"""
        with self.assertRaises(TypeError):
            gcd(True, 6)
        with self.assertRaises(TypeError):
            gcd(False, 0)

    def test_float_raises_type_error(self):
        with self.assertRaises(TypeError):
            gcd(3.5, 2)

    def test_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            gcd(3, "a")

    def test_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            gcd(None, 5)

    def test_both_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            gcd(0, 0)


# ════════════════════════════════════════════════════════════
#  8. 意図的に失敗するテスト（BuggyGcd を使用）
#
#  各メソッドは「バグがある実装」に対して「正しい期待値」を
#  アサートするため、必ず失敗する。
#  バグの内容と失敗理由はdocstringに記載。
# ════════════════════════════════════════════════════════════

class TestIntentionallyFailing(unittest.TestCase):
    """
    BuggyGcd に対するテスト群。
    すべて FAIL することが意図された「バグ検出テスト」。
    """

    def setUp(self):
        self.buggy = BuggyGcd()

    def test_failing_A_no_abs(self):
        """
        [Bug A] 絶対値変換なし
        ─────────────────────────────────────
        原因: abs() を呼ばないため、入力によっては a が負のまま
              ループを抜け、非負性 P1 を違反した値を返すことがある。
        例:   gcd_no_abs(-7, 3)
              → Python の % は正の余りを返すが最終的に a=-1 となり
                戻り値が -1 になる（正しくは 1）。
        期待: 1  /  実際: -1  →  FAIL
        """
        result = self.buggy.no_abs(-7, 3)
        self.assertEqual(result, 1,
            f"Bug A: 絶対値未変換。期待=1, 実際={result}")

    def test_failing_B_no_zero_guard(self):
        """
        [Bug B] gcd(0, 0) ガード節なし
        ─────────────────────────────────────
        原因: ValueError を送出すべき事前条件チェックが欠落。
              (0, 0) を渡すと while b: が一度も実行されず
              return a = 0 を返してしまう。
        期待: ValueError 発生  /  実際: 0 を返す  →  FAIL
        """
        with self.assertRaises(ValueError,
                msg="Bug B: gcd(0,0) で ValueError が発生すべき"):
            self.buggy.no_zero_guard(0, 0)

    def test_failing_C_wrong_base_case(self):
        """
        [Bug C] 基底ケースの終了条件が逆（while a: を使用）
        ─────────────────────────────────────
        原因: 正しくは `while b:` で b=0 になったら終了すべきところ
              `while a:` としているため、b=0 になった次のループで
              `a % b = a % 0` → ZeroDivisionError が発生する。
        期待: 正常終了して 6 を返す  /  実際: ZeroDivisionError  →  ERROR
        補足: FAIL ではなく ERROR になるのはバグがクラッシュを引き起こすため。
              正しい実装ではこの例外は発生しない。
        """
        with self.assertRaises(ZeroDivisionError,
                msg="Bug C: 終了条件逆転により ZeroDivisionError が発生する"):
            self.buggy.wrong_base_case(48, 18)

    def test_failing_D_swapped_assignment(self):
        """
        [Bug D] (a, b) の更新順序が逆
        ─────────────────────────────────────
        原因: 正しくは `a, b = b, a % b` だが
              `a, b = a % b, b` としているため b が変化せず、
              a だけが縮み続けて a=0 に到達した時点で
              `0 % b = 0` が続き事実上ループが機能しない。
              上限ガードにより -1 を返す。
        期待: gcd(12, 8) = 4  /  実際: -1  →  FAIL
        """
        result = self.buggy.swapped_assignment(12, 8)
        self.assertEqual(result, 4,
            f"Bug D: 更新順序誤り。期待=4, 実際={result}")

    def test_failing_E_no_type_check(self):
        """
        [Bug E] 型チェック（isinstance）なし
        ─────────────────────────────────────
        原因: float が渡されても TypeError を送出しない。
              abs(3.5) = 3.5 のままループし、丸め誤差のある
              float 値を返す（例: 0.5）。
        期待: TypeError 発生  /  実際: float 値を返す  →  FAIL
        """
        with self.assertRaises(TypeError,
                msg="Bug E: float 入力で TypeError が発生すべき"):
            self.buggy.no_type_check(3.5, 2.0)


# ════════════════════════════════════════════════════════════
#  エントリポイント
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    unittest.main(verbosity=2)
