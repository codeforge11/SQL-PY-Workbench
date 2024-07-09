from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QTextEdit, QVBoxLayout, QWidget
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

        self.hostlabel = QLabel("Host:", self)
        self.hostlabel.setAlignment(Qt.AlignCenter)
        self.hostlabel.setFont(QFont('Arial', 16))

        self.portlabel = QLabel("Port:", self)
        self.portlabel.setAlignment(Qt.AlignCenter)
        self.portlabel.setFont(QFont('Arial', 16))

        self.userlabel = QLabel("User:", self)
        self.userlabel.setAlignment(Qt.AlignCenter)
        self.userlabel.setFont(QFont('Arial', 16))

        self.passwordlabel = QLabel("Password:", self)
        self.passwordlabel.setAlignment(Qt.AlignCenter)
        self.passwordlabel.setFont(QFont('Arial', 16))

        self.host_input_field = QLineEdit(self)
        self.host_input_field.setFont(QFont('Arial', 20))
        self.host_input_field.setPlaceholderText("localhost")

        self.user_input_field = QLineEdit(self)
        self.user_input_field.setFont(QFont('Arial', 20))

        self.password_input_field = QLineEdit(self)
        self.password_input_field.setFont(QFont('Arial', 20))

        self.port_input_field = QLineEdit(self)
        self.port_input_field.setFont(QFont('Arial', 20))
        self.port_input_field.setPlaceholderText("3306")

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

        self.exit_button = QPushButton("Exit", self)
        self.exit_button.move(0, 0)
        self.exit_button.clicked.connect(self.exit_database)

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
        layout.addWidget(self.hostlabel)
        layout.addWidget(self.host_input_field)
        layout.addWidget(self.portlabel)
        layout.addWidget(self.port_input_field)
        layout.addWidget(self.userlabel)
        layout.addWidget(self.user_input_field)
        layout.addWidget(self.passwordlabel)
        layout.addWidget(self.password_input_field)
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
        layout.addWidget(self.exit_button)

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
        self.exit_button.hide()
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
        self.exit_button.show()
        self.setFixedSize(800, 800)

    def button_clicked(self):
        self.host = self.host_input_field.text() if self.host_input_field.text() else "127.0.0.1"
        self.user = self.user_input_field.text()
        self.password = self.password_input_field.text()
        port_text = self.port_input_field.text()
        self.port = int(port_text) if port_text else 3306

        try:
            self.db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port
            )

            self.hostlabel.hide()
            self.userlabel.hide()
            self.passwordlabel.hide()
            self.portlabel.hide()
            self.host_input_field.hide()
            self.user_input_field.hide()
            self.password_input_field.hide()
            self.port_input_field.hide()
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
                result = cursor.execute(sql_code, multi=True)
                if result is not None:
                    for res in result:
                        if res.with_rows:
                            result_data = list(res.fetchall())
                            self.display_results(result_data, res)
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

    def exit_database(self):
        if self.db is not None and self.db.is_connected():
            self.db.close()
            self.db = None
        self.hide_elements()
        self.hostlabel.show()
        self.userlabel.show()
        self.passwordlabel.show()
        self.portlabel.show()
        self.host_input_field.show()
        self.user_input_field.show()
        self.password_input_field.show()
        self.port_input_field.show()
        self.connect_button.show()
        self.setFixedSize(800, 400)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
