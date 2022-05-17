import json
import os.path
from glob import glob
from uuid import uuid4

import win32api
import win32con
from fpdf import FPDF

from package.api.constants import RECEIPT_DIR, PATH_APP_DATA, MONTLY_RECEIPT_DIR, ADVANCE_RECEIPT_DIR


def load_receipts():
    receipts = []
    files = glob(os.path.join(RECEIPT_DIR, "*.json"))
    for file in files:
        with open(file, "r") as f:
            receipt_data = json.load(f)
            receipt_user_tenant_last_name = receipt_data.get("user_tenant_last_name")
            receipt_user_tenant_first_name = receipt_data.get("user_tenant_first_name")
            receipt_user_manager_last_name = receipt_data.get("user_manager_last_name")
            receipt_user_manager_first_name = receipt_data.get("user_manager_first_name")
            receipt_date = receipt_data.get("date")
            receipt_advance = receipt_data.get("advance")
            receipt_title = receipt_data.get("title")
            receipt_title_pdf = receipt_data.get("title_pdf")
            # creation d'un objet recu
            receipt = Receipt(receipt_user_tenant_last_name,
                              receipt_user_tenant_first_name,
                              receipt_user_manager_last_name,
                              receipt_user_manager_first_name,
                              receipt_date,
                              receipt_title_pdf,
                              receipt_title,
                              receipt_advance)
            # ajout de l'objet a la liste de recu
            receipts.append(receipt)
    return receipts


def search_receipt():
    pass


