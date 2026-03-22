# popups.py

from tkinter import messagebox


def confirm_send_without_lm(company_name: str) -> bool:
    return messagebox.askyesno(
        "Lettre de motivation manquante",
        f"Aucune lettre de motivation trouvée pour {company_name}.\n\n"
        "Souhaitez-vous envoyer le mail sans lettre de motivation ?"
    )

def confirm_send_all_without_lm() -> bool:
    return messagebox.askyesno(
        "Aucune lettre de motivation",
        f"Aucune lettre de motivation trouvée.\n\n"
        "Souhaitez-vous envoyer les mails sans lettre de motivation ?"
    )