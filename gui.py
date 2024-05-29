import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from tkinter import font
from Final_functionfile import *
from receipts import *

#function to initialize total
def initialize_total():
    conn = sqlite3.connect('finalproject.db')
    c = conn.cursor()
    c.execute("SELECT final FROM total ORDER BY rowid DESC LIMIT 1")
    result = c.fetchone()
    conn.commit()
    conn.close()
    return result[0] if result else 0

total = initialize_total()
#class to connect database
class ProjectDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
#main window class
class Application(tk.Tk):
    def __init__(self, db_file):
        super().__init__()
        self.geometry("355x450")
        self.minsize(355, 450)
        self.maxsize(355, 450)

        self.title("Expense Tracker")
        self.db = ProjectDB(db_file)
        self.create_widgets()

#main screen window
    def create_widgets(self):
        global total
        self.mainframe=tk.Frame(self,relief=tk.RAISED, bd=2,bg="white")
        self.mainframe.place(x=0,y=0,width=355,height=450)

        self.currentbalanceframe = tk.Frame(self.mainframe,bg="white")
        self.currentbalanceframe.pack(fill=tk.X, pady=5)
        self.currentlabel = tk.Label(
            self.currentbalanceframe, text=str( initialize_total())+"$", font="ariel 18 bold",foreground="green",bg="white")
        self.currentlabel.grid(row=0, column=0,sticky="w",padx=10)

        self.menubutton_frame=tk.Frame(self.currentbalanceframe,bg="white")
        self.menubutton_frame.grid(row=0,column=1 ,padx=5, pady=5)
        self.menu_var = tk.StringVar()
        self.menu_combobox = ttk.Combobox(self.menubutton_frame, textvariable=self.menu_var, values=["Analysis", "Edit", "Delete","Expense Sharing"],height=1,width=11)
        self.menu_combobox.bind("<<ComboboxSelected>>", self.combofunction)
        self.menu_combobox.grid(row=0,column=2,sticky="w")
        self.menu_combobox.set("Menu")

        self.value_label = tk.Label(self.currentbalanceframe, text="Current Balance", font="ariel 8 bold", foreground="grey",bg="white")
        self.value_label.grid(row=1, column=0, padx=10,sticky="w")
        self.tranhistory = tk.Label(self.currentbalanceframe, text="Transaction History:                    ", font="ariel 12 bold",bg="white")
        self.tranhistory.grid(row=2, column=0, padx=5)

        self.history_frame = tk.Frame(self.mainframe,bg="white")
        self.history_frame.pack(fill=tk.X,padx=5)
        self.lbx2=tk.Listbox(self.history_frame,width=47,height=18)
        self.lbx2.grid(row=0,column=0,padx=5)
        ana_all(self)

        self.button_frame = tk.Frame(self.mainframe,bg="white")
        self.button_frame.pack(padx=10,pady=5)
        self.inbutton = tk.Button(self.button_frame, text="CASH IN", width=10, height=2,command=self.IN,foreground="white",background="green")
        self.inbutton.pack(side=tk.LEFT, padx=10,pady=5)
        self.outbutton = tk.Button(self.button_frame, text="CASH OUT", width=10, height=2,command=self.OUT,foreground="white",background="red")
        self.outbutton.pack(side=tk.LEFT, padx=10,pady=5)

#cash in window
    def IN(self):
        self.frame1=tk.Frame(self,bg="white")
        self.frame1.place(x=0,y=0,width=355,height=450)
        self.label1=tk.Label(self.frame1,text="Deposit:                  ",padx=10,pady=20,font="ariel 12 bold",bg="white")
        self.label1.grid(row=0,column=0)
        self.label2=tk.Label(self.frame1,text="Amount :",padx=10,pady=10,bg="white")
        self.label2.grid(row=1,column=0)
        self.integer=tk.IntVar()
        self.entry1=tk.Entry(self.frame1,textvariable=self.integer,highlightthickness=2)
        self.entry1.config( highlightcolor="black")
        self.entry1.grid(row=1,column=1)
        self.button4=tk.Button(self.frame1,text="Create",width=8,height=1,bg="black",fg="white",command=lambda: in_(self,self.entry1))
        self.button4.grid(row=2,column=0,pady=10)
        self.button5=tk.Button(self.frame1,text="Home",width=8,height=1,command=self.create_widgets,bg="black",fg="white")
        self.button5.grid(row=2,column=1,pady=10)

# cash out window
    def OUT(self):
        self.frame2=tk.Frame(self,bg="white")
        self.frame2.place(x=0,y=0,width=355,height=450)
        self.label4=tk.Label(self.frame2,text="Withdraw:                  ",padx=10,pady=20,font="ariel 12 bold",bg="white")
        self.label4.grid(row=0,column=0)
        self.label5=tk.Label(self.frame2,text="Amount :",padx=10,pady=10,bg="white")
        self.label5.grid(row=2,column=0)
        self.integer1=tk.IntVar()
        self.entry5=tk.Entry(self.frame2,textvariable=self.integer1,highlightthickness=2)  # Set the border width
        self.entry5.config( highlightcolor="black")
        self.entry5.grid(row=2,column=1)
        self.label6=tk.Label(self.frame2,text="Category :",padx=10,pady=10,bg="white")
        self.label6.grid(row=3,column=0)

        self.catg_var = tk.StringVar()
        self.catg_combobox = ttk.Combobox(self.frame2, textvariable=self.catg_var, values=["Grocery", "School fee", "Monthly Rent","Electricity","Gas","Other"],height=1,width=17)
        self.catg_combobox.bind("<<ComboboxSelected>>", self.combofunction)
        self.catg_combobox.grid(row=3,column=1)
        self.catg_combobox.current(5)

        self.button6=tk.Button(self.frame2,text="Create",width=8,height=1,command=lambda: out_(self,self.entry5,self.catg_var),bg="black",fg="white")
        self.button6.grid(row=4,column=0,pady=10)
        self.button7=tk.Button(self.frame2,text="Home",command=self.create_widgets,width=8,height=1,bg="black",fg="white")
        self.button7.grid(row=4,column=1,pady=10)