class Receipt:
    def __init__(self,
                 user_tenant_last_name,
                 user_tenant_first_name,
                 user_manager_last_name,
                 user_manager_first_name,
                 date,
                 title_pdf=None,
                 title=None,
                 advance=False):
        self.user_tenant_last_name = user_tenant_last_name
        self.user_tenant_first_name = user_tenant_first_name
        self.user_manager_last_name = user_manager_last_name
        self.user_manager_first_name = user_manager_first_name
        self.date = date
        self.advance = advance
        if title is None:
            self.title = str(uuid4())
        else:
            self.title = title
        if title_pdf is None:
            self.title_pdf = None
        else:
            self.title_pdf = title_pdf

    def __str__(self):
        return f"{self.user_tenant_last_name}_{self.user_tenant_first_name}_{self.date}"

    def __repr__(self):
        return f"{self.user_tenant_last_name}_{self.user_tenant_first_name}_{self.date}_{self.title}"

    def delete(self):
        os.remove(self.path)
        if self.advance:
            os.remove(os.path.join(ADVANCE_RECEIPT_DIR, f"{self.title_pdf}"))
        else:
            os.remove(os.path.join(MONTLY_RECEIPT_DIR, f"{self.title_pdf}"))
        if os.path.exists(self.path):
            return False
        return True

    @property
    def get_user(self):
        return f"{self.user_tenant_last_name} {self.user_tenant_first_name}"

    @property
    def path(self):
        return os.path.join(RECEIPT_DIR, f"{self.title}.json")

    def save_advance(self, location, amount):
        titre_doc = f"A_{self.user_tenant_last_name}_{self.user_tenant_first_name}.pdf"
        load_receipts()
        for receipt in load_receipts():
            if receipt.title_pdf == titre_doc:
                raise "receipt exist"

        if not os.path.exists(RECEIPT_DIR):
            os.makedirs(RECEIPT_DIR)
            win32api.SetFileAttributes(PATH_APP_DATA, win32con.FILE_ATTRIBUTE_HIDDEN)

        ligne_nom = "Nom complet du locataire: " + self.user_tenant_last_name + " " + self.user_tenant_first_name
        ligne_somme = "La Somme versée: " + str(amount)
        ligne_mois = "Pour avance avant amenagement des lieux"
        ligne_quartier = "Maison sise à: " + location
        ligne_date = "Date: " + self.date
        ligne_controleur = self.user_manager_last_name + " " + self.user_manager_first_name
        pdf = FPDF('L', 'mm', 'Legal')
        pdf.add_page()
        pdf.set_font('Times', 'B', 50)
        pdf.cell(325, 30, 'Recu Avance de loyer', "", 1, 'C')
        pdf.set_font('Courier', '', 25)
        pdf.cell(300, 20, ligne_nom, 0, 1)
        pdf.cell(300, 20, ligne_somme, 0, 1)
        pdf.cell(300, 20, ligne_mois, 0, 1)
        pdf.cell(300, 20, ligne_quartier, 0, 1)
        pdf.cell(300, 20, ligne_date, 0, 1)
        pdf.cell(300, 20, 'Nom et signature du Gerant:', 0, 1)
        pdf.cell(300, 35, ligne_controleur, 0, 1, 'R')
        if not os.path.exists(ADVANCE_RECEIPT_DIR):
            os.makedirs(ADVANCE_RECEIPT_DIR)
        pdf.output(os.path.join(ADVANCE_RECEIPT_DIR, f"{titre_doc}"))

        data = {"user_tenant_last_name": self.user_tenant_last_name,
                "user_tenant_first_name": self.user_tenant_first_name,
                "user_manager_last_name": self.user_manager_last_name,
                "user_manager_first_name": self.user_manager_first_name,
                "date": self.date,
                "advance": True,
                "title": self.title,
                "title_pdf": titre_doc}
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

    def save_monthly(self, location, monthly_amount, month):
        titre_doc = f"M_{self.user_tenant_last_name}_{self.user_tenant_first_name}_{month}.pdf"
        # verifie si l'occurence existe deja
        load_receipts()
        for receipt in load_receipts():
            if receipt.title_pdf == titre_doc:
                raise "receipt exist"
        if not os.path.exists(RECEIPT_DIR):
            os.makedirs(RECEIPT_DIR)
            win32api.SetFileAttributes(PATH_APP_DATA, win32con.FILE_ATTRIBUTE_HIDDEN)

        ligne_nom = "Nom complet du locataire: " + self.user_tenant_last_name + " " + self.user_tenant_first_name
        ligne_somme = "La Somme versée: " + str(monthly_amount)
        ligne_mois = "Pour le loyer du mois de: " + month
        ligne_quartier = "Maison sise à: " + location
        ligne_date = "Date: " + self.date
        ligne_controleur = self.user_manager_last_name + " " + self.user_manager_first_name
        pdf = FPDF('L', 'mm', 'Legal')
        pdf.add_page()
        pdf.set_font('Times', 'B', 50)
        pdf.cell(325, 30, 'Recu Mensuel de loyer', "", 1, 'C')
        pdf.set_font('Courier', '', 25)
        pdf.cell(300, 20, ligne_nom, 0, 1)
        pdf.cell(300, 20, ligne_somme, 0, 1)
        pdf.cell(300, 20, ligne_mois, 0, 1)
        pdf.cell(300, 20, ligne_quartier, 0, 1)
        pdf.cell(300, 20, ligne_date, 0, 1)
        pdf.cell(300, 20, 'Nom et signature du Gerant:', 0, 1)
        pdf.cell(300, 35, ligne_controleur, 0, 1, 'R')
        if not os.path.exists(MONTLY_RECEIPT_DIR):
            os.makedirs(MONTLY_RECEIPT_DIR)
        pdf.output(os.path.join(MONTLY_RECEIPT_DIR, f"{titre_doc}"))

        data = {"user_tenant_last_name": self.user_tenant_last_name,
                "user_tenant_first_name": self.user_tenant_first_name,
                "user_manager_last_name": self.user_manager_last_name,
                "user_manager_first_name": self.user_manager_first_name,
                "date": self.date,
                "advance": self.advance,
                "title": self.title,
                "title_pdf": titre_doc}
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)


if __name__ == '__main__':
    r = Receipt("B", "A", "U", "V", "20/10/15", advance=True)
    r.save_advance("Cala", 20000)
