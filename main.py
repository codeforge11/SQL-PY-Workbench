from tkinter import Tk, PhotoImage, Button, Label, Entry, Text, Frame
import tkinter as tk
import tkinter.ttk as ttk
import mysql.connector


class MainWindow:
    def __init__(self, root):
        # Initialize the main window and set properties
        self.db = None
        self.root = root
        self.root.resizable(width=False, height=False)
        self.root.title("SQL-PY-Workbench")
        self.small_icon = PhotoImage(file="./Images/16ico.png")
        self.large_icon = PhotoImage(file="./Images/32ico.png")
        self.root.iconphoto(False, self.large_icon, self.small_icon)

        # Set color style and theme images
        self.colSty = False
        self.WHITE = PhotoImage(file="./Images/Themes/L.png")
        self.BLACK = PhotoImage(file="./Images/Themes/Li.png")

        # Create and pack theme button
        self.theme_button = Button(self.root, image=self.WHITE, command=self.change_color, bd=0, highlightthickness=0)
        self.theme_button.pack(side=tk.TOP, anchor=tk.NE, padx=0, pady=0)

        # Create and pack labels and entry fields for database connection
        self.label1 = Label(self.root, text="Host:")
        self.label2 = Label(self.root, text="User:")
        self.label3 = Label(self.root, text="Password:")

        self.label1.pack(pady=0)
        self.text_field1 = Entry(self.root, width=30)
        self.text_field1.pack(pady=0)

        self.label2.pack(pady=0)
        self.text_field2 = Entry(self.root, width=30)
        self.text_field2.pack(pady=0)

        self.label3.pack(pady=0)
        self.text_field3 = Entry(self.root, width=30)
        self.text_field3.pack(pady=0)

        # Create and pack connect button
        self.connect_button = Button(self.root, text="Connect to database", command=self.button_clicked)
        self.connect_button.pack(pady=10)

        # Create and pack error label
        self.error_label = Label(self.root, text="", fg="red")
        self.error_label.pack(pady=10)

        # Create and pack SQL frame
        self.sql_frame = Frame(self.root, bg="white")
        self.sql_frame.pack(expand=True, fill='both')

        # Create and pack SQL entry widgets
        self.sql_label = Label(self.sql_frame, text="Enter SQL code:")
        self.sql_label.pack(pady=5)

        self.sql_entry = Text(self.sql_frame, height=10, width=60)
        self.sql_entry.pack(pady=5)

        # Create and pack SQL execution buttons and labels
        self.execute_button = Button(self.sql_frame, text="Execute SQL", command=self.execute_sql)
        self.clear_results_button = Button(self.sql_frame, text="Clear", command=self.clear_results)
        self.status_label = Label(self.sql_frame, text="", fg="green")

        # Create and pack result display widgets
        self.result_label = Label(self.sql_frame, text="Results:")
        self.result_label.pack(pady=5)

        self.result_text = Text(self.sql_frame, height=10, width=60)
        self.result_text.pack(pady=5)

        # Create and pack messages display widgets
        self.messages_label = Label(self.root, text="Messages:")
        self.messages_label.pack(pady=5)

        self.messages_text = Text(self.root, height=5, width=60)
        self.messages_text.pack(pady=5)

        # Hide elements initially
        self.hide_elements()

    def change_color(self):
        # Toggle color theme and update the appearance
        if self.colSty:
            self.root.configure(bg="light gray")
            self.theme_button.config(image=self.WHITE)
        else:
            self.root.configure(bg="black")
            self.theme_button.config(image=self.BLACK)
        self.colSty = not self.colSty

    def hide_elements(self):
        # Hide SQL-related elements
        self.sql_label.pack_forget()
        self.sql_entry.pack_forget()
        self.execute_button.pack_forget()
        self.clear_results_button.pack_forget()
        self.result_label.pack_forget()
        self.result_text.pack_forget()
        self.messages_label.pack_forget()
        self.messages_text.pack_forget()

    def show_elements(self):
        # Show SQL-related elements
        self.sql_label.pack(pady=5)
        self.sql_entry.pack(pady=5)
        self.execute_button.pack(pady=10)
        self.clear_results_button.pack(pady=5)
        self.result_label.pack(pady=5)
        self.result_text.pack(pady=5)
        self.messages_label.pack(pady=5)
        self.messages_text.pack(pady=5)
        self.root.geometry('800x800')

    def button_clicked(self):
        # Handle database connection button click
        self.host = self.text_field1.get()
        self.user = self.text_field2.get()
        self.password = self.text_field3.get()

        try:
            # Attempt to connect to the MySQL database
            self.db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )

            # Hide connection-related elements
            self.label1.pack_forget()
            self.label2.pack_forget()
            self.label3.pack_forget()
            self.text_field1.pack_forget()
            self.text_field2.pack_forget()
            self.text_field3.pack_forget()
            self.connect_button.pack_forget()
            self.error_label.pack_forget()

            # Show SQL-related elements
            self.show_elements()

        except mysql.connector.Error as err:
            # Handle connection error
            self.error_label.config(text=f"Connection error: {err}")
            self.display_message(f"Error: {err}")

    def execute_sql(self):
        # Clear the Treeview widget
        if hasattr(self, 'tree'):
            for i in self.tree.get_children():
                self.tree.delete(i)

        # Execute entered SQL code and display results or errors
        if self.db is not None and self.db.is_connected():
            cursor = self.db.cursor()
            sql_code = self.sql_entry.get("1.0", 'end-1c')
            try:
                cursor.execute(sql_code)
                if cursor.description:
                    result_data = list(cursor.fetchall())
                    self.display_results(result_data)  # Use display_results instead of display_table
                    self.status_label.config(text="SQL executed successfully", fg="green")
                else:
                    self.status_label.config(text="SQL executed successfully", fg="green")
            except mysql.connector.Error as err:
                # Handle SQL execution error
                self.status_label.config(text=f"SQL execution error: {err}", fg="red")
                self.display_message(f"Error: {err}")
        else:
            self.status_label.config(text="Not connected to the database", fg="red")

    def display_results(self, data):
        # Display query results in the result_text widget
        self.result_text.delete("1.0", tk.END)
        for row in data:
            self.result_text.insert(tk.END, " | ".join(map(str, row)) + "\n")

    def clear_results(self):
        # Clear result_text and messages_text widgets
        self.result_text.delete("1.0", tk.END)
        self.messages_text.delete("1.0", tk.END)

        # Recreate the Treeview widget
        if hasattr(self, 'tree'):
            self.tree.destroy()
            self.tree = ttk.Treeview(self.sql_frame, show='headings')
            self.tree.pack()

    def display_message(self, message):
        # Display a message in the messages_text widget
        self.messages_text.insert(tk.END, message + "\n")



# Main section
if __name__ == "__main__":
    root = Tk()
    main_window = MainWindow(root)
    root.mainloop()