#menu button combobox function
    def combofunction(self,event):
        selected=self.menu_combobox.get()
        if selected== "Analysis":
            self.Analysiswindow()
        elif selected== "Edit":
            self.Editwindow()
        elif selected== "Delete":
            self.Deletewindow()
        elif selected== "Expense Sharing":
            self.Expensewindow()

#Analysis button window  (frame 3)
    def Analysiswindow(self):
        self.frame3=tk.Frame(self,bg="white")
        self.frame3.place(x=0,y=0,width=355,height=450)

        self.analysisbuttonframe=tk.Frame(self.frame3,bg="white")
        self.analysisbuttonframe.grid(row=0,column=0,padx=5,pady=5)

        #All buttons--------------------------------------------------
        self.monthlybutton=tk.Button(self.analysisbuttonframe,text="Monthly",width=8,height=1,command=self.askmonthlywindow,bg="black",fg="white")
        self.monthlybutton.grid(row=0,column=0,padx=5,pady=5,sticky="w")
        self.weeklybutton=tk.Button(self.analysisbuttonframe,text="Weekly",width=8,height=1,command=self.askweeklywindow,bg="black",fg="white")
        self.weeklybutton.grid(row=3,column=0,padx=5,pady=5,sticky="w")
        self.dailybutton=tk.Button(self.analysisbuttonframe,text="Daily",command=self.askdailywindow,width=8,height=1,bg="black",fg="white")
        self.dailybutton.grid(row=4,column=0,padx=5,pady=5,sticky="w")
        self.categorybutton=tk.Button(self.analysisbuttonframe,text="Category",command=self.askcategorywindow,width=8,height=1,bg="black",fg="white")
        self.categorybutton.grid(row=5,column=0,padx=5,pady=5,sticky="w")

        #list box frame and box-------------------------------------------
        self.listframe=tk.Frame(self.frame3,bg="white")
        self.listframe.grid(row=1,column=0,padx=10,pady=5)
        self.lbx=tk.Listbox(self.listframe,width=50,height=12,bd=1, relief="sunken")
        self.lbx.grid(row=0,column=0,padx=10,pady=5)
        self.homebutton45=tk.Button(self.listframe,text="Home",command=self.create_widgets,width=8,height=1,bg="black",fg="white")
        self.homebutton45.grid(row=1,column=0,padx=10,pady=5)

#window to ask parameters for month (frame 4)
    def askmonthlywindow(self):
        self.frame4=tk.Frame(self,bg="white")
        self.frame4.place(x=0,y=0,width=355,height=450)

        #button frame
        self.manalysisbuttonframe=tk.Frame(self.frame4,bg="white")
        self.manalysisbuttonframe.grid(row=0,column=0,padx=5,pady=5)

        # monthly button----------------------------------------
        self.monthlybutton=tk.Button(self.manalysisbuttonframe,text="Monthly",width=8,height=1,command=self.askmonthlywindow,bg="black",fg="white")
        self.monthlybutton.grid(row=0,column=0,padx=5,pady=5,sticky="w")

        #labels and combo boxes to ask-------------------------------------
        self.monthlabel=tk.Label(self.manalysisbuttonframe,text="Month",bg="white")
        self.monthlabel.grid(row=1,column=0,padx=5,pady=5,sticky="w")

        self.month_var1 = tk.StringVar()
        self.numbers = list(range(1, 13))
        self.month_combobox = ttk.Combobox(self.manalysisbuttonframe, textvariable=self.month_var1, values=self.numbers,height=1,width=4)
        self.month_combobox.bind("<Return>", self.showmonthly)
        self.month_combobox.grid(row=1,column=1,sticky="w")
        self.month_combobox.current(0)

        self.yearlabel=tk.Label(self.manalysisbuttonframe,text="Year",bg="white")
        self.yearlabel.grid(row=2,column=0,padx=5,pady=5,sticky="w")
        self.year_var1 = tk.StringVar()
        self.numbers2=list(range(2024,2030))
        self.year_combobox = ttk.Combobox(self.manalysisbuttonframe, textvariable=self.year_var1, values=self.numbers2,height=1,width=4)
        self.year_combobox.bind("<<ComboboxSelected>>", self.showmonthly)
        #self.year_combobox.bind("<Return>", self.showmonthly)

        self.year_combobox.grid(row=2,column=1,sticky="w")
        self.year_combobox.current(0)



        #weekly,daily and category button---------------------------------------
        self.weeklybutton=tk.Button(self.manalysisbuttonframe,text="Weekly",command=self.askweeklywindow,width=8,height=1,bg="black",fg="white")
        self.weeklybutton.grid(row=3,column=0,padx=5,pady=5,sticky="w")
        self.dailybutton=tk.Button(self.manalysisbuttonframe,text="Daily",command=self.askdailywindow,width=8,height=1,bg="black",fg="white")
        self.dailybutton.grid(row=4,column=0,padx=5,pady=5,sticky="w")

        self.categorybutton=tk.Button(self.manalysisbuttonframe,text="Category",command=self.askcategorywindow,width=8,height=1,bg="black",fg="white")
        self.categorybutton.grid(row=5,column=0,padx=5,pady=5,sticky="w")

        #listbox---------------------------------------------------------
        self.listframe=tk.Frame(self.frame4,bg="white")
        self.listframe.grid(row=1,column=0,padx=5,pady=5)
        self.lbx=tk.Listbox(self.listframe,width=50,height=8,bd=1, relief="sunken")
        self.lbx.grid(row=0,column=0,padx=10,pady=5)

        self.btframe=tk.Frame(self.frame4,bg="white")
        self.btframe.grid(row=2,column=0,padx=5,pady=5)
        self.homebutton=tk.Button(self.btframe,text="Home",command=self.create_widgets,width=8,height=1,bg="black",fg="white")
        self.homebutton.grid(row=0,column=0,padx=5,pady=5,sticky="w")
        self.Recieptbutton=tk.Button(self.btframe,text="Reciept",command=lambda:mon_recipt(self,int(self.month_var1.get()),int(self.year_var1.get())),width=8,height=1,bg="black",fg="white")
        self.Recieptbutton.grid(row=0,column=1,padx=5,pady=5,sticky="w")
