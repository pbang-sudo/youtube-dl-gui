from tkinter import *
from tkinter import ttk
from pytube import *
from PIL import Image,ImageTk
import requests
import io
from os import path,mkdir
from socket import create_connection

class YouTube_app:
    def __init__(self,root):
        self.root = root
        self.root.title("Youtube Downloader")
        self.root.geometry("530x450+300+50")
        self.root.resizable(False,False)
        self.root.config(bg='white')
        self.pic=PhotoImage(file='icon.png')
        self.root.iconphoto(False,self.pic)
        
        self.var_url = StringVar()
        
        lbl_url = Label(self.root,text='Video URL',font=("arial",15),bg='white').place(x=10,y=50)
        txt_url = Entry(self.root,font=("arial",14),textvariable=self.var_url,bg='lightyellow').place(x=120,y=50,width=400)
        
        lbl_filetype = Label(self.root,text='File Type',font=("arial",15),bg='white').place(x=10,y=90)
        
        self.var_fileType = StringVar()
        self.var_fileType.set('Video')
        video_radio = Radiobutton(self.root,text='Video',variable=self.var_fileType,value='Video',font=("arial",15),bg='white',activebackground='white').place(x=120,y=90)
        audio_radio = Radiobutton(self.root,text='Audio',variable=self.var_fileType,value='Audio',font=("arial",15),bg='white',activebackground='white').place(x=240,y=90)
        
        self.btn_search = Button(self.root,text='Search',command=self.search,font='arial',bg='blue',fg='white')
        self.btn_search.place(x=400,y=90,height=30,width=120)
        
        frame1 = Frame(self.root,bd=2,relief=RIDGE,bg='lightyellow')
        frame1.place(x=20,y=130,width=500,height=180)
        
        self.video_title = Label(frame1,text='Video Title Here',font=("arial",12),bg='lightgray',anchor='w')
        self.video_title.place(x=0,y=0,relwidth=1)
        
        self.video_image = Label(frame1,text='Video \nImage',font=("arial",15),bg='lightgray',bd=2,relief=RIDGE)
        self.video_image.place(x=5,y=30,width=180,height=140)
        
        lbl_video_desc = Label(frame1,text='Description',font=("arial",15),bg='lightyellow').place(x=190,y=30)
        
        self.video_desc = Text(frame1,font=("arial",12),bg='lightyellow',bd=2,relief=RIDGE)
        self.video_desc.place(x=190,y=60,width=302,height=110)

        self.lbl_size = Label(self.root,text='Total Size: 0 MB',font=("arial",13),bg='white')
        self.lbl_size.place(x=10,y=315)
        
        self.lbl_percentage = Label(self.root,text='Downloading: 0%',font=("arial",13),bg='white')
        self.lbl_percentage.place(x=185,y=315)
        
        self.btn_clear = Button(self.root,text='Clear',command=self.clear,font=('arial',13),bg='lightgray',fg='white')
        self.btn_clear.place(x=370,y=315,height=30,width=60)
        self.btn_download = Button(self.root,text='Download',state=DISABLED,command=self.download,font=('arial',13),bg='green',fg='white')
        self.btn_download.place(x=435,y=315,height=30,width=90)

        self.prog = ttk.Progressbar(self.root,orient=HORIZONTAL,length=590,mode='determinate')
        self.prog.place(x=10,y=360,width=510,height=25)        

        self.lbl_message = Label(self.root,text='',font=("arial",13),bg='white')
        self.lbl_message.place(x=10,y=390,width=510)
        
        #Firstly checking the Internet Connection by running check_connection function
        if self.check_connection()==False:
            self.lbl_message.config(text='Your system is not connected to the Internet.\nFirst connect to a network then restart the app.',font=('arial',13,'bold'),fg='red')
            self.btn_search.config(state=DISABLED)
            self.btn_clear.config(state=DISABLED)
        
        #making directory for files
        if path.exists('Audios')==False:
            mkdir('Audios')
        if path.exists('Videos')==False:
            mkdir('Videos')
        
    def search(self):
        if self.var_url.get()=='':
            self.lbl_message.config('Video URL is required',fg='red')
        else:
            yt = YouTube(self.var_url.get())
        
            #converting image thumbnail url into image
            response = requests.get(yt.thumbnail_url)
            img_byte = io.BytesIO(response.content)
            self.img = Image.open(img_byte)
            self.img = self.img.resize((180,140),Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.img)
            self.video_image.config(image=self.img)
        
            #taking the file type as choice
            if self.var_fileType.get()=='Video':
                select_file = yt.streams.filter(progressive=True).first()
            if self.var_fileType.get()=='Audio':
                select_file = yt.streams.filter(only_audio=True).first()
        
            #calculating size of file
            self.size_inBytes = select_file.filesize
            max_size = self.size_inBytes/1024000
            self.mb = str(round(max_size,2))+'MB'
        
            #sending file metadata as inputs to GUI
            self.lbl_size.config(text='Total Size:'+self.mb)
            self.video_title.config(text=yt.title)
            self.video_desc.delete('1.0',END)
            self.video_desc.insert(END,yt.description)
            self.btn_download.config(state=NORMAL)
        
    def progress_(self,streams,chunk,bytes_remaining):
        percentage = (float(abs(bytes_remaining-(self.size_inBytes))/(self.size_inBytes)))*float(100)
        self.prog['value']=percentage
        self.prog.update()
        self.lbl_percentage.config(text=f'Downloading: {str(round(percentage,2))}%')
        
        if round(percentage,2)==100:
            self.lbl_message.config(text='Download Completed',fg='green')
            self.btn_download.config(state=DISABLED)

    def clear(self):
        self.var_fileType.set('Video')
        self.var_url.set('')
        self.prog['value']=0
        self.btn_download.config(state=DISABLED)
        self.lbl_message.config(text='')
        self.video_title.config(text='Video Title: ')
        self.video_desc.delete('1.0',END)
        self.video_image.config(image='')
        self.lbl_size.config(text='Total Size: 0 MB')
        self.lbl_percentage.config(text='Downloading: 0%')
        
    def download(self):
        yt = YouTube(self.var_url.get(),on_progress_callback=self.progress_)
        
        #taking the file type as choice
        if self.var_fileType.get()=='Video':
            select_file = yt.streams.filter(progressive=True).first()
            select_file.download('Videos/')
        if self.var_fileType.get()=='Audio':
            select_file = yt.streams.filter(only_audio=True).first()
            select_file.download('Audios/')

    #For checking if system is connected to Internet
    def check_connection(self):
        try:
            create_connection(('Google.com',80))
            return True
        except OSError:
            return False

root = Tk()
obj = YouTube_app(root)
root.mainloop()