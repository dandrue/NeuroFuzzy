import itertools


def combination(list_1, list_2):
    # unique_combinations = []
    # permut = itertools.permutations(list_1, len(list_2))
    # for comb in permut:
    #     zipped = zip(comb, list_2)
    #     unique_combinations.append(list(zipped))

    unique_combinations = list(itertools.product(list_1, list_2))
    return unique_combinations


def linrepr(totalrule):
    for i in range(len(totalrule)):
        print("if " + str(totalrule[i][0][0]) + " and " + str(totalrule[i][0][1]) + " then " + str(totalrule[i][1]))


class RuleGenerator:
    def __init__(self, variables):
        self.variables = variables

    def gencomb(self):
        mfs = []
        for i in self.variables:
            mfs.append(i.mfunctions)
        antecedent = combination(mfs[0], mfs[1])
        totalrule = combination(antecedent, mfs[2])
        return antecedent, totalrule


