import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from tkinter import font
from Final_GUI import *

# Function to initialize total
def initialize_total():
    conn = sqlite3.connect('finalproject.db')
    c = conn.cursor()
    c.execute("SELECT final FROM total ORDER BY rowid DESC LIMIT 1")
    result = c.fetchone()
    conn.commit()
    conn.close()
    return result[0] if result else 0

# Function to get current date components
def get_date():
    now = datetime.now()
    day = now.day
    month = now.month
    year = now.year
    input_date = datetime(year, month, day)
    week = input_date.isocalendar()[1]
    return day, month, week, year

# Function for cash in
def in_(self, entry_widget):
    print("Function called")
    try:
        add = entry_widget.get()
        if not add.isdigit() or int(add) <= 0:
            raise ValueError("Please enter a positive numeric value.")
        add = int(add)
        total = initialize_total()  # Fetch the current total
        total += add
        dates = get_date()
        type_ = 'Added'
        date, month, week, year = dates
        values = (type_, add, total, date, month, week, year)
        self.db.cursor.execute("INSERT INTO add_amount (type, add_, total, date, month, week, year) VALUES (?,?,?,?,?,?,?)", values)
        self.db.cursor.execute("INSERT INTO total (final) VALUES(?)", (total,))
        self.db.conn.commit()
        messagebox.showinfo("Success", "Amount added successfully.")
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))

# Function for cash out
def out_(self, entry_widget, entry_widget2):
    try:
        drop = entry_widget.get()
        if not drop.isdigit() or int(drop) <= 0:
            raise ValueError("Please enter a positive numeric value for the amount.")
        drop = int(drop)
        total = initialize_total()  # Fetch the current total
        if total - drop < 0:
            raise ValueError("Insufficient funds for this withdrawal.")
        catg = entry_widget2.get()
        if not catg.strip():
            raise ValueError("Category cannot be empty or only whitespace.")
        total -= drop
        dates = get_date()
        type_ = 'Withdrawn'
        date, month, week, year = dates
        vls = (type_, drop, total, date, month, week, year)
        dup_vls = (type_, drop, total, catg, date, month, week, year)
        self.db.cursor.execute("INSERT INTO drop_amount (type, drop_, total, date, month, week, year) VALUES (?, ?, ?, ?, ?, ?, ?)", vls)
        self.db.cursor.execute("INSERT INTO dup_drop (type, drop_, total, categories, date, month, week, year) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", dup_vls)
        self.db.cursor.execute("INSERT INTO total (final) VALUES(?)", (total,))
        self.db.conn.commit()
        messagebox.showinfo("Success", "Amount withdrawn successfully.")
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))

# Function for monthly analysis
def ana_mon(self, yr: int, mn: int):
    monospaced_font = font.Font(family="Courier", size=10)
    self.db.cursor.execute("SELECT * FROM CombinedView WHERE month = ? AND year = ?", (mn, yr))
    self.lbx.delete(0, tk.END)
    p = self.db.cursor.fetchall()
    if p:
        header = "{:<10}{:<10} {:<15}".format("Type", "Amount", "Timestamp")
        self.lbx.insert(tk.END, header)
        self.lbx.config(font=monospaced_font)
        for r in p:
            formatted_line = "{:<10}{:<10} {:<15}".format(str(r[0]), str(r[1]), str(r[7]))
            self.lbx.insert(tk.END, formatted_line)
    else:
        self.lbx.insert(tk.ANCHOR, "No records found for the given date.")

# Function for daily analysis
def ana_dal(self, yr: int, mn: int, dt: int):
    monospaced_font = font.Font(family="Courier", size=10)
    self.db.cursor.execute('SELECT * FROM (SELECT * FROM add_amount UNION ALL SELECT * FROM drop_amount ORDER BY timestamp) WHERE month = ? AND year = ? AND date = ?', (mn, yr, dt))
    p = self.db.cursor.fetchall()
    self.dlbx.delete(0, tk.END)
    if p:
        header = "{:<10}{:<6} {:<15}".format("Type", "Amount", "Timestamp")
        self.dlbx.insert(tk.END, header)
        self.dlbx.config(font=monospaced_font)
        for r in p:
            formatted_line = "{:<10}{:<6} {:<15}".format(str(r[0]), str(r[1]), str(r[7]))
            self.dlbx.insert(tk.END, formatted_line)
    else:
        self.dlbx.insert(tk.ANCHOR, "No records found for the given date.")

# Function for weekly analysis
def ana_wek(self, yr: int, mn: int, wk: int):
    monospaced_font = font.Font(family="Courier", size=10)
    self.db.cursor.execute('SELECT * FROM CombinedView WHERE month = ? AND year = ? AND week = ?', (mn, yr, wk))
    self.wlbx.delete(0, tk.END)
    p = self.db.cursor.fetchall()
    if p:
        header = "{:<10}{:<6} {:<15}".format("Type", "Amount", "Timestamp")
        self.wlbx.insert(tk.END, header)
        self.wlbx.config(font=monospaced_font)
        for r in p:
            formatted_line = "{:<10}{:<6} {:<15}".format(str(r[0]), str(r[1]), str(r[7]))
            self.wlbx.insert(tk.END, formatted_line)
    else:
        self.wlbx.insert(tk.ANCHOR, "No records found for the given date.")

