#
# Copyright 2022 Santanu Sen. All Rights Reserved.
#
# Licensed under the Apache License 2.0 (the "License"). You may not use
# this file except in compliance with the License. You can obtain a copy
# in the file LICENSE in the source distribution
#

import threading
import tkinter as tk
from tkinter import ttk

import exam_manager


class ExamGui:
    """
    This is the `View` component of the application.

    Implements a graphical user interface using tkinter.
    Interacts with the `Controller` ExamManager class.
    """

    def __init__(self):
        """
        Instantiates ExamManager and creates the root frame.
        The root frame remains throughout the life of the application.
        Other frames are drawn on top of the root frame as and when
        required.
        """
        self._emgr = exam_manager.ExamManager()
        self._root = tk.Tk()
        self._root.title("Examinator")
        self._root.geometry("500x500")
        self._font = ("Comic Sans MS", 20, "bold")
        self._font2 = ("Comic Sans MS", 14, "bold")
        self._cur_qnum = -1
        self._tick_timer = None
        self._timer_label = None

    def _ask_next_question(self):
        """
        Get the next question from the question paper, take the response
        answer from the user and submit the answer to the exam manager.
        """
        # Get the next question.
        self._cur_qnum += 1
        qpaper = self._emgr.get_question_paper()
        if self._cur_qnum >= len(qpaper):
            self._root.after(0, lambda: self._show_results())
            return

        q = qpaper[self._cur_qnum]

        # Layout the question on a frame.
        frame = tk.Frame(self._root, width=100, height=50)
        frame.pack()

        r = 0
        tk.Label(
            frame,
            text="Question " + str(self._cur_qnum + 1) + " of " + str(len(qpaper)),
            fg="blue",
        ).grid(row=r, column=0)
        r += 1

        tk.Label(frame, text=" ").grid(row=r, column=0)
        r += 1
        tk.Label(frame, text=" ").grid(row=r, column=0)
        r += 1

        tk.Label(frame, text=q.text, font=self._font).grid(row=r, column=0)

        e = tk.Entry(frame, width=10, font=self._font)
        e.focus_set()
        e.grid(row=r, column=2)
        r += 1

        def on_submit(gui):
            # Validate and collect user response and submit it to the exam manager.
            answer = e.get().strip()
            if len(answer) == 0:
                return
            sa_success = gui._emgr.submit_answer(self._cur_qnum, answer)
            frame.destroy()
            if sa_success:
                gui._root.after(0, lambda: gui._evaluate_response())
            else:
                # Exam manager refused to take the answer, exam time up.
                gui._root.after(0, lambda: gui._show_results())

        tk.Label(frame, text=" ").grid(row=1)

        tk.Button(
            frame,
            text="Submit",
            width=20,
            font=self._font,
            command=lambda: on_submit(self),
        ).grid(row=r)

    def _evaluate_response(self):
        """
        Ask exam manager to evaluate the answer to the current question and
        show the result to the user.
        """
        frame = tk.Frame(self._root, width=100, height=50)
        frame.pack()

        if self._emgr.evaluate_answer(self._cur_qnum):
            tk.Label(frame, font=self._font, text="Correct!!!", fg="green").pack()
        else:
            tk.Label(frame, font=self._font, text="Wrong!!!", fg="red").pack()

        tk.Label(frame, text=" ").pack()

        def on_next(gui):
            frame.destroy()
            gui._root.after(0, lambda: gui._ask_next_question())

        tk.Button(
            frame, text="Next", width=20, font=self._font, command=lambda: on_next(self)
        ).pack()

    def _show_results(self):
        """
        Ask exam manager to end the exam and show the results.
        """
        frame = tk.Frame(self._root, width=100, height=50)
        frame.pack()

        self._emgr.stop_exam()
        score = 0
        r = 0

        qpaper = self._emgr.get_question_paper()
        apaper = self._emgr.get_answer_sheet()
        for i in range(0, len(qpaper)):
            txt = qpaper[i].text
            if apaper[i] is not None:
                txt += apaper[i]
            tk.Label(frame, font=self._font, text=txt).grid(
                row=r, column=0, columnspan=2
            )

            ttk.Separator(frame, orient="vertical").grid(row=r, column=2, sticky="ns")
            if self._emgr.evaluate_answer(i):
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

        tk.Label(
            frame,
            font=self._font,
            fg="blue",
            text="Score: " + str(score) + " / " + str(len(qpaper)),
        ).grid(row=r)
        r += 1

        ttk.Separator(frame, orient="horizontal").grid(row=r, column=0, sticky="ew")
        r += 1

        tt = round(self._emgr.time_taken())
        tstr = "%02d : %02d : %02d" % (tt // 3600, (tt % 3600) // 60, tt % 60)
        tk.Label(frame, font=self._font2, fg="green", text="Time: " + tstr).grid(row=r)
        r += 1

    def _on_timer_tick(self):
        """
        On each tick, check how much time is remaining with exam manager and display it.
        """
        if self._timer_label is None:
            return
        trem = round(self._emgr.time_remaining())
        tstr = None
        if trem == 0:
            tstr = "-- : -- : --"
        else:
            tstr = "%02d : %02d : %02d" % (trem // 3600, (trem % 3600) // 60, trem % 60)
        # Change color based on urgency!
        fgcol = "green"
        if trem < 60:
            fgcol = "red"
        elif trem < 300:
            fgcol = "purple"

        self._timer_label.config(text=tstr, foreground=fgcol)
        self._tick_timer = threading.Timer(1, self._on_timer_tick)
        self._tick_timer.start()

    def _start_exam(self, duration):
        """
        Ask exam manager to start the exam. Create the top frame to display
        remaining time through the exam. Start timer to show remaining time. 
        """
        self._emgr.start_exam(duration)

        # Top frame.
        tframe = tk.Frame(self._root, width=100, height=10)
        tk.Label(
            tframe, text="Examinator", fg="magenta", font=self._font, anchor="w"
        ).grid()

        # Label to display remaining time.
        self._timer_label = tk.Label(
            tframe, width=30, text="", font=self._font2, anchor="e"
        )
        self._timer_label.grid(row=0, column=1)
        self._tick_timer = threading.Timer(0, self._on_timer_tick)
        self._tick_timer.start()

        # Add separator.
        tk.Label(tframe, text=" ", font=self._font).grid(row=2)
        tframe.pack()
        ttk.Separator(self._root, orient="horizontal").pack(fill="x")
        self._root.after(0, lambda: self._ask_next_question())

    def _practice_menu(self):
        """
        Menu to select from a list of tests offered, set exam time and
        number of questions.
        """
        frame = tk.Frame(self._root, width=100, height=50)
        frame.pack()
        tk.Label(frame, text=" ").pack()
        tl_label = tk.Label(frame, text="Select Tests", font=self._font2, fg="blue")
        tl_label.pack()

        # Get the list of tests offered and display them as check boxes.
        menu = self._emgr.get_practice_test_list()
        vl = []
        for tst in menu:
            v = tk.StringVar()
            vl.append(v)
            tk.Checkbutton(
                frame, font=self._font, text=tst, variable=v, onvalue=tst, offvalue=""
            ).pack(fill="x", ipady=5)

        tk.Label(frame, text=" ").pack()
        ttk.Separator(frame, orient="horizontal").pack(fill="x")
        tk.Label(frame, text=" ").pack()

        nq_label = tk.Label(
            frame, text="Number of Questions", font=self._font, fg="blue"
        )
        nq_label.pack()
        nq_entry = tk.Entry(frame, width=3)
        nq_entry.pack()

        tm_label = tk.Label(frame, text="Time (minutes)", font=self._font, fg="blue")
        tm_label.pack()
        tm_entry = tk.Entry(frame, width=3)
        tm_entry.pack()

        def on_start(gui):
            """
            Validate and collect user input. If input is invalid turn the text
            in corresponding label red. If input is fine, configure the exam
            manager with the tests selected and start the exam.
            """
            tl = []
            for i in range(0, len(vl)):
                t = vl[i].get()
                if len(t) != 0:
                    tl.append(t)
            if len(tl) == 0:
                tl_label.config(fg="red")
                return
            tl_label.config(fg="blue")

            nqstr = nq_entry.get().strip()
            nq = int(nqstr) if nqstr.isdigit() else 0
            if nq <= 0:
                nq_label.config(fg="red")
                return
            nq_label.config(fg="blue")

            tmstr = tm_entry.get().strip()
            tm = int(tmstr) if tmstr.isdigit() else 0
            if tm <= 0:
                tm_label.config(fg="red")
                return
            tm_label.config(fg="blue")

            frame.destroy()
            gui._emgr.configure_practice_test(tl, nq)
            gui._start_exam(tm * 60)

        tk.Label(frame, text=" ").pack()

        tk.Button(
            frame,
            text="Start",
            width=20,
            font=self._font,
            command=lambda: on_start(self),
        ).pack()

    def _clean_up(self):
        """
        Clean up resources.
        """
        if self._tick_timer is not None:
            self._tick_timer.cancel()
        self._emgr.stop_exam()

    def run(self):
        """
        API to start the GUI session.
        """
        self._practice_menu()
        self._root.mainloop()
        self._clean_up()