#display of moonthly analysis
    def showmonthly(self,event):
        ana_mon(self,int(self.year_var1.get()),int(self.month_var1.get()))

#window to ask parameters for weekly analysis (frame 5)
    def askweeklywindow(self):
        self.frame5=tk.Frame(self,bg="white")
        self.frame5.place(x=0,y=0,width=350,height=450)

        self.wanalysisbuttonframe=tk.Frame(self.frame5,bg="white")
        self.wanalysisbuttonframe.grid(row=0,column=0,padx=5,pady=5)

        #monthly and weeekly button---------------------------------------
        self.monthlybutton2=tk.Button(self.wanalysisbuttonframe,text="Monthly",width=8,height=1,command=self.askmonthlywindow,bg="black",fg="white")
        self.monthlybutton2.grid(row=0,column=0,padx=5,pady=5,sticky="w")
        self.weeklybutton2=tk.Button(self.wanalysisbuttonframe,text="Weekly",command=self.askweeklywindow,width=8,height=1,bg="black",fg="white")
        self.weeklybutton2.grid(row=1,column=0,padx=5,pady=5,sticky="w")

        #labels and comboboxes-----------------------------------------------------
        self.monthlabel2=tk.Label(self.wanalysisbuttonframe,text="Month",bg="white")
        self.monthlabel2.grid(row=2,column=0,padx=5,pady=5,sticky="w")

        self.month_var2= tk.StringVar()
        self.numbers2_1 = list(range(1, 13))
        self.month_combobox2 = ttk.Combobox(self.wanalysisbuttonframe, textvariable=self.month_var2, values=self.numbers2_1,height=1,width=4)
        self.month_combobox2.bind("<Return>", self.showweekly)
        self.month_combobox2.grid(row=2,column=1,sticky="w")
        self.month_combobox2.current(0)

        self.yearlabel2=tk.Label(self.wanalysisbuttonframe,text="Year",bg="white")
        self.yearlabel2.grid(row=3,column=0,padx=5,pady=5,sticky="w")

        self.year_var2 = tk.StringVar()
        self.numbers2_2=list(range(2024,2030))
        self.year_combobox2 = ttk.Combobox(self.wanalysisbuttonframe, textvariable=self.year_var2, values=self.numbers2_2,height=1,width=4)
        self.year_combobox2.bind("<Return>", self.showweekly)
        self.year_combobox2.grid(row=3,column=1,sticky="w")
        self.year_combobox2.current(0)

        self.weeklabel2=tk.Label(self.wanalysisbuttonframe,text="Week",bg="white")
        self.weeklabel2.grid(row=4,column=0,padx=5,pady=5,sticky="w")

        self.week_var2 = tk.StringVar()
        self.numbers2_3=list(range(1,50))
        self.week_combobox2 = ttk.Combobox(self.wanalysisbuttonframe, textvariable=self.week_var2, values=self.numbers2_3,height=1,width=4)
        self.week_combobox2.bind("<<ComboboxSelected>>", self.showweekly)
        self.week_combobox2.grid(row=4,column=1,sticky="w")
        self.week_combobox2.current(0)

        #daily and category button--------------------------------------------------
        self.dailybutton=tk.Button(self.wanalysisbuttonframe,text="Daily",command=self.askdailywindow,width=8,height=1,bg="black",fg="white")
        self.dailybutton.grid(row=5,column=0,padx=5,pady=5,sticky="w")
        self.categorybutton=tk.Button(self.wanalysisbuttonframe,text="Category",command=self.askcategorywindow,width=8,height=1,bg="black",fg="white")
        self.categorybutton.grid(row=6,column=0,padx=5,pady=5,sticky="w")

        #listbox---------------------------------------------------------------------------
        self.wlistframe=tk.Frame(self.frame5,bg="white")
        self.wlistframe.grid(row=1,column=0,padx=10,pady=5)
        self.wlbx=tk.Listbox(self.wlistframe,width=50,height=8,bd=1, relief="sunken")
        self.wlbx.grid(row=0,column=0,padx=10,pady=5)

        self.bt2frame=tk.Frame(self.frame5,bg="white")
        self.bt2frame.grid(row=2,column=0,padx=5,pady=5)
        self.homebutton2=tk.Button(self.bt2frame,text="Home",command=self.create_widgets,width=8,height=1,bg="black",fg="white")
        self.homebutton2.grid(row=0,column=0,padx=5,pady=5,sticky="w")
        self.Recieptbutton2=tk.Button(self.bt2frame,text="Reciept",command=lambda:week_reciept(self,int(self.month_var2.get()),int(self.year_var2.get()),int(self.week_var2.get())),width=8,height=1,bg="black",fg="white")
        self.Recieptbutton2.grid(row=0,column=1,padx=5,pady=5,sticky="w")
