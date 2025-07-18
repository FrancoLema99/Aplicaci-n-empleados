import sys
import psycopg2
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QHeaderView
)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont

from util.database import data_base, user, password, host, port

# Connecting to the DataBase

connection = psycopg2.connect(
    dbname = data_base,
    user = user,
    password = password, # For development environment
    host = host,
    port = port
)

# Saving the information in the database
def save_employee(name_input, position_input, salary_input, table):
    name = name_input.text() 
    position = position_input.text()
    salary = salary_input.text()

    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO employees(name, position, salary) VALUES(%s, %s, %s)", 
        (name, position, salary)
        )
    
    connection.commit()
    cursor.close()

    name_input.clear()
    position_input.clear()
    salary_input.clear()

    table.clearSelection()

    load_employees(table)

# Loading data from the database
def load_employees(table):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employees ORDER BY id")

    employees = cursor.fetchall()

    cursor.close()

    table.setRowCount(len(employees))
    table.setColumnCount(5) # id, Nombre, Puesto, Salario, Botón para eliminar
    table.setHorizontalHeaderLabels(['ID', 'Nombre', 'Puesto', 'Salario', 'Acción'])

    for i, employee in enumerate(employees):
        for j, column in enumerate(employee):
            item = QTableWidgetItem(str(column))
            item.setTextAlignment(Qt.AlignCenter)

            table.setItem(i, j, item)

        delete_button = QPushButton()
        delete_button.setIcon(QIcon('delete.png'))
        delete_button.setIconSize(QSize(24, 24))
        delete_button.setFlat(True)

        table.setCellWidget(i, 4, delete_button)



# Main window
def create_window():

    window = QWidget()
    window.setWindowTitle('Employee maintenance')
    window.setGeometry(100, 100, 900, 400)

    layout = QVBoxLayout()

# ----- Name Layout -----------------
    name_layout = QVBoxLayout() # Vertical
    entry_layout = QHBoxLayout() # Horizontal

    # Text Box
    name_input = QLineEdit()
    name_input.setMinimumSize(200, 35)
    name_input.setFont(QFont('Arial', 12))

    name_label = QLabel('Nombre')
    name_label.setFont(QFont('Arial', 11))

    name_layout.addWidget(name_label)
    name_layout.addWidget(name_input)

    entry_layout.addLayout(name_layout)

# ----- Position Layout -----------------

    position_layout = QVBoxLayout()
    

    # Text Box
    position_input = QLineEdit()
    position_input.setMinimumSize(200, 35)
    position_input.setFont(QFont('Arial', 12))

    position_label = QLabel('Puesto')
    position_label.setFont(QFont('Arial', 12))


    position_layout.addWidget(position_label)
    position_layout.addWidget(position_input)

    entry_layout.addLayout(position_layout)


# ----- Salary  Layout -----------------


    salary_layout = QVBoxLayout()

    # Text Box
    salary_input = QLineEdit()
    salary_input.setMinimumSize(200, 35)
    salary_input.setFont(QFont('Arial', 12))

    salary_label = QLabel('Sueldo')
    salary_label.setFont(QFont('Arial', 12))


    salary_layout.addWidget(salary_label)
    salary_layout.addWidget(salary_input)

    entry_layout.addLayout(salary_layout)


# ----- Adding the 'Save' button -----

    save_button = QPushButton()
    save_button.setIcon(QIcon('save.png'))
    save_button.setIconSize(QSize(36, 36))
    save_button.setFlat(True) # Borderless
    save_button.setToolTip('Guardar cambios.')

    entry_layout.addWidget(save_button)

# ------ Label distribution -------

    entry_layout.setStretch(0 ,3) # Name
    entry_layout.setStretch(1, 1) # Position
    entry_layout.setStretch(2, 1) # Salary
    entry_layout.setStretch(3, 0)

    layout.addLayout(entry_layout)


# ----- Creating the grid graphic element ------

    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(['ID', 'Nombre', 'Puesto', 'Salario'])
    table.horizontalHeader().setStretchLastSection(True)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    layout.addWidget(table)

    save_button.clicked.connect(lambda: save_employee(name_input, position_input, salary_input, table))

    window.setLayout(layout)

    # Calling load_employees function
    load_employees(table)

    window.show()

    return window


# Function that executes the application
 
def main():
    app = QApplication(sys.argv)
    window = create_window()
    sys.exit(app.exec_())

if __name__== '__main__':
    main()


