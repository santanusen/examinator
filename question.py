#
# Copyright 2022 Santanu Sen. All Rights Reserved.
#
# Licensed under the Apache License 2.0 (the "License"). You may not use
# this file except in compliance with the License. You can obtain a copy
# in the file LICENSE in the source distribution
#


class Question(object):
    def __init__(self, txt, ans):
        self._text = txt
        self._answer = ans
        self._response = ""

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, r):
        self._response = r

    @property
    def text(self):
        return self._text

    @property
    def answer(self):
        return self._answer

    def evaluate(self):
        return self._answer.upper() == self._response.upper()
