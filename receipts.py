from tkinter import ttk, messagebox
import tkinter as tk
import sqlite3
from datetime import datetime
from tkinter import font
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

class Expense:
    def __init__(self,type, drop_, total, date, month, week, year,timestamp):
        self.type = type
        self.drop_ = drop_
        self.total = total
        self.date = date
        self.month = month
        self. week =  week
        self.year = year
        self.timestamp = timestamp

class Expense_dup_drop:
    def __init__(self,type, drop_, total,categories, date, month, week, year,timestamp):
        self.type = type
        self.drop_ = drop_
        self.total = total
        self.categories = categories
        self.date = date
        self.month = month
        self. week =  week
        self.year = year
        self.timestamp = timestamp

#function for monthly receipts
def mon_recipt(self,a,b):
        print("function called")
        mon=self.db.cursor.execute("SELECT * FROM CombinedView WHERE month = ? AND year = ?", (a,b))
        rows = self.db.cursor.fetchall()
        month1 = [Expense(row[0], row[1], row[2],row[3],row[4],row[5],row[6] ,row[7]) for row in rows]
        #month1 = [Expense(row[0], row[1], row[2], row[7]) for row in rows]
        if month1:
            data = [["Type", "Amount", "Total","Date","Month","Week","Year","Timestamp"]]
            for s in month1:
                data.append([str(s.type), str(s.drop_), str(s.total),str(s.date),str(s.month),str(s.week),str(s.year),str(s.timestamp)])

            pdf_filename = "Monthly_Receipt.pdf"
            doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
            table = Table(data)
            style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.seagreen),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)])
            table.setStyle(style)
            doc.build([table])
        else:
            messagebox.showinfo("No Records", "No records found.")

#function for weekly receipts
def week_reciept(self,a,b,c):
        week=self.db.cursor.execute("SELECT * FROM CombinedView WHERE month = ? AND year = ?AND week=?", (a,b,c))
        rows = self.db.cursor.fetchall()
        week1 = [Expense(row[0], row[1], row[2],row[3],row[4],row[5],row[6] ,row[7]) for row in rows]

        if week1:
            data = [["Type", "Amount", "Total","Date","Month","Week","Year","Timestamp"]]
            for s in week1:
                data.append([str(s.type), str(s.drop_), str(s.total),str(s.date),str(s.month),str(s.week),str(s.year),str(s.timestamp)])

            pdf_filename = "Weekly_Receipt.pdf"
            doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
            table = Table(data)
            style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.seagreen),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)])
            table.setStyle(style)
            doc.build([table])
        else:
            messagebox.showinfo("No Records", "No records found.")


    #daily_reciept________________________________________

#function for daily receipts
def daily_reciept(self,a,b,c):
        daily1=self.db.cursor.execute("SELECT * FROM CombinedView WHERE month = ? AND year = ? AND date=?", (a,b,c))
        rows = self.db.cursor.fetchall()
        daily1 = [Expense(row[0], row[1], row[2],row[3],row[4],row[5],row[6] ,row[7]) for row in rows]

        if daily1:
            data = [["Type", "Amount", "Total","Date","Month","Week","Year","Timestamp"]]
            for s in daily1:
                data.append([str(s.type), str(s.drop_), str(s.total),str(s.date),str(s.month),str(s.week),str(s.year),str(s.timestamp)])

            pdf_filename = "Daily_Receipt.pdf"
            doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
            table = Table(data)
            style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.seagreen),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)])
            table.setStyle(style)
            doc.build([table])
        else:
            messagebox.showinfo("No Records", "No records found.")
    # category_reciept_____________________________

#function for category receipts
def category_reciept(self,a):
        cat1=self.db.cursor.execute("SELECT *  FROM dup_drop WHERE categories = ?", (a,))
        rows = self.db.cursor.fetchall()
        cat1 = [Expense_dup_drop(row[0], row[1], row[2],row[3],row[4],row[5],row[6] ,row[7],row[8]) for row in rows]

        if cat1:
            data = [["Type", "Amount", "Total","categories","Date","Month","Week","Year","Timestamp"]]
            for s in cat1:
                data.append([str(s.type), str(s.drop_), str(s.total),str(s.categories), str(s.date),str(s.month),str(s.week),str(s.year),str(s.timestamp)])

            pdf_filename = "Category_Receipt.pdf"
            doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
            table = Table(data)
            style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.seagreen),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)])
            table.setStyle(style)
            doc.build([table])
        else:
            messagebox.showinfo("No Records", "No records found.")
