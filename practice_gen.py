#
# Copyright 2022 Santanu Sen. All Rights Reserved.
#
# Licensed under the Apache License 2.0 (the "License"). You may not use
# this file except in compliance with the License. You can obtain a copy
# in the file LICENSE in the source distribution
#

import random
import yaml

import question


class PracticeSetGen:
    @staticmethod
    def _get_one_add_question(slf):
        nmax = 1000000
        n1 = random.randint(0, nmax)
        n2 = random.randint(0, nmax)
        ans = str(n1 + n2)
        txt = str(n1) + " + " + str(n2) + " = "
        q = question.Question(txt)
        return q, ans

    @staticmethod
    def _get_one_multiply_question(slf):
        nmax = 10
        n1 = random.randint(0, nmax)
        n2 = random.randint(0, nmax)
        ans = str(n1 * n2)
        txt = str(n1) + " \u2715 " + str(n2) + " = "
        q = question.Question(txt)
        return q, ans

    @staticmethod
    def _get_one_subtract_question(slf):
        nmax = 1000000
        v1 = random.randint(0, nmax)
        v2 = random.randint(0, nmax)
        n1 = max(v1, v2)
        n2 = min(v1, v2)
        ans = str(n1 - n2)
        txt = str(n1) + " - " + str(n2) + " = "
        q = question.Question(txt)
        return q, ans

    @staticmethod
    def _get_one_opposites_question(slf):
        word, opp = random.choice(list(slf._opposites.items()))
        ans = opp
        txt = "The opposite of '" + word + "' is "
        q = question.Question(txt)
        return q, ans

    def __init__(self):
        self._qpaper = None
        self._anskey = None
        self._opposites = None

    def gen_question_paper(self, optests, numq):
        if self._qpaper is not None:
            return self._qpaper
        if len(optests) == 0:
            return self._qpaper

        self._qpaper = []
        self._anskey = []
        if "Opposites" in optests:
            with open("samples/opposites.yaml", "r") as stream:
                data = yaml.safe_load(stream)
                self._opposites = data["Opposites"]
        for i in range(0, numq):
            q, a = PracticeSetGen._tests[optests[random.randint(0, len(optests) - 1)]](
                self
            )
            self._qpaper.append(q)
            self._anskey.append(a)
        return self._qpaper

    def get_question_paper():
        return self._qpaper

    def evaluate_answer(self, qnum, ans):
        if ans is None:
            return False
        return ans.upper() == self._anskey[qnum].upper()

    def get_test_list(self):
        return PracticeSetGen._tests.keys()


PracticeSetGen._tests = {
    "Addition": PracticeSetGen._get_one_add_question,
    "Subtraction": PracticeSetGen._get_one_subtract_question,
    "Multiplication": PracticeSetGen._get_one_multiply_question,
    "Opposites": PracticeSetGen._get_one_opposites_question,
}
