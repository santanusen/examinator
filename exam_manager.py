#
# Copyright 2022 Santanu Sen. All Rights Reserved.
#
# Licensed under the Apache License 2.0 (the "License"). You may not use
# this file except in compliance with the License. You can obtain a copy
# in the file LICENSE in the source distribution
#

import random
import threading
import yaml

import question


class ExamManager:
    def __init__(self):
        self._qtotal = 1
        self._qremain = 1
        self._answer_sheet = []

        self._exam_running = False
        self._exam_timer = None

        self._tests = {
            "Addition": self._get_one_add_question,
            "Subtraction": self._get_one_subtract_question,
            "Multiplication": self._get_one_multiply_question,
            "Opposites": self._get_one_opposites_question,
        }
        self._optests = []

        self._opposites = None

    @property
    def questions_remaining(self):
        return self._qremain

    @property
    def num_questions(self):
        return self._qtotal

    @num_questions.setter
    def num_questions(self, n):
        self._qtotal = n
        self._qremain = n

    @property
    def tests(self):
        return self._tests

    @property
    def opted_tests(self):
        return self._optests

    @opted_tests.setter
    def opted_tests(self, tl):
        self._optests = tl
        if "Opposites" in tl:
            with open("samples/opposites.yaml", "r") as stream:
                data = yaml.safe_load(stream)
                self._opposites = data["Opposites"]

    def _get_one_add_question(self):
        n1 = random.randint(0, 10)
        n2 = random.randint(0, 10)
        ans = str(n1 + n2)
        txt = str(n1) + " + " + str(n2) + " = "
        q = question.Question(txt, ans)
        return q

    def _get_one_multiply_question(self):
        n1 = random.randint(0, 10)
        n2 = random.randint(0, 10)
        ans = str(n1 * n2)
        txt = str(n1) + " \u2715 " + str(n2) + " = "
        q = question.Question(txt, ans)
        return q

    def _get_one_subtract_question(self):
        v1 = random.randint(0, 10)
        v2 = random.randint(0, 10)
        n1 = max(v1, v2)
        n2 = min(v1, v2)
        ans = str(n1 - n2)
        txt = str(n1) + " - " + str(n2) + " = "
        q = question.Question(txt, ans)
        return q

    def _get_one_opposites_question(self):
        word, opp = random.choice(list(self._opposites.items()))
        ans = opp
        txt = "The opposite of '" + word + "' is "
        q = question.Question(txt, ans)
        return q

    def get_next_question(self):
        if self._qremain <= 0 or not self._exam_running:
            self.stop_exam()
            return None
        else:
            self._qremain -= 1

        q = self._tests[self._optests[random.randint(0, len(self._optests) - 1)]]()

        self._answer_sheet.append(q)
        return q

    def get_answer_sheet(self):
        return self._answer_sheet

    def stop_exam(self):
        if not self._exam_running:
            return
        self._exam_running = False
        self._exam_timer.cancel()

    def start_exam(self, tsec):
        if self._exam_running:
            return
        self._exam_running = True
        self._exam_timer = threading.Timer(tsec, self.stop_exam)
        self._exam_timer.start()

    def __del__(self):
        self.stop_exam()
