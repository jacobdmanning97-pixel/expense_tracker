import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BudgetPlotter:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker with CSV Upload")
        self.root.geometry("1200x900")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize data
        self.transactions = []
        self.cards = ["Amex", "Wells Fargo", "US Bank", "Citi Bank", "Discover"]
        
        self.setup_gui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_gui(self):
        # Create main frames
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Left frame for input and controls
        left_frame = ttk.LabelFrame(main_frame, text="Input", padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W), padx=(0, 10))
        
        # Right frame for display
        right_frame = ttk.LabelFrame(main_frame, text="Financial Overview", padding="10")
        right_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)

        ttk.Label(left_frame, text="Initial Balance:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.starting_balance = tk.DoubleVar()
        ttk.Entry(left_frame, textvariable=self.starting_balance, width=20).grid(row=0, column=1, pady=2, padx=(5, 0))
        
        ttk.Separator(left_frame, orient='horizontal').grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)


        # Input form
        ttk.Label(left_frame, text="Date:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%m/%d/%Y"))
        ttk.Entry(left_frame, textvariable=self.date_var, width=20).grid(row=2, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(left_frame, text="Amount:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.amount_var = tk.DoubleVar()
        ttk.Entry(left_frame, textvariable=self.amount_var, width=20).grid(row=3, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(left_frame, text="Transaction Type:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.transaction_type_var = tk.StringVar()
        transaction_type_combo = ttk.Combobox(left_frame, textvariable=self.transaction_type_var, 
                                     values=['Expense', 'Income'], width=18)
        transaction_type_combo.grid(row=4, column=1, pady=2, padx=(5, 0))

        ttk.Label(left_frame, text="Card:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.card_var = tk.StringVar()
        card_combo = ttk.Combobox(left_frame, textvariable=self.card_var, 
                                     values=self.cards, width=18)
        card_combo.grid(row=5, column=1, pady=2, padx=(5, 0))
        
        ttk.Button(left_frame, text="Add Transaction", command=self.add_transaction, width=20).grid(row=6, column=0, columnspan=2, pady=10)
        
        # Change button
        ttk.Label(left_frame, text="Updated Transaction Type:").grid(row=14, column=0, sticky=tk.W, pady=2)
        self.updated_transaction_type_var = tk.StringVar()
        updated_transaction_type_combo = ttk.Combobox(left_frame, textvariable=self.updated_transaction_type_var, 
                                     values=['Expense', 'Income'], width=18)
        updated_transaction_type_combo.grid(row=14, column=1, pady=2, padx=(5, 0))

        ttk.Label(left_frame, text="Updated Card:").grid(row=15, column=0, sticky=tk.W, pady=2)
        self.updated_card_var = tk.StringVar()
        updated_card_combo = ttk.Combobox(left_frame, textvariable=self.updated_card_var, 
                                     values=self.cards, width=18)
        updated_card_combo.grid(row=15, column=1, pady=2, padx=(5, 0))
    
        ttk.Button(left_frame, text="Change Selected", command=self.change_transaction_type, width=20).grid(row=16, column=0, columnspan=2, pady=10)

        ttk.Separator(left_frame, orient='horizontal').grid(row=17, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # CSV Upload section
        ttk.Separator(left_frame, orient='horizontal').grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        ttk.Button(left_frame, text="Upload Saved CSV", command=self.upload_csv, width=20).grid(row=9, column=0, columnspan=2, pady=5)

        # Transactions table
        columns = ("Date", "Amount", "Transaction Type", "Card")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add scrollbar to treeview
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Summary section
        summary_frame = ttk.Frame(right_frame)
        summary_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)        

        # Chart frame
        chart_frame = ttk.Frame(right_frame)
        chart_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Create a figure for the chart
        self.fig, self.ax2 = plt.subplots(figsize=(8, 4))
        self.canvas2 = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        ttk.Separator(left_frame, orient='horizontal').grid(row=11, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Delete button
        ttk.Button(left_frame, text="Delete Selected", command=self.delete_transaction, width=20).grid(row=12, column=0, columnspan=2, pady=10)
        
        ttk.Separator(left_frame, orient='horizontal').grid(row=13, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(left_frame, text="Upload Bank CSV", font=('Arial', 10, 'bold')).grid(row=18, column=0, columnspan=2, pady=5)
        ttk.Button(left_frame, text="Upload Bank CSV", command=self.clean_csv, width=20).grid(row=19, column=0, columnspan=2, pady=5)

        ttk.Label(left_frame, text="Which Bank CSV?:").grid(row=20, column=0, sticky=tk.W, pady=2)
        self.card_to_read = tk.StringVar()
        bank_csv_combo = ttk.Combobox(left_frame, textvariable=self.card_to_read, 
                                     values=self.cards, width=18)
        bank_csv_combo.grid(row=20, column=1, pady=2, padx=(5, 0))

    def add_transaction(self):
        
        date = self.date_var.get()
        amount = self.amount_var.get()
        transaction_type = self.transaction_type_var.get()
        card = self.card_var.get()
        
        if transaction_type == 'Income':
            if not all([date, amount, transaction_type]):
                messagebox.showerror("Error", "Please fill all fields with valid values")
                return
        elif transaction_type == 'Expense':
            if not all([date, amount, transaction_type, card]):
                messagebox.showerror("Error", "Please fill all fields with valid values")
                return
        
        # Add to transactions list
        transaction = {
            "Date": date,
            "Amount": abs(amount),
            "Transaction Type": transaction_type,
            "Card": card
        }

        self.transactions.append(transaction)
        self.update_display()
        
        # Clear input fields
        self.amount_var.set(0.0)
        self.transaction_type_var.set('')
        self.card_var.set('')
    
    def clean_csv(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return

        
        # Read CSV file
        df = pd.read_csv(file_path, header = None)

        if self.card_to_read.get() == "Amex":
            df.columns = ['Date', 'Description', 'Card Member', 'Account #', 'Amount']
            df = df.drop(['Description', 'Card Member', 'Account #'], axis = 1)
            df = df.drop(0)
            df = df[df['Amount'].astype(float) > 0]
            df['Amount'] = -df['Amount'].astype(float)
            df['Card'] = ['Amex']*len(df)

        elif self.card_to_read.get() == "Wells Fargo":
            df.columns = ['Date', 'Amount', 'Blank 1', 'Blank 2', 'Description']
            df = df.drop(['Blank 1', 'Blank 2', 'Description'], axis=1)
            df = df[df['Amount'] < 0]
            df['Card'] = ['Wells Fargo']*len(df)

        elif self.card_to_read.get() == "US Bank":
            df.columns = ['Date', 'Transaction', 'Name', 'Memo', 'Amount']
            df = df.drop(['Transaction', 'Memo', 'Name'], axis=1)
            df = df.drop(0)
            df.columns = ['Date', 'Amount']
            df = df[df['Amount'].astype(float) < 0]
            df['Amount'] = df['Amount'].astype(float)
            df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%m/%d/%Y')
            df['Card'] = ['US Bank']*len(df)

        elif self.card_to_read.get() == "Citi Bank":
            df.columns = ['Status', 'Date', 'Description', 'Debit', 'Credit']
            df = df.drop(['Status', 'Credit', 'Description'], axis=1)
            df = df.drop(0)
            df.columns = ['Date', 'Amount']
            df = df.dropna(subset=['Amount'])
            df['Amount'] = -df['Amount'].astype(float)
            df['Card'] = ['Citi Bank']*len(df)

        elif self.card_to_read.get() == "Discover":
            df.columns = ['Trans. Date', 'Post Date', 'Description', 'Amount', 'Category']
            df = df.drop(['Post Date', 'Category', 'Description'], axis=1)
            df = df.drop(0)
            df.columns = ['Date', 'Amount']
            df = df[df['Amount'].astype(float) > 0]
            df['Amount'] = -df['Amount'].astype(float)
            df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%m/%d/%Y')
            df['Card'] = ['Discover']*len(df)

        df["Transaction Type"] = 'Expense'

        # Add transactions from CSV
        for _, row in df.iterrows():
            transaction = {
                "Date": row['Date'],
                "Amount": abs(float(row['Amount'])),
                "Transaction Type": row["Transaction Type"],
                "Card": row['Card']
            }
            self.transactions.append(transaction)
        
        self.update_display()
        messagebox.showinfo("Success", f"Successfully imported {len(df)} transactions")
        
    def upload_csv(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            
            # Check required columns
            required_columns = ['Date', 'Amount', "Transaction Type", 'Card']
            if not all(col in df.columns for col in required_columns):
                messagebox.showerror("Error", "CSV file must contain columns: Date, Description, Amount, Category")
                return
            
            # Add transactions from CSV
            for _, row in df.iterrows():
                transaction = {
                    "Date": row['Date'],
                    "Amount": abs(float(row['Amount'])),
                    "Transaction Type": row["Transaction Type"],
                    "Card": row['Card']
                }
                self.transactions.append(transaction)
            
            self.update_display()
            messagebox.showinfo("Success", f"Successfully imported {len(df)} transactions")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read CSV file: {str(e)}")
    
    def delete_transaction(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a transaction to delete")
            return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this transaction?"):
            index = int(selected_item[0].lstrip('I')) - 1
            if 0 <= index < len(self.transactions):
                del self.transactions[index]
                self.update_display()

    def change_transaction_type(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a transaction to change the transaction type")
            return
        
        updated_transaction_type_var = self.updated_transaction_type_var.get()
        updated_card_var = self.updated_card_var.get()

        if updated_transaction_type_var == 'Income':
            if not all([updated_transaction_type_var]):
                    messagebox.showerror("Error", "Please fill all fields with valid values")
                    return
        elif updated_transaction_type_var == 'Expense':
            if not all([updated_transaction_type_var, updated_card_var]):
                    messagebox.showerror("Error", "Please fill all fields with valid values")
                    return

        index = int(selected_item[0].lstrip('I')) - 1
        self.transactions[index]["Transaction Type"] = updated_transaction_type_var
        self.transactions[index]["Card"] = updated_card_var
        self.update_display()
        self.updated_transaction_type_var.set('')
        self.updated_card_var.set('')
    
    def update_display(self):
        try:
            self.transactions = sorted([item for item in self.transactions], key=lambda x: x["Date"])

            # Clear tree
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for i, transaction in enumerate(self.transactions):
                if transaction["Transaction Type"] == 'Expense':
                    self.tree.insert("", "end", iid=f"I{i+1:03d}", values=(
                        pd.to_datetime(transaction["Date"]).date(),
                        f"(${transaction["Amount"]:.2f})",
                        transaction["Transaction Type"],
                        transaction["Card"]
                    ))
                elif transaction["Transaction Type"] == 'Income':
                    self.tree.insert("", "end", iid=f"I{i+1:03d}", values=(
                        pd.to_datetime(transaction["Date"]).date(),
                        f"${transaction["Amount"]:.2f}",
                        transaction["Transaction Type"],
                        ''
                    ))

            # Update chart
            self.update_graph()
        except:
            self.transactions = sorted([item for item in self.transactions], key=lambda x: x["Date"])

            # Clear tree
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for i, transaction in enumerate(self.transactions):
                if transaction["Transaction Type"] == 'Expense':
                    self.tree.insert("", "end", iid=f"I{i+1:03d}", values=(
                        pd.to_datetime(transaction["Date"]).date(),
                        f"(${transaction["Amount"]:.2f})",
                        transaction["Transaction Type"],
                        transaction["Card"]
                    ))
                elif transaction["Transaction Type"] == 'Income':
                    self.tree.insert("", "end", iid=f"I{i+1:03d}", values=(
                        pd.to_datetime(transaction["Date"]).date(),
                        f"${transaction["Amount"]:.2f}",
                        transaction["Transaction Type"],
                        ''
                    ))
            self.ax2.clear()
            self.canvas2.draw()
    
    def update_graph(self):
        # Clear previous chart
        self.ax2.clear()

        df = pd.DataFrame(self.transactions)
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

        cards_used = np.unique(df['Card'])
        payment_dates = []

        for card in cards_used:
            if card == "Amex":
                try:
                    last_date = df[df['Card'] == card]['Date'].to_list()[-1]
                    if last_date.month == 12:
                        payment_date = pd.Timestamp(year=last_date.year + 1, month=1, day=20)
                    else:
                        payment_date = pd.Timestamp(year=last_date.year, month=last_date.month + 1, day=20)
                    payment_dates.append(payment_date)
                except:
                    pass
            elif card == "Wells Fargo":
                try:
                    last_date = df[df['Card'] == card]['Date'].to_list()[-1]
                    if last_date.month == 12:
                        payment_date = pd.Timestamp(year=last_date.year + 1, month=1, day=20) + pd.offsets.MonthEnd(0)
                    else:
                        payment_date = pd.Timestamp(year=last_date.year, month=last_date.month + 1, day=20) + pd.offsets.MonthEnd(0)
                    payment_dates.append(payment_date)
                except:
                    pass
            elif card == "US Bank":
                try:
                    last_date = df[df['Card'] == card]['Date'].to_list()[-1]
                    if last_date.month == 12:
                        payment_date = pd.Timestamp(year=last_date.year + 1, month=1, day=10)
                    else:
                        payment_date = pd.Timestamp(year=last_date.year, month=last_date.month + 1, day=10)
                    payment_dates.append(payment_date)
                except:
                    pass
            elif card == "Citi Bank":
                try:
                    last_date = df[df['Card'] == card]['Date'].to_list()[-1]
                    if last_date.month == 12:
                        payment_date = pd.Timestamp(year=last_date.year + 1, month=1, day=28)
                    else:
                        payment_date = pd.Timestamp(year=last_date.year, month=last_date.month + 1, day=28)
                    payment_dates.append(payment_date)
                except:
                    pass
            elif card == "Discover":
                try:
                    last_date = df[df['Card'] == card]['Date'].to_list()[-1]
                    if last_date.month == 12:
                        payment_date = pd.Timestamp(year=last_date.year + 1, month=1, day=25)
                    else:
                        payment_date = pd.Timestamp(year=last_date.year, month=last_date.month + 1, day=25)
                    payment_dates.append(payment_date)
                except:
                    pass

        payments = {'Card': [card for card in cards_used if card != ''],
                'Amount': [-sum(df[df['Card'] == card]['Amount']) for card in cards_used if card != ''],
                'Date': payment_dates
                }
        payments = pd.DataFrame(payments)

        if not payments.empty:
            start_time = datetime.now()
            if len(np.unique(df['Date'])) == 1:
                start_time = pd.Timestamp(year=start_time.year, month=start_time.month - 1, day=1)
            else:
                start_time = pd.Timestamp(year=start_time.year, month=start_time.month, day=1)
            calender = pd.date_range(start = min(start_time, df['Date'].min()), end = payments['Date'].max(), freq = 'D')

            pay_days = []
            for date in calender:
                if date.day == 15:
                    pay_days.append(date.date().strftime('%m/%d/%Y'))
                elif date == date + pd.offsets.MonthEnd(0):
                    pay_days.append(date.date().strftime('%m/%d/%Y'))
            
            df_income = df[df["Transaction Type"] == 'Income']

            income_amount = [1_331]*len(pay_days)
            income_amount.extend(df_income['Amount'].to_list())
            pay_days.extend(df_income['Date'].to_list())

            income = pd.DataFrame({'Date': pay_days, 'Amount': income_amount})

            calender = pd.DataFrame([date.date().strftime('%m/%d/%Y') for date in calender])
            calender.columns = ['Date']

            net_worth = pd.concat([income, payments.drop('Card', axis = 1), calender], ignore_index = True).fillna(0)
            net_worth['Date'] = pd.to_datetime(net_worth['Date'], format = '%m/%d/%Y')
            net_worth = net_worth.groupby('Date', as_index = False)['Amount'].sum()
            net_worth = net_worth.sort_values('Date')
            net_worth.set_index('Date')

            net_worth['Balance'] = self.starting_balance.get() + net_worth['Amount'].cumsum()
            net_worth['Balance'] = net_worth['Balance'].ffill()

            self.ax2.plot(net_worth['Date'], net_worth['Balance'])
            self.ax2.xaxis.set_major_locator(mdates.MonthLocator())
            self.ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
            self.canvas2.draw()

    def on_closing(self):
        """Clean up before closing"""
        df = pd.DataFrame(self.transactions)
        df.to_csv("C:\\Users\\jacob\\OneDrive\\Desktop\\Budget\\Budget Plotting.csv", index = False)
        # Perform any cleanup needed
        self.root.destroy()
        self.root.quit()  # This helps terminate mainloop properly

root = tk.Tk()
app = BudgetPlotter(root)
root.mainloop()