from impl import permutation_sum

class TestPermutationSum:
    def test_case_1(self):
        assert permutation_sum([.25, .5, 1]) == [5/48, 11/48, 2/3]

    def test_case_2(self):
        assert permutation_sum([.125, .25, .5, 1]) == [37/768, 77/768, 169/768, 485/768]