# Function for category wise analysis
def ana_catg(self, catog: str):
    monospaced_font = font.Font(family="Courier", size=10)
    self.db.cursor.execute('SELECT * FROM dup_drop WHERE categories = ?', (catog,))
    p = self.db.cursor.fetchall()
    self.clbx.delete(0, tk.END)
    if p:
        header = "{:<10}{:<6} {:<15}".format("Type", "Amount", "Timestamp")
        self.clbx.insert(tk.END, header)
        self.clbx.config(font=monospaced_font)
        for r in p:
            formatted_line = "{:<10}{:<6} {:<15}".format(str(r[0]), str(r[1]), str(r[7]))
            self.clbx.insert(tk.END, formatted_line)
    else:
        self.clbx.insert(tk.ANCHOR, "No records found for the given date.")

# Function to display transaction history
def ana_all(self):
    monospaced_font = font.Font(family="Courier", size=10)
    self.db.cursor.execute('SELECT * FROM (SELECT rowid, * FROM add_amount UNION ALL SELECT rowid, * FROM drop_amount) ORDER BY timestamp')
    p = self.db.cursor.fetchall()
    if p:
        header = "{:<3} {:<10}{:<6} {:<15}".format("Sr#", "Type", "Amount", "Timestamp")
        self.lbx2.insert(tk.END, header)
        self.lbx2.config(font=monospaced_font)
        for r in p:
            formatted_line = "{:<3} {:<10}{:<6} {:<15}".format(str(r[0]), str(r[1]), str(r[2]), str(r[8]))
            self.lbx2.insert(tk.END, formatted_line)
    else:
        self.lbx2.insert(tk.ANCHOR, "No records found for the given date.")

# Function for delete
def del_rec(self, a, b):
    self.db.cursor.execute('SELECT * FROM (SELECT rowid, * FROM add_amount UNION ALL SELECT rowid, * FROM drop_amount ORDER BY timestamp) WHERE rowid = ? AND type = ?', (a, b))
    p = self.db.cursor.fetchall()
    if p:
        tp = p[0]
        total = initialize_total()  # Fetch the current total
        if tp[1] == 'Added':
            self.db.cursor.execute('DELETE FROM add_amount WHERE rowid = ?', (a,))
            total -= tp[2]
        elif tp[1] == 'Withdrawn':
            self.db.cursor.execute('DELETE FROM drop_amount WHERE rowid = ?', (a,))
            total += tp[2]
        self.db.cursor.execute("INSERT INTO total (final) VALUES(?)", (total,))
        self.db.conn.commit()
    else:
        print("No record found with the given row ID.")

# Function for edit
def edit_rec(self, a, b, c, d=''):
    self.db.cursor.execute('SELECT * FROM (SELECT rowid, * FROM add_amount UNION ALL SELECT rowid, * FROM drop_amount ORDER BY timestamp) WHERE rowid = ? AND type = ?', (a, b))
    p = self.db.cursor.fetchall()
    if p:
        tp = p[0]
        old_amount = tp[2]
        total = initialize_total() 
        if tp[1] == 'Added':
            total = total - int(old_amount) + int(c)
            self.db.cursor.execute('UPDATE add_amount SET add_ = ?, total = ? WHERE rowid = ?', (c, total, a))
        elif tp[1] == 'Withdrawn':
            total = total + int(old_amount) - int(c)
            self.db.cursor.execute('UPDATE drop_amount SET drop_ = ?, total = ? WHERE rowid = ?', (c, total, a))
            if d:
                self.db.cursor.execute('UPDATE dup_drop SET drop_ = ?, total = ?, categories = ? WHERE rowid = ?', (c, total, d, a))
        self.db.cursor.execute("INSERT INTO total (final) VALUES(?)", (total,))
        self.db.conn.commit()
    else:
        print("No record found with the given row ID.")

# new things
def expense_sharing(self):
    if self.menu_comboboxexp.get() == 'Equal Share':
        try:
            amount = float(self.amountentry.get())
            num_friends = int(self.peopleentry.get())
            if num_friends <= 0:
                raise ValueError("Number of friends should be positive.")
            
            expense_per_friend = amount / num_friends
            self.eqlbx.delete(0, tk.END)
            self.eqlbx.insert(tk.ANCHOR, "Expense per friend: "+str( expense_per_friend)+"$")
            #print("Expense per friend: $", round(expense_per_friend, 2))
        except ValueError as ve:
            print("Input Error:", ve)
    elif self.menu_comboboxexp.get() == 'Unequal Share':
        try:
            num_friends = int(self.num_combobox.get())
            if num_friends <= 0:
                raise ValueError("Number of friends should be positive.")

            '''friends = []
            for i in range(num_friends):
                friend_name = input(f"Enter the name of friend {i+1}: ")
                percentage = float(input(f"Enter the percentage for {friend_name}: "))
                if percentage < 0 or percentage > 100:
                    raise ValueError("Percentage should be between 0 and 100.")
                friends.append((friend_name, percentage))'''

            total_amount = float( self.amountentry2.get())
            self.nqlbx2.delete(0, tk.END)
            if total_amount <= 0:
                raise ValueError("Total amount should be positive.")

            for friend, percentage in self.names:
                if int(percentage) < 0 or int(percentage) > 100:
                    messagebox.showerror("Input Errpr","Percentage should be between 0 and 100.")

                    raise ValueError("Percentage should be between 0 and 100.")
                expense = (int(percentage) / 100) * total_amount
                self.nqlbx2.insert(tk.ANCHOR, (str(friend)+"'s "+"expense: "+str(round(expense, 2))+"$"))

                #print(f"{friend}'s expense: $", round(expense, 2))
        except ValueError as ve:
            print("Input Error:", ve)
    else:
        print("Invalid type. Please choose 'fixed' or 'variable'.")


