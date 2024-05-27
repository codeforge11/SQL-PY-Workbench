from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QTextEdit, QVBoxLayout, QWidget
import mysql.connector
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.db = None
        self.setWindowTitle("SQL-PY-Workbench")
        self.setGeometry(0, 0, 800, 800)

        self.setWindowIcon(QIcon('Images/32ico.png'))

        self.setFixedSize(800, 800)

        self.label1 = QLabel("Host:", self)
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setFont(QFont('Arial', 16))

        self.label4 = QLabel("Port:", self)
        self.label4.setAlignment(Qt.AlignCenter)
        self.label4.setFont(QFont('Arial', 16))

        self.label2 = QLabel("User:", self)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setFont(QFont('Arial', 16))

        self.label3 = QLabel("Password:", self)
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.setFont(QFont('Arial', 16))

        self.text_field1 = QLineEdit(self)
        self.text_field1.setFont(QFont('Arial', 20))
        self.text_field1.setPlaceholderText("localhost")

        self.text_field2 = QLineEdit(self)
        self.text_field2.setFont(QFont('Arial', 20))

        self.text_field3 = QLineEdit(self)
        self.text_field3.setFont(QFont('Arial', 20))

        self.text_field4 = QLineEdit(self)
        self.text_field4.setFont(QFont('Arial', 20))
        self.text_field4.setPlaceholderText("3306")

        self.connect_button = QPushButton("Connect to database", self)
        self.connect_button.clicked.connect(self.button_clicked)
        self.connect_button.setStyleSheet("background-color: #3a86ff; color: white; font-size: 25px;")

        self.error_label = QLabel("", self)
        self.error_label.setStyleSheet("color: red")

        self.sql_label = QLabel("Enter SQL code:", self)
        self.sql_label.setAlignment(Qt.AlignCenter)
        self.sql_label.setFont(QFont('Arial', 20))

        self.sql_entry = QTextEdit(self)
        self.sql_entry.setFont(QFont('Arial', 22))

        self.execute_button = QPushButton("Execute SQL", self)
        self.execute_button.clicked.connect(self.execute_sql)
        self.execute_button.setStyleSheet("background-color: #3a86ff; color: white; font-size: 16px;")

        self.status_label = QLabel("", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont('Arial', 20))

        self.result_label = QLabel("Results:", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont('Arial', 20))

        self.result_text = QTextEdit(self)
        self.result_text.setReadOnly(True)

        self.messages_label = QLabel("Messages:", self)
        self.messages_label.setAlignment(Qt.AlignCenter)
        self.messages_label.setFont(QFont('Arial', 20))

        self.messages_text = QTextEdit(self)
        self.messages_text.setReadOnly(True)

        self.hide_elements()

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.addWidget(self.label1)
        layout.addWidget(self.text_field1)
        layout.addWidget(self.label4)
        layout.addWidget(self.text_field4)
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
        self.sql_label.hide()
        self.sql_entry.hide()
        self.execute_button.hide()
        self.result_label.hide()
        self.result_text.hide()
        self.messages_label.hide()
        self.messages_text.hide()
        self.setStyleSheet("background-color: light gray")
        self.setFixedSize(800, 400)

    def show_elements(self):
        self.sql_label.show()
        self.sql_entry.show()
        self.execute_button.show()
        self.result_label.show()
        self.result_text.show()
        self.messages_label.show()
        self.messages_text.show()
        self.setFixedSize(800, 800)

    def button_clicked(self):
        self.host = self.text_field1.text() if self.text_field1.text() else "127.0.0.1"
        self.user = self.text_field2.text()
        self.password = self.text_field3.text()
        port_text = self.text_field4.text()
        self.port = int(port_text) if port_text else 3306

        try:
            self.db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port
            )

            self.label1.hide()
            self.label2.hide()
            self.label3.hide()
            self.label4.hide()
            self.text_field1.hide()
            self.text_field2.hide()
            self.text_field3.hide()
            self.text_field4.hide()
            self.connect_button.hide()
            self.error_label.hide()
            self.messages_text.clear()

            self.show_elements()

        except mysql.connector.Error as err:
             self.display_message(f"Connection error: {err}")
             self.error_label.setText(str(err))

    def execute_sql(self):
        self.messages_text.clear()
        self.status_label.setText("")
        self.status_label.setStyleSheet("")

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
                self.display_message(f"SQL execution error: {err}")
        else:
            self.status_label.setText("Not connected to the database")
            self.status_label.setStyleSheet("color: red")

    def display_results(self, data, cursor):
        self.result_text.clear()

        column_names = [i[0] for i in cursor.description]
        self.result_text.append(" | ".join(column_names))

        for row in data:
            row_data = [f"{val}" for col, val in zip(column_names, row)]
            self.result_text.append(" | ".join(row_data))
            self.result_text.append("-" * 40)

    def display_message(self, message):
        self.messages_text.append(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
