from implement import random_shuffle_prob
from implement import test as permu_t
from random import random
from verahelper import loose_match


zipmatch = lambda a, b: all(map(loose_match, a, b))


## Used with pytest ##
class TestPermutationSum:
    def test_case_1(self):
        assert zipmatch(random_shuffle_prob([.25, .5, 1]), [5/48, 11/48, 2/3])

    def test_case_2(self):
        assert zipmatch(random_shuffle_prob([.125, .25, .5, 1]), [37/768, 77/768, 169/768, 485/768])

    def test_case_3(self):
        rand = [random() for _ in range(5)]
        assert zipmatch(random_shuffle_prob(rand), permu_t(rand))
