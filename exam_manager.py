#
# Copyright 2022 Santanu Sen. All Rights Reserved.
#
# Licensed under the Apache License 2.0 (the "License"). You may not use
# this file except in compliance with the License. You can obtain a copy
# in the file LICENSE in the source distribution
#

import threading

import question
import practice_gen


class ExamManager:
    def __init__(self):
        self._qcomposer = None

        self._answer_sheet = None

        self._exam_running = False
        self._exam_timer = None

    def get_practice_test_list(self):
        return practice_gen.PracticeSetGen._tests

    def configure_practice_test(self, optests, numq):
        self._qcomposer = practice_gen.PracticeSetGen(optests, numq)
        self._answer_sheet = [None] * len(self._qcomposer.get_question_paper())

    def get_question_paper(self):
        return self._qcomposer.get_question_paper()

    def get_answer_sheet(self):
        if self._exam_running:
            return None
        return self._answer_sheet

    def stop_exam(self):
        if not self._exam_running:
            return
        self._exam_running = False
        self._exam_timer.cancel()

    def submit_answer(self, qnum, ans):
        if not self._exam_running:
            return
        self._answer_sheet[qnum] = ans

    def evaluate_answer(self, qnum):
        ans = self._answer_sheet[qnum]
        if ans is None:
            return False
        anskey = self._qcomposer.get_answer_key()
        return ans.upper() == anskey[qnum].upper() 

    def start_exam(self, tsec):
        if self._exam_running:
            return
        self._exam_running = True
        self._exam_timer = threading.Timer(tsec, self.stop_exam)
        self._exam_timer.start()

    def __del__(self):
        self.stop_exam()
