import Tkinter
import tkFileDialog
from Tkinter import *
import myhl



class UI(Tkinter.Tk):
	def __init__(self):
		Tkinter.Tk.__init__(self)
		self.reserved_words = [""]
		self.input_value = StringVar()
		self.myhl = myhl.MyHL()
		self.initialize()

	def initialize(self):
		self.filename = None

		self.title("Very Simple IDE")
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
		self.console = Text(self.console_frame, width=105, height=10, bg="#333")
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
		self.myhl.execute(text)


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

	def get_input(self):
		self.inputDialog = Toplevel()
		frame = Frame(self.inputDialog, bg="#333")
		Label(frame, text="ENTER VALUE: ", width=50,fg="white", bg="#333").pack(pady=10)
		Entry(frame, textvariable=self.input_value).pack(pady=5)
		Button(frame, text='GO', padx=10, command=self.ok_button_click).pack(pady=10)
		frame.pack()

	def ok_button_click(self):
		if self.input_value:
			self.inputDialog.destroy()
			self.myhl.get_raw_input(self.input_value.get())
			return self.input_value.get()
		else:
			self.inputDialog.destroy()
			return None


if __name__ == '__main__':
	ui = UI()
	ui.mainloop()