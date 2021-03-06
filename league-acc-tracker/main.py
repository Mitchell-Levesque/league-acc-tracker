import tkinter as tk
from tkinter import messagebox
import pickle
import os
import webbrowser

# Global variables
e1 = None
e2 = None
e3 = None
window = None
root = None
accountDisplay = None
accPass = None
accUserName = None
accSumName = None
showFlag = 0
doubleClickFlag = 0
passShow = None
accountList = []
accountNames = []
file_path = None

class Account:
    def __init__(self, summonerName, userName, password):
        self.summonerName = summonerName
        self.userName = userName
        self.password = password

    def __str__(self):
        return "Summoner name: %s\nUsername: %s\nPassword: %s\n" % (self.summonerName, self.userName, self.password)

def showPass():
    global e3, showFlag
    if(showFlag == 1):
        showFlag = 0
        e3.config(show="*")
        passShow.config(text="Show")
    else:
        showFlag = 1
        e3.config(show="")
        passShow.config(text="Hide")

def addAccount():
    global e1, e2, e3, showFlag, passShow,window
    window = tk.Toplevel(root)
    window.geometry('400x150+350+220')
    window.resizable(width=False, height=False)
    window.title("Add Account")
    window.grab_set()
    window.focus()
    window.iconbitmap("icon.ico")

    tk.Label(window, text="Summoner Name", font=("Helvetica", 12), padx=15, pady=5).grid(row=0)
    tk.Label(window, text="Account Username", font=("Helvetica", 12), padx=15, pady=5).grid(row=1)
    tk.Label(window, text="Account Password", font=("Helvetica", 12), padx=15, pady=5).grid(row=2)

    e1 = tk.Entry(window, font=("Helvetica", 12))
    e2 = tk.Entry(window, font=("Helvetica", 12))
    e3 = tk.Entry(window, font=("Helvetica", 12), show="*")

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)

    passShow = tk.Button(window, text="Show", command=showPass)
    passShow.grid(row=2, column=3)

    addAcc = tk.Button(window, text="Add Account", command=confirmAccount)
    addAcc.place(x=150, y=110, width=100)

def confirmAccount():
    global e1,e2,e3,accountList,window
    summonerName = e1.get()
    userName = e2.get()
    password = e3.get()
    if summonerName == "" or userName == "" or password == "":
        messagebox.showwarning("Blank Field", "No field can be left empty.")
        return
    account = Account(summonerName, userName, password)
    accountList.append(account)
    accountNames.append(account.summonerName)
    accountDisplay.insert(tk.END, account.summonerName)
    window.destroy()

def editAccount():
    global e1, e2, e3,passShow,window, accountList, accSumName, accountNames
    accountName = accSumName.cget("text")
    if(accountName == ""):
        return
    index = accountNames.index(accountName)
    account = accountList[index]

    window = tk.Toplevel(root)
    window.geometry('400x150+350+220')
    window.resizable(width=False, height=False)
    window.title("Edit Account")
    window.grab_set()
    window.focus()
    window.iconbitmap("icon.ico")

    tk.Label(window, text="Summoner Name", font=("Helvetica", 12), padx=15, pady=5).grid(row=0)
    tk.Label(window, text="Account Username", font=("Helvetica", 12), padx=15, pady=5).grid(row=1)
    tk.Label(window, text="Account Password", font=("Helvetica", 12), padx=15, pady=5).grid(row=2)

    e1 = tk.Entry(window, font=("Helvetica", 12))
    e2 = tk.Entry(window, font=("Helvetica", 12))
    e3 = tk.Entry(window, font=("Helvetica", 12), show="*")

    e1.insert(0, account.summonerName)
    e2.insert(0, account.userName)
    e3.insert(0, account.password)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)

    passShow = tk.Button(window, text="Show", command=showPass)
    passShow.grid(row=2, column=3)

    addAcc = tk.Button(window, text="Save Changes", command=saveChanges)
    addAcc.place(x=150, y=110, width=100)

def saveChanges():
    global e1, e2, e3, accountList, accSumName, accountNames, accountDisplay, accUserName, accPass
    accountName = accSumName.cget("text")
    if(accountName == ""):
        return
    index = accountNames.index(accountName)
    account = accountList[index]

    summonerName = e1.get()
    userName = e2.get()
    password = e3.get()
    if summonerName == "" or userName == "" or password == "":
        messagebox.showwarning("Blank Field", "No field can be left empty.")
        return

    account.summonerName = summonerName
    account.userName = userName
    account.password = password
    accountNames[index] = summonerName

    accountDisplay.delete(index)
    accountDisplay.insert(index, summonerName)
    
    accSumName.config(text=summonerName)
    accUserName.config(text=userName)
    starpass = ""
    for i in range(len(password)):
        starpass = starpass+"*"
    accPass.config(text=starpass)

    window.destroy()

def OPGG():
    global accSumName
    accName = accSumName.cget("text")
    if(accName == ""):
        return
    opstr = 'https://na.op.gg/summoner/userName='
    link = opstr + accName
    webbrowser.open_new_tab(link)

