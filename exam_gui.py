#
# Copyright 2022 Santanu Sen. All Rights Reserved.
#
# Licensed under the Apache License 2.0 (the "License"). You may not use
# this file except in compliance with the License. You can obtain a copy
# in the file LICENSE in the source distribution
#

import tkinter as tk
from tkinter import ttk

import exam_manager


class ExamGui:
    def __init__(self):
        self._emgr = exam_manager.ExamManager()
        self._root = tk.Tk()
        self._root.title("Examinator")
        self._root.geometry("500x500")
        self._font = ("Comic Sans MS", 20, "bold")

    def _ask_question(self):
        q = self._emgr.get_next_question()
        if q is None:
            self._root.after(0, lambda: self._show_results())
            return

        frame = tk.Frame(self._root, width=100, height=50)
        frame.pack()

        tk.Label(frame, text=q.text, font=self._font).grid(row=0, column=0)

        e = tk.Entry(frame, width=10, font=self._font)
        e.focus_set()
        e.grid(row=0, column=2)

        def on_submit(gui, q):
            answer = e.get().strip()
            if len(answer) == 0:
                return
            q.response = answer
            frame.destroy()
            gui._root.after(0, lambda: gui._evaluate_response(q))

        tk.Label(frame, text=" ").grid(row=1)

        tk.Button(
            frame,
            text="Submit",
            width=20,
            font=self._font,
            command=lambda: on_submit(self, q),
        ).grid(row=2)

    def _evaluate_response(self, q):
        frame = tk.Frame(self._root, width=100, height=50)
        frame.pack()

        if q.evaluate():
            tk.Label(frame, font=self._font, text="Correct!!!", fg="green").pack()
        else:
            tk.Label(frame, font=self._font, text="Wrong!!!", fg="red").pack()

        tk.Label(frame, text=" ").pack()

        def on_next(gui):
            frame.destroy()
            if gui._emgr.questions_remaining > 0:
                gui._root.after(0, lambda: gui._ask_question())
            else:
                gui._root.after(0, lambda: gui._show_results())

        tk.Button(
            frame, text="Next", width=20, font=self._font, command=lambda: on_next(self)
        ).pack()

    def _show_results(self):
        frame = tk.Frame(self._root, width=100, height=50)
        frame.pack()

        score = 0
        r = 0
        for q in self._emgr.get_answer_sheet():
            l = tk.Label(frame, font=self._font, text=q.text + q.response)
            l.grid(row=r, column=0, columnspan=2)

            s = ttk.Separator(frame, orient="vertical")
            s.grid(row=r, column=2, sticky="ns")
            if q.evaluate():
                tk.Label(frame, font=self._font, text=u"\u2713", fg="green").grid(
                    row=r, column=3
                )
                score += 1
            else:
                tk.Label(frame, font=self._font, text=u"\u2715", fg="red").grid(
                    row=r, column=3
                )

            r += 1

        ttk.Separator(frame, orient="horizontal").grid(row=r, column=0, sticky="ew")
        r += 1

        l3 = tk.Label(
            frame,
            font=self._font,
            fg="blue",
            text="Score: " + str(score) + " / " + str(self._emgr.num_questions),
        )
        l3.grid(row=r)

    def _start_exam(self, testlist, numquest, duration):
        self._emgr.opted_tests = testlist
        self._emgr.num_questions = numquest
        self._emgr.start_exam(duration)

        tframe = tk.Frame(self._root, width=100, height=10)
        tk.Label(tframe, text="Examinator", font=self._font).grid()
        tk.Label(tframe, text="", font=self._font).grid(row=3)
        tframe.pack()

        ttk.Separator(self._root, orient="horizontal").pack(fill="x")
        self._root.after(0, lambda: self._ask_question())

    def _menu(self):
        frame = tk.Frame(self._root, width=100, height=50)
        frame.pack()
        tk.Label(frame, text=" ").pack()
        tk.Label(frame, text="Select Tests", font=self._font, fg="blue").pack()

        menu = self._emgr.tests
        vl = []
        for (tst, f) in menu.items():
            v = tk.StringVar()
            vl.append(v)
            tk.Checkbutton(
                frame, font=self._font, text=tst, variable=v, onvalue=tst, offvalue=""
            ).pack(fill="x", ipady=5)

        tk.Label(frame, text=" ").pack()
        ttk.Separator(frame, orient="horizontal").pack(fill="x")
        tk.Label(frame, text=" ").pack()

        tk.Label(frame, text="Number of Questions", font=self._font, fg="blue").pack()
        e = tk.Entry(frame, width=3)
        e.pack()

        def on_start(gui):
            n = int(e.get().strip())
            if n <= 0:
                return

            tl = []
            for i in range(0, len(vl)):
                t = vl[i].get()
                if len(t) != 0:
                    tl.append(t)
            if len(tl) == 0:
                return

            frame.destroy()
            gui._start_exam(tl, n, 3600)

        tk.Label(frame, text=" ").pack()

        tk.Button(
            frame,
            text="Start",
            width=20,
            font=self._font,
            command=lambda: on_start(self),
        ).pack()

    def run(self):
        self._menu()
        self._root.mainloop()
        self._emgr.stop_exam()