#display of weekly analysis
    def showweekly(self,event):
        ana_wek(self,int(self.year_var2.get()),int(self.month_var2.get()),int(self.week_var2.get()))

#window to ask parameters for daily analysis (frame 6)
    def askdailywindow(self):
        self.frame6=tk.Frame(self,bg="white")
        self.frame6.place(x=0,y=0,width=355,height=450)

        #button frame
        self.danalysisbuttonframe=tk.Frame(self.frame6,bg="white")
        self.danalysisbuttonframe.grid(row=0,column=0,padx=5,pady=5)

        # monthly,weely and daily button----------------------------------------
        self.dmonthlybutton=tk.Button(self.danalysisbuttonframe,text="Monthly",width=8,height=1,command=self.askmonthlywindow,bg="black",fg="white")
        self.dmonthlybutton.grid(row=0,column=0,padx=5,pady=5,sticky="w")
        self.dweeklybutton=tk.Button(self.danalysisbuttonframe,text="Weekly",command=self.askweeklywindow,width=8,height=1,bg="black",fg="white")
        self.dweeklybutton.grid(row=1,column=0,padx=5,pady=5,sticky="w")
        self.ddailybutton=tk.Button(self.danalysisbuttonframe,text="Daily",command=self.askdailywindow,width=8,height=1,bg="black",fg="white")
        self.ddailybutton.grid(row=2,column=0,padx=5,pady=5,sticky="w")

        #labels and combo boxes to ask-------------------------------------
        self.dmonthlabel=tk.Label(self.danalysisbuttonframe,text="Month",bg="white")
        self.dmonthlabel.grid(row=3,column=0,padx=5,pady=5,sticky="w")

        self.month_var3 = tk.StringVar()
        self.numbers3_1 = list(range(1, 12))
        self.dmonth_combobox = ttk.Combobox(self.danalysisbuttonframe, textvariable=self.month_var3, values=self.numbers3_1,height=1,width=4)
        self.dmonth_combobox.bind("<Return>", self.showdaily)
        self.dmonth_combobox.grid(row=3,column=1,sticky="w")
        self.dmonth_combobox.current(0)

        self.dyearlabel=tk.Label(self.danalysisbuttonframe,text="Year",bg="white")
        self.dyearlabel.grid(row=4,column=0,padx=5,pady=5,sticky="w")

        self.year_var3 = tk.StringVar()
        self.numbers3_2=list(range(2024,2030))
        self.dyear_combobox = ttk.Combobox(self.danalysisbuttonframe, textvariable=self.year_var3, values=self.numbers3_2,height=1,width=4)
        self.dyear_combobox.bind("<Return>", self.showdaily)
        self.dyear_combobox.grid(row=4,column=1,sticky="w")
        self.dyear_combobox.current(0)

        self.ddatelabel=tk.Label(self.danalysisbuttonframe,text="Date",bg="white")
        self.ddatelabel.grid(row=5,column=0,padx=5,pady=5,sticky="w")

        self.date_var3 = tk.StringVar()
        self.numbers3_3=list(range(1,32))
        self.dyear_combobox = ttk.Combobox(self.danalysisbuttonframe, textvariable=self.date_var3, values=self.numbers3_3,height=1,width=4)
        self.dyear_combobox.bind("<<ComboboxSelected>>", self.showdaily)
        self.dyear_combobox.grid(row=5,column=1,sticky="w")
        self.dyear_combobox.current(0)

        #category button--------------------------------------------------------------------------
        self.categorybutton=tk.Button(self.danalysisbuttonframe,text="Category",command=self.askcategorywindow,width=8,height=1,bg="black",fg="white")
        self.categorybutton.grid(row=6,column=0,padx=5,pady=5,sticky="w")

        #listbox---------------------------------------------------------
        self.dlistframe=tk.Frame(self.frame6,bg="white")
        self.dlistframe.grid(row=1,column=0,padx=10,pady=5)
        self.dlbx=tk.Listbox(self.dlistframe,width=50,height=8,bd=1, relief="sunken")
        self.dlbx.grid(row=0,column=0,padx=10,pady=5)

        self.bt3frame=tk.Frame(self.frame6,bg="white")
        self.bt3frame.grid(row=2,column=0,padx=5,pady=5)
        self.homebutton3=tk.Button(self.bt3frame,text="Home",command=self.create_widgets,width=8,height=1,bg="black",fg="white")
        self.homebutton3.grid(row=0,column=0,padx=5,pady=5,sticky="w")
        self.Recieptbutton3=tk.Button(self.bt3frame,text="Reciept",command=lambda:daily_reciept(self,int(self.month_var3.get()),int(self.year_var3.get()),int(self.date_var3.get())),width=8,height=1,bg="black",fg="white")
        self.Recieptbutton3.grid(row=0,column=1,padx=5,pady=5,sticky="w")
