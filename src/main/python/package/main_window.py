import os

from PySide6.QtCore import QDate
from PySide6.QtGui import QAction, Qt, QFont
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QGridLayout, \
    QPushButton, QListWidget, QCheckBox, QComboBox, QDateEdit, QTextEdit, QMessageBox

from package.api.constants import INTRO_TEXT, MONTH, PATH_APP
from package.api.functions import explore
from package.api.receipt import Receipt, load_receipts
from package.api.user import User, load_users


class HelpWidget(QWidget):  # Interface "Aide" de l'application. INTRO_TEXT est dans constants.py
    def __init__(self):
        super().__init__()

        # creation des widgets
        content = QTextEdit()

        content.setReadOnly(True)
        content.setHtml(INTRO_TEXT)
        content.setFixedSize(400, 250)
        content.setAlignment(Qt.AlignJustify)
        content.setEnabled(False)

        # creation des layouts
        box = QHBoxLayout(self)

        # ajout des widgets dans les layouts
        box.addWidget(content)


class Form(QWidget):  # utiliser pour les modifications de user tenant
    def __init__(self, user):
        super().__init__()

        self.current_user = user

        # creation des widgets du GridLayout
        self.l_last_name = QLabel("Nom")
        self.l_first_name = QLabel("Prénom")
        self.l_location = QLabel("Localisation")
        self.l_monthly_amount = QLabel("Montant mensuel")
        self.clear_button = QPushButton("Annuler")
        self.save_button = QPushButton("Sauvegarder")
        self.le_modify_occurence = QLineEdit(user.get_name)
        self.le_modify_occurence.setEnabled(False)
        self.le_last_name = QLineEdit(user.last_name)
        self.le_first_name = QLineEdit(user.first_name)
        self.le_location = QLineEdit(user.location)
        self.le_monthly_amount = QLineEdit(str(user.monthly_amount))

        # creation des Layouts
        self.box = QVBoxLayout(self)
        self.form = QGridLayout()

        # ajout des widgets dans les layouts
        self.form.addWidget(self.le_modify_occurence, 0, 0, 1, 2)
        self.form.addWidget(self.l_last_name, 1, 0, 1, 1)
        self.form.addWidget(self.le_last_name, 1, 1, 1, 1)
        self.form.addWidget(self.l_first_name, 2, 0, 1, 1)
        self.form.addWidget(self.le_first_name, 2, 1, 1, 1)
        self.form.addWidget(self.l_location, 3, 0, 1, 1)
        self.form.addWidget(self.le_location, 3, 1, 1, 1)
        self.form.addWidget(self.l_monthly_amount, 4, 0, 1, 1)
        self.form.addWidget(self.le_monthly_amount, 4, 1, 1, 1)
        self.form.addWidget(self.clear_button, 5, 0, 1, 1)
        self.form.addWidget(self.save_button, 5, 1, 1, 1)

        self.box.addLayout(self.form)

        # connexion
        self.clear_button.clicked.connect(self.close)
        self.save_button.clicked.connect(self.save)

    def save(self):
        last_name = self.le_last_name.text()
        first_name = self.le_first_name.text()
        location = self.le_location.text()
        monthly_amount = int(self.le_monthly_amount.text())
        self.current_user.modify(last_name=last_name,
                                 first_name=first_name,
                                 location=location,
                                 monthly_amount=monthly_amount,
                                 manager=False)
        self.close()
        message_box = QMessageBox()
        message_box.setText("Information modifier")
        message_box.setIcon(QMessageBox.Information)
        message_box.exec_()


