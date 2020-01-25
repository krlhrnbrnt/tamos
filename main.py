#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import os
import random
import textwrap
from tkinter import *

ABOUT_TEXT = """
About

Version: 0.0.3
"""
DISCLAIMER = """
Disclaimer

This software comes with no guarantee. Use at your own risk! """


class Option():
    def __init__(self, option, answer):
        self.option = option
        self.answer = answer


class Questions():
    def __init__(self, question, options, answer):
        self.question = question
        self.options = []
        for i, opt in enumerate(options):
            self.options.append(Option(opt, answer[i]))


class TamosGame(Frame):
    def __init__(self, master, defaultbg, fileid):
        self.fileid = find_files()
        self.question_text = StringVar()
        self.text_width = 100
        self.score = 0
        self.open_history()
        self.menu_button_width = 25
        self.defaultbg = defaultbg
        self.score_label_text = StringVar()
        self.total_questions_text = StringVar()
        self.total_questions_text.set('Questions: 0')
        self.search_var = 0

        # The big frame
        self.frame = Frame(master)
        self.frame.pack()

        # Frame for menu
        self.frame_menu = Frame(self.frame, bg='grey', bd=1, relief=GROOVE)
        self.frame_menu.pack(side=LEFT, anchor=W, fill=Y, expand=1)

        # Frame for the game
        self.main_frame = Frame(self.frame, bg=self.defaultbg)
        self.show_game()

        # Frame for settings
        self.settings_frame = Frame(self.frame, bg=self.defaultbg, width=100)
        self.setup_settings()

        # Frame for new question
        self.new_question_frame = Frame(self.frame, bg=self.defaultbg)
        self.setup_new_question()

        # Status bar
        self.status_text = 'TaMoS the Game'
        self.status_label_text = StringVar()
        self.status_label_text.set(self.status_text)
        status_label = Label(
            master, textvariable=self.status_label_text, bd=1, relief=SUNKEN, anchor=W)
        status_label.pack(side=BOTTOM, fill=X)

        # Menu
        self.setup_menu()

    def setup_menu(self):
        self.menu_button_bg = 'white'
        self.restart_button = Button(self.frame_menu, text='Restart', command=self.click_restart,
                                     width=self.menu_button_width, bg=self.menu_button_bg, font=('Helvetica', 11))
        self.settings_button = Button(self.frame_menu, text='Search', command=self.click_settings,
                                      width=self.menu_button_width, bg=self.menu_button_bg, font=('Helvetica', 11))
        self.new_question_button = Button(self.frame_menu, text='New question', command=self.click_new_question,
                                          width=self.menu_button_width, bg=self.menu_button_bg, font=('Helvetica', 11))
        self.quit_button = Button(self.frame_menu, text='Quit!', fg="red", command=self.frame.quit,
                                  width=self.menu_button_width, bg=self.menu_button_bg, font=('Helvetica', 11))
        self.about_button = Button(self.frame_menu, text='About', command=self.click_about,
                                   width=self.menu_button_width, bg=self.menu_button_bg, font=('Helvetica', 11))
        self.score_label = Label(self.frame_menu, textvariable=self.score_label_text, font=(
            'Helvetica', 15), bg='grey', bd=2, relief=RAISED)
        self.total_questions = Label(self.frame_menu, textvariable=self.total_questions_text, font=(
            'Helvetica', 15), bg='grey', bd=2, relief=RAISED)
        self.exams_label = Label(self.frame_menu, text='Exams', font=(
            'Helvetica', 15), bg='grey', bd=2)

        self.frame_exams = Frame(self.frame_menu, bg='gray')

        self.tamos_label = Label(
            self.frame_menu, text='TaMoS the Game!', font=('fixedsys', 18), bg='grey')
        
        self.tamos_label.pack(pady=10)
        self.restart_button.pack(fill=X)
        self.settings_button.pack(fill=X)
        self.new_question_button.pack(fill=X)
        self.about_button.pack(fill=X)
        self.score_label.pack(fill=X, pady=5)
        self.total_questions.pack(fill=X, pady=5)
        self.exams_label.pack(fill=X, pady=5)
        self.frame_exams.pack()
        self.quit_button.pack(side=BOTTOM, fill=X)
        self.exams_settings()
        self.start_game()

    def exams_settings(self):
        self.exams = []
        r = 0
        for i in range(0, len(self.fileid)):
            self.exams.append(IntVar())
            name = self.fileid[i].strip('./Questions/').strip('.json')
            c = Checkbutton(self.frame_exams, text=name,
                            variable=self.exams[i], bg='gray', font=('Helvetica', 11))
            if i == 0:  # Minst en tenta
                self.exams[0].set(1)
                c.select()
            if not i % 2 == 0:
                col = 1
            else:
                r += 1
                col = 0
            c.grid(row=r, column=col)

    def start_game(self):
        self.score = 0
        self.max_score = 0
        if self.search_var == 0:
            self.update_questions()
        else:
            self.search_var = 0
        # Game label
        self.question_text = StringVar()
        self.question_text.set('Game label')
        self.game_label = Label(self.main_frame, textvariable=self.question_text,
                                justify=LEFT, anchor=E, bg=self.defaultbg, font=('Helvetica', 13, "bold"))
        self.game_label.grid(row=0, column=1, columnspan=4, pady=5, padx=5)

        self.make_checkbuttons()
        self.show_score()
        self.show_question()

    def click_restart(self):
        self.destroy_widgets()
        self.start_game()
        self.status_label_text.set('Game restarted')
        self.question_info()

    def click_new_question(self):
        self.hide_game()
        self.show_new_question()
        self.status_label_text.set('Add a new question')

    def save_question(self):
        filename = self.new_file('TEST')  # Datum
        if self.control_entry():
            try:
                file = open(filename, 'r')
                json_data = json.load(file)
            except:
                json_data = []
            data_tmp = []
            file = open(filename, 'w+')
            data_tmp.append(self.data[0].get())
            for n in range(0, 4):
                data_tmp.append(self.data[n+1].get())
            data_tmp.append('')
            if self.var[0].get() == 1:
                data_tmp[5] += 'a,'
            if self.var[1].get() == 1:
                data_tmp[5] += 'b,'
            if self.var[2].get() == 1:
                data_tmp[5] += 'c,'
            if self.var[3].get() == 1:
                data_tmp[5] += 'd,'
            json_data.append(data_tmp)
            json.dump(json_data, file)
            self.clear()
        else:
            self.status_label_text.set('Inputs missing. Try again!')

    def new_file(self, name):
        directory = "./Questions"
        filename = directory+'/' + name+'.json'
        return filename

    def control_entry(self):
        s = 0
        for n in range(0, 4):
            if self.data[n].get() == '':
                return False
            s += self.var[n].get()
        if s < 1:
            return False

        return True

    def hide_game(self):
        self.main_frame.pack_forget()

    def show_game(self):
        try:
            self.hide_settings()
            self.update_questions_search()
            self.restart_button.configure(
                text='Restart', command=self.click_restart)
            self.status_label_text.set(self.status_text)
        except:
            pass
        try:
            self.hide_new_question()
            self.restart_button.configure(
                text='Restart', command=self.click_restart)
            self.status_label_text.set(self.status_text)
        except:
            pass

        self.main_frame.pack(side=RIGHT, expand=1, fill=BOTH, anchor=W)

    def show_new_question(self):
        try:
            self.hide_settings()
        except AttributeError:
            pass
        except:
            print("Unexpected error")
            raise
        self.new_question_frame.pack(side=RIGHT, expand=1, fill=BOTH, anchor=W)
        self.restart_button.configure(text='Play', command=self.show_game)

    def hide_new_question(self):
        self.new_question_frame.pack_forget()

    def show_settings(self):
        try:
            self.hide_new_question()
        except AttributeError:
            pass
        except:
            print("Unexpected error")
            raise
        self.settings_frame.pack(side=RIGHT, expand=1, fill=BOTH, anchor=W)
        self.restart_button.configure(text='Play', command=self.show_game)

    def hide_settings(self):
        self.settings_frame.pack_forget()

    def clear(self):
        for n in range(0, 5):
            self.data[n].set("")
        for n in range(0, 4):
            self.new_checkbutton[n].deselect()

    def destroy_widgets(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def update_questions(self):
        self.questions = []
        self.questions = read_file(self.fileid, self.exams)
        self.total_questions_text.set("Questions: " + str(len(self.questions)))

    def update_questions_search(self):
        self.total_questions_text.set(
            "Questions: " + str(len(self.questions)+1))

    def next_question(self):
        if len(self.questions) > 0:
            self.change_game_button()
            self.status_label_text.set(self.status_text)
            self.show_question()

    def make_checkbuttons(self):
        self.varOpt = []
        self.option = []
        self.strOpt = []

        for n in range(0, 4):
            self.varOpt.append(IntVar())
            self.strOpt.append(StringVar())
            self.option.append(Checkbutton(
                self.main_frame, textvariable=self.strOpt[n], variable=self.varOpt[n], font=('Helvetica', 13), justify=LEFT))
            self.option[n].grid(row=n+1, column=1,
                                columnspan=3, sticky=W, padx=5, pady=4)

        self.game_button_text = StringVar()
        self.game_button_text.set('Check answer!')
        self.game_button = Button(
            self.main_frame, textvariable=self.game_button_text, command=self.check_ans)
        self.game_button.grid(row=5, columnspan=4, pady=5)
        self.game_edit_button = Button(
            self.main_frame, text='Edit', command=self.click_edit)
        self.game_edit_button.grid(row=5, column=5, pady=10, padx=10)

    def click_edit(self):
        self.data = []
        toplevel = Toplevel()
        toplevel.title('Edit Question')
        entryfields = []
        var = []
        checkbutton = []
        checkbutton_text = ['a)', 'b)', 'c)', 'd)']

        edit_question_label = Label(toplevel, text='Edit question!', font=(
            'Helvetica', 11), bg=self.defaultbg)
        edit_question_label.grid(row=0, column=1, pady=5)

        question_label = Label(toplevel, text='Question')
        question_label.grid(row=1, column=0)

        for n in range(0, 5):
            self.data.append(StringVar())
            if n < 1:
                self.data[n].set(self.question.question)
            else:
                self.data[n].set(self.question.options[n-1].option)

            entryfields.append(
                Entry(toplevel, width=100, textvariable=self.data[n]))
            entryfields[n].grid(row=n+1, column=1, padx=20, pady=5)

        for n in range(0, 4):
            var.append(IntVar())
            checkbutton.append(Checkbutton(
                toplevel, text=checkbutton_text[n], variable=self.var[n]))
            checkbutton[n].deselect()
            checkbutton[n].grid(row=n+2, column=0)

        save_button = Button(
            toplevel, text='Save changes!', command=self.save_edit)
        save_button.grid(row=7, column=1, padx=5, pady=10)

    def save_edit(self):
        pass

    def update_checkbuttons(self):
        random.shuffle(self.question.options)
        for n in range(0, 4):
            self.strOpt[n].set(textwrap.fill(
                self.question.options[n].option, width=self.text_width))
            self.option[n].configure(bg=self.defaultbg, state=NORMAL)
            self.option[n].deselect()

    def disable_checkbuttons(self):
        for n in range(0, 4):
            self.option[n].configure(state=DISABLED)

    def show_question(self):
        if len(self.questions) > 0:
            self.question = self.questions.pop(0)
            self.question_text.set(textwrap.fill(
                self.question.question, width=self.text_width))
            self.update_checkbuttons()
            self.question_info()
            self.max_score += 1

    def question_info(self):
        key = self.question.question
        if key in self.history:
            p = 100*(float(self.history[key][0])/float(self.history[key][1]))
            output = 'Stats: %.2f ' % p
            self.status_label_text.set(output+'%')
        else:
            self.status_label_text.set('No stats')

    def check_ans(self):
        fail = False
        self.disable_checkbuttons()
        for n in range(0, len(self.question.options)):
            ans = self.varOpt[n].get()
            correct = int(self.question.options[n].answer)
            if ans is not correct and correct is not 1:
                self.option[n].configure(bg='red')
                fail = True

            elif ans is not correct and correct is 1:
                self.option[n].configure(bg='green')
                fail = True
            elif ans is correct and correct is 1:
                self.option[n].configure(bg='green')

        if fail:
            self.questions.append(self.question)
            self.status_label_text.set('Wrong!')
            self.save_history(self.question.question, 0)
        else:
            self.score += 1
            self.status_label_text.set('Correct!')
            self.save_history(self.question.question, 1)
        self.show_score()
        self.change_game_button()

    def change_game_button(self):
        if self.game_button_text.get() == 'Next question!':
            self.game_button_text.set('Check answer!')
            self.game_button.configure(command=self.check_ans)
        else:
            if len(self.questions) < 1:
                self.game_button_text.set('No questions left!')
                self.game_button.configure(state=DISABLED)
            else:
                self.game_button_text.set('Next question!')
                self.game_button.configure(command=self.next_question)

    def show_score(self):
        score = "Score: %d/%d" % (self.score, self.max_score)
        self.score_label_text.set(score)

    def click_settings(self):
        self.hide_game()
        self.show_settings()

    def setup_settings(self):
        self.search_word = StringVar()
        l = Label(self.settings_frame, text='Search!', font=('Helvetica', 15))
        l.pack(padx=50, pady=15)
        e = Entry(self.settings_frame, width=25,
                  textvariable=self.search_word, justify=CENTER)
        e.pack(pady=20, padx=10)
        b = Button(self.settings_frame, text='Search!', command=self.search)
        b.pack()

    def search(self):
        self.search_var = 1
        tmp = []
        for question in self.questions:
            q = question.question.lower()
            val = q.find(self.search_word.get())
            if not val == -1:
                tmp.append(question)

        self.questions = tmp
        self.click_restart()
        self.show_game()

    def setup_new_question(self):
        self.data = []
        self.entryfields = []
        self.var = []
        checkbutton_text = ['a)', 'b)', 'c)', 'd)']
        self.new_checkbutton = []

        self.new_question_label = Label(self.new_question_frame, text='Add a new question!', font=(
            'Helvetica', 11), bg=self.defaultbg)
        self.new_question_label.grid(row=0, column=1, pady=5)
        self.question_label = Label(self.new_question_frame, text='Question')
        self.question_label.grid(row=1, column=0)

        # entryfields for new question
        for n in range(0, 5):
            self.data.append(StringVar())
            self.entryfields.append(
                Entry(self.new_question_frame, width=100, textvariable=self.data[n]))
            self.entryfields[n].grid(row=n+1, column=1, padx=20, pady=5)

        # checkbuttons for new question
        for n in range(0, 4):
            self.var.append(IntVar())
            self.new_checkbutton.append(Checkbutton(
                self.new_question_frame, text=checkbutton_text[n], variable=self.var[n]))
            self.new_checkbutton[n].grid(row=n+2, column=0)

        self.save_button = Button(
            self.new_question_frame, text='Save question!', command=self.save_question)
        self.save_button.grid(row=7, column=1, padx=5, pady=10)

    def click_about(self):
        toplevel = Toplevel()
        toplevel.geometry('350x250')
        toplevel.title('About')
        label1 = Label(toplevel, text=ABOUT_TEXT, height=0, width=100)
        label1.pack()
        label2 = Label(toplevel, text=DISCLAIMER, height=0, width=100)
        label2.pack()

    def open_history(self):
        self.history = {}
        try:
            for key, val in csv.reader(open("history.csv")):
                val = val.replace('[', "")
                val = val.replace(']', "")
                val = val.replace(',', "")
                val = val.split()
                val[0] = int(val[0])
                val[1] = int(val[1])
                self.history[key] = val
        except:
            pass

    def save_history(self, key, val):
        if key in self.history:
            self.history[key][0] += val
            self.history[key][1] += 1
        else:
            self.history[key] = [val, 1]
        w = csv.writer(open("history.csv", "w"))
        for key, val in self.history.items():
            w.writerow([key, val])

    def save_stats(self, key, val):
        file = open('stats.json', 'r')
        stats = json.load(file)


def find_files():
    exams = []
    directory = "./Questions"
    for file in os.listdir(directory):
        if file.endswith(".json"):
            exams.append(directory+'/'+file)
    return exams


def read_file(filenames, exams):
    questions = []
    for n in range(0, len(filenames)):
        filename = filenames[n]
        if exams[n].get() == 1:
            file = open(filename, 'r')
            data = json.load(file)
            file.close()
            numq = len(data)
            for i in range(0, numq):
                questions.append(
                    Questions(data[i][0], data[i][1:5], ans_list(data[i][5])))
    random.shuffle(questions)
    return questions


def ans_list(answer):
    answer = answer.split(',')
    anstemp = []
    a = ['a', 'b', 'c', 'd']
    for n in a:
        if n in answer:
            anstemp.append(1)
        else:
            anstemp.append(0)

    return anstemp


def main():
    fileid = 'tamos_test2.json'
    tk = Tk()
    tk.title('TaMoS')
    defaultbg = tk.cget("bg")
    tamos = TamosGame(tk, defaultbg, fileid)
    tk.mainloop()


if __name__ == '__main__':
    main()
