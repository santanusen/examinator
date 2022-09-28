#
# Copyright 2022 Santanu Sen. All Rights Reserved.
#
# Licensed under the Apache License 2.0 (the "License"). You may not use
# this file except in compliance with the License. You can obtain a copy
# in the file LICENSE in the source distribution
#


class Question(object):
    def __init__(self, txt, marks=1):
        self._text = txt
        self._marks = marks

    @property
    def text(self):
        return self._text