#--display of daily analysis
    def showdaily(self,event):
        ana_dal(self,int(self.year_var3.get()),int(self.month_var3.get()),int(self.date_var3.get()))

#window to ask parameters for category analysis (frame 7)
    def askcategorywindow(self):
        self.frame7=tk.Frame(self,bg="white")
        self.frame7.place(x=0,y=0,width=355,height=450)

        #button frame
        self.canalysisbuttonframe=tk.Frame(self.frame7,bg="white")
        self.canalysisbuttonframe.grid(row=0,column=0,padx=5,pady=5)

        # monthly,weekly,daily,category button----------------------------------------
        self.cmonthlybutton=tk.Button(self.canalysisbuttonframe,text="Monthly",width=8,height=1,command=self.askmonthlywindow,bg="black",fg="white")
        self.cmonthlybutton.grid(row=0,column=0,padx=5,pady=5,sticky="w")
        self.cweeklybutton=tk.Button(self.canalysisbuttonframe,text="Weekly",command=self.askweeklywindow,width=8,height=1,bg="black",fg="white")
        self.cweeklybutton.grid(row=1,column=0,padx=5,pady=5,sticky="w")
        self.cdailybutton=tk.Button(self.canalysisbuttonframe,text="Daily",command=self.askdailywindow,width=8,height=1,bg="black",fg="white")
        self.cdailybutton.grid(row=2,column=0,padx=5,pady=5,sticky="w")
        self.ccategorybutton=tk.Button(self.canalysisbuttonframe,text="Category",command=self.askcategorywindow,width=8,height=1,bg="black",fg="white")
        self.ccategorybutton.grid(row=3,column=0,padx=5,pady=5,sticky="w")

        #labels and combo boxes to ask-------------------------------------
        self.ccategorylabel=tk.Label(self.canalysisbuttonframe,text="Category",bg="white")
        self.ccategorylabel.grid(row=4,column=0,padx=5,pady=5,sticky="w")

        self.category_var4 = tk.StringVar()
        self.ccategory_combobox = ttk.Combobox(self.canalysisbuttonframe, textvariable=self.category_var4, values=["Grocery", "School fee", "Monthly Rent","Electricity","Gas","Other"],height=1,width=8)
        self.ccategory_combobox.bind("<<ComboboxSelected>>", self.showcategory)
        self.ccategory_combobox.grid(row=4,column=1,sticky="w")
        self.ccategory_combobox.current(0)

        #listbox---------------------------------------------------------
        self.clistframe=tk.Frame(self.frame7,bg="white")
        self.clistframe.grid(row=1,column=0,padx=10,pady=5)
        self.clbx=tk.Listbox(self.clistframe,width=50,height=10,bd=1, relief="sunken")
        self.clbx.grid(row=0,column=0,padx=10,pady=5)

        self.btframe4=tk.Frame(self.frame7,bg="white")
        self.btframe4.grid(row=2,column=0,padx=5,pady=5)
        self.homebutton4=tk.Button(self.btframe4,text="Home",command=self.create_widgets,width=8,height=1,bg="black",fg="white")
        self.homebutton4.grid(row=0,column=0,padx=10,pady=5,sticky="w")
        self.Recieptbutton4=tk.Button(self.btframe4,text="Reciept",command=lambda:category_reciept(self,(self.category_var4.get())),width=8,height=1,bg="black",fg="white")
        self.Recieptbutton4.grid(row=0,column=1,padx=10,pady=5,sticky="w")

#display of category analysis
    def showcategory(self,event):
        ana_catg(self,self.category_var4.get())

# creating edit window_____________________________________________________________________
    def Editwindow(self):
        self.frame12=tk.Frame(self,bg="white")
        self.frame12.place(x=0,y=0,width=350,height=450)

        self.frame8 = tk.Frame(self.frame12,bg="white")
        self.frame8.grid(row=0, column=0, padx=10, pady=20)

        tk.Label(self.frame8, text=" SELECT TYPE : ",bg="white").grid(row=0, column=0,padx=20,pady=10)

        tk.Label(self.frame8, text="Type : ",bg="white").grid(row=2, column=0)
        self.edit_var = tk.StringVar()
        self.menu_combobox = ttk.Combobox(self.frame8, textvariable=self.edit_var, values=["Added", "Withdrawn"],height=1,width=8)
        self.menu_combobox.bind("<<ComboboxSelected>>", self.combofunction1)
        self.menu_combobox.grid(row=2,column=1,padx=20,pady=10)
        self.menu_combobox.set("Added")

