import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QComboBox, QLineEdit,
                            QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                            QWidget, QTextEdit, QMessageBox, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QFont

class POSApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cart_items = []
        self.total_amount = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Task Week 4 - POS Application')
        self.setGeometry(300, 300, 400, 400)
        self.setFixedSize(400, 400)  # Menetapkan ukuran tetap

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # My ingpo
        student_section = QVBoxLayout()

        top_line = QFrame()
        top_line.setFrameShape(QFrame.HLine)
        top_line.setFrameShadow(QFrame.Sunken)
        student_section.addWidget(top_line)

        student_info = QLabel('Nama: UMAM ALPARIZI\nNIM: F1D02310141')
        student_info.setAlignment(Qt.AlignCenter)
        student_info.setStyleSheet("font-weight: bold; padding: 5px;")
        student_section.addWidget(student_info)

        bottom_line = QFrame()
        bottom_line.setFrameShape(QFrame.HLine)
        bottom_line.setFrameShadow(QFrame.Sunken)
        student_section.addWidget(bottom_line)

        main_layout.addLayout(student_section)

        # Product field
        product_layout = QHBoxLayout()
        product_label = QLabel('Product')
        product_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        product_label.setFixedWidth(80)
        self.product_combo = QComboBox()
        self.product_combo.addItem("")
        self.product_combo.addItems(['Kecap ABC (Rp. 7,000)', 'Bimoli (Rp. 20,000)', 'Gula (Rp. 15,000)', 'Teh (Rp. 5,000)'])
        self.product_combo.setFixedHeight(25)
        product_layout.addWidget(product_label)
        product_layout.addWidget(self.product_combo)

        self.prices = {
            '': 0,
            'Kecap ABC (Rp. 7,000)': 7000,
            'Bimoli (Rp. 20,000)': 20000,
            'Gula (Rp. 15,000)': 15000,
            'Teh (Rp. 5,000)': 5000
        }

        # Quantity field
        quantity_layout = QHBoxLayout()
        quantity_label = QLabel('Quantity')
        quantity_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        quantity_label.setFixedWidth(80)
        self.quantity_input = QLineEdit()
        self.quantity_input.setValidator(QIntValidator(1, 999))
        self.quantity_input.setFixedHeight(25)
        quantity_layout.addWidget(quantity_label)
        quantity_layout.addWidget(self.quantity_input)

        # Discount input
        discount_layout = QHBoxLayout()
        discount_label = QLabel('Discount')
        discount_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        discount_label.setFixedWidth(80)
        self.discount_combo = QComboBox()
        self.discount_combo.addItem("")
        self.discount_combo.addItems(['0%', '5%', '10%', '15%', '20%'])
        self.discount_combo.setFixedHeight(25)
        discount_layout.addWidget(discount_label)
        discount_layout.addWidget(self.discount_combo)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton('Add to Cart')
        self.clear_button = QPushButton('Clear')
        self.add_button.setFixedHeight(25)
        self.clear_button.setFixedHeight(25)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.clear_button)

        # Cart
        self.cart_display = QTextEdit()
        self.cart_display.setReadOnly(True)
        self.cart_display.setMinimumHeight(150)
        self.cart_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
            }
        """)

        total_separator = QFrame()
        total_separator.setFrameShape(QFrame.HLine)
        total_separator.setFrameShadow(QFrame.Sunken)
        total_separator.setFixedHeight(5)

        total_layout = QHBoxLayout()
        self.total_label = QLabel('Total: Rp. 0')
        self.total_label.setFont(QFont('Arial', 12, QFont.Bold))
        self.total_label.setStyleSheet("margin-top: 5px;")
        total_layout.addWidget(self.total_label)
        total_layout.setAlignment(Qt.AlignLeft)

        main_layout.addLayout(product_layout)
        main_layout.addLayout(quantity_layout)
        main_layout.addLayout(discount_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.cart_display)
        main_layout.addWidget(total_separator)
        main_layout.addLayout(total_layout)

        self.add_button.clicked.connect(self.add_to_cart)
        self.clear_button.clicked.connect(self.clear_cart)

        # Styles
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 12px;
            }
            QComboBox, QLineEdit {
                font-size: 12px;
                padding: 2px 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton {
                font-size: 12px;
                padding: 2px 10px;
                background-color: #f8f8f8;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e8e8e8;
            }
            QTextEdit {
                font-size: 12px;
            }
        """)

    def add_to_cart(self):
        quantity_text = self.quantity_input.text()
        product = self.product_combo.currentText()
        discount_text = self.discount_combo.currentText()

        # Validasi input produk
        if not product:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Invalid Input")
            msg_box.setText("Please select a product.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f0f0f0;
                }
                QMessageBox QLabel {
                    font-size: 12px;
                    color: #000;
                }
                QPushButton {
                    font-size: 12px;
                    padding: 5px 10px;
                    background-color: #f8f8f8;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
            """)
            msg_box.exec_()
            return

        # Validasi input quantity
        if not quantity_text:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Invalid Input")
            msg_box.setText("Please enter a quantity.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f0f0f0;
                }
                QMessageBox QLabel {
                    font-size: 12px;
                    color: #000;
                }
                QPushButton {
                    font-size: 12px;
                    padding: 5px 10px;
                    background-color: #f8f8f8;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
            """)
            msg_box.exec_()
            return

        # Validasi input diskon
        if not discount_text:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Invalid Input")
            msg_box.setText("Please select a discount.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f0f0f0;
                }
                QMessageBox QLabel {
                    font-size: 12px;
                    color: #000;
                }
                QPushButton {
                    font-size: 12px;
                    padding: 5px 10px;
                    background-color: #f8f8f8;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
            """)
            msg_box.exec_()
            return

        try:
            quantity = int(quantity_text)
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Invalid Input")
            msg_box.setText("Please enter a valid quantity.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f0f0f0;
                }
                QMessageBox QLabel {
                    font-size: 12px;
                    color: #000;
                }
                QPushButton {
                    font-size: 12px;
                    padding: 5px 10px;
                    background-color: #f8f8f8;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
            """)
            msg_box.exec_()
            return

        price = self.prices[product]

        if discount_text == "":
            discount_percentage = 0
        else:
            discount_percentage = int(discount_text.replace('%', ''))

        total_price = price * quantity
        discount_amount = total_price * discount_percentage / 100
        final_price = total_price - discount_amount

        product_name = product.split(' ')[0] if ' ' in product else product

        item_text = f"{product_name} (Rp. {price:,}) - {quantity} x Rp. {price:,} (disc {discount_percentage}%)"
        self.cart_items.append((item_text, final_price))
        self.update_cart_display()
        self.reset_inputs()

    def reset_inputs(self):
        """Reset semua inputan ke nilai default"""
        self.product_combo.setCurrentIndex(0)
        self.quantity_input.clear()
        self.discount_combo.setCurrentIndex(0)

    def clear_cart(self):
        self.cart_items = []
        self.update_cart_display()

    def update_cart_display(self):
        self.cart_display.clear()
        for item_text, _ in self.cart_items:
            self.cart_display.append(item_text)
        self.total_amount = sum(price for _, price in self.cart_items)
        self.total_label.setText(f"Total: Rp. {int(self.total_amount):,}")

def main():
    app = QApplication(sys.argv)
    pos = POSApplication()
    pos.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
