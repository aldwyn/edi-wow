import Tkinter
import tkFileDialog
from Tkinter import *
import re
import calculator


class UI(Tkinter.Tk):
	def __init__(self):
		Tkinter.Tk.__init__(self)
		self.input_value = StringVar()
		self.lines_dict = {}
		self.memory = {}
		self.reserved_words = ['begin', 'end', 'vars', 'statements', 'read', 'print']
		self.init = []
		self.statements = []
		self.initialize()


	def execute(self, text):
		to_continue = self.parse_input(text)
		if to_continue:
			to_continue = self.parse_vars()
			if to_continue:
				self.execute_statements()


	def parse_input(self, text):
		self.fc = text
		fc_clone = []
		self.lines = [l.strip() for l in self.fc.split('\n')]
		for l in xrange(len(self.lines)):
			if self.lines[l].find('//') != -1:
				self.lines[l] = self.lines[l][:self.lines[l].find('//')]
		for l in xrange(len(self.lines)):
			self.lines_dict[self.lines[l].strip(';')] = str(l + 1)
		init_begin_index = -1
		init_end_index = -1
		if 'begin vars' in self.lines:
			init_begin_index = self.lines.index('begin vars')
		if 'end vars' in self.lines:
			init_end_index = self.lines.index('end vars')
		if init_begin_index != -1 and init_end_index != -1 and init_begin_index < init_end_index:
			self.init = [l.strip() for l in self.lines[init_begin_index + 1: init_end_index] if l.strip() != '']
		if init_begin_index == -1 or init_end_index == -1:
			self.log_error(self.lines[0].rstrip(';'), 'Missing `vars`.')
		statements_begin_index = -1
		statements_end_index = -1
		if 'begin statements' in self.lines:
			statements_begin_index = self.lines.index('begin statements')
		if 'end statements' in self.lines:
			statements_end_index = self.lines.index('end statements')
		if statements_begin_index == -1 or statements_end_index == -1:
			self.log_error(self.lines[0].rstrip(';'), 'Missing `statements`.')
		if statements_begin_index != -1 and statements_end_index != -1 and statements_begin_index < statements_end_index:
			self.statements = [l.strip() for l in self.lines[statements_begin_index + 1: statements_end_index] if l.strip() != '']
		input_spaces = self.lines[:init_begin_index] + self.lines[init_end_index+1:statements_begin_index] + self.lines[statements_end_index+1:]
		input_spaces = [e for e in input_spaces if e != '']
		if input_spaces:
			print input_spaces
			self.log_error(input_spaces[0].rstrip(';'), 'Syntax error')
			return False
		return True



	def check_valid_varname(self, v):
		if v[0].isalpha() or v[0] == '_' or v[0] == '$':
			if v.isalnum() or (v.isalnum() and v.find('_') != -1):
				if v not in self.reserved_words and v not in self.memory:
					return v
				else:
					return None
			return None
		return None

	def parse_vars(self):
		for i in self.init:
			if not i.endswith(';'):
				self.log_error(i.rstrip(';'), 'No semicolon found')
				return False
			i_split = i.rstrip(';')
			i_split = i_split.split('use as')
			var_split = i_split[0].split(',')
			for v in var_split:
				varname = self.check_valid_varname(v.strip())
				if varname:
					self.memory[varname] = [None, i_split[1].strip()]
				else:
					print i
					self.log_error(i.rstrip(';'), 'Invalid variable name')
					return False
		return True

	def execute_statements(self):
		for s in self.statements:
			if not s.endswith(';'):
				self.log_error(s.rstrip(';').rstrip(';'), 'No semicolon found.')
				return False
			s_split = s.rstrip(';')
			s_split = s_split.split(' ')
			if s_split[0] == 'read':
				if len(s_split) > 2:
					self.log_error(s.rstrip(';'), 'Multiple variables found')
					return False
				else:
					key = s_split[1].strip()
					curr_type = self.memory[key][1]
					self.get_input(key)

					input_ = self.input_value.get()
					print input_, type(input_)
					if curr_type == 'number':
						if self.is_number(input_):
							self.memory[key][0] = float(input_)
						else:
							self.log_error(s.rstrip(';'), 'Incompatible type')
							return False
					elif curr_type == 'word':
						self.memory[key][0] = input_
					else:
						self.log_error(s.rstrip(';'), 'Unknown datatype')
						return False
			elif s_split[0] == 'print':
				if len(s_split) > 2:
					self.log_error(s.rstrip(';'), 'Multiple variables found')
					return False
				else:
					print '>>> ' + str(self.memory[s_split[1].strip()][0])
					temp = '>>> ' + str(self.memory[s_split[1].strip()][0]) + "\n"
					self.console.insert(END, temp)
					self.console.yview(END)
			else:
				if s_split[0] not in self.memory:
					self.log_error(s.rstrip(';'), 'Variable undefined')
					return False
				else:
					if s_split[1] == '=':
						exp = s[s.find('=')+1:].strip().rstrip(';')
						exp_split = re.split('(\\+)|(\\-)|(\\*)|(\\/)|(\\()|(\\))|(\\^)|(\\".+?\\")', exp)
						exp_list = [e.strip() for e in exp_split if e and e.strip() != '']
						is_arithmetic = self.check_expr_type(exp_list)
						if is_arithmetic:
							exp_to_eval = self.translate_arithmetic(exp_list, s)
							if exp_to_eval:
								value = calculator.PostfixCalculator().converter(exp_to_eval)
								if value:
									self.memory[s_split[0]][0] = value
								else:
									self.log_error(s.rstrip(';'), 'Invalid expression')
									return False
							else:
								self.log_error(s.rstrip(';'), 'Invalid expression')
								return False
						else:
							exp_to_word = self.translate_word_expr(exp_list, s)
							if exp_to_word:
								self.memory[s_split[0]][0] = exp_to_word
							else:
								self.log_error(s.rstrip(';'), 'String concatenation error')
								return False
					else:
						self.log_error(s.rstrip(';'), 'Assignment error')
						return False
		return True


	def is_number(self, string):
		try:
			float(string)
			return True
		except:
			return False

	def check_expr_type(self, exp_list):
		is_arithmetic = True
		for exp in exp_list:
			if exp in self.memory:
				if self.memory[exp][1] == 'word':
					is_arithmetic = False
					break
		return is_arithmetic

	def translate_arithmetic(self, exp_list, s):
		to_return = ''
		for exp in exp_list:
			if exp in self.memory:
				if self.memory[exp][1] == 'number':
					if self.memory[exp][0]:
						to_return += str(self.memory[exp][0]) + ' '
					else:
						self.log_error(s.rstrip(';'), 'Null-pointer exception')
				else:
					return None
			else:
				if self.is_number(exp) or exp in ['+', '-', '*', '/', '(', ')', '^']:
					to_return += exp + ' '
				else:
					print 'not number'
					return None
		return to_return

	def translate_word_expr(self, exp_list, s):
		to_return = ''
		print exp_list
		for exp in exp_list:
			if exp in self.memory:
				if self.memory[exp][1] == 'number':
					if self.memory[exp][0]:
						mod = self.memory[exp][0] % 1.0
						to_concat = int(self.memory[exp][0]) if mod == 0 else float(self.memory[exp][0])
						to_return += str(to_concat)
					else:
						self.log_error(s.rstrip(';'), 'Null-pointer exception')
				else:
					to_return += self.memory[exp][0]
			else:
				if exp in ['-', '*', '/', '^']:
					return None
				elif exp == '+' or exp == '(' or exp == ')':
					continue
				elif exp.startswith('"') and exp.startswith('"'):
					to_return += exp.strip('"')
				else:
					if self.is_number(exp):
						mod = float(exp) % 1.0
						to_concat = int(float(exp)) if mod == 0 else float(exp)
						to_return += str(to_concat)
					else:
						return None
		return to_return


	def log_error(self, s, message):
		print 'S' ,s , message
		print 'Error at line ' + self.lines_dict[s] + ': ' + message + '.'
		error = 'Error at line ' + self.lines_dict[s] + ': ' + message + '\n'
		self.console.insert(END, error)
		self.console.yview(END)



	def initialize(self):
		self.filename = None
		self.title("IDE-WOW")
		self.menubar = Menu(self)
		self.config(menu = self.menubar)
		filemenu = Menu(self.menubar, tearoff=0)
		filemenu.add_command(label='Open', command=self.browse_file)
		filemenu.add_command(label='Save', command=self.save_file)
		filemenu.add_command(label='Reset', command=self.reset)
		filemenu.add_command(label='Exit', command=self.exit_program)
		self.menubar.add_cascade(label='File', menu=filemenu)
		filemenu_2 = Menu(self.menubar, tearoff=0)
		filemenu_2.add_command(label='Run File', command=self.run_file)
		self.menubar.add_cascade(label='Run', menu=filemenu_2)
		filemenu_3 = Menu(self.menubar, tearoff=0)
		filemenu_3.add_command(label='About')
		self.menubar.add_cascade(label='Help', menu=filemenu_3)
		self.main_frame = Frame(self, bg="#777")
		self.main_frame.bind("<Return>", self.run_file)

		self.input_field = Frame(self.main_frame, bg="black")
		self.line_number = Text(self.input_field, borderwidth=0, bg="#333", fg="magenta", width=5, height=30)
		self.line_number.pack(side=LEFT)
		self.text_area = Text(self.input_field, width=100, fg="green", bg="#333", height=30)
		self.text_area.config(insertbackground="white")
		self.text_area.pack()

		bindtags = list(self.text_area.bindtags())
		bindtags.insert(2, "custom")
		self.text_area.bindtags(tuple(bindtags))
		self.text_area.bind_class("custom", "<Key>", self.countlines)

		self.input_field.pack()

		self.console_frame = Frame(self.main_frame, bg="black")
		self.console = Text(self.console_frame, width=105, height=10, fg="white", bg="#333")
		self.console.pack()
		self.console_frame.pack(pady=5)
		self.main_frame.pack()

		self.resizable(False,False)

	def exit_program(self):
		exit()


	def reset(self):
		self.destroy()
		self.__init__()


	def countlines(self,event):
		(line, c) = map(int, event.widget.index("end-1c").split("."))
		self.line_number.config(state=NORMAL)
		self.line_number.delete(1.0, END)
		for x in xrange(line):
			string = ' ' + str(x+1) + '\n'
			self.line_number.insert(END, string)
			self.line_number.yview(END)
		self.line_number.config(state=DISABLED)
		self.line_number.yview(END)


	def run_file(self):
		text = self.text_area.get(1.0, END)
		self.execute(text)
		self.menubar.entryconfig("Run", state=DISABLED)


	def browse_file(self):
		variable = tkFileDialog.askopenfilename()
		if variable:
			self.filename = variable
			print self.filename
			with open(self.filename, 'r') as f:
				lines = f.readlines()
				for line in lines:
					self.text_area.insert(END, line)
				self.line_number.config(state=NORMAL)
				self.line_number.delete(1.0, END)
				for x in xrange(len(lines)):
					string = ' ' + str(x+1) + '\n'
					self.line_number.insert(END, string)
					self.line_number.yview(END)
				self.line_number.config(state=DISABLED)


	def save_file(self):	
		text = self.text_area.get(1.0, END)
		filename = tkFileDialog.asksaveasfilename()
		with open(filename, 'w') as f:
			f.write(text)

	def get_input(self, variable):
		self.inputDialog = Toplevel()
		frame = Frame(self.inputDialog, bg="#333")
		t = "ENTER VALUE FOR " + variable +": "
		Label(frame, text=t, width=50,fg="white", bg="#333").pack(pady=10)
		self.e = Entry(frame, textvariable=self.input_value)
		self.e.delete(0, END)
		self.e.insert(0, "")
		self.e.pack(pady=5)
		Button(frame, text='GO', padx=10, command=self.ok_button_click).pack(pady=10)
		frame.pack()
		self.wait_window(self.inputDialog)

	def ok_button_click(self):
		if self.input_value:
			self.inputDialog.destroy()
			return self.input_value.get()
		else:
			self.inputDialog.destroy()
			return None


if __name__ == '__main__':
	ui = UI()
	ui.mainloop()