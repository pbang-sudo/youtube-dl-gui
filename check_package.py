from tkinter import *
from tkinter import messagebox, ttk
from time import sleep
from subprocess import check_output,check_call
from sys import executable,exit
from socket import create_connection

class File_Check:
    #Initialising the main file checking window.
    def __init__(self,root):
        self.root = root
        self.root.title("File Checker")
        self.root.geometry("425x150+500+200")
        self.root.resizable(False,False)
        self.root.config(bg='lightgray')
        self.pic=PhotoImage(file='icon.png')
        self.root.iconphoto(False,self.pic)
        
        lbl_message1 = Label(self.root, text="NOTE: ",font=("Arial",13,'bold'),bg='lightgray',fg='red',anchor='w').place(x=10,y=5)
        lbl_message2 = Label(self.root,text="This is a one time process only. Please be patient.",font=("Arial",13),bg='lightgray',anchor='w').place(x=10,y=30)
        
        self.btn_start = Button(self.root,text='Check',font=('Arial',13,'bold'),fg='white',activeforeground='green',bd=1.5,command=self.check)
        self.btn_start.place(x=255,y=75,width=80)
        
        btn_abort = Button(self.root,text='Abort',font=('Arial',13,'bold'),fg='white',activeforeground='red',bd=1.5,command=exit).place(x=340,y=75)
        
        self.lbl_message = Label(self.root,text='DO NOT CLOSE THIS WINDOW.',font=("arial",13,'bold'),fg='red')
        self.lbl_message.place(x=10,y=120,width=410,height=25)
        
    #Function for checking if the required packages are installed in the system or not.    
    def check(self):
        reqs = check_output([executable,'-m','pip','freeze'])
        installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
        required_packages = ['Pillow','requests','pytube']
        self.not_installed=[]
        for i in required_packages:
            if i not in installed_packages:
                self.not_installed.append(i)

        self.message=""
        
        if not self.not_installed:
            self.message+="Everything looks fine, you are good to go." 
            self.response=messagebox.showinfo("Result",self.message)
            self.lbl_message.config(text='Now you can close this window or Click ABORT',fg='green')
            self.btn_start.config(state=DISABLED)
    
        else:
            if len(self.not_installed)==1:
                self.message+="Package: "
            else:
                self.message+="Packages: "
    
            for i in self.not_installed:
                self.message+=i
                if(self.not_installed.index(i)!=(len(self.not_installed)-1)):
                    self.message+=", "
    
            if len(self.not_installed)==1:
                self.message+=" is not installed in your system."
            else:
                self.message+=" are not installed in your system."
            messagebox.showerror("Error",self.message,icon='warning')
            if len(self.not_installed)>1:
                self.answer = messagebox.askyesno("Suggestion","Do you want to install missing packages?")
            else:
                self.answer = messagebox.askyesno("Suggestion","Do you want to install missing package?")
            if(self.answer==True):
                self.install_missing_packages()
            else:
                exit()
    
    #For checking if system is connected to Internet
    def check_connection(self):
        try:
            create_connection(('Google.com',80))
            return True
        except OSError:
            return False
    
    #Installing Missing Packages
    def install_missing_packages(self):
        #Firstly checking the Internet Connection by executing the function check_connection()
        if self.check_connection()==False:
            messagebox.showwarning('Error','Your system is not connected to Internet. First connect to a network then restart the app.')
        #Now if Internet is present then initiating the download and installation of the required packages
        else:
            for i in self.not_installed:
                check_call([executable,'-m','pip','install','--upgrade',str(i)])
            self.install_message = ""
            if len(self.not_installed)==1:
                self.install_message = "Package "+self.not_installed(0)+" has been successfully installed in your system."
            else:
                self.install_message+="Packages "
                for i in self.not_installed:
                    self.not_installed+=i+""
                    if self.not_installed.index(i)<(len(self.not_installed)-1):
                        self.install_message+=", "
        
root = Tk()
obj = File_Check(root)
root.mainloop()