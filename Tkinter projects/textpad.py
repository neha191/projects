from tkinter import* 
from tkinter import filedialog, messagebox
import os
root=Tk()
root.title('Text Pad')

def on_find():
	t2=Toplevel(root)
	t2.title('Find')
	t2.geometry('262x65+200+250')
	t2.transient(root)
	Label(t2, text="Find All:").grid(row=0, column=0, sticky='e')
	v=StringVar()
	e=Entry(t2, width=25, textvariable=v)
	e.grid(row=0, column=1, padx=2, pady=2, sticky='we')
	e.focus_set()
	c=IntVar()
	Checkbutton(t2, text='Ignore Case', variable=c).grid(row=1, column=1, sticky='e', padx=2, pady=2)
	Button(t2, text='Find All', underline=0, command=lambda:search_for(v.get(), c.get(), textPad, t2, e)).grid(row=0, column=2, sticky='e'+'w', padx=2, pady=2)

def close_search():
	textPad.tag_remove('match','1.0',END)
	t2.destroy()
	
	t2.protocol('WM_DELETE_WINOW', close_search)

def search_for(needle, cssnstv, textPad, t2, e):
	textPad.tag_remove('match','1.0',END)
	count=0
	if needle:
		pos='1.0'
		while True:
			pos=textPad.search(needle, pos, nocase=cssnstv, stopindex=END)
			if not pos:
				break
			lastpos='%s+%dc' %(pos, len(needle))
			textPad.tag_add('match', pos, lastpos)
			count+=1
			pos = lastpos
	textPad.tag_config('match', foreground='red', background='yellow')
	e.focus_set()
	t2.title('%d matches found' %count)
	
def open_file():
		global filename
		filename=filedialog.askopenfilename(defaultextension='.txt', filetypes=[('All Files','*.*'),('Text Files','*.txt')])
		if filename=='':
			filename=None
		else:
			root.title(os.path.basename(filename)+'-pyPad')
			textPad.delete(1.0, END)
			fh=open(filename, 'r')
			textPad.insert(1.0, fh.read())
			fh.close()

def save():
	global filename
	try:
		f=open(filename, 'w')
		letter=textPad.get(1.0, 'end')
		f.write(letter)
		f.close()
	except:
		save_as()
		
def save_as():
	try:
		f=filedialog.asksaveasfilename(initaialfile='Untitled.txt', defaultextension='.txt', filetypes=[('All Files','*.*'),('Text Files','*.txt')])
		fh=open(f,'w')
		textoutput=textPad.get(1.0, END)
		fh.write(textoutput)
		fh.close()
		root.title(os.path.basename(f)+"-pyPad")
	except:
		pass

def new_file():
	root.title('Untitled')
	global filename
	filename=None
	textPad.delete(1.0, END)
	
def exit_editor():
	if messagebox.askokcancel('Quit','Do you really want to quit?'):
		root.destroy()
root.protocol('WM_DELETE_WINDOW', exit_editor)
	
	
menubar=Menu(root)

filemenu=Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='New File', command=new_file, compound=LEFT)
filemenu.add_command(label='Open', command=open_file, compound=LEFT)
filemenu.add_command(label='Save', command=save, compound=LEFT)
filemenu.add_command(label='Save as', command=save_as, compound=LEFT)
filemenu.add_command(label='Exit', command=exit_editor, compound=LEFT)

editmenu=Menu(menubar, tearoff=0)
menubar.add_cascade(label='Edit', menu=editmenu)
editmenu.add_command(label='Undo', compound=LEFT)
editmenu.add_command(label='Find', compound=LEFT, command=on_find)

viewmenu=Menu(menubar, tearoff=0)
menubar.add_cascade(label='View', menu=viewmenu)

aboutmenu=Menu(menubar, tearoff=0)
menubar.add_cascade(label='About', menu=aboutmenu)
root.config(menu=menubar)

shortcutbar=Frame(root, height=25, bg='light sea green').pack(expand=NO, fill=X)
Inlabel=Label(root, width=2, bg='antique white').pack(side=LEFT, anchor='nw', fill=Y)

textPad=Text(root, undo=True)
textPad.pack(expand=YES, fill=BOTH)
scroll=Scrollbar(textPad)
textPad.config(yscrollcommand=scroll.set)
scroll.config(command=textPad.yview)
scroll.pack(side=RIGHT, fill=BOTH)


root.mainloop()