class FormManager(QWidget):  # utiliser pour les modifications de user manager
    def __init__(self, user):
        super().__init__()

        self.current_user = user

        # creation des widgets
        self.l_last_name = QLabel("Nom")
        self.l_first_name = QLabel("Prénom")
        self.clear_button = QPushButton("Annuler")
        self.save_button = QPushButton("Sauvegarder")
        self.le_modify_occurence = QLineEdit(user.get_name)
        self.le_modify_occurence.setEnabled(False)
        self.le_last_name = QLineEdit(user.last_name)
        self.le_first_name = QLineEdit(user.first_name)

        # creation des layouts
        self.box = QVBoxLayout(self)
        self.form = QGridLayout()

        # ajout des widgets dans les layouts
        self.form.addWidget(self.le_modify_occurence, 0, 0, 1, 2)
        self.form.addWidget(self.l_last_name, 1, 0, 1, 1)
        self.form.addWidget(self.le_last_name, 1, 1, 1, 1)
        self.form.addWidget(self.l_first_name, 2, 0, 1, 1)
        self.form.addWidget(self.le_first_name, 2, 1, 1, 1)
        self.form.addWidget(self.clear_button, 3, 0, 1, 1)
        self.form.addWidget(self.save_button, 3, 1, 1, 1)

        self.box.addLayout(self.form)

        # connexion
        self.clear_button.clicked.connect(self.close)
        self.save_button.clicked.connect(self.save)

    def save(self):
        last_name = self.le_last_name.text()
        first_name = self.le_first_name.text()
        self.current_user.modify(last_name=last_name,
                                 first_name=first_name,
                                 manager=True)
        self.close()
        message_box = QMessageBox()
        message_box.setText("Information modifier")
        message_box.setIcon(QMessageBox.Information)
        message_box.exec_()


class RegistrationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.get_item = None
        self.get_list_item = None
        self.box = None
        font = QFont("Roboto", 20)

        # creation des widgets
        self.info_register = QLabel("Enregistrer un locataire / un gerant")
        self.info_register.setFont(font)
        self.info_register.setAlignment(Qt.AlignCenter)

        self.tenant_list = QListWidget()
        self.manager_list = QListWidget()
        self.manager_list.setFixedSize(250, 180)
        self.tenant_list.setFixedSize(250, 180)
        # ajout des elements dans manager_list et tenant_list
        for user in load_users():
            if not user.manager:
                self.tenant_list.addItem(user.get_name)
            else:
                self.manager_list.addItem(user.get_name)

        self.modify_tenant = QPushButton("Info")
        self.modify_manager = QPushButton("Info")
        self.delete_manager = QPushButton("Supprimer")
        self.delete_tenant = QPushButton("Supprimer")

        # Definition des layouts
        self.main_box = QHBoxLayout(self)
        self.left_box = QVBoxLayout()
        self.right_box = QVBoxLayout()
        self.box_tenant_tool = QHBoxLayout()
        self.box_manager_tool = QHBoxLayout()
        self.form = QGridLayout()
        self.box_form = QHBoxLayout()

        self.is_manager = QCheckBox()
        self.is_manager.setText("Gerant")
        self.clear_button = QPushButton("Tout effacer")
        self.save_button = QPushButton("Enregistrer")
        self.save_button.clicked.connect(self.click_save_button)
        self.clear_button.clicked.connect(self.clear_all)

        self.le_last_name = QLineEdit()
        self.le_last_name.setPlaceholderText("Nom")
        self.le_first_name = QLineEdit()
        self.le_first_name.setPlaceholderText("Prénom")
        self.le_location = QLineEdit()
        self.le_location.setPlaceholderText("Localisation")
        self.le_monthly_amount = QLineEdit()
        self.le_monthly_amount.setPlaceholderText("Montant Mensuel")

        self.le_last_name.setMinimumHeight(30)
        self.le_first_name.setMinimumHeight(30)
        self.le_location.setMinimumHeight(30)
        self.le_monthly_amount.setMinimumHeight(30)
        self.clear_button.setMinimumHeight(30)
        self.save_button.setMinimumHeight(30)

        # ajout des widgets aux layouts
        self.box_tenant_tool.addWidget(self.modify_tenant)
        self.box_tenant_tool.addWidget(self.delete_tenant)
        self.box_manager_tool.addWidget(self.modify_manager)
        self.box_manager_tool.addWidget(self.delete_manager)

        self.main_box.addLayout(self.left_box)
        self.main_box.addLayout(self.right_box)

        self.box_form.addLayout(self.form)
        self.left_box.addLayout(self.box_form)

        self.right_box.addWidget(QLabel("Liste des locataires"))
        self.right_box.addWidget(self.tenant_list)
        self.right_box.addLayout(self.box_tenant_tool)
        self.right_box.addWidget(QLabel("Liste des gerants"))
        self.right_box.addWidget(self.manager_list)
        self.right_box.addLayout(self.box_manager_tool)

        self.form.addWidget(self.info_register, 0, 0, 2, 3)
        self.form.addWidget(self.le_last_name, 2, 0, 2, 3)
        self.form.addWidget(self.le_first_name, 3, 0, 2, 3)
        self.form.addWidget(self.le_location, 4, 0, 2, 3)
        self.form.addWidget(self.le_monthly_amount, 5, 0, 2, 3)
        self.form.addWidget(self.is_manager, 6, 0, 2, 1)
        self.form.addWidget(self.clear_button, 7, 0, 2, 1)
        self.form.addWidget(self.save_button, 7, 1, 2, 2)

        # connexion
        self.is_manager.stateChanged.connect(self.manager_option)
        self.modify_tenant.clicked.connect(self.show_form)
        self.modify_manager.clicked.connect(self.show_form_manager)
        self.delete_tenant.clicked.connect(self.delete_user)
        self.delete_manager.clicked.connect(self.delete_user)
        self.tenant_list.itemClicked.connect(self.get_list_item_text)
        self.manager_list.itemClicked.connect(self.get_list_item_text)

    def manager_option(self):
        if self.is_manager.isChecked():
            self.le_location.setEnabled(False)
            self.le_monthly_amount.setEnabled(False)
        else:
            self.le_location.setEnabled(True)
            self.le_monthly_amount.setEnabled(True)

    def click_save_button(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("Notification")
        try:
            nom = self.le_last_name.text()
            prenom = self.le_first_name.text()
            location = self.le_location.text()
            monthly_amount = self.le_monthly_amount.text()
            if self.is_manager.isChecked():
                user = User(nom, prenom, manager=True)
                user.save()
                self.manager_list.addItem(user.get_name)
            else:
                user = User(nom, prenom, location, int(monthly_amount))
                user.save()
                self.tenant_list.addItem(user.get_name)
            self.le_last_name.clear()
            self.le_first_name.clear()
            self.le_location.clear()
            self.le_monthly_amount.clear()
            message_box.setText("Enregistremenet effectuer")
            message_box.setIcon(QMessageBox.Information)
            message_box.exec_()
        except:
            message_box.setText("Enregistrement non effectuer")
            message_box.setIcon(QMessageBox.Warning)
            message_box.exec_()

    def clear_all(self):
        self.le_last_name.clear()
        self.le_first_name.clear()
        self.le_location.clear()
        self.le_monthly_amount.clear()

    def get_list_item_text(self, item):
        self.get_item = item
        self.get_list_item = item.text()
        return self.get_list_item

    def show_form(self):
        for user in load_users():
            if user.get_name == self.get_list_item:
                if not user.ismanager:
                    self.box = Form(user)
                    self.box.setWindowTitle("Locataire")
                    self.box.show()

    def show_form_manager(self):
        for user in load_users():
            if user.get_name == self.get_list_item:
                if user.ismanager:
                    self.box = FormManager(user)
                    self.box.setWindowTitle("Gerant")
                    self.box.show()

    def delete_user(self):
        for user in load_users():
            if user.get_name == self.get_list_item:
                user.delete()
                if user.ismanager:
                    self.manager_list.takeItem(self.manager_list.row(self.get_item))
                else:
                    self.tenant_list.takeItem(self.tenant_list.row(self.get_item))
                message_box = QMessageBox()
                message_box.setText("Utilisateur Supprimer")
                message_box.setIcon(QMessageBox.Warning)
                message_box.exec_()


class ReceiptWidget(QWidget):
    def __init__(self):
        super().__init__()

        # creation des widgets
        self.tenant_box_list = QComboBox()
        self.manager_box_list = QComboBox()

        # ajout des elements dans manager_box_list et tenant_box_list
        for user in load_users():
            if user.ismanager:
                self.manager_box_list.addItem(user.get_name)
            else:
                self.tenant_box_list.addItem(user.get_name)

        self.tenant_box_list.addItem("")
        self.manager_box_list.addItem("")
        self.delete_button = QPushButton("Supprimer")
        self.tool_box = QHBoxLayout()
        self.month_list = QComboBox()
        self.month_list.addItems(MONTH)
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.l_title = QLabel("Creer un Reçu")
        self.l_title.setAlignment(Qt.AlignCenter)
        self.l_title.setFont(QFont("Roboto", 20))
        self.l_tenant_list = QLabel("Liste des locataires")
        self.l_manager_list = QLabel("Liste des gerants")
        self.l_month = QLabel("Mois soldé")
        self.l_date = QLabel("Date du paiement")
        self.l_advance_amount = QLabel("Montant de l'avance")
        self.advance_amount = QLineEdit()
        self.advance_amount.setPlaceholderText("ex: 45000")
        self.advance_amount.setEnabled(False)
        self.is_advance = QCheckBox("Avance")
        self.is_advance.stateChanged.connect(self.advance_option)
        self.clear_button = QPushButton("Tout effacer")
        self.save_button = QPushButton("Créer")

        self.l_title.setMaximumHeight(30)
        self.tenant_box_list.setMinimumHeight(30)
        self.manager_box_list.setMinimumHeight(30)
        self.date_edit.setMinimumHeight(30)
        self.month_list.setMinimumHeight(30)
        self.advance_amount.setMinimumHeight(30)
        self.save_button.setMinimumHeight(30)
        self.clear_button.setMinimumHeight(30)
        self.delete_button.setMinimumHeight(30)

        # creation des layouts
        self.main_box = QHBoxLayout(self)
        self.left_box = QVBoxLayout()
        self.right_box = QVBoxLayout()
        self.form = QGridLayout()
        self.tenant_box_pdf_list = QListWidget()

        # ajout des widgets aux layouts
        self.main_box.addLayout(self.left_box)
        self.main_box.addLayout(self.right_box)
        self.left_box.addWidget(self.l_title)
        self.left_box.addLayout(self.form)

        self.tool_box.addWidget(self.delete_button)
        self.right_box.addWidget(self.tenant_box_pdf_list)
        self.right_box.addLayout(self.tool_box)

        self.form.addWidget(self.l_tenant_list, 0, 0, 2, 1)
        self.form.addWidget(self.tenant_box_list, 0, 1, 2, 1)
        self.form.addWidget(self.l_month, 1, 0, 2, 1)
        self.form.addWidget(self.month_list, 1, 1, 2, 1)
        self.form.addWidget(self.l_date, 2, 0, 2, 1)
        self.form.addWidget(self.date_edit, 2, 1, 2, 1)
        self.form.addWidget(self.l_manager_list, 3, 0, 2, 1)
        self.form.addWidget(self.manager_box_list, 3, 1, 2, 1)
        self.form.addWidget(self.is_advance, 4, 0, 2, 1)
        self.form.addWidget(self.l_advance_amount, 5, 0, 2, 1)
        self.form.addWidget(self.advance_amount, 5, 1, 2, 1)
        self.form.addWidget(self.clear_button, 6, 0, 2, 1)
        self.form.addWidget(self.save_button, 6, 1, 2, 1)

        # connexion
        self.save_button.clicked.connect(self.create_pdf)
        self.tenant_box_list.currentIndexChanged.connect(self.show_pdf_list)
        self.delete_button.clicked.connect(self.delete_pdf)

    def advance_option(self):
        if self.is_advance.isChecked():
            self.advance_amount.setEnabled(True)
        else:
            self.advance_amount.setEnabled(False)

    def create_pdf(self):
        message_box = QMessageBox()
        try:
            tenant_text = self.tenant_box_list.currentText()
            manager_text = self.manager_box_list.currentText()
            month = self.month_list.currentText()
            date = self.date_edit.text()
            advance_amount = self.advance_amount.text()
            tenant = None
            manager = None
            for user in load_users():
                if user.get_name == manager_text:
                    manager = user
                if user.get_name == tenant_text:
                    tenant = user
            if self.is_advance.isChecked():
                receipt = Receipt(tenant.last_name,
                                  tenant.first_name,
                                  manager.last_name,
                                  manager.first_name,
                                  date,
                                  advance=True)
                receipt.save_advance(tenant.location, int(advance_amount))
            else:
                receipt = Receipt(tenant.last_name,
                                  tenant.first_name,
                                  manager.last_name,
                                  manager.first_name,
                                  date,
                                  advance=False)
                receipt.save_monthly(tenant.location, tenant.monthly_amount, month)
            message_box.setText("Reçu creer")
            message_box.setIcon(QMessageBox.Information)
            message_box.exec_()
        except:
            message_box.setText("Reçu non creer")
            message_box.setIcon(QMessageBox.Warning)
            message_box.exec_()

    def show_pdf_list(self):
        self.tenant_box_pdf_list.clear()
        for elt in load_receipts():
            if elt.get_user == self.tenant_box_list.currentText():
                self.tenant_box_pdf_list.addItem(elt.title_pdf)

    def delete_pdf(self):
        receipt_name = self.tenant_box_pdf_list.currentItem().text()
        for elt in load_receipts():
            if elt.title_pdf == receipt_name:
                elt.delete()
                self.tenant_box_pdf_list.takeItem(self.tenant_box_pdf_list.row(self.tenant_box_pdf_list.currentItem()))
        message_box = QMessageBox(QMessageBox.Warning, "Reçu supprimer")
        message_box.exec_()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tenant Manager")
        f = QFont("Roboto")
        self.setFont(f)

        # Creation des actions associer a l'application
        self.open = QAction("Ouvrir")
        self.quit_app = QAction("Quitter")
        self.open.triggered.connect(open_pdf_doc)
        self.quit_app.triggered.connect(self.close)

        # Creation des actions associer aux utilisateurs
        self.registration = QAction("Enregistrer un utilisateur")

        # Creation des actions associer aux recus
        self.receipt = QAction("Creer un recu")

        # Creation de l'action help
        self.help = QAction("Aide")

        # Definition de Helpwidget comme widget principal
        self.main_widget = RegistrationWidget()
        self.setCentralWidget(self.main_widget)

        # Creation des menus de navigation
        self.menu = self.menuBar()
        self.menu_app = self.menu.addMenu("Menu")
        self.menu_registration = self.menu.addMenu("Utilisateurs")
        self.menu_receipt = self.menu.addMenu("Gerer les reçus")
        self.menu_help = self.menu.addAction(self.help)

        # Ajout des actions aux menu
        self.menu_app.addActions([self.open, self.quit_app])
        self.menu_registration.addActions([self.registration])
        self.menu_receipt.addActions([self.receipt])

        # connection des actions du menu
        self.help.triggered.connect(self.show_help_widget)
        self.registration.triggered.connect(self.show_registration_widget)
        self.receipt.triggered.connect(self.show_receipt_widget)

    # affichage des differents fenetres
    def show_help_widget(self):
        self.main_widget = HelpWidget()
        self.setCentralWidget(self.main_widget)

    def show_registration_widget(self):
        self.main_widget = RegistrationWidget()
        self.setCentralWidget(self.main_widget)

    def show_receipt_widget(self):
        self.main_widget = ReceiptWidget()
        self.setCentralWidget(self.main_widget)


def open_pdf_doc():
    if not os.path.exists(PATH_APP):
        os.makedirs(PATH_APP)
    explore(PATH_APP)
