#!/usr/bin/env python
# -*- coding: utf-8 -*-



import hashlib
import csv
import random
import textwrap
import os
import json
from Tkinter import *

ABOUT_TEXT = """
About

Version: 0.0.2
"""
DISCLAIMER = """
Disclaimer

This software comes with no guarantee. Use at your own risk! """


class Option():
	def __init__(self,option,answer):
		self.option = option
		self.answer = answer
  
		
class Questions():
	def __init__(self,question,options,answer):
		self.question = question
		self.options = []
		for i in range(0,len(options)):
			self.options.append(Option(options[i],answer[i]))
   

class TamosGame(Frame):   
	def __init__(self, master,defaultbg,fileid):
		#bajs
		self.fileid=findFiles()
		#self.find_files()
		self.question_text = StringVar()
		self.text_width = 100
		self.score = 0
		self.openHistory() 
		self.menu_button_width = 25
		self.defaultbg = defaultbg
		self.score_label_text = StringVar()
		self.total_questions_text = StringVar()
		self.total_questions_text.set('Questions: 0')
		self.searchVar = 0
		
		# The big frame
		self.frame = Frame(master)
		self.frame.pack()
		
		# Frame for menu
		self.frame_menu = Frame(self.frame,bg='grey',bd=1,relief=GROOVE)
		self.frame_menu.pack(side=LEFT,anchor=W,fill=Y,expand=1)
		
		# Frame for the game
		self.main_frame=Frame(self.frame,bg=self.defaultbg)
		self.showGame()
		#master.minsize(width=300, height=100)
		
		# Frame for settings
		self.settings_frame=Frame(self.frame,bg=self.defaultbg,width=100)
		self.setupSettings()
		
		# Frame for new question
		self.new_question_frame=Frame(self.frame,bg=self.defaultbg)
		self.setupNewQuestion()
		
		# Status bar
		self.status_text = 'TaMoS the Game'
		self.status_label_text=StringVar()        
		self.status_label_text.set(self.status_text)   
		status_label = Label(master, textvariable=self.status_label_text, bd=1, relief=SUNKEN, anchor=W)
		status_label.pack(side=BOTTOM, fill=X)
		
		# Menu
		self.setup_menu()
		
	def setup_menu(self):
		self.menu_button_bg = 'white'
		self.restart_button = Button(self.frame_menu,text='Restart',command=self.clickRestart,width=self.menu_button_width, bg=self.menu_button_bg,font=('Helvetica',11))
		self.settings_button = Button(self.frame_menu,text='Search',command=self.clickSettings,width=self.menu_button_width, bg=self.menu_button_bg,font=('Helvetica',11))
		self.new_question_button = Button(self.frame_menu,text='New question',command=self.clickNewQuestion,width=self.menu_button_width, bg=self.menu_button_bg,font=('Helvetica',11))
		self.quit_button = Button(self.frame_menu,text='Quit!',fg="red",command=self.frame.quit,width=self.menu_button_width, bg=self.menu_button_bg,font=('Helvetica',11))
		self.about_button = Button(self.frame_menu,text='About',command=self.clickAbout,width=self.menu_button_width, bg=self.menu_button_bg,font=('Helvetica',11))
		self.score_label = Label(self.frame_menu,textvariable=self.score_label_text,font=('Helvetica',15),bg='grey',bd=2,relief=RAISED)
		self.total_questions = Label(self.frame_menu,textvariable=self.total_questions_text,font=('Helvetica',15),bg='grey',bd=2,relief=RAISED)
		self.exams_label = Label(self.frame_menu,text='Exams',font=('Helvetica',15),bg='grey',bd=2)
		
		self.frame_exams = Frame(self.frame_menu,bg='gray')
		
		self.tamos_label = Label(self.frame_menu,text='TaMoS the Game!',font=('fixedsys',18),bg='grey')
		self.tamos_label.pack(pady=10)
		self.restart_button.pack(fill=X)
		self.settings_button.pack(fill=X)
		self.new_question_button.pack(fill=X)
		self.about_button.pack(fill=X)
		self.score_label.pack(fill=X,pady=5)
		self.total_questions.pack(fill=X,pady=5)
		self.exams_label.pack(fill=X,pady=5)
		self.frame_exams.pack()
		self.quit_button.pack(side=BOTTOM,fill=X)
		self.examsSettings()
		self.startGame()
		
	def examsSettings(self):
		self.exams = []
		r = 0
		for i in range(0,len(self.fileid)):
			self.exams.append(IntVar())
			name = self.fileid[i].strip('./Questions/').strip('.json')
			c=Checkbutton(self.frame_exams,text=name,variable=self.exams[i],bg='gray',font=('Helvetica',11))
			if i == 0: # Minst en tenta
				self.exams[0].set(1)
				c.select()
			if not i%2 == 0:
				col = 1
			else:
				r+=1
				col =0
			c.grid(row=r,column=col)
			
			
		
	def startGame(self):
		self.score=0
		self.max_score = 0
		if self.searchVar == 0:
			self.update_questions()
		else:
			self.searchVar = 0
		# Game label
		self.question_text = StringVar()
		self.question_text.set('Game label')
		self.game_label = Label(self.main_frame,textvariable=self.question_text,justify=LEFT,anchor=E,bg=self.defaultbg,font=('Helvetica',13,"bold"))
		self.game_label.grid(row=0,column=1,columnspan=4,pady=5,padx=5)
		
		self.makeCheckbuttons()
		self.showScore()
		self.showQuestion()
	
	
	def clickRestart(self):
		self.destroy_widgets()
		self.startGame()
		self.status_label_text.set('Game restarted')
		self.questionInfo()
		
	def clickNewQuestion(self):
		self.hideGame()
		self.showNewQuestion()
		self.status_label_text.set('Add a new question')
		
	def saveQuestion(self):
		filename = self.newFile('TEST')		#Datum
		if self.controlEntry():
			try: 
				file = open(filename, 'r')
				json_data  = json.load(file)
			except:
				json_data = []
			data_tmp = []
			file = open(filename, 'w+')
			data_tmp.append(self.data[0].get())
			for n in range(0,4):
				data_tmp.append(self.data[n+1].get())
			data_tmp.append('')
			if self.var[0].get() == 1:
				data_tmp[5] +='a,'
			if self.var[1].get() == 1:
				data_tmp[5] +='b,'
			if self.var[2].get() == 1:
				data_tmp[5] +='c,'
			if self.var[3].get() == 1:
				data_tmp[5] +='d,'
			json_data.append(data_tmp)
			json.dump(json_data, file)
			self.clear()
		else:
			self.status_label_text.set('Inputs missing. Try again!')
	
	def newFile(self,name):
		directory = "./Questions"
		filename = directory+'/'+ name+'.json'
		return filename
		
	def controlEntry(self):
		s = 0
		for n in range(0,4):
			if self.data[n].get() == '':
				return False
			s += self.var[n].get()
		if s < 1:
			return False
 	
		return True
		
	def hideGame(self):
		self.main_frame.pack_forget()
	
	def showGame(self):
		try:
			self.hideSettings()
			self.updateQuestionsSearch()
			self.restart_button.configure(text='Restart',command=self.clickRestart)
			self.status_label_text.set(self.status_text)
		except:
			pass
		try:
			self.hideNewQuestion()
			self.restart_button.configure(text='Restart',command=self.clickRestart)
			self.status_label_text.set(self.status_text)
		except:
			pass
			
		
		self.main_frame.pack(side=RIGHT,expand=1,fill=BOTH,anchor=W)
		
	def showNewQuestion(self):
		try:
			self.hideSettings()
		except AttributeError:
			pass
		except:
			print "Unexpected error:", sys.exc_info()[0]
			raise
		self.new_question_frame.pack(side=RIGHT,expand=1,fill=BOTH,anchor=W)
		self.restart_button.configure(text='Play',command=self.showGame)
		
	def hideNewQuestion(self):
		self.new_question_frame.pack_forget()
		
	def showSettings(self):
		try:
			self.hideNewQuestion()
		except AttributeError:
			pass
		except:
			print "Unexpected error:", sys.exc_info()[0]
			raise
		self.settings_frame.pack(side=RIGHT,expand=1,fill=BOTH,anchor=W)
		self.restart_button.configure(text='Play',command=self.showGame)
		
	def hideSettings(self):
		self.settings_frame.pack_forget()
		
	def clear(self):
		for n in range(0,5):
			self.data[n].set("")
		for n in range(0,4):
			self.new_checkbutton[n].deselect()
		
	def destroy_widgets(self):
		for widget in self.main_frame.winfo_children():
			widget.destroy()
		
	def update_questions(self):
		self.questions = []
		self.questions = readFile(self.fileid,self.exams)
		self.total_questions_text.set("Questions: " + str(len(self.questions)))
		
	def updateQuestionsSearch(self):
		self.total_questions_text.set("Questions: " + str(len(self.questions)+1))
		
	def nextQuestion(self):
		if len(self.questions)>0:
			self.change_game_button()
			self.status_label_text.set(self.status_text) 
			self.showQuestion()
			
	def makeCheckbuttons(self):
		self.varOpt =[]		
		self.option = []	
		self.strOpt = []

		for n in range(0,4):
			self.varOpt.append(IntVar())
			self.strOpt.append(StringVar())
			self.option.append(Checkbutton(self.main_frame,textvariable=self.strOpt[n],variable=self.varOpt[n],font=('Helvetica',13),justify=LEFT))
			self.option[n].grid(row=n+1,column=1,columnspan=3,sticky=W,padx=5,pady=4)
		
		self.game_button_text = StringVar()
		self.game_button_text.set('Check answer!')
		self.game_button = Button(self.main_frame,textvariable=self.game_button_text,command=self.checkAns)
		self.game_button.grid(row=5,columnspan=4,pady=5)
		self.game_edit_button = Button(self.main_frame,text='Edit',command=self.clickEdit)
		self.game_edit_button.grid(row=5,column=5,pady=10,padx=10)
		
	def clickEdit(self):
		self.data = []
		toplevel = Toplevel()
		toplevel.title('Edit Question')
		entryfields = []
		var = []
		checkbutton = []
		checkbutton_text=['a)','b)','c)','d)']
		
		edit_question_label=Label(toplevel,text='Edit question!',font=('Helvetica',11),bg=self.defaultbg)
		edit_question_label.grid(row=0,column=1,pady=5)
		
		question_label=Label(toplevel,text='Question')
		question_label.grid(row=1,column=0)
		
		for n in range(0,5):
			self.data.append(StringVar())
			if n < 1:
				self.data[n].set(self.question.question)
			else:
				self.data[n].set(self.question.options[n-1].option)
			
			entryfields.append(Entry(toplevel,width=100,textvariable=self.data[n]))
			entryfields[n].grid(row=n+1,column=1,padx=20,pady=5)
		
		for n in range(0,4):
			var.append(IntVar())
			checkbutton.append(Checkbutton(toplevel,text=checkbutton_text[n],variable=self.var[n]))
			checkbutton[n].deselect()
			checkbutton[n].grid(row=n+2,column=0)
			
		save_button = Button(toplevel,text='Save changes!',command=self.saveEdit)
		save_button.grid(row = 7,column = 1,padx=5,pady=10)
		
	def saveEdit(self):
		pass
	
	def updateCheckbuttons(self):
		random.shuffle(self.question.options)
		for n in range(0,4):
				self.strOpt[n].set(textwrap.fill(self.question.options[n].option,width=self.text_width))
				self.option[n].configure(bg=self.defaultbg,state=NORMAL)
				self.option[n].deselect()
				
	def disableCheckbuttons(self):
		for n in range(0,4):
			self.option[n].configure(state=DISABLED)
	
	def showQuestion(self):
		if len(self.questions) > 0:
			self.question = self.questions.pop(0)		
			self.question_text.set(textwrap.fill(self.question.question,width=self.text_width))
			self.updateCheckbuttons()
			self.questionInfo()
			self.max_score += 1
			
	def questionInfo(self):
		key = hashlib.sha224(self.question.question).hexdigest()
		if self.history.has_key(key):
			p = 100*(float(self.history[key][0])/float(self.history[key][1]))
			output = 'Stats: %.2f '% p
			self.status_label_text.set(output+'%')
		else:
			self.status_label_text.set('No stats')
			
	def checkAns(self):
		fail = False
		self.disableCheckbuttons()
		for n in range(0,len(self.question.options)):
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
			self.saveHistory(self.question.question,0)
		else:
			self.score += 1
			self.status_label_text.set('Correct!') 
			self.saveHistory(self.question.question,1)
		self.showScore()
		self.change_game_button()
		
	def change_game_button(self):
		if self.game_button_text.get() == 'Next question!':
			self.game_button_text.set('Check answer!')
			self.game_button.configure(command=self.checkAns)
		else:
			if len(self.questions) < 1:
				self.game_button_text.set('No questions left!')
				self.game_button.configure(state=DISABLED)
			else:
				self.game_button_text.set('Next question!')
				self.game_button.configure(command=self.nextQuestion)
		
	def showScore(self):
		score = "Score: %d/%d"%(self.score,self.max_score)
		self.score_label_text.set(score)
		
	def clickSettings(self):
		self.hideGame()
		self.showSettings()
		
	def setupSettings(self):
		self.search_word = StringVar()
		l = Label(self.settings_frame,text='Search!',font=('Helvetica',15))
		l.pack(padx=50,pady=15)
		e = Entry(self.settings_frame,width=25,textvariable=self.search_word,justify=CENTER)
		e.pack(pady=20,padx=10)
		b=Button(self.settings_frame,text='Search!',command=self.search)
		b.pack()
		
	def search(self):
		self.searchVar = 1
		tmp = []
		for question in self.questions:
			q = question.question.lower()
			val = q.find(self.search_word.get())
			if not val == -1:
				tmp.append(question)

		self.questions = tmp
		self.clickRestart()
		self.showGame()
		
	def setupNewQuestion(self):
		self.data = []
		self.entryfields = []
		self.var = []
		checkbutton_text=['a)','b)','c)','d)']
		self.new_checkbutton = []
		
		self.new_question_label=Label(self.new_question_frame,text='Add a new question!',font=('Helvetica',11),bg=self.defaultbg)
		self.new_question_label.grid(row=0,column=1,pady=5)
		self.question_label=Label(self.new_question_frame,text='Question')
		self.question_label.grid(row=1,column=0)
		
		# entryfields for new question
		for n in range(0,5):
			self.data.append(StringVar())
			self.entryfields.append(Entry(self.new_question_frame,width=100,textvariable=self.data[n]))
			self.entryfields[n].grid(row=n+1,column=1,padx=20,pady=5)
		
		# checkbuttons for new question
		for n in range(0,4):
			self.var.append(IntVar())
			self.new_checkbutton.append(Checkbutton(self.new_question_frame,text=checkbutton_text[n],variable=self.var[n]))
			self.new_checkbutton[n].grid(row=n+2,column=0)
		
		self.save_button = Button(self.new_question_frame,text='Save question!',command=self.saveQuestion)
		self.save_button.grid(row = 7,column = 1,padx=5,pady=10)
					
	def clickAbout(self):
		toplevel = Toplevel()
		toplevel.geometry('350x250')
		toplevel.title('About')
		label1 = Label(toplevel, text=ABOUT_TEXT, height=0, width=100)
		label1.pack()
		label2 = Label(toplevel, text=DISCLAIMER, height=0, width=100)
		label2.pack()
		
	def openHistory(self):
		self.history={}
		try:
			for key, val in csv.reader(open("history.csv")):
				val = val.replace('[',"")
				val = val.replace(']',"")
				val = val.replace(',',"")
				val = val.split()
				val[0]  =int(val[0])
				val[1] = int(val[1])
				self.history[key] = val
		except:
			pass
			
	def saveHistory(self,key,val):
		key = hashlib.sha224(key).hexdigest()
		if self.history.has_key(key):
			self.history[key][0] += val
			self.history[key][1] += 1
		else:
			self.history[key] = [val,1]
		w = csv.writer(open("history.csv", "w"))
		for key, val in self.history.items():
			w.writerow([key,val])

	def saveStats(self,key,val):
		file = open('stats.json', 'r')
		stats  = json.load(file)


def findFiles():
	exams = []
	directory = "./Questions"
	for file in os.listdir(directory):
		if file.endswith(".json"):
			exams.append(directory+'/'+file)
	return exams		
	
def readFile(filenames,exams):
	questions = []
	for n in range(0, len(filenames)):
		filename = filenames[n]
		if exams[n].get() == 1:
			file = open(filename, 'r')
			data  = json.load(file)
			numq = len(data)
			for i in range(0,numq):
				questions.append(Questions(data[i][0],data[i][1:5],ansList(data[i][5])))
	random.shuffle(questions)
	return questions	

def ansList(answer):
	answer = answer.split(',')
	anstemp = []
	a = ['a','b','c','d']
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
	tamos = TamosGame(tk,defaultbg,fileid)
	tk.mainloop()

if __name__ == '__main__':
    main()

