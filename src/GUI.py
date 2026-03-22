import tkinter as tk
from tkinter.ttk import *
import DB, texToPDF, config
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import parse, time, sendMail, os

def runGUI():
    root = tk.Tk()
    root.title("Lexium")
    root.geometry("800x450")
    Label(root, text="|||| LEXIUM ||||", font =("Courier", 14)).pack(pady=20)
    Label(root, text="Bienvenue sur Lexium, une application conçue pour automatiser l’envoi d’e-mails de \n" \
    "candidature auprès des entreprises. Premiere fois sur l'application ? \nJe vous invite à ouvrir la rubrique instruction.", 
          font =("Courier", 10)).pack(pady=20)


    ####################################################################################################
    # Creation des frames pour avoir d'un coté la partie BDD et de l'autre les boutons actions 
    ####################################################################################################
    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True)
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=0)
    main_frame.columnconfigure(2, weight=1)
    main_frame.rowconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=0)
    left_frame = ttk.Frame(main_frame)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=20)
    separator = ttk.Separator(main_frame, orient="vertical")
    separator.grid(row=0, column=1, sticky="ns", padx=10)
    right_frame = ttk.Frame(main_frame)
    right_frame.grid(row=0, column=2, sticky="nsew", padx=20)


    ####################################################################################################
    # BDD action
    ####################################################################################################

    def windowAddCompany():

        def save_and_close():
            if "@" not in entryEmail.get():
                messagebox.showerror("Erreur", "Email invalide")
                return

            DB.addCompany(
                entryCompany.get(),
                entryEmail.get()
            )
            new_window.destroy()

        new_window = tk.Toplevel(root)
        new_window.title("Lexium")
        new_window.geometry("400x300")

        tk.Label(new_window, text="Nom entreprise :").pack(pady=20)
        entryCompany = tk.Entry(new_window)
        entryCompany.pack()

        tk.Label(new_window, text="email :").pack(pady=20)
        entryEmail = tk.Entry(new_window)
        entryEmail.pack()

        tk.Button(new_window, text="Enregistrer", command=save_and_close).pack(pady=20)

    def windowReadData():

        def refresh():
            new_window.destroy()
            windowReadData()
            
        new_window = tk.Toplevel(root)
        new_window.title("Lexium")
        new_window.geometry("1000x300")

        data = DB.readDB()
        table = ttk.Treeview(new_window)
        table['columns'] = ('companyName', 'email', 'parsedFile' ,'converted', 'emailSent', 'date')
        table.column('#0', width=100, anchor=CENTER)
        table.heading('#0', text='ID')
        for col in table['columns']:
            table.column(col, width=100, anchor=CENTER)
            table.heading(col, text=col.title())
        for item in data:
            table.insert('', 'end', text=item[0], values=item[1:])
        table.pack()

        tk.Button(new_window,text="Rafraichir", command=refresh).pack(pady=20)

    def windowRemoveLine():

        def save_and_close():
            try:
                DB.removeLineInDB(int(id.get()))
                new_window.destroy()
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer un nombre entier")

        new_window = tk.Toplevel(root)
        new_window.title("Lexium")
        new_window.geometry("1000x300")

        tk.Label(new_window, text="ID :").pack(pady=20)
        id = tk.Entry(new_window)
        id.pack()

        tk.Button(new_window, text="Supprimer", command=save_and_close).pack(pady=20)

    def parseGUI():
        # Si les champs sont vides alors je ne fais rien 
        def isConfigComplete():
            cfg = config.loadCurrentConfig()
            required_fields = ["firstName", "lastName", "email", "synchroKeyEmail",]
            for field in required_fields:
                if not cfg[field].strip():
                    return False
            return True

        if os.path.isdir("../LM_ref") and not os.listdir("../LM_ref"):
            messagebox.showerror(title="Erreur", message="Le fichier model.tex est introuvable.")

        elif not isConfigComplete():
            messagebox.showwarning(title="Configuration incomplète", message=("Veuillez renseigner le prénom, le nom, l’adresse mail et la clé de synchronisation "
                    "dans la rubrique Configurations."))

        else:
            parse.copyAndRename()
            time.sleep(2)
            messagebox.showinfo(title="Succès", message=("Les fichiers .tex ont bien été créés.\nVous pouvez les modifier avant de les convertir en PDF."))
    
    def convertToPDF():
        texToPDF.convertTexToPdf()
        messagebox.showinfo(title="Succès", message="Les fichiers .tex ont étaient convertis.")


    def sendEMails():
        if os.path.isdir("../CV") and not os.listdir("../CV"):
            messagebox.showerror(title="Erreur", message="Le fichier CV est introuvable.")

        sendMail.loopCompanies()
        messagebox.showinfo(title="Succès", message="Les mails ont étaient envoyés.")



    tk.Button(left_frame,text="Ajouter une entreprise", command=windowAddCompany, width=25).pack(pady=10)
    tk.Button(left_frame,text="Lire la base de donnée", command=windowReadData, width=25).pack(pady=10)
    tk.Button(left_frame,text="Supprimer l'entreprise", command=windowRemoveLine, width=25).pack(pady=10)

    ####################################################################################################
    # Others action
    ####################################################################################################

    tk.Button(right_frame, text="Parser tous les fichiers", command=parseGUI, width=25).pack(pady=10)
    tk.Button(right_frame, text="Convertir les fichiers en PDF", command=convertToPDF, width=25).pack(pady=10)
    tk.Button(right_frame, text="Envoi de mail", command=sendEMails, width=25).pack(pady=10)
    
    ####################################################################################################
    # Setup
    ####################################################################################################
    
    def windowSetup():
        
        current_config = config.loadCurrentConfig()

        def keep_old_if_empty(new_value, old_value):
            return new_value if new_value.strip() else old_value

        def save_and_close():
            new_firstName = keep_old_if_empty(firstName.get(), current_config["firstName"])
            new_lastName = keep_old_if_empty(lastName.get(), current_config["lastName"])
            new_email = keep_old_if_empty(email.get(), current_config["email"])
            new_synchro = keep_old_if_empty(synchroKeyEmail.get(), current_config["synchroKeyEmail"])
            new_frequency = keep_old_if_empty(frequency.get(), current_config["frequency"])
            new_object = keep_old_if_empty(objectMail.get(), current_config["objectMail"])
            new_text = keep_old_if_empty(textMail.get("1.0", "end-1c"), current_config["textMail"])

            config.setNewConfig(
                new_firstName,
                new_lastName,
                new_email,
                new_synchro,
                new_object,
                new_text,
                new_frequency
            )

            new_window.destroy()

        new_window = tk.Toplevel(root)
        new_window.title("Lexium")
        new_window.geometry("1000x500")

        form = ttk.Frame(new_window, padding=20)
        form.grid(sticky="nsew")

        new_window.columnconfigure(0, weight=1)
        new_window.rowconfigure(0, weight=1)

        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="Prénom :").grid(row=0, column=0, sticky="w", pady=5)
        firstName = ttk.Entry(form)
        firstName.grid(row=1, column=0, sticky="ew", pady=5)
        firstName.insert(0, current_config["firstName"])

        ttk.Label(form, text="Nom :").grid(row=2, column=0, sticky="w", pady=5)
        lastName = ttk.Entry(form)
        lastName.grid(row=3, column=0, sticky="ew", pady=5)
        lastName.insert(0, current_config["lastName"])

        ttk.Label(form, text="Votre adresse mail :").grid(row=0, column=1, sticky="w", pady=5, padx=(20, 0))
        email = ttk.Entry(form)
        email.grid(row=1, column=1, sticky="ew", pady=5, padx=(20, 0))
        email.insert(0, current_config["email"])

        ttk.Label(form, text="Clé de synchronisation email :").grid(row=2, column=1, sticky="w", pady=5, padx=(20, 0))
        synchroKeyEmail = ttk.Entry(form, show="*")
        synchroKeyEmail.grid(row=3, column=1, sticky="ew", pady=5, padx=(20, 0))
        synchroKeyEmail.insert(0, current_config["synchroKeyEmail"])

        ttk.Label(form, text="Fréquence de relance (en jours) :").grid(row=4, column=0, sticky="w", pady=5)
        frequency = ttk.Entry(form)
        frequency.grid(row=5, column=0, sticky="ew", pady=5)
        frequency.insert(0, current_config["frequency"])

        ttk.Label(form, text="Objet du mail :").grid(row=6, column=0, sticky="w", pady=(20, 0))
        objectMail = ttk.Entry(form)
        objectMail.grid(row=7, column=0, sticky="ew", pady=5)
        objectMail.insert(0, current_config["objectMail"])

        ttk.Label(form, text="Corps du mail :").grid(
            row=8, column=0, columnspan=2, sticky="w", pady=(20, 5))

        textMail = tk.Text(form, height=10)
        textMail.grid(row=9, column=0, columnspan=2, sticky="nsew")
        textMail.insert("1.0", current_config["textMail"])

        form.rowconfigure(9, weight=1)

        ttk.Button(form, text="Enregistrer", command=save_and_close).grid(row=10, column=0, columnspan=2, pady=20)
    
    bottom_frame = ttk.Frame(main_frame)
    bottom_frame.grid(
        row=1,
        column=0,
        columnspan=3,
        pady=15
    )
    
    tk.Button(bottom_frame, text="Configurations", command=windowSetup, width=25).pack(pady=10)

    def windowInsctuction():
        new_window = tk.Toplevel(root)
        new_window.title("Lexium")
        new_window.geometry("1000x500")
        Label(new_window, text="|||| LEXIUM ||||", font =("Courier", 14)).pack(pady=20)
        Label(new_window, text="Avant tout chose, pour valider le bon comportement du programme je vous invite a ajouter votre premiere entreprise avec VOTRE adresse mail" \
        "\nceci vous permettra derouler les boutons de la \ncolonne de droite (parse - convert - send) pour verifier le bon fonctionnement." \
        "\n\n1 - Aller dans l'onglet configuration et remplissez les differents champs. \nVeuillez penser à enregistrer afin de valider les champs" \
        "\n\t1.1 - Prenom : Mettez votre prénom" \
        "\n\t1.2 - Nom : Mettez votre nom" \
        "\n\t1.3 - Email : Mettez votre adresse email" \
        "\n\t1.4 - Clé de synchronisation : bite" \
        "\n\t1.4 - Text email : Votre texte que vous voulez dans votre email (le texte apres l'objet)", font =("Courier", 10)).pack(pady=20)

    tk.Button(bottom_frame, text="Instructions", command=windowInsctuction, width=25).pack(pady=10)


    root.mainloop()