#Function for added in edit _____________________________________________________________________
    def add_(self):

        self.frame13=tk.Frame(self,bg="white")
        self.frame13.place(x=0,y=0,width=350,height=450)

        self.frame14 = tk.Frame(self.frame13,bg="white")
        self.frame14.grid(row=0, column=0, padx=10, pady=20)
        tk.Label(self.frame14, text="Editing The Transaction  ",bg="white").grid(row=0, column=0,padx=20,pady=10)

        tk.Label(self.frame14, text="Type : ",bg="white").grid(row=1, column=0,padx=20,pady=10)
        self.menu_combobox = ttk.Combobox(self.frame14, textvariable=self.edit_var, values=["Added", "Withdrawn"],height=1,width=17)
        self.menu_combobox.bind("<<ComboboxSelected>>", self.combofunction1)
        self.menu_combobox.grid(row=1,column=1,padx=20,pady=10)
        self.menu_combobox.set("Added")

        tk.Label(self.frame14, text="RowId : ",bg="white").grid(row=3, column=0)
        self.rowid = tk.StringVar()
        self.rowid_entry = tk.Entry(self.frame14, textvariable=self.rowid,highlightthickness=2)
        self.rowid_entry.config( highlightcolor="black")
        self.rowid_entry.grid(row=3, column=1,padx=20,pady=10)

        tk.Label(self.frame14, text="New Amount :",bg="white").grid(row=4, column=0)
        self.new_amount = tk.StringVar()
        self.new_amount_entry = tk.Entry(self.frame14, textvariable=self.new_amount,highlightthickness=2)
        self.new_amount_entry.config( highlightcolor="black")
        self.new_amount_entry.grid(row=4, column=1,padx=20,pady=10)

        self.frame15 = tk.Frame(self.frame13,bg="white")
        self.frame15.grid(row=1, column=0, padx=10, pady=20)

        self.edit_button = tk.Button(self.frame15, text="Enter",width=8,height=2,bg="black",fg="white", command=lambda:edit_rec(self,int(self.rowid_entry.get()),"Added",int(self.new_amount_entry.get())))
        self.edit_button.grid(row=2, column=0, padx=10, pady=15)

        self.hom_button5=tk.Button(self.frame15,text="Home",width=8,height=2,command=self.create_widgets,bg="black",fg="white")
        self.hom_button5.grid(row=2,column=3)

#Function for  withdrawn in edit__________________________________________________
    def Withdrawn_(self):
        self.frame16=tk.Frame(self,bg="white")
        self.frame16.place(x=0,y=0,width=350,height=450)

        self.frame17 = tk.Frame(self.frame16,bg="white")
        self.frame17.grid(row=0, column=0, padx=10, pady=20)

        tk.Label(self.frame17, text="Editing The Transaction  ",bg="white").grid(row=0, column=0,padx=20,pady=10)
        tk.Label(self.frame17, text="Type : ",bg="white").grid(row=1, column=0,padx=20,pady=10)
        self.menu_combobox = ttk.Combobox(self.frame17, textvariable=self.edit_var, values=["Added", "Withdrawn"],height=1,width=17)
        self.menu_combobox.bind("<<ComboboxSelected>>", self.combofunction1)
        self.menu_combobox.grid(row=1,column=1,padx=20,pady=10)
        self.menu_combobox.set("Withdrawn")

        tk.Label(self.frame17, text="RowId : ",bg="white").grid(row=2, column=0)
        self.rowid = tk.StringVar()
        self.rowid_entry = tk.Entry(self.frame17, textvariable=self.rowid,highlightthickness=2)
        self.rowid_entry.config( highlightcolor="black")
        self.rowid_entry.grid(row=2, column=1,padx=8, pady=15)

        tk.Label(self.frame17, text="New Amount :",bg="white").grid(row=3, column=0)
        self.new_amount = tk.StringVar()
        self.new_amount_entry = tk.Entry(self.frame17, textvariable=self.new_amount,highlightthickness=2)
        self.new_amount_entry.config( highlightcolor="black")
        self.new_amount_entry.grid(row=3, column=1,padx=8, pady=15)

        tk.Label(self.frame17, text="New Category : ",bg="white").grid(row=4, column=0)
        self.category_var7 = tk.StringVar()
        self.cat_combobox = ttk.Combobox(self.frame17, textvariable=self.category_var7, values=["Grocery", "School fee", "Monthly Rent","Electricity","Gas","Other"],height=1,width=17)
        #self.cat_combobox.bind("<<ComboboxSelected>>", self.showcategory)
        self.cat_combobox.grid(row=4,column=1,padx=20,pady=10)
        self.cat_combobox.current(0)

        self.frame18 = tk.Frame(self.frame16,bg="white")
        self.frame18.grid(row=1, column=0, padx=10, pady=20)

        self.edit_button = tk.Button(self.frame18, text="Enter",width=8,height=2,bg="black",fg="white", command=lambda:edit_rec(self,int(self.rowid_entry.get()),"Withdrawn",int(self.new_amount_entry.get()),self.category_var7.get()))
        self.edit_button.grid(row=2, column=0, padx=10, pady=15)

        self.hom_button5=tk.Button(self.frame18,text="Home",width=8,height=2,bg="black",fg="white",command=self.create_widgets)
        self.hom_button5.grid(row=2,column=3)

#combo function for edit _____________________________________
    def combofunction1(self,event):
        selected=self.menu_combobox.get()
        if selected== "Added":
            self.add_()
        elif selected== "Withdrawn":
            self.Withdrawn_()


