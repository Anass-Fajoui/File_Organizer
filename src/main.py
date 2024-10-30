import tkinter as tk
import os
from tkinter import messagebox, filedialog

#---------------------- Functions ------------------------

pathy = ""
default_path = os.path.expanduser("~")
def chose_folder() :
    global pathy
    global default_path
    pathy = default_path = filedialog.askdirectory(initialdir=default_path, title = "Select a Folder")
    path_label.configure(text = f"Selected path : {pathy}")

def empty_dir(dir) :
    return os.listdir(dir) == []

def empty_file(file) :
    return os.stat(file).st_size == 0

def is_all_file(path, listy) :
    for item in listy :
        item = os.path.join(path, item)
        if os.path.isdir(item) :
            return False
    return True

def is_same_ext(path, listy) :
    if is_all_file(path, listy) :
        list_ext = list(map(lambda x : os.path.splitext(x)[1], listy))
        return len(set(list_ext)) == 1
    return False


def organize(path, final = 0) :
    if not os.path.exists(path) :
        messagebox.showwarning(title = "Path Issue", message = "The path you select is not valid or You haven't selected it yet")
        return
    item_list = os.listdir(path)
    #Check if the folder contain files with same extention and no folder is there, because if this is the case there is no need to organize
    if is_same_ext(path, item_list):
        if final == 0 :
            messagebox.showinfo(title = "Mission Complete", message = "Done")

        return
    
    for item in item_list :
        item_p = os.path.join(path, item)
        #check
        if os.path.isdir(item_p) and empty_dir(item_p) and var1.get():
            os.rmdir(item_p)
            continue
        if os.path.isfile(item_p) and empty_file(item_p) and var2.get():
            os.remove(item_p)
            continue
        if os.path.isdir(item_p) and var3.get() :
            organize(item_p, final = 1)
            continue
            
        if os.path.isfile(item_p) :
            n_dir = f"{path}\\Folder {os.path.splitext(item)[1]}"
            item_np= os.path.join(n_dir, item)
            if os.path.exists(n_dir) :
                os.replace(item_p, item_np)
            else :
                os.mkdir(n_dir)
                os.replace(item_p, item_np)

    if final == 0 :
        messagebox.showinfo(title = "Done", message = "The folder now is well organized")
        var1.set(0)
        var2.set(0)
        var3.set(0)
        global pathy
        pathy = ""
        path_label.configure(text = f"Selected path : {pathy}")


#---------------------- GUI ----------------------

app = tk.Tk()
app.title("File Organizer")
app.geometry("400x200")
app.iconbitmap("../assets/filemanager.ico")

label = tk.Label(app, text = "Enter the path :")
label.pack(padx = 10, pady = 5)

btn2 = tk.Button(app, text = "Select a folder", command = chose_folder)
btn2.pack()

path_label = tk.Label(app, text = f"Selected path : {pathy}")
path_label.pack()

var1 = tk.IntVar()       
check1 = tk.Checkbutton(app, text = "delete empty folder", variable =  var1)
check1.pack()
 
var2 = tk.IntVar()       
check2 = tk.Checkbutton(app, text = "delete empty file", variable = var2)
check2.pack()
  
var3 = tk.IntVar()       
check3 = tk.Checkbutton(app, text = "include subfolder", variable = var3)
check3.pack()
 
btn=tk.Button(app,text="submit",command = lambda : organize(pathy))
btn.pack(padx = 10, pady = 5)
app.resizable(False, False)

app.mainloop()
