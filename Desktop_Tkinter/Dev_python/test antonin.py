from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk


class App(tk.Tk):
    """ Application GUI in Tkinter"""
    def __init__(self):
        """ Application constructor (heritage=Tk object)"""
        super().__init__()
        self.screen_h = self.winfo_screenwidth()
        self.screen_v = self.winfo_screenheight()
        self.screen_x = 0
        self.screen_y = 0
        geometry = f"{self.screen_h}x{self.screen_v}+{self.screen_x}+{self.screen_y}"
        self.geometry(geometry)
        self.resizable(True, True)  # (width, height)
        self.minsize(100, 100)
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight())
        self.attributes('-alpha', 0.9)  # window transparency

        #### ICONE WINDOWS APPLI ###
        try:
            
            icon_path = Path("/home/user/Images/BARBAK.png")
            icon_img = Image.open(icon_path)
            icon_img = icon_img.convert("RGBA")
            self.icon_img = ImageTk.PhotoImage(icon_img)
            self.tk.call('wm', 'iconphoto', self._w, self.icon_img)

            self.title("Barbak")
            self.initWidget()

        except Exception as e:
            print(f"Error setting window icon: {e}")

    def initWidget(self):
        """ Init all widgets of the main window """

        self.img = tk.PhotoImage(file=Path("/home/user/Images/BARBAK.png"))
        print("Main image loaded successfully")      

        self.image = ttk.Label(self, image=self.img, text='UIMM', compound='top')
        self.image.pack()

        self.message = ttk.Label(self, text="Hello, MSIR5!", font=("Courier", 18), foreground="White", background="Blue")
        self.message.pack()

        self.btn1 = ttk.Button(self, text='Production', command=self.onBtn1Click)
        self.btn1.pack()

        self.btn2 = ttk.Button(self, text='Bom', command=self.onBtn2Click)
        self.btn2.bind('<Return>', self.onBtn2Click)  # need event arg
        self.btn2.focus()
        self.btn2.pack()

        self.quit_icon = tk.PhotoImage(file=Path("image/Quit.png"))
        self.btnQuit = ttk.Button(self, text='Exit',
        image=self.quit_icon, command=self.onBtnQuitClick)
        self.btnQuit.pack()
        
    def onBtn1Click(self):
        """ Callback Btn1 pressed """
        self.message['text'] = "mrp.production"

    def onBtn2Click(self, event=None):
        """ Callback Btn2 pressed """
        self.message.config(text="mrp.bom")
    
    def onBtnQuitClick(self):
        """ Callback Btn3 pressed """
        MsgBox = messagebox.askquestion (
        title='Quitter Application',
        message='Etes vous sur de vouloir quitter ?',
        icon='warning')
        if MsgBox == 'yes':
            self.quit()

if __name__ == "__main__":
    myApp = App()
    myApp.mainloop()
