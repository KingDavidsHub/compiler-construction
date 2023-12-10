from tkinter import *

import tkinter.scrolledtext as scrolledtext

#To be able to prompt the user to save
from tkinter.filedialog import asksaveasfilename, askopenfilename

#For asynchronous execution of the code
import subprocess

#initializing the compiler
compiler = Tk()

#Naming the compiler
compiler.title("My Compiler Project")

#Storing the file path
file_path = ''

#Function that captures the file path
def set_file_path(path):
    global file_path
    file_path = path

#Declaring the open file function
def open_File():
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        #Reads the content of the file to be opened
        code = file.read()
        #Clears the text editor of existing content if any
        editor.delete('1.0', END)
        #Inserts the content of file to be opened
        editor.insert('1.0', END)
        #Storing the file path
        set_file_path(path)

#Declaring the Save As function
def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
        path = file_path    
    with open(path, 'w') as file:
        #Gets the content of the file to be saved
        code = editor.get('1.0', END)
        file.write(code)
        #Storing the file path
        set_file_path(path)

#Declaring a function that runs the code when the run button is clicked
def run():
    #Gets the 
    code = editor.get("1.0", END)
    
    try:
        # Declares the process variable as global, making it accessible outside the function's scope
        global process
        # Starts a new process and passes the Python interpreter, the script name ("compiler.py"), and the code as arguments
        process = subprocess.Popen(
             # Command to run the Python script externally
            ["python", "compiler.py", code], 
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        # Communicates with the process, capturing the standard output and standard error
        stdout, stderr = process.communicate(input=None)

        # Sets the state of the output to normal (editable)
        code_output.config(state=NORMAL)
        #Clears the output section of the IDE
        code_output.delete("1.0", END)
        #Inserts the output into the output
        code_output.insert(END, stdout)
         # If there is an error (stderr) inserts it into the output with a "red" tag
        if stderr:
            code_output.insert(END, stderr, "error")
         # Sets the state of the output to disabled (non-editable)
        code_output.config(state=DISABLED)
    # If an exception occurs, display an error message in the output area
    except Exception as e:
        code_output.config(state=NORMAL)
        code_output.delete("1.0", END)
        code_output.insert(END, f"Error: {str(e)}")
        code_output.config(state=DISABLED)

#Used to exit the IDE
def exit_program():
        compiler.destroy()

#Used to cut text from the text editor
def cut_text():
        Text.event_generate("<<Cut>>")

#Used to copy text from the text editor
def copy_text(self):
        Text.event_generate("<<Copy>>")

#Used to paste text into the text editor
def paste_text(self):
        Text.event_generate("<<Paste>>")

#Creating a menu bar
menu_bar = Menu(compiler)

#Creating a file menu
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Open', command=open_File)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_separator()

#Creating an exit button for the IDE
file_menu.add_command(label='Exit', command=exit)

 # Edit menu
edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Paste", command=paste_text)
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=Text.edit_undo)
edit_menu.add_command(label="Redo", command=Text.edit_redo)


#Creating a run bar on top of the menu bar
run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)
compiler.config(menu=menu_bar)

#creating a text environment for the compiler and specifying the color
editor = Text(bg="Beige", width=100, fg="Dark blue")
editor.pack()

#To label the output part of our IDE
text_label = Label(compiler, text="OUTPUT:")
text_label.pack()

#To create a code output area in our IDE
code_output = scrolledtext.ScrolledText(bg="Beige", fg='Dark blue', height=14, width=100)
code_output.pack(expand=True, fill='both')
code_output.tag_configure("error", foreground="red")
code_output.config(state=DISABLED)

#Starts the main event loop allowing the GUI to respond to user interactions
compiler.mainloop()