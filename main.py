from tkinter import *
from tkinter import filedialog
from tkinter import font
from pathlib import Path
from tkinter import colorchooser
import os, sys
import win32print
import win32api

root = Tk()
root.title('AliFGT - Text Editor')
root.iconbitmap('assets/spaceship_red.ico')
root.geometry('1200x725')
ft = 'Helvetica'


# Set Var for Open File Name
global open_status_name
open_status_name = False

global selected
selected = False


# Create New File def
def new_file():
    my_text.delete('1.0', END)
    root.title('New File! - Text Editor')
    status_bar.config(text='New File        ')

    global open_status_name
    open_status_name = False


# Open Files
def open_file():
    my_text.delete('1.0', END)

    # Grab Filename
    text_file = filedialog.askopenfilename(initialdir=
        '/users/classroom/', title='Open Text',
            filetypes=[("Text File", "*.txt")])

    # Check to see if there is a file name
    if text_file:
        global open_status_name
        open_status_name = text_file

    # Update Status Bars and Replace Dialog
    name = text_file
    
    #لاخفاء الامتداد وعرض فقط اسم الملف
    p = Path(name)
    # print(p.stem)
    # print(p.name)

    status_bar.config(text=p.name + '        ')
    root.title(f'{p.stem} - Text Editor')

    # Open the File
    text_file = open(text_file, 'r')
    stuff = text_file.read()
    
    my_text.insert(END, stuff)
    text_file.close()


# Save As File
def save_as_file():
    text_file = filedialog.asksaveasfilename(
        initialdir='/users/classroom/', title='Save File',
        filetypes=[("Text Files", "*.txt")])
    
    if text_file:
        name = text_file
        p = Path(name)
        root.title(f'{p.stem} - Text Editor')
        status_bar.config(text=f'Saved {p.name}        ')

        # Save the File
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))
        text_file.close()


def save_file():
    global open_status_name
    if open_status_name:
        p = Path(open_status_name)
        # Save the File
        text_file = open(open_status_name, 'w')
        text_file.write(my_text.get(1.0, END))
        text_file.close()

        status_bar.config(text=f'Saved {p.name}        ')
    
    else:
        save_as_file()


def cut_text(e):
    global selected
    # Check to see if we used keyboard shortcuts
    if e:
        selected = root.clipboard_get()

    else:
        if my_text.selection_get():
            selected = my_text.selection_get()
            # Delete Selected Text from Text Box
            my_text.delete('sel.first', 'sel.last')

            root.clipboard_clear()
            root.clipboard_append(selected)


def copy_text(e):
    global selected
    # Check to see if we used keyboard shortcuts
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        selected = my_text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected)


def paste_text(e):
    global selected
    # Check to see if we used keyboard shortcuts
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)


# Bold
def bold_it():
    bold_font = font.Font(my_text, my_text.cget("font"))
    bold_font.configure(weight='bold')

    # Configure a Tag
    my_text.tag_configure('bold', font=bold_font)

    # Define current_tags
    current_tags = my_text.tag_names('sel.first')
    
    # If Statement to see tag has been set
    if 'bold' in current_tags:
        my_text.tag_remove("bold", 'sel.first', 'sel.last')
    else:
        my_text.tag_add('bold', 'sel.first', 'sel.last')


# Italics
def italics_it():
    italics_font = font.Font(my_text, my_text.cget("font"))
    italics_font.configure(slant='italic')

    # Configure a Tag
    my_text.tag_configure('italic', font=italics_font)

    # Define current_tags
    current_tags = my_text.tag_names('sel.first')
    
    # If Statement to see tag has been set
    if 'italic' in current_tags:
        my_text.tag_remove("italic", 'sel.first', 'sel.last')
    else:
        my_text.tag_add('italic', 'sel.first', 'sel.last')


# Change Selected Text Color
def text_color():
    # Pick a Color
    my_color = colorchooser.askcolor()[1]

    if my_color:

        color_font = font.Font(my_text, my_text.cget("font"))

        # Configure a Tag
        my_text.tag_configure('colored', font=color_font,
            foreground=my_color)

        # Define current_tags
        current_tags = my_text.tag_names('sel.first')
        
        # If Statement to see tag has been set
        if 'colored' in current_tags:
            my_text.tag_remove("colored", 'sel.first', 'sel.last')
        else:
            my_text.tag_add('colored', 'sel.first', 'sel.last')


def bg_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(bg=my_color)


def all_text_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(fg=my_color)


def print_file():
    # Take Printer Name
    # printer_name = win32print.GetDefaultPrinter()
    # status_bar.config(text=printer_name)
    
    # Grab Filename
    file_to_print = filedialog.askopenfilename(initialdir=
        '/users/classroom/', title='Open Text File',
            filetypes=[('Text Files', '*.txt')])
    
    if file_to_print:
        win32api.ShellExecute(0, 'print', file_to_print,
            None, '.', 0)