def multiOPGG():
    global accountNames
    link = 'https://na.op.gg/multi/query='
    for name in accountNames:
        name = name.replace(" ", "")
        print(name)

def viewAccount():
    global accPass, accSumName, accUserName
    try:
        accName = accountDisplay.get(accountDisplay.curselection())
    except:
        return
    index = accountNames.index(accName)
    account = accountList[index]
    summoner = account.summonerName
    username = account.userName
    password = account.password
    starpass = ""
    for i in range(len(password)):
        starpass = starpass+"*"
    accPass.config(text=starpass)
    accUserName.config(text=username)
    accSumName.config(text=summoner)

def deleteAccount():
    global accountDisplay, accountList, accSumName
    accountName = accSumName.cget("text")
    if(accountName == ""):
        return
    delete = messagebox.askokcancel("Delete %s?" % accountName,"Would you like to delete account %s?" % accountName)
    if(delete):
        idx = accountNames.index(accountName)
        accountDisplay.delete(idx)
        accountList.pop(idx)
        accountNames.pop(idx)
        resetInfo()

def updateAccountDisplay():
    global accountDisplay, accountList
    accountDisplay.delete(0, tk.END)
    for account in accountList:
        accountDisplay.insert(tk.END, account.summonerName)

def resetInfo():
    global accPass, accUserName, accSumName
    accPass.config(text="")
    accUserName.config(text="")
    accSumName.config(text="")

def copyPass():
    global root, accPass, accSumName, accountNames, accountList
    summoner = accSumName.cget("text")
    index = accountNames.index(summoner)
    psw = accountList[index].password
    root.clipboard_clear()
    root.clipboard_append(psw)
    root.update()

def copyUser():
    global root, accUserName
    root.clipboard_clear()
    user = accUserName.cget("text")
    root.clipboard_append(user)
    root.update()

if __name__ == "__main__":
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'accdata')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    
    file_path = os.path.join(final_directory, r'accdata.dat')
    if(os.path.exists(file_path)):
        try:
            with open(file_path, 'rb') as datafile:
                accountList = pickle.load(datafile)
            for account in accountList:
                accountNames.append(account.summonerName)
        except Exception as e:
            print(e)

    root = tk.Tk()
    root.resizable(width=False, height=False)
    root.geometry('600x300+300+200')
    root.title("League Account Manager")
    root.iconbitmap("icon.ico")

    addAccount = tk.Button(root, text="Add Account", padx=2, pady=2, width=12, command=addAccount)
    addAccount.place(x=400,y=18)

    frame = tk.Frame(root, padx=2, pady=2,highlightbackground="black", highlightthickness=1)
    frame.place(x=300, y=60, width=298, height=238)

    accInfoLabel = tk.Label(frame, text="Account Info", font=("Helvetica", 16))
    accInfoLabel.pack()

    accSumNameLbl = tk.Label(frame, text="Summoner:", font=("Helvetica", 12))
    accSumNameLbl.place(x=7, y=40)

    accSumName = tk.Label(frame, text="", font=("Helvetica", 12))
    accSumName.place(x=100, y=40)

    accUserNameLbl = tk.Label(frame, text="Username:", font=("Helvetica", 12))
    accUserNameLbl.place(x=7, y=80)

    accUserName = tk.Label(frame, text="", font=("Helvetica", 12))
    accUserName.place(x=100, y=80)

    accPassLbl = tk.Label(frame, text="Password:", font=("Helvetica", 12))
    accPassLbl.place(x=7, y=120)

    accPass = tk.Label(frame, text="", font=("Helvetica", 12))
    accPass.place(x=100, y=120)

    copyUserButton = tk.Button(frame, text="Copy", command=copyUser)
    copyUserButton.place(x=250,y=80)

    copyPassButton = tk.Button(frame, text="Copy", command=copyPass)
    copyPassButton.place(x=250,y=120)

    removeButton = tk.Button(frame, text="Remove", padx=2, pady=2, width=10, command=deleteAccount)
    removeButton.place(x=195,y=200)

    editButton = tk.Button(frame, text="OP.GG", padx=2, pady=2, width=10, command=OPGG)
    editButton.place(x=15,y=200)

    viewButton = tk.Button(frame, text="Edit", padx=2, pady=2, width=10, command=editAccount)
    viewButton.place(x=105,y=200)

    accountDisplay = tk.Listbox(root, font=("Helvetica", 13), activestyle="none", selectbackground="#999999")
    accountDisplay.place(width=300, height=300)
    scrollbar = tk.Scrollbar(accountDisplay, orient="vertical")
    scrollbar.config(command=accountDisplay.yview)
    scrollbar.pack(side="right", fill="y")
    accountDisplay.config(yscrollcommand=scrollbar.set)
    accountDisplay.bind('<<ListboxSelect>>', lambda x: viewAccount())

    updateAccountDisplay()
    
    root.mainloop()

    with open(file_path, 'wb') as datafile:
        pickle.dump(accountList, datafile)
