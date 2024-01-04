import sys
import datetime as dt
#=================================================================
class App(tk.Tk):
    """ Application GUI in TKinter"""
    def __init__(self):
        """ Application constructor (heritage=Tk object)"""
        super().__init__()
        self.ifOdoo = IF_Odoo("172.20.10.9", "8069", "vitre", "inter", "inter")
    
    def update(self):
        """ Application graphics user interface update """
        date = dt.datetime.now()
        date_str = f'[{date:%d-%m-%Y :: %H hrs %M min %S sec}]'
        self.after(5000, self.update) # refresh in 5000msec
