import numpy as np


def combination(list_1, list_2, list_3):
    c = {key: list_3 for key in list_2}
    rules = {key: c for key in list_1}
    return rules


def linrepr(totalrule):
    counter = 0
    for (keys, values) in totalrule.items():
        for (key, val) in values.items():
            for ac in val:
                counter = counter + 1
                print('Rule #' + str(counter) + ':')
                print(
                    'If temperature is ' + str(keys) + ' and pressure is ' + str(key) + ' then actuator is ' + str(ac))
                print('\n')


class RuleGenerator:
    def __init__(self, variables):
        """
        Class for the generation of rules
        Parameters
        ----------
        variables, list of fuzzy variables
        """
        self.variables = variables

    def gencomb(self):
        mfs = []
        for i in self.variables:
            # print(i.mfunctions)
            mfs.append(i.mfunctions)
        rules = combination(mfs[0], mfs[1], mfs[2])
        return rules


class ErrorComputation:
    @staticmethod
    def error(o_desired, o_computed, beta, o_range):
        """
        The error following "A fuzzy perceptron as a generic model for neuro-fuzzy approaches"

        Parameters
        ----------
        o_desired, desired output
        o_computed, computed output
        beta, learning rate
        o_range, output range

        Returns
        -------
        E, error computed comparing the desired and the actual forecasting
        """

        E = 1 - np.exp(beta * ((o_computed - o_desired) / o_range) ** 2)
        return E

    @staticmethod
    def sgn_desired(o_desired):
        """
        Return the sign of the output desired
        Parameters
        ----------
        o_desired, output desired

        Returns
        -------
        the sign of the desired output
        """
        return np.sign(o_desired)

    @staticmethod
    def sgn(o_computed, o_desired):
        """
        To compute the sign of the difference between the desired output and the actual forecast
        Parameters
        ----------
        o_desired, desired output
        o_computed, actual output

        Returns
        -------
        The sign of the difference between the desired output and the actual forecast

        """
        return np.sign(o_computed - o_desired)

    @staticmethod
    def taucomputation(e_a, e_n):
        """
        Tau computation where tau is the error tendency
        Parameters
        ----------
        e_a, actual error
        e_n, next error

        Returns
        -------
        tau, error tendency

        """
        tau = 0
        e_p = e_a * e_n
        if (np.abs(e_n) >= np.abs(e_a)) & (e_p >= 0):
            tau = 1
        elif (np.abs(e_a) > np.abs(e_n)) & (e_p >= 0):
            tau = 0
        elif e_p < 0:
            tau = -1
        return tau
