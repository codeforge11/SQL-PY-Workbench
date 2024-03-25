from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QTextEdit, QVBoxLayout, QWidget
import mysql.connector
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Initialize the main window and set properties
        self.db = None
        self.setWindowTitle("SQL-PY-Workbench")
        self.setGeometry(0, 0, 800, 800)

        # Set the window icon
        self.setWindowIcon(QIcon('Images/32ico.png'))

        # Set the window size to be fixed
        self.setFixedSize(800, 800)

        # Create and pack labels and entry fields for database connection
        self.label1 = QLabel("Host:", self)
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setFont(QFont('Arial', 16))

        self.label2 = QLabel("User:", self)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setFont(QFont('Arial', 16))

        self.label3 = QLabel("Password:", self)
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.setFont(QFont('Arial', 16))

        self.text_field1 = QLineEdit(self)
        self.text_field1.setFont(QFont('Arial', 20))

        self.text_field2 = QLineEdit(self)
        self.text_field2.setFont(QFont('Arial', 20))

        self.text_field3 = QLineEdit(self)
        self.text_field3.setFont(QFont('Arial', 20))

        # Create and pack connect button
        self.connect_button = QPushButton("Connect to database", self)
        self.connect_button.clicked.connect(self.button_clicked)
        self.connect_button.setStyleSheet("background-color: #3a86ff; color: white; font-size: 25px;")

        # Create and pack error label
        self.error_label = QLabel("", self)
        self.error_label.setStyleSheet("color: red")

        # Create and pack SQL entry widgets
        self.sql_label = QLabel("Enter SQL code:", self)
        self.sql_label.setAlignment(Qt.AlignCenter)
        self.sql_label.setFont(QFont('Arial', 20))

        self.sql_entry = QTextEdit(self)
        self.sql_entry.setFont(QFont('Arial', 22))  # Set the font size to 22

        # Create and pack SQL execution buttons and labels
        self.execute_button = QPushButton("Execute SQL", self)
        self.execute_button.clicked.connect(self.execute_sql)
        self.execute_button.setStyleSheet("background-color: #3a86ff; color: white; font-size: 16px;")
        # Define status_label
        self.status_label = QLabel("", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont('Arial', 20))

        # Create and pack result display widgets
        self.result_label = QLabel("Results:", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont('Arial', 20))

        self.result_text = QTextEdit(self)
        self.result_text.setReadOnly(True)

        # Create and pack messages display widgets
        self.messages_label = QLabel("Messages:", self)
        self.messages_label.setAlignment(Qt.AlignCenter)
        self.messages_label.setFont(QFont('Arial', 20))

        self.messages_text = QTextEdit(self)
        self.messages_text.setReadOnly(True)

        # Hide elements initially
        self.hide_elements()

        # Set layout
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.addWidget(self.label1)
        layout.addWidget(self.text_field1)
        layout.addWidget(self.label2)
        layout.addWidget(self.text_field2)
        layout.addWidget(self.label3)
        layout.addWidget(self.text_field3)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.error_label)
        layout.addWidget(self.sql_label)
        layout.addWidget(self.sql_entry)
        layout.addWidget(self.execute_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_text)
        layout.addWidget(self.messages_label)
        layout.addWidget(self.messages_text)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def hide_elements(self):
        # Hide SQL-related elements
        self.sql_label.hide()
        self.sql_entry.hide()
        self.execute_button.hide()
        self.result_label.hide()
        self.result_text.hide()
        self.messages_label.hide()
        self.messages_text.hide()
        self.setStyleSheet("background-color: light gray")

    def show_elements(self):
        # Show SQL-related elements
        self.sql_label.show()
        self.sql_entry.show()
        self.execute_button.show()
        self.result_label.show()
        self.result_text.show()
        self.messages_label.show()
        self.messages_text.show()

    def button_clicked(self):
        # Handle database connection button click
        self.host = self.text_field1.text()
        self.user = self.text_field2.text()
        self.password = self.text_field3.text()

        try:
            # Attempt to connect to the MySQL database
            self.db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )

            # Hide connection-related elements
            self.label1.hide()
            self.label2.hide()
            self.label3.hide()
            self.text_field1.hide()
            self.text_field2.hide()
            self.text_field3.hide()
            self.connect_button.hide()
            self.error_label.hide()
            self.messages_text.clear()

            # Show SQL-related elements
            self.show_elements()

        except mysql.connector.Error as err:
            # Handle connection error
            self.display_message(f"Connection error: {err}")

    def execute_sql(self):
        # Clear the messages_text widget and reset the status_label
        self.messages_text.clear()
        self.status_label.setText("")
        self.status_label.setStyleSheet("")

        # Execute entered SQL code and display results or errors
        if self.db is not None and self.db.is_connected():
            cursor = self.db.cursor()
            sql_code = self.sql_entry.toPlainText()
            try:
                cursor.execute(sql_code)
                if cursor.description:
                    result_data = list(cursor.fetchall())
                    self.display_results(result_data, cursor)  
                    self.status_label.setText("SQL executed successfully")
                    self.status_label.setStyleSheet("color: green")
                else:
                    self.status_label.setText("SQL executed successfully")
                    self.status_label.setStyleSheet("color: green")
            except mysql.connector.Error as err:
                # Handle SQL execution error
                self.display_message(f"SQL execution error: {err}")
        else:
            self.status_label.setText("Not connected to the database")
            self.status_label.setStyleSheet("color: red")

    def display_results(self, data, cursor):
        # Display query results in the result_text widget
        self.result_text.clear()

        # Display column names
        column_names = [i[0] for i in cursor.description]
        self.result_text.append(" | ".join(column_names))

        # Display rows
        for row in data:
            row_data = [f"{val}" for col, val in zip(column_names, row)]
            self.result_text.append(" | ".join(row_data))
            self.result_text.append("-" * 40)  # Add a line after each row

    def display_message(self, message):
        # Display a message in the messages_text widget
        self.messages_text.append(message)


# Main section
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())