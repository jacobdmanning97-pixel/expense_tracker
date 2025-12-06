import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BudgetTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker with CSV Upload")
        self.root.geometry("1200x900")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize data
        self.transactions = []
        self.categories = ["Food", "Gas", "Entertainment", "Utilities", "Housing", "Shopping", "Healthcare", "Fast Food", "Insurance", "Other"]
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
        
        # Input form
        ttk.Label(left_frame, text="Date:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(left_frame, textvariable=self.date_var, width=20).grid(row=0, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(left_frame, text="Description:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.desc_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.desc_var, width=20).grid(row=1, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(left_frame, text="Amount:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.amount_var = tk.DoubleVar()
        ttk.Entry(left_frame, textvariable=self.amount_var, width=20).grid(row=2, column=1, pady=2, padx=(5, 0))
        
        ttk.Label(left_frame, text="Category:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(left_frame, textvariable=self.category_var, 
                                     values=self.categories, width=18)
        category_combo.grid(row=3, column=1, pady=2, padx=(5, 0))
        
        ttk.Button(left_frame, text="Add Transaction", command=self.add_transaction, width=20).grid(row=6, column=0, columnspan=2, pady=10)
        
        # CSV Upload section
        ttk.Separator(left_frame, orient='horizontal').grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        ttk.Button(left_frame, text="Upload Saved CSV", command=self.upload_csv, width=20).grid(row=9, column=0, columnspan=2, pady=5)

        # Transactions table
        columns = ("Date", "Description", "Amount", "Category")
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
        
        self.food_var = tk.StringVar(value="Food: $0.00")
        self.gas_var = tk.StringVar(value="Gas: $0.00")
        self.entertainment_var = tk.StringVar(value="Entertainment: $0.00")
        self.utilities_var = tk.StringVar(value="Utilities: $0.00")
        self.housing_var = tk.StringVar(value="Housing: $0.00")
        self.shopping_var = tk.StringVar(value="Shopping: $0.00")
        self.healthcare_var = tk.StringVar(value="Healthcare: $0.00")
        self.fast_food_var = tk.StringVar(value="Fast Food: $0.00")
        self.insurance_var = tk.StringVar(value="Insurance: $0.00")
        self.other_var = tk.StringVar(value="Other: $0.00")
        
        ttk.Label(summary_frame, textvariable=self.food_var, font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Label(summary_frame, textvariable=self.gas_var, font=('Arial', 10)).grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        ttk.Label(summary_frame, textvariable=self.entertainment_var, font=('Arial', 10)).grid(row=0, column=2, sticky=tk.W, padx=(0, 20))
        ttk.Label(summary_frame, textvariable=self.utilities_var, font=('Arial', 10)).grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
        ttk.Label(summary_frame, textvariable=self.housing_var, font=('Arial', 10)).grid(row=0, column=4, sticky=tk.W, padx=(0, 20))
        ttk.Label(summary_frame, textvariable=self.shopping_var, font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Label(summary_frame, textvariable=self.healthcare_var, font=('Arial', 10)).grid(row=1, column=1, sticky=tk.W, padx=(0, 20))
        ttk.Label(summary_frame, textvariable=self.fast_food_var, font=('Arial', 10)).grid(row=1, column=2, sticky=tk.W, padx=(0, 20))
        ttk.Label(summary_frame, textvariable=self.insurance_var, font=('Arial', 10)).grid(row=1, column=3, sticky=tk.W, padx=(0, 20))
        ttk.Label(summary_frame, textvariable=self.other_var, font=('Arial', 10)).grid(row=1, column=4, sticky=tk.W, padx=(0, 20))
        
        # Chart frame
        chart_frame = ttk.Frame(right_frame)
        chart_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Create a figure for the chart
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        ttk.Separator(left_frame, orient='horizontal').grid(row=11, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Delete button
        ttk.Button(left_frame, text="Delete Selected", command=self.delete_transaction, width=20).grid(row=12, column=0, columnspan=2, pady=10)
        
        ttk.Separator(left_frame, orient='horizontal').grid(row=13, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Change button
        ttk.Label(left_frame, text="Updated Category:").grid(row=14, column=0, sticky=tk.W, pady=2)
        self.updated_category_var = tk.StringVar()
        category_combo = ttk.Combobox(left_frame, textvariable=self.updated_category_var, 
                                     values=self.categories, width=18)
        category_combo.grid(row=14, column=1, pady=2, padx=(5, 0))
    
        ttk.Button(left_frame, text="Change Selected", command=self.change_category, width=20).grid(row=15, column=0, columnspan=2, pady=10)

        ttk.Separator(left_frame, orient='horizontal').grid(row=16, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(left_frame, text="Upload Bank CSV", font=('Arial', 10, 'bold')).grid(row=17, column=0, columnspan=2, pady=5)
        ttk.Button(left_frame, text="Upload Bank CSV", command=self.clean_csv, width=20).grid(row=18, column=0, columnspan=2, pady=5)

        ttk.Label(left_frame, text="Which Bank CSV?:").grid(row=19, column=0, sticky=tk.W, pady=2)
        self.card_to_read = tk.StringVar()
        category_combo = ttk.Combobox(left_frame, textvariable=self.card_to_read, 
                                     values=self.cards, width=18)
        category_combo.grid(row=19, column=1, pady=2, padx=(5, 0))

    def add_transaction(self):
        try:
            date = self.date_var.get()
            description = self.desc_var.get()
            amount = self.amount_var.get()
            category = self.category_var.get()
            
            if not all([date, description, category]) or amount <= 0:
                messagebox.showerror("Error", "Please fill all fields with valid values")
                return
            
            # Add to transactions list
            transaction = {
                "Date": date,
                "Description": description,
                "Amount": amount,
                "Category": category,
            }
            
            self.transactions.append(transaction)
            self.update_display()
            
            # Clear input fields
            self.desc_var.set("")
            self.amount_var.set(0.0)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
    
    def clean_csv(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Read CSV file
            df = pd.read_csv(file_path)

            if self.card_to_read.get() == "Amex":
                df = df.drop(['Card Member', 'Account #'], axis=1)
                df = df[df["Amount"] > 0]

            elif self.card_to_read.get() == "Wells Fargo":
                df.columns = ["Date", "Amount", "Blank 1", "Blank 2", "Description"]
                df = df.drop(['Blank 1', 'Blank 2'], axis=1)
                df = df[df["Amount"] < 0]
                df["Amount"] = -1*df["Amount"]

            elif self.card_to_read.get() == "US Bank":
                df = df.drop(["Transaction", "Memo"], axis=1)
                df.columns = ["Date", "Description", "Amount"]
                df = df[df["Amount"] < 0]
                df["Amount"] = -1*df["Amount"]

            elif self.card_to_read.get() == "Citi Bank":
                df = df.drop(["Status", "Credit"], axis=1)
                df.columns = ["Date", "Description", "Amount"]
                df = df.dropna(subset=["Amount"])

            elif self.card_to_read.get() == "Discover":
                df = df.drop(["Post Date", "Category"], axis=1)
                df.columns = ["Date", "Description", "Amount"]
                df = df[df["Amount"] > 0]

            category = []
            for _, row in df.iterrows():
                category.append(self.sort_purchases(row["Description"]))
            df["Category"] = category

            # Add transactions from CSV
            for _, row in df.iterrows():
                transaction = {
                    "Date": row['Date'],
                    "Description": row['Description'],
                    "Amount": float(row['Amount']),
                    "Category": row['Category']
                }
                self.transactions.append(transaction)
            
            self.update_display()
            messagebox.showinfo("Success", f"Successfully imported {len(df)} transactions")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read CSV file: {str(e)}")

    def sort_purchases(self, description):
        label = "Other"

        sorter = {category: [] for category in self.categories}
        
        sorter["Food"] = ["FOOD LION", "INGLES", "SAMS", "WM", "WAL-MART"]
        sorter["Gas"] = ["QT", "STOP A MINIT"]
        sorter["Entertainment"] = ["CINEMAS"]
        sorter["Utilities"] = ["CITY OF FOUNTAIN INN", "LAURENS ELECTRIC", "GREENVILLE WATER", "ATT"]
        sorter["Housing"] = ["LOWES", "HARDWARE"]
        sorter["Shopping"] = ["YouTubePremium", "TARGET", "MICHAELS", "CLEMSON", "AMAZON", "Kindle", "REBELSTORK", "DESERET BOOK"]
        sorter["Healthcare"] = ["GREAT CLIPS", "CVS", "PRISMA"]
        sorter["Insurance"] = ["Ambetter", "GEICO"]
        sorter["Fast Food"] = ["BURGER KING", "GRUBHUB", "PANDA", "FIVE GUYS", "UBER EATS", "DUNKIN"]

        for category in self.categories:
            for identifier in sorter[category]:
                if identifier in description:
                    label = category

        return label

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
            required_columns = ['Date', 'Description', 'Amount', 'Category']
            if not all(col in df.columns for col in required_columns):
                messagebox.showerror("Error", "CSV file must contain columns: Date, Description, Amount, Category")
                return
            
            # Add transactions from CSV
            for _, row in df.iterrows():
                transaction = {
                    "Date": row['Date'],
                    "Description": row['Description'],
                    "Amount": abs(float(row['Amount'])),
                    "Category": row['Category']
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

    def change_category(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a transaction to change the category")
            return
        
        index = int(selected_item[0].lstrip('I')) - 1
        print(self.transactions[index]["Category"])
        self.transactions[index]["Category"] = self.updated_category_var.get()
        print(self.transactions[index]["Category"])
        self.update_display()
    
    def update_display(self):
        self.transactions = sorted([item for item in self.transactions], key=lambda x: x["Category"])

        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        df = pd.DataFrame(self.transactions)
        
        for i, transaction in enumerate(self.transactions):
            self.tree.insert("", "end", iid=f"I{i+1:03d}", values=(
                pd.to_datetime(transaction["Date"]).date(),
                transaction["Description"],
                f"(${abs(transaction["Amount"]):.2f})",
                transaction["Category"]
            ))

        self.food_var.set(f"Food: ${sum([amount for amount in df[df["Category"] == "Food"]["Amount"]]):.2f}")
        self.gas_var.set(f"Gas: ${sum([amount for amount in df[df["Category"] == "Gas"]["Amount"]]):.2f}")
        self.entertainment_var.set(f"Entertainment: ${sum([amount for amount in df[df["Category"] == "Entertainment"]["Amount"]]):.2f}")
        self.utilities_var.set(f"Utilities: ${sum([amount for amount in df[df["Category"] == "Utilities"]["Amount"]]):.2f}")
        self.housing_var.set(f"Housing: ${sum([amount for amount in df[df["Category"] == "Housing"]["Amount"]]):.2f}")
        self.shopping_var.set(f"Shopping: ${sum([amount for amount in df[df["Category"] == "Shopping"]["Amount"]]):.2f}")
        self.healthcare_var.set(f"Healthcare: ${sum([amount for amount in df[df["Category"] == "Healthcare"]["Amount"]]):.2f}")
        self.fast_food_var.set(f"Fast Food: ${sum([amount for amount in df[df["Category"] == "Fast Food"]["Amount"]]):.2f}")
        self.insurance_var.set(f"Insurance: ${sum([amount for amount in df[df["Category"] == "Insurance"]["Amount"]]):.2f}")
        self.other_var.set(f"Other: ${sum([amount for amount in df[df["Category"] == "Other"]["Amount"]]):.2f}")

        # Update chart
        self.update_chart()
    
    def update_chart(self):
        # Clear previous chart
        self.ax.clear()
        
        # Group expenses by category
        expenses_by_category = {}
        for transaction in self.transactions:
            category = transaction["Category"]
            amount = transaction["Amount"]
            expenses_by_category[category] = expenses_by_category.get(category, 0) + amount
        
        if expenses_by_category:
            # Create pie chart
            categories = list(expenses_by_category.keys())
            amounts = list(expenses_by_category.values())
            
            self.ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
            self.ax.set_title('Expenses by Category')
            self.ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        else:
            self.ax.text(0.5, 0.5, 'No expense data available', 
                        horizontalalignment='center', verticalalignment='center',
                        transform=self.ax.transAxes)
            self.ax.set_title('Expenses by Category')
        
        self.canvas.draw()

    def on_closing(self):
        """Clean up before closing"""
        df = pd.DataFrame(self.transactions)
        df.to_csv("C:\\Users\\jacob\\Downloads\\saved.csv", index = False)
        # Perform any cleanup needed
        self.root.destroy()
        self.root.quit()  # This helps terminate mainloop properly

root = tk.Tk()
app = BudgetTracker(root)
root.mainloop()