#creating delete window
    def Deletewindow(self):
        self.frame13=tk.Frame(self,bg="white")
        self.frame13.place(x=0,y=0,width=350,height=450)

        self.frame10 = tk.Frame(self.frame13,bg="white")
        self.frame10.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(self.frame10, text="Deleting a Transaction",bg="white").grid(row=0, column=1,padx=10,pady=10)
        self.framee = tk.Frame(self.frame13,bg="white")
        self.framee.grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self.framee, text="RowId :",bg="white").grid(row=0, column=1,padx=20,pady=10)
        self.rowid = tk.StringVar()
        self.rowid_entry = tk.Entry(self.framee,textvariable=self.rowid,highlightthickness=2)
        self.rowid_entry.config( highlightcolor="black")
        self.rowid_entry.grid(row=0, column=2)

        tk.Label(self.framee, text="Type :",bg="white").grid(row=1, column=1,padx=20,pady=10)
        self.type_ = tk.StringVar()
        self.l=["Added","Withdrawn"]
        self.type_entry = ttk.Combobox(self.framee,textvariable=self.type_,values=self.l,width=17)
        self.type_entry.grid(row=1, column=2)
        self.type_entry.set("Added")
        self.frame11 = tk.Frame(self.frame13,bg="white")
        self.frame11.grid(row=2, column=0, padx=20, pady=10)

        self.del_button = tk.Button(self.frame11, text="Enter",bg="black",fg="white",width=8,height=1, command=lambda:del_rec(self,int(self.rowid.get()),self.type_.get()))
        self.del_button.grid(row=1, column=0, padx=20, pady=10)

        self.ho_button5=tk.Button(self.frame11,text="Home",bg="black",fg="white",width=8,height=1,command=self.create_widgets)
        self.ho_button5.grid(row=1,column=3, padx=20, pady=10)
#expensesharingwindows
    def Expensewindow(self):
        self.frameexp=tk.Frame(self,bg="white")
        self.frameexp.place(x=0,y=0,width=355,height=450)

        self.frameexp2 = tk.Frame(self.frameexp,bg="white")
        self.frameexp2.grid(row=0, column=0, padx=20, pady=20)

        tk.Label(self.frameexp2, text="Select Type : ",bg="white").grid(row=0, column=0,padx=20,pady=30)
        self.exp_var = tk.StringVar()
        self.menu_comboboxexp = ttk.Combobox(self.frameexp2, textvariable=self.exp_var, values=["Equal Share", "Unequal Share"],height=1,width=15)
        self.menu_comboboxexp.bind("<<ComboboxSelected>>", self.combofunction2)
        self.menu_comboboxexp.grid(row=0,column=1,padx=20,pady=30)
        self.menu_comboboxexp.set("Equal Share")

        self.homebtframe1=tk.Frame(self.frameexp,bg="white")
        self.homebtframe1.grid(row=1,column=0,padx=5,pady=5)
        self.homebutton2=tk.Button(self.homebtframe1,text="Home",command=self.create_widgets,width=8,height=1,bg="black",fg="white")
        self.homebutton2.grid(row=0,column=0,padx=5,pady=5,sticky="w")
#combo function for type of expense
    def combofunction2(self,event):
        selected=self.menu_comboboxexp.get()
        if selected=="Equal Share":
            self.equalwindows()

        elif selected=="Unequal Share":
            self.unequalwindows()
#windows for equal share expense
    def equalwindows(self):
        self.frameeq=tk.Frame(self,bg="white")
        self.frameeq.place(x=0,y=0,width=355,height=450)

        self.frameeq2 = tk.Frame(self.frameeq,bg="white")
        self.frameeq2.grid(row=0, column=0, padx=20, pady=20)

        tk.Label(self.frameeq2, text="Total Amount : ",bg="white").grid(row=0, column=0,padx=20,pady=30)
        tk.Label(self.frameeq2, text="Number of People : ",bg="white").grid(row=1, column=0,padx=20,pady=30)
        self.amountentry=tk.Entry(self.frameeq2,highlightthickness=2)
        self.amountentry.config( highlightcolor="black")
        self.amountentry.grid(row=0, column=1,padx=20,pady=30)
        self.peopleentry=tk.Entry(self.frameeq2,highlightthickness=2)
        self.peopleentry.config( highlightcolor="black")
        self.peopleentry.grid(row=1, column=1,padx=20,pady=30)
        self.peopleentry.bind('<Return>',self.showexpense_sharing)

        self.listframeeq=tk.Frame(self.frameeq,bg="white")
        self.listframeeq.grid(row=1,column=0,padx=10,pady=5)
        self.eqlbx=tk.Listbox(self.listframeeq,width=50,height=10,bd=1, relief="sunken")
        self.eqlbx.grid(row=0,column=0,padx=10,pady=5)

        self.homebtframe=tk.Frame(self.frameeq,bg="white")
        self.homebtframe.grid(row=2,column=0,padx=5,pady=5)
        self.homebutton1=tk.Button(self.homebtframe,text="Home",command=self.create_widgets,width=8,height=1,bg="black",fg="white")
        self.homebutton1.grid(row=0,column=0,padx=5,pady=5,sticky="w")
#function to show equal expense
    def showexpense_sharing(self,event):
        expense_sharing(self)