def select_all(e):
    # Add sel Tag to Select All
    my_text.tag_add('sel', '1.0', 'end')


def clear_all():
    my_text.delete(1.0, END)


def night_on():
    main_color = '#0A0D0C'
    second_color = '#373737'
    text_color = 'white'

    root.config(bg='#030F15')
    status_bar.config(bg='#030F15', fg=text_color)
    my_text.config(bg='#031425', fg=text_color)
    toolbar_frame.config(bg='#030F15')


def night_off():
    main_color = 'SystemButtonFace'

    root.config(bg=main_color)
    status_bar.config(bg=main_color, fg=main_color)
    my_text.config(bg=main_color, fg=main_color)
    toolbar_frame.config(bg=main_color)



# Create a ToolBar Frame
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X)

# Create Main Frame
my_frame = Frame(root)
my_frame.pack(pady=5)


# Create our ScrollBar
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)


# Horizontal ScrollBar
hor_scroll = Scrollbar(my_frame, orient=HORIZONTAL)
hor_scroll.pack(side=BOTTOM, fill=X)


# Create Text Box
my_text = Text(my_frame, width=77, height=19, font=(ft, 16),
    selectbackground='yellow', selectforeground='black',
        undo = True, yscrollcommand=text_scroll.set,
            wrap='none', xscrollcommand=hor_scroll.set)
# Wrap = اذا وصلنا نهاية السطر ماينزل للسطر الجديد ولديها عدة قيم
# Wrap = 'none' OR 'word' OR 'char'
my_text.pack()


# Configure our ScrollBar
text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)


# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add File Menu
file_menu = Menu(my_menu, tearoff = False)
# Tearoff = الخط الي بالبدايه نشيله

my_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='New', command=new_file)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_file)
file_menu.add_command(label='Save As', command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label='Print File', command=print_file)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.quit)


# Add Edit Menu
edit_menu = Menu(my_menu, tearoff=False)
# Tearoff = الخط الي بالبدايه نشيله

my_menu.add_cascade(label='Edit', menu=edit_menu)

edit_menu.add_command(label='Cut    ', accelerator="Ctrl+X",
    command=lambda: cut_text(False))
edit_menu.add_command(label='Copy    ', accelerator='Ctrl+C',
    command=lambda: copy_text(False))
edit_menu.add_command(label='Paste    ', accelerator="Ctrl+V",
    command=lambda: paste_text(False))

edit_menu.add_separator()
edit_menu.add_command(label='Undo    ', accelerator='Ctrl+Z',
    command=my_text.edit_undo)
edit_menu.add_command(label='Redo    ', accelerator='Ctrl+Y',
    command=my_text.edit_redo)

edit_menu.add_separator()
edit_menu.add_command(label='Select All    ',
    accelerator='Ctrl+A', command=lambda: select_all(True))
edit_menu.add_command(label='Clear All', command=clear_all)


# Add Color Menu
color_menu = Menu(my_menu, tearoff=False)

my_menu.add_cascade(label='Colors', menu=color_menu)

color_menu.add_command(label='Change Selected Text',
    command=text_color)
color_menu.add_command(label='All Text',command=all_text_color)
color_menu.add_command(label='Background',command=bg_color)


###########################################################################################################################
# Add Options Menu
options_menu = Menu(my_menu, tearoff = False)
my_menu.add_cascade(label='Options', menu=options_menu)
options_menu.add_command(label='Night Mode On',
    command=night_on)
options_menu.add_command(label='Night Mode Off',
    command=night_off)
###########################################################################################################################


# Add Status Bar to Bottom of App
status_bar = Label(root, text='Ready        ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)


# Edit Bindings
root.bind("<Control-x>", cut_text)
root.bind("<Control-c>", copy_text)
root.bind("<Control-v>", paste_text)
# Select Binding
root.bind('<Control-A>', select_all)
root.bind('<Control-a>', select_all)


# Create Buttons

# Bold Button
bold_button = Button(toolbar_frame, text='Bold',
    command=bold_it)
bold_button.grid(row=0, column=0, sticky=W, padx=5)

# Italics Button
italics_button = Button(toolbar_frame, text='Italics',
    command=italics_it)
italics_button.grid(row=0, column=1, padx=5)

# Undo & Redo Buttons
undo_button = Button(toolbar_frame, text='Undo',
    command=my_text.edit_undo)
undo_button.grid(row=0, column=2, padx=5)

redo_button = Button(toolbar_frame, text='Redo',
    command=my_text.edit_redo)
redo_button.grid(row=0, column=3, padx=5)


# Text Color
color_text_buuton = Button(toolbar_frame, text='Text Color',
    command=text_color)
color_text_buuton.grid(row=0, column=4, padx=5)



root.mainloop()