#windows for unequal share expense
    def  unequalwindows(self):
        self.framenq=tk.Frame(self,bg="white")
        self.framenq.place(x=0,y=0,width=355,height=450)

        self.framenq1 = tk.Frame(self.framenq,bg="white")
        self.framenq1.grid(row=0, column=0, padx=30, pady=30)   

        tk.Label(self.framenq1, text="Number of People : ",bg="white").grid(row=0, column=0,padx=20, pady=30)

        self.num = tk.StringVar()
        self.numlist=list(range(1,11))
        self.num_combobox = ttk.Combobox(self.framenq1, textvariable=self.num, values=self.numlist,height=1,width=8)
        self.num_combobox.bind("<<ComboboxSelected>>", self.take_input)
        #self.year_combobox.bind("<Return>", self.showmonthly)
        self.num_combobox.grid(row=0,column=1,sticky="w",padx=20, pady=30)
        self.num_combobox.current(0)
#windows for loop entries
    def take_input(self,event):
        self.framenq2=tk.Frame(self,bg="white")
        self.framenq2.place(x=0,y=0,width=355,height=450)

        self.framenq2_1 = tk.Frame(self.framenq2,bg="white")
        self.framenq2_1.grid(row=0, column=0, padx=5, pady=5)   
        self.names=[]
    
        self.num_inputs = int(self.num_combobox.get())  # Get the number of inputs from the entry widget
        self.j=0
        tk.Label(self.framenq2_1,text="Person Name "+str(self.j+1)+":",bg="white").grid(row=self.j, column=0,padx=3,pady=3)
        self.new_entry = tk.Entry(self.framenq2_1,highlightthickness=2)
        self.new_entry.config( highlightcolor="black")
        self.new_entry.grid(row=self.j,column=1,padx=3, pady=3)
        tk.Label(self.framenq2_1,text="Percentage: ",bg="white").grid(row=self.j, column=2,padx=3, pady=3)
        self.new_entry2 = tk.Entry(self.framenq2_1,width=5,highlightthickness=2)
        self.new_entry2.config( highlightcolor="black")
        self.new_entry2.grid(row=self.j,column=3,padx=3, pady=3)
        
        self.j=self.j+1
        self.new_entry2.bind("<Return>",self.entries)
        
        self.listframeeq2=tk.Frame(self.framenq2,bg="white")
        self.listframeeq2.grid(row=1,column=0)
       
        
        self.nqlbx2=tk.Listbox(self.listframeeq2,width=50,height=10)
        self.nqlbx2.grid(row=0,column=0)

        self.homebtframe2=tk.Frame(self.framenq2,bg="white")
        self.homebtframe2.grid(row=2,column=0,padx=5,pady=5)
        self.homebutton2=tk.Button(self.homebtframe2,text="Home",command=self.create_widgets,width=8,height=1,bg="black",fg="white")
        self.homebutton2.grid(row=0,column=0,padx=5,pady=5,sticky="w")
#loop entries
    def entries(self,event):
        self.names.append((self.new_entry.get(),self.new_entry2.get()))
        if int(self.new_entry2.get()) < 0 or int(self.new_entry2.get()) > 100:
            messagebox.showerror("Input Error","percentage should be between 1 and 100")
            self.unequalwindows()
        
        tk.Label(self.framenq2_1,text="Person Name "+str(self.j+1)+":",bg="white").grid(row=self.j, column=0,padx=3, pady=3)
        self.new_entry = tk.Entry(self.framenq2_1,highlightthickness=2)
        self.new_entry.config( highlightcolor="black")
        self.new_entry.grid(row=self.j,column=1,padx=3, pady=3)
        tk.Label(self.framenq2_1,text="Percentage: ",bg="white").grid(row=self.j, column=2,padx=3, pady=3)
        self.new_entry2 = tk.Entry(self.framenq2_1,width=5,highlightthickness=2)
        self.new_entry2.config( highlightcolor="black")
        self.new_entry2.grid(row=self.j,column=3,padx=3, pady=3)
        self.j=self.j+1
        if self.j==self.num_inputs:
            self.new_entry2.bind("<Return>",self.appendfunc)
            
        
            #self.appendfunc()
            #self.names.append((self.new_entry.get(),self.new_entry2.get()))
        else:
            self.new_entry2.bind("<Return>",self.entries)
        #self.names.append((self.new_entry.get(),self.new_entry2.get()))
#appending entries in list  
    def appendfunc(self,event):    
        self.names.append((self.new_entry.get(),self.new_entry2.get()))
        if int(self.new_entry2.get()) < 0 or int(self.new_entry2.get()) > 100:
            messagebox.showerror("Input Error","percentage should be between 1 and 100")
            self.unequalwindows()
        tk.Label(self.framenq2_1, text="Total Amount : ",bg="white").grid(row=self.j, column=0,padx=5,pady=3)
        self.amountentry2=tk.Entry(self.framenq2_1,highlightthickness=2)
        self.amountentry2.config( highlightcolor="black")
        self.amountentry2.grid(row=self.j, column=1,padx=5,pady=3)
        self.amountentry2.bind('<Return>',self.showunequalsharing)
#function to show unequal expense   
    def showunequalsharing(self,event):
        expense_sharing(self)


if __name__ == "__main__":

    app = Application('finalproject.db')
    app.mainloop()
