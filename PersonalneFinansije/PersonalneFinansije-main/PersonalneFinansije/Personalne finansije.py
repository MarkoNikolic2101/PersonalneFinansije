import sqlite3
import webbrowser
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from typing import Tuple

import matplotlib.cbook
import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageTk
from tkinter import filedialog
import warnings
from tooltips import CreateToolTip
from Autocomplete import AutocompleteCombobox
warnings.filterwarnings("ignore", category=matplotlib.cbook.
                        MatplotlibDeprecationWarning)
import random
import pandas
from sqlite3 import OperationalError
import time
from matplotlib import MatplotlibDeprecationWarning


class Diplomski():

    """Program Personalne finansije koji omogucava korisniku da se registruje
    da bi napravio svoj akaunt pomocu koga moze da se loguje i da unose
    vrednosti za prihod i rashod i da kad god se loguje pokazuje mu unete
    vrednosti i moze da radi upite sa kojima moze da prati troskove i prihode.
    Moze da menja, brise vrednosti iz tabele u kojima su mu prikazani vrednosti
    koje je unosio.
    Ima opciju da eksportuje vrednosti iz tabele ali prvo mora izabrati tabelu!"""

    def meni(self):

        #
        # Prozor meni koji korisniku omogucava da izabere izmedju tri dugmeta
        # Prvo dugme login da se loguje
        # Drugo dugme registracija da napravi svoj akaunt
        # Trece dugme izlaz da izadje iz programa
        #
        self.wind = Tk()
        self.wind.title("Upravljanje troskovima")
        self.wind.geometry("350x400")
        self.wind.wm_iconbitmap('slike/emblem-money-2.ico')

        frame = Frame(self.wind)
        # Label Login i registracija naslov prozora
        self.label1 = Label(frame, text="Login i registracija", fg="white",
                            font="times 25", background="#1d5eb8")
        self.label1.grid(row=0, column=0, pady=20)
        # Dugme koje nas vodi u prozor login
        self.btn1 = Button(frame, text="Login", width=20, bg="white", height=3,
                           fg="#1d5eb8", bd=5, command=self.login,
                           font="arial 11 bold ")
        self.btn1.grid(row=1, column=0, pady=20)
        CreateToolTip(self.btn1, "Pretisni dugme da se logujes")
        # Dugme koje nas vodi u prozor registracija
        self.btn2 = Button(frame, text="Registracija", bg="white", width=20,
                           fg="#1d5eb8", height=3, bd=5,
                           command=self.registracija,
                           font="arial 11 bold")

        self.btn2.grid(row=2, column=0, pady=20)
        # Funckija tooltips koja ispisuje oblacic sa porukom
        CreateToolTip(self.btn2, "Pretisni dugme da se registrujes")
        #Dugme koje nam omogucava da izadjemo iz programa
        self.btn3 = Button(frame, text="Izlaz", bg="white", width=20,
                           fg="#1d5eb8", height=3, bd=5,
                           command=self.wind.destroy,
                           font="arial 11 bold")
        self.btn3.grid(row=3, column=0)
        CreateToolTip(self.btn3, "Pretisni dugme da napustis program")
        frame.config(bg="#1d5eb8")
        frame.pack()
        self.wind.config(bg="#1d5eb8")
        self.wind.mainloop()

    def about(self):
        #
        #Funkcija koja otvara prozor koji nam pokazuje ko je radio program
        # i za koga tj koja skola je u pitanju
        #

        self.newTop = Toplevel()
        self.newTop.title("About")
        self.newTop.geometry("400x300")
        self.newTop.wm_iconbitmap('slike/emblem-money-2.ico')
        self.my_img = ImageTk.PhotoImage(file="slike/Skola.png")
        Label(self.newTop, text="Diplomski rad",bg="#2b306e",fg="white", font="times 20").grid(row=0,
                                                                       column=0,
                                                                       pady=20)
        Label(self.newTop, text="Student:  Marko Nikolic ",
              font="times 20",bg="#2b306e",fg="white").grid(row=1, column=0, pady=20)
        Label(self.newTop, text="Skola : ", font="times 20",fg="white",bg="#2b306e").grid(row=2,
                                                                  column=0,
                                                                  sticky=W)
        # Dugme koje nas vodi na sajt skole
        self.bt = Button(self.newTop, image=self.my_img,bg="white",
                         command=lambda: self.callback(
                             "https://vsar.edu.rs/")).grid(
            row=2, column=0, sticky=E)
        self.newTop.configure(bg="#2b306e")
        self.newTop.mainloop()

    def registracija(self):
        #
        # Prozor registracija koja nam omogucava da napravimo svoj akaunt
        #
        self.registracija_window = Toplevel()
        self.registracija_window.title("Registracija")
        self.registracija_window.geometry("450x200")
        self.registracija_window.wm_iconbitmap('slike/emblem-money-2.ico')

        self.frame2 = Frame(self.registracija_window)
        self.label1 = Label(self.frame2, text="Korisnicko ime:", fg="white",
                            font="times 15", background="#1d5eb8")
        self.label1.grid(row=1, column=1)

        self.label2 = Label(self.frame2, text="Lozinka: ", fg="white",
                            font="times 15", background="#1d5eb8")
        self.label2.grid(row=3, column=1)

        self.name_text = StringVar()
        self.ent1 = Entry(self.frame2, textvariable=self.name_text, bg="white",
                          fg="black", bd=5, font='times')
        self.ent1.grid(row=1, column=2, pady=10)
        CreateToolTip(self.ent1, "Unesi korisnicko ime")
        # Promenljiva ispod znaci da vrednosti koju unosimo
        # ce biti tumacen kao string
        self.password_text = StringVar()
        self.ent2 = Entry(self.frame2, textvariable=self.password_text,
                          bg="white", fg="black", show="*", bd=5, font='times')
        self.ent2.grid(row=3, column=2, pady=10, padx=10)
        CreateToolTip(self.ent2, "Unesi lozinku")
        self.btn1 = Button(self.frame2, text="Kreiraj", bg="white", width=10,
                           fg="#1d5eb8", height=2, bd=5, font='arial 11 bold',
                           command=self.registracija_baza)
        self.btn1.grid(row=4, column=2)
        CreateToolTip(self.btn1, "Pretisni dugme da se registrujes")
        # Ucitavamo slike pomocu modula pillow da bi ih prikazali na dugmetu
        self.my_img1 = ImageTk.PhotoImage(file="slike/show_50x50.png")
        self.my_img2 = ImageTk.PhotoImage(file="slike/noshow_50x50.png")
        # Dugme koje nam skriva ili prikazuje vrednosti lozinke
        self.dugmeregistracija = Button(self.frame2, text="",
                                        image=self.my_img2,
                                        command=self.prikazivanje_lozinke,
                                        height=35, width=40)
        self.dugmeregistracija.grid(row=3, column=3)

        self.frame2.configure(background="#1d5eb8")
        self.frame2.pack()
        #konfigurisemo boju prozora
        self.registracija_window.configure(background="#1d5eb8")
        #zatvaramo prozor registracije
        self.registracija_window.mainloop()

    def prikazivanje_lozinke(self):
        #funkcija za prikazavivanje ili ne lozinke u prozoru registracija
        if self.ent2.cget('show') == '':
            self.ent2.config(show="*")
            self.dugmeregistracija.config(image=self.my_img2)
        else:
            self.ent2.config(show="")
            self.dugmeregistracija.config(image=self.my_img1)

    def prikazivanje_lozinke2(self):
        # funkcija za prikazavivanje ili ne lozinke u prozoru login
        if self.ent2.cget('show') == '':
            self.ent2.config(show="*")
            self.dugmelogin.config(image=self.my_img4)
        else:
            self.ent2.config(show="")
            self.dugmelogin.config(image=self.my_img3)

    def validreg(self):
        # funkcija koja kaze da mora da se unese neka vrednost u polje za unos
        # u prozoru registracije i logina
        return len(self.name_text.get()) != 0 and len(
            self.password_text.get()) != 0

    def save(self):
        f = filedialog.asksaveasfile(initialfile='Untitled.txt',
                                     defaultextension=".txt",
                                     filetypes=[("All Files", "*.*"),
                                                ("Text Documents", "*.txt")])
        f.write()

    def login(self):
        #
        # Prozor login koji nam omogucava ako se dobro ulogujemo da nas odvede
        # u drugi delove aplikacije ili programa
        #
        self.login_window = Toplevel()
        self.login_window.geometry("450x200")
        self.login_window.wm_iconbitmap('slike/emblem-money-2.ico')
        self.frame3 = Frame(self.login_window)
        self.label1 = Label(self.frame3, text="Korisnicko ime:", fg="white",
                            font="times 20", background="#1d5eb8")
        self.label1.grid(row=1, column=1, pady=10)
        self.label2 = Label(self.frame3, text="Lozinka:", fg="white",
                            font="times 20", background="#1d5eb8")
        self.label2.grid(row=2, column=1, pady=10)
        self.label3 = Label(self.frame3, font="times 20")
        self.label3.grid(row=5, column=2, pady=10)

        self.name_text = StringVar()
        self.ent1 = Entry(self.frame3, textvariable=self.name_text, bd=5,
                          font='times')
        self.ent1.grid(row=1, column=2, pady=10)
        self.password_text = StringVar()
        CreateToolTip(self.ent1, "Unesi korisnicko ime")
        self.ent2 = Entry(self.frame3, textvariable=self.password_text,
                          show="*", bd=5, font='times')
        self.ent2.grid(row=2, column=2, pady=10, padx=10)
        CreateToolTip(self.ent2, "Unesi lozinku")
        self.btn1 = Button(self.frame3, text="login", bg="white", fg="#1d5eb8",
                           font="arial 11 bold", width=10, height=2,
                           command=self.login_baza, bd=5)
        self.btn1.grid(row=4, column=2, pady=10)
        CreateToolTip(self.btn1, "Pretisni dugme da se ulogujes")
        self.my_img3 = ImageTk.PhotoImage(file="slike/show_50x50.png")
        self.my_img4 = ImageTk.PhotoImage(file="slike/noshow_50x50.png")
        self.dugmelogin = Button(self.frame3, text="", image=self.my_img4,
                                 command=self.prikazivanje_lozinke2, width=40,
                                 height=35)
        self.dugmelogin.grid(row=2, column=3)

        self.frame3.configure(background="#1d5eb8")
        self.frame3.pack()
        self.login_window.configure(background="#1d5eb8")
        self.login_window.title("Login")
        self.login_window.mainloop()

    def login_baza(self):
        #
        # Funkcija koja omogucava da proveri da li smo se dobro ulogovali
        # i ucitava nam nas akaunt i vrednost iz njega prikazuje
        #
        ime_baze = self.ent1.get()
        conn = sqlite3.connect("account.db")
        cur = conn.cursor()
        # Upit koji nam pokazuje da li smo uneli dobro korisnicko ime i lozinku
        cur.execute("SELECT * FROM user WHERE name=? AND password=?",
                    (self.ent1.get(), self.ent2.get()))
        row = cur.fetchall()
        conn.close()
        # Ako se prvi put logujemo pravi se tabele sa njenim kolonima
        if row:
            self.login_window.destroy()
            conn = sqlite3.connect(ime_baze + ".db")
            c = conn.cursor()

            c.execute(
                'CREATE TABLE IF NOT EXISTS rashod'
                ' (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,datum DATE,'
                'ime TEXT,kategorija TEXT,podkategorija TEXT,'
                'vrstatransakcije TEXT,vrstaplacanja TEXT,primaoc TEXT,'
                'kontakt TEXT,iznos REAL )')

            c.execute(
                'CREATE TABLE IF NOT EXISTS prihod'
                ' (id   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
                'datum DATE,ime TEXT,kategorija TEXT,podkategorija TEXT,'
                'vrstatransakcije TEXT,vrstaplacanja TEXT,platioc TEXT,'
                'kontakt TEXT,iznos REAL )')
            # kad se ulogujemo ucitava se tab meni  izlazi iz svih prozora login
            self.db_name = (ime_baze + ".db")
            self.ime_korisnika = ime_baze
            self.wind.destroy()
            self.main()
            return self.db_name
        else:
            self.login_window.destroy()
            # ako logovanje nije dobro izlazi greska
            messagebox.showerror(title="Greska",
                                 message="Akaunt ne postoji!!!",icon="error")

    def registracija_baza(self):
        conn = sqlite3.connect("account.db")
        cur = conn.cursor()
        # Kad se registrujemo u bazi se upisuju korisnicko ime i lozinka korisnika
        cur.execute(
            "CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY,name text, password text)")
        if self.validreg():
            cur.execute("INSERT INTO user Values(Null,?,?)",
                        (self.ent1.get(), self.ent2.get()))
            self.ent1.delete(0, END)
            self.ent2.delete(0, END)
            conn.commit()
            conn.close()
            messagebox.showinfo(title="Info",
                                message="Uspesno si se registrovao!!!",
                                icon="info")
        else:
            messagebox.showerror(title="Greska ",
                                 message="Ne moze biti prazno polje!!!")

    def about1(self):
        self.newTop = Toplevel()
        self.newTop.title("About")
        self.newTop.geometry("400x300")
        self.newTop.wm_iconbitmap('slike/emblem-money-2.ico')
        self.my_img = ImageTk.PhotoImage(file="slike/Skola.png")
        Label(self.newTop, text="Diplomski rad", font="times 20").grid(row=0,
                                                                       column=0,
                                                                       pady=20)
        Label(self.newTop, text="Student:  Marko Nikolic ",
              font="times 20").grid(row=1, column=0, pady=20)
        Label(self.newTop, text="Skola : ", font="times 20").grid(row=2,
                                                                  column=0,
                                                                  sticky=W)
        self.bt = Button(self.newTop, image=self.my_img,
                         command=lambda: self.callback(
                             "https://vsar.edu.rs/")).grid(
            row=2, column=0, sticky=E)
        self.newTop.mainloop()

    def callback(self, url):
        webbrowser.open(url)

    def exit(self):
        #funkcija koja nam omogucava da izadjemo iz programa
        self.wind2.destroy()
        try:
            self.dodaj_prozor.destroy()
        except AttributeError:
            pass


    def open_excel(self):
        filedialog.askopenfilename()

    def main(self):
        #
        #Tab meni koja nam omogucava da unosimo,menjamo,brisemo i eksportujemo
        # vrednosti iz tabele, da preko upita vidimo kako i na sta trosimo.

        #
        self.wind2 = Tk()
        self.wind2.title("Upravljanje troskovima")
        # Sirina i visina prozora
        self.wind2.geometry("1025x675")
        # Ikonica koja stoji u gornjem levom uglu
        self.wind2.wm_iconbitmap('slike/emblem-money-2.ico')
        # Pravljenje menubara
        self.menubar = Menu(self.wind2)
        self.wind2.config(menu=self.menubar)
        self.subMenu = Menu(self.menubar, tearoff=0)
        # Menu izlaz koji omogucava da izadje iz programa
        self.menubar.add_cascade(label="Izlaz", menu=self.subMenu)
        self.subMenu.add_command(label="Izlaz", command=self.exit)
        # Menu info koji ima svoju podmenu about koji prikazuje prozor koja nam
        # pokazuje ko je radio kod i za koju namenu
        self.subMenuHelp = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Info", menu=self.subMenuHelp)
        self.subMenuHelp.add_command(label="About", command=self.about)
        # Pravljenje Notebook-a neke vrste sveske koja ima svoje tabove ili
        # listove na kojima se nalaze razlicite stvari
        self.tab_control = ttk.Notebook(self.wind2)
        # pravljanje listova i stavljanje boje
        self.tab1 = Frame(self.tab_control, bg="#2b306e")
        self.tab2 = Frame(self.tab_control, bg="#2b306e")
        self.tab3 = Frame(self.tab_control, bg="#2b306e")
        self.tab4 = Frame(self.tab_control, bg="#2b306e")
        self.tab5 = Frame(self.tab_control, bg="#2b306e")

        self.tab1.pack(expand=1, fill="both")
        self.tab2.pack(expand=1, fill="both")
        self.tab3.pack(expand=1, fill="both")
        self.tab4.pack(expand=1, fill="both")
        self.tab5.pack(expand=1, fill="both")
        # Nazivi listova
        self.tab_control.add(self.tab1, text="Meni")
        self.tab_control.add(self.tab2, text="Upiti1")
        self.tab_control.add(self.tab3, text="Upiti2")
        self.tab_control.add(self.tab4, text="Upiti3")
        self.tab_control.add(self.tab5, text="Upiti4")
        self.tab_control.pack(expand=1, fill="both")

        self.slika_dugme = ImageTk.PhotoImage(
            file="slike/crveno dugme_40x40.jpg")
        # pravljenje reklame label koji prikazuje tekst u vrhu ekrana
        self.reklama = "Aplikacija 'Personalne finansije'"
        self.brojac = 0
        self.text = ""
        self.label_reklama = Label(self.tab1, text=self.reklama,
                                   font=('times', 25, 'italic bold'),
                                   relief=RIDGE, borderwidth=4, width=30,
                                   bg="#3482b3")
        self.label_reklama.grid(row=0, column=1, columnspan=4, pady=10)
        self.reklama_funkcija()
        self.reklama_boje()
        # Pravljaenje promenljivi koji imaju slike koje ce se dodavati na dugmice
        self.dugme_promena = ImageTk.PhotoImage(
            file="slike/dugme-promena 50.png")
        self.dugme_delete = ImageTk.PhotoImage(file="slike/dugme-delete.png")
        self.dugme_add = ImageTk.PhotoImage(file="slike/dugme-add.png")
        self.dugme_csv = ImageTk.PhotoImage(file="slike/dugme-csv.png")
        self.dugme_facebook = ImageTk.PhotoImage(
            file="slike/facebook-icon.png")
        self.dugme_twiter = ImageTk.PhotoImage(file="slike/twitter-icon.png")
        self.dugme_instagram = ImageTk.PhotoImage(
            file="slike/instagram-icon.png")
        self.dugme_youtube = ImageTk.PhotoImage(file="slike/youtube-icon.png")
        #Dugmici za  dodavanje , menjanje , brisanje i eksportovanje vrednosti
        self.dugme_dodavanje = Button(self.tab1, text="Dodaj vrednost", command=self.dodaj,
               font=('times', 15, 'bold'), bd=6,
               activebackground="#EF6C33", relief=RIDGE,
               activeforeground='white', image=self.dugme_add)
        self.dugme_dodavanje.grid(row=2,column=0,pady=5,sticky=W,padx=50)

        CreateToolTip(self.dugme_dodavanje,"Klikni dugme da udjes u prozor u kojem mozes dodavati vrednosti")
        self.dugme_menjanje = Button(self.tab1, text="Promeni vrednost",
               command=self.promeni_vrednosti,
               font=('times', 15, 'bold'), bd=6,
               activebackground="#EF6C33", relief=RIDGE,
               activeforeground='white', image=self.dugme_promena)
        self.dugme_menjanje.grid(row=3,column=0,pady=5,sticky=W,padx=50)

        CreateToolTip(self.dugme_menjanje,"Klikni dugme da promenis odredjenu vrednosti iz tabele")
        self.dugme_uklanjanje= Button(self.tab1, text="Ukloni vrednost",
               command=self.izbrisi_vrednosti,
               font=('times', 15, 'bold'), bd=6,
               activebackground="#EF6C33", relief=RIDGE,
               activeforeground='white', image=self.dugme_delete)
        self.dugme_uklanjanje.grid(row=4,column=0,pady=5,sticky=W,padx=50)
        CreateToolTip(self.dugme_uklanjanje,"Klikni dugme da izbrises vrednosti iz tabele")

        self.dugme_eksport = Button(self.tab1, text="Exportuj vrednosti",
               command=self.export_csv_file,
               font=('times', 15, 'bold'), bd=6,
               activebackground="#EF6C33", relief=RIDGE,
               activeforeground='white', image=self.dugme_csv)
        self.dugme_eksport.grid(row=5,column=0,pady=5,sticky=W,padx=50)
        CreateToolTip(self.dugme_eksport,"Klikni na dugme da eksportujes vrednosti iz tabele")
        # Dugmici za facebook,tviter,instagram i youtube
        self.fejsbuk = Button(self.tab1, image=self.dugme_facebook,command=lambda: self.callback(
                             "https://www.facebook.com/"))
        self.fejsbuk.grid(row=2, column=8,padx=50)
        CreateToolTip(self.fejsbuk,"Klikni dugme da se otvori fejsbuk u veb pretrazivacu")
        self.tviter = Button(self.tab1, image=self.dugme_twiter,command=lambda: self.callback(
                             "https://twitter.com/"))
        self.tviter.grid(row=3, column=8,padx=50)
        CreateToolTip(self.tviter,"Klikni dugme da se otvori tviter u veb pretrazivacu")
        self.instagram = Button(self.tab1, image=self.dugme_instagram,command=lambda: self.callback(
                             "https://www.instagram.com/accounts/login/"))
        self.instagram.grid(row=4, column=8,padx=50)
        CreateToolTip(self.instagram,"Klikni dugme da se otvori instagram u veb pretrazivacu")
        self.youtube = Button(self.tab1, image=self.dugme_youtube,command=lambda: self.callback(
                             "https://www.youtube.com/"))
        self.youtube.grid(row=5, column=8,padx=50)
        CreateToolTip(self.youtube,"Klikni dugme da se otvori youtube u veb pretrazicacu")
        # Label  koji prikazuje ukupan prihod
        Label(self.tab1, text="Ukupan prihod:", fg="#05ff3f", bg="#2b306e",
              font="Arial 15 bold").grid(row=6, column=1,
                                         padx=40)
        self.label_prihod = Label(self.tab1, text="", fg="#05ff3f",
                                  bg="#2b306e", font="Arial 15 bold")
        self.label_prihod.grid(row=6, column=1, pady=10, sticky=E)
        # Label koji prikazuje ukupan rashod
        Label(self.tab1, text="Ukupan rashod:", fg="orange", bg="#2b306e",
              font="Arial 15 bold").grid(row=7, column=1,
                                         padx=40)
        self.label_rashod = Label(self.tab1, text="", fg="orange",
                                  bg="#2b306e", font="Arial 15 bold")
        self.label_rashod.grid(row=7, column=1, pady=10, sticky=E)
        # Label za deficit i suficit
        self.suficit_deficit = Label(self.tab1, text="", fg='white',
                                     bg="#2b306e", font="Arial 15 bold")
        self.suficit_deficit.grid(row=8, column=1, sticky=E, pady=10)

        Label(self.tab1, text="Tabela:", fg="white", bg="#2b306e",
              font="Arial 15 bold").grid(row=1, column=1, sticky=W)
        opcije = "Tabela Rashod", "Tabela Prihod"
        # Kombobox koju nudi opcije da se bira cije vrednosti tabele zelimo
        # da vidimo u tabeli na ekranu
        self.opcija3 = ttk.Combobox(self.tab1, state='readonly', value=opcije)
        self.opcija3.grid(row=1, column=1)
        Button(self.tab1, command=self.prikaz_tabela,
               image=self.slika_dugme).grid(row=1, column=1, sticky=E)
        # Pravljenje stila za izgleda tabele prikazane na ekranu
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure('Treeview', font=('times', 12,),
                             background='cyan', foreground='black')
        self.style.configure('Treeview.Heading', font=('times', 12, 'bold'),
                             foreground='black')
        self.style.configure("Mystyle.Treeview", foreground="white",
                             background="#c9b387", fieldbackground="silver",
                             rowheight=25)
        self.style.map("Mystyle.Treeview", background=[("selected", "green")])
        # Pravljenje tabele u kojoj ce biti prikazane vrednosti iz tabela
        self.tree = ttk.Treeview(self.tab1)
        self.tree.configure(style="Mystyle.Treeview")

        self.tree["columns"] = (
            "#0", "#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9")
        self.tree.grid(row=2, column=1, columnspan=3, rowspan=4,
                       sticky=S + W + E + N)

        self.treescrollbar = ttk.Scrollbar(self.tab1, orient="vertical",
                                           command=self.tree.yview)

        self.scrollbarhoriz = ttk.Scrollbar(self.tab1, orient="horizontal",
                                            command=self.tree.xview)
        self.scrollbarhoriz.grid(row=2, column=1, columnspan=3, rowspan=4,
                                 sticky=W + S + E)

        self.treescrollbar.grid(row=2, column=4, columnspan=3, rowspan=4,
                                sticky=S + E + N)
        self.tree.configure(yscrollcommand=self.treescrollbar.set,
                            xscrollcommand=self.scrollbarhoriz.set)
        # postavljanje pozadine boja u tabeli
        self.tree.tag_configure('oddrow', background="#3482b3")
        self.tree.tag_configure('evenrow', background="white")
        # Numerisanje duzina kolone u tabeli
        self.tree.column("#0", width=5, minwidth=10)
        self.tree.column("#1", width=50, minwidth=100)
        self.tree.column("#2", width=50, minwidth=100)
        self.tree.column("#3", width=50, minwidth=100)
        self.tree.column("#4", width=50, minwidth=100)
        self.tree.column("#5", width=50, minwidth=100)
        self.tree.column("#6", width=50, minwidth=100)
        self.tree.column("#7", width=50, minwidth=100)
        self.tree.column("#8", width=50, minwidth=100)
        self.tree.column("#9", width=50, minwidth=100)
        # davanje imena kolonama u tabeli
        self.tree.heading('#0', text='')
        self.tree.heading('#1', text='Datum')
        self.tree.heading("#2", text='Ime')
        self.tree.heading("#3", text="Kategorija")
        self.tree.heading("#4", text="Pod kategorija")
        self.tree.heading("#5", text="Vrsta transakcije")
        self.tree.heading("#6", text="Vrsta placanja")
        self.tree.heading("#7", text="Primaoc vrednosti")
        self.tree.heading("#8", text="Kontakt")
        self.tree.heading("#9", text="Iznos")
        self.tree["displaycolumns"] = (
            "#0", "#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9")

        # funkcija koja prikazuje vrednosti za prihod,rashod i suficit/deficit
        self.live_prikaz()


        """
        U narednim tabovima su prikazani upiti koji nam pokazuje vrednosti u
        zavisnosti od toga koje su vrednosti unete u tabeli
        U zavisnosti od izabrane tabele ,opcije i vrednosti ce biti prikazani 
        graficki ,u tabeli iii listboxu vrednosti upita ce biti prikazani
        """
        # Labeli za upite
        Label(self.tab2, font=15, bg="#2b306e", fg="white",
              text="Izaberi opciju i vidi njen procenat").grid(row=1, column=1,
                                                               pady=20)
        Label(self.tab2, font=15, bg="#2b306e", fg="white",
              text="Izaberi mesec opciju i vidi procenat vrednosti za taj mesec").grid(
            row=2, column=1,
            pady=20)
        Label(self.tab2, font=15, bg="#2b306e", fg="white",
              text="Izaberi opciju i vrednost te opcije da vidis "
                   "vrednosti i sortirane po datumima").grid(
            row=3, column=1, pady=5)
        Label(self.tab2, font=15, bg="#2b306e", fg="white",
              text="Izaberi opciju i njene vrednosti i "
                   "vidi ukupnu i prosek iznosa po mesecu").grid(
            row=4,
            column=1,
            pady=20)
        Label(self.tab2, font=15, bg="#2b306e", fg="white",
              text="Ukucaj godinu,izaberi opciju i unesi ili"
                   " izaberi vrednost da vidis\n prosecan i ukupan"
                   "  iznos po mesecu za zadatu godinu").grid(
            row=5, column=1, pady=20)
        ras_pri = "Rashod", "Prihod"
        # Opcija u kojoj biramo za koju tabelu zelimo da vidimo upit
        self.opcija_prihod_rashod = ttk.Combobox(self.tab2, value=ras_pri,
                                                 state='readonly', width=8)
        self.opcija_prihod_rashod.current(newindex=0)
        self.opcija_prihod_rashod.grid(row=1, column=0, pady=5, padx=5)
        CreateToolTip(self.opcija_prihod_rashod, "Izaberi tabelu")
        # opcija koju biramo i onda na osnovu nje biramo ili unosimo vrednost
        self.upit_opcija1 = ttk.Combobox(self.tab2, width=15, state='readonly')
        # opcija ima default vrednosti
        self.upit_opcija1[
            'value'] = "Kategorija", "Vrsta Transakcije", "Vrsta placanja", "Primaoc/Platioc"
        self.upit_opcija1.grid(row=1, column=2, pady=5)
        CreateToolTip(self.upit_opcija1, "Izaberi opciju")
        Button(self.tab2, text="Potvrdi", command=self.upit1,
               image=self.slika_dugme).grid(row=1, column=3, pady=5)
        self.opcija_prihod_rashod1 = ttk.Combobox(self.tab2, value=ras_pri,
                                                  state='readonly', width=8)
        self.opcija_prihod_rashod1.current(newindex=0)
        self.opcija_prihod_rashod1.grid(row=2, column=0, pady=5, padx=5)
        CreateToolTip(self.opcija_prihod_rashod1, "Izaberi tabelu")
        # promenljiva meseci u kojoj se u listi prikazani svi meseci u godini
        self.meseci = ['Januar', 'Februar', 'Mart', 'April', 'Maj', 'Jun',
                       'Jul', 'Avgust', 'Septembar', 'Oktobar',
                       'Novembar', 'Decembar']
        self.upitdatum1 = ttk.Combobox(self.tab2, width=15, value=self.meseci,
                                       state='readonly')
        self.upitdatum1.grid(row=2, column=2, pady=5, padx=5)
        CreateToolTip(self.upitdatum1, "Izaberi mesec")
        # opcija koje su default vrednosti za opcije koju biramo u upitima
        opc = ["Kategorija", "Vrsta Transakcije", "Vrsta placanja",
               "Primaoc/Platioc"]
        self.upit_opcija1_1 = ttk.Combobox(self.tab2, width=15,
                                           state='readonly')
        self.upit_opcija1_1[
            'value'] = "Kategorija", "Vrsta Transakcije", "Vrsta placanja", "Primaoc/Platioc"
        self.upit_opcija1_1.grid(row=2, column=3, pady=5, padx=5)
        CreateToolTip(self.upit_opcija1_1, "Izaberi opciju")
        Button(self.tab2, text="Potvrdi", command=self.upit2,
               image=self.slika_dugme).grid(row=2, column=4, pady=5)
        self.opcija_prihod_rashod2 = ttk.Combobox(self.tab2, value=ras_pri,
                                                  state='readonly', width=8)
        self.opcija_prihod_rashod2.current(newindex=0)
        self.opcija_prihod_rashod2.grid(row=3, column=0, pady=5, padx=5)
        CreateToolTip(self.opcija_prihod_rashod2, "Izaberi tabelu")
        self.upit_opcija2 = ttk.Combobox(self.tab2, width=15, value=opc,
                                         state='readonly')
        self.upit_opcija2.bind("<<ComboboxSelected>>", self.combo_opcija1)
        self.upit_opcija2.grid(row=3, column=2, pady=10, padx=5)
        CreateToolTip(self.upit_opcija2, "Izaberi opciju")
        self.upit_vrednost2 = AutocompleteCombobox(self.tab2, width=15)
        self.upit_vrednost2.grid(row=3, column=3, pady=5, padx=5)
        CreateToolTip(self.upit_vrednost2, "Unesi ili izaberi vrednost")
        Button(self.tab2, text="Potvrdi", command=self.upit3,
               image=self.slika_dugme).grid(row=3, column=4, pady=5)
        self.opcija_prihod_rashod3 = ttk.Combobox(self.tab2, value=ras_pri,
                                                  state='readonly', width=8)
        self.opcija_prihod_rashod3.current(newindex=0)
        self.opcija_prihod_rashod3.grid(row=4, column=0, pady=5, padx=5)
        CreateToolTip(self.opcija_prihod_rashod3, "Izaberi tabelu")
        self.upit_opcija3 = ttk.Combobox(self.tab2, width=15, value=opc,
                                         state='readonly')
        self.upit_opcija3.bind("<<ComboboxSelected>>", self.combo_opcija2)
        self.upit_opcija3.grid(row=4, column=2, pady=5, padx=5)
        CreateToolTip(self.upit_opcija3, "Izaberi opciju")
        self.upit_vrednost3 = AutocompleteCombobox(self.tab2, width=15)
        self.upit_vrednost3.grid(row=4, column=3, pady=5, padx=5)
        CreateToolTip(self.upit_vrednost3, "Unesi ili izaberi vrednost")
        Button(self.tab2, text="Potvrdi", command=self.upit4,
               image=self.slika_dugme).grid(row=4, column=4, pady=5, padx=5)
        self.opcija_prihod_rashod4 = ttk.Combobox(self.tab2, value=ras_pri,
                                                  state='readonly', width=8)
        self.opcija_prihod_rashod4.current(newindex=0)
        self.opcija_prihod_rashod4.grid(row=5, column=0, pady=5, padx=5)
        CreateToolTip(self.opcija_prihod_rashod4, "Izaberi tabelu")
        self.upit_godina1 = ttk.Combobox(self.tab2, width=15)
        self.upit_godina1.grid(row=5, column=2, pady=5, padx=5)
        CreateToolTip(self.upit_godina1, "Unesi godinu")
        self.upit_opcija4 = ttk.Combobox(self.tab2, width=15, value=opc,
                                         state='readonly')
        self.upit_opcija4.bind("<<ComboboxSelected>>", self.combo_opcija11)
        self.upit_opcija4.grid(row=5, column=3, pady=5, padx=5)
        self.upit_vrednost14 = AutocompleteCombobox(self.tab2, width=15)
        self.upit_vrednost14.grid(row=5, column=4, pady=5, padx=5)
        CreateToolTip(self.upit_opcija4, "Izaberi opciju")
        Button(self.tab2, text="Potvrdi", command=self.upit5,
               image=self.slika_dugme).grid(row=5, column=5, pady=5)
        Label(self.tab3, font=15, bg="#2b306e", fg="white",
              text="Izaberi opciju ,vrednost opcije i mesec i na kraju opciju po\n kojoj zelis da vidis vrednosti u tabeli odredjenog meseca ").grid(
            row=5, column=1, pady=10)
        Label(self.tab3, font=15, bg="#2b306e", fg="white",
              text="Izaberi opciju  i vrednost opcije   da vidis u \n tabeli vrednosti gde se  vrednost opcije nalazi").grid(
            row=3, column=1, pady=10)
        Label(self.tab3, font=15, bg="#2b306e", fg="white",
              text="Izaberi datum i znak i vidi u tabeli vrednosti \n u zavisnosti od znaka i datuma ").grid(
            row=2, column=1, pady=10)
        self.opcija_prihod_rashod6 = ttk.Combobox(self.tab3, value=ras_pri,
                                                  width=8, state='readonly')
        self.opcija_prihod_rashod6.current(newindex=0)
        self.opcija_prihod_rashod6.grid(row=2, column=0, pady=5, padx=5)
        CreateToolTip(self.opcija_prihod_rashod6, "Izaberi tabelu")
        self.opcija_prihod_rashod8 = ttk.Combobox(self.tab3, value=ras_pri,
                                                  width=8, state='readonly')
        self.opcija_prihod_rashod8.current(newindex=0)
        self.opcija_prihod_rashod8.grid(row=3, column=0, pady=5, padx=5)
        CreateToolTip(self.opcija_prihod_rashod8, "Izaberi tabelu")
        self.opcija_prihod_rashod10 = ttk.Combobox(self.tab3, value=ras_pri,
                                                   width=8, state='readonly')
        self.opcija_prihod_rashod10.current(newindex=0)
        self.opcija_prihod_rashod10.grid(row=5, column=0, pady=5, padx=5)
        CreateToolTip(self.opcija_prihod_rashod10, "Izaberi tabelu")
        self.upit_opcija8 = ttk.Combobox(self.tab3, width=15, state='readonly',
                                         value=opc)
        self.upit_opcija8.bind("<<ComboboxSelected>>", self.combo_opcija3)
        self.upit_opcija8.grid(row=5, column=2, pady=10, padx=5)
        CreateToolTip(self.upit_opcija8, "Izaberi opciju")
        self.upit_vrednost4 = AutocompleteCombobox(self.tab3, width=15)
        self.upit_vrednost4.grid(row=5, column=3, pady=10, padx=5)
        CreateToolTip(self.upit_vrednost4, "Unesi ili izaberi vrednost")
        self.upit_mesec1 = ttk.Combobox(self.tab3, state='readonly',
                                        value=self.meseci, width=12)
        self.upit_mesec1.grid(row=5, column=4, pady=10, sticky=W)
        CreateToolTip(self.upit_mesec1, "Izaberi mesec")
        Button(self.tab3, text="Potvrdi", command=self.upit9,
               image=self.slika_dugme).grid(row=5, column=5, padx=5)
        self.upit_opcija9 = ttk.Combobox(self.tab3, state='readonly',
                                         value=opc, width=15)
        self.upit_opcija9.bind("<<ComboboxSelected>>", self.combo_opcija4)
        self.upit_opcija9.grid(row=3, column=2, pady=10)
        CreateToolTip(self.upit_opcija9, "Izaberi opciju")
        self.upit_vrednost5 = AutocompleteCombobox(self.tab3, width=15)
        self.upit_vrednost5.grid(row=3, column=3, pady=10)
        CreateToolTip(self.upit_vrednost5, "Unesi ili izaberi vrednost")
        Button(self.tab3, text="Potvrdi", command=self.upit10,
               image=self.slika_dugme).grid(row=3, column=4, pady=4)
        self.upit_vrednost6 = ttk.Combobox(self.tab3, width=13)
        self.upit_vrednost6['value'] = self.daj_upit(
            "SELECT datum from rashod group by datum union all SELECT datum from prihod group by datum")
        self.upit_vrednost6.grid(row=2, column=2, pady=10)
        CreateToolTip(self.upit_vrednost6, "Unesi vrednost")
        # znaci koji biramo u komboboxu za upite
        znaci = "<", ">","="
        self.znak = ttk.Combobox(self.tab3, state='readonly', width=5,
                                 value=znaci)
        self.znak.grid(row=2, column=3, pady=10)
        CreateToolTip(self.znak, "Izaberi znak")
        Button(self.tab3, text="Potvrdi", command=self.upit11,
               image=self.slika_dugme).grid(row=2, column=4, pady=10)
        self.opcija_prihod_rashod12 = ttk.Combobox(self.tab3, width=8,
                                                   state='readonly',
                                                   value=ras_pri)
        self.opcija_prihod_rashod12.current(newindex=0)
        self.opcija_prihod_rashod12.grid(row=1, column=0, pady=5, padx=5)
        CreateToolTip(self.opcija_prihod_rashod12, "Izaberi tabelu")

        Label(self.tab3, font=15, bg="#2b306e", fg="white",
              text="Unesi iznos i izaberi znak da vidis u tabeli rezultate u zavisnosti od znaka").grid(
            row=1, column=1, pady=10)
        self.unos_iznos = Entry(self.tab3, width=10)
        self.unos_iznos.grid(row=1, column=2, pady=10)
        CreateToolTip(self.unos_iznos, "Unesi iznos")
        self.znak1 = ttk.Combobox(self.tab3, state='readonly', width=5,
                                  value=znaci)
        self.znak1.grid(row=1, column=3, pady=10, padx=10)
        CreateToolTip(self.znak1, "Izaberi znak")
        Button(self.tab3, text="Ok", command=self.upit12,
               image=self.slika_dugme).grid(row=1, column=4, pady=10)

        Label(self.tab3, font=15, bg="#2b306e", fg="white",
              text="Unesi godinu i izaberi mesec  pogledaj u tabeli \n"
                   "sve vrednosti za unetu godinu i mesec").grid(row=4,
                                                                     column=1,
                                                                     pady=10)
        self.opcija_prihod_rashod13 = ttk.Combobox(self.tab3, width=8,
                                                   state='readonly',
                                                   value=ras_pri)
        self.opcija_prihod_rashod13.current(newindex=0)
        self.opcija_prihod_rashod13.grid(row=4, column=0, padx=5, pady=5)
        CreateToolTip(self.opcija_prihod_rashod13, "Izaberi tabelu")
        self.upit_godina2 = Entry(self.tab3, width=10)
        self.upit_godina2.grid(row=4, column=2, pady=10)
        CreateToolTip(self.upit_godina2, "Unesi godinu")
        self.upit_mesec2 = ttk.Combobox(self.tab3, value=self.meseci,
                                        state='readonly', width=15)
        self.upit_mesec2.grid(row=4, column=3, pady=10)
        CreateToolTip(self.upit_mesec2, "Izaberi mesec")
        Button(self.tab3, text="Potvrdi", command=self.upit13,
               image=self.slika_dugme).grid(row=4, column=4, pady=10)
        # tabela u kojoj su prikazani rezultati upita
        self.tree_upiti = ttk.Treeview(self.tab3)
        self.tree_upiti.configure(style="Mystyle.Treeview")
        self.tree_upiti["columns"] = (
            "#0", "#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10")
        self.tree_upiti.grid(row=7, column=1, columnspan=3,
                             sticky=S + W + E + N)
        self.treescrollbar2 = ttk.Scrollbar(self.tab3, orient="vertical",
                                            command=self.tree_upiti.yview)
        self.scrollbarhoriz2 = ttk.Scrollbar(self.tab3, orient='horizontal',
                                             command=self.tree_upiti.xview)
        self.scrollbarhoriz2.grid(row=7, column=1, columnspan=3,
                                  sticky=W + S + E)
        self.treescrollbar2.grid(row=7, column=3, sticky=S + E + N)
        self.tree_upiti.configure(yscrollcommand=self.treescrollbar2.set,
                                  xscrollcommand=self.scrollbarhoriz2.set)
        self.tree_upiti.tag_configure('oddrow', background="#3482b3")
        self.tree_upiti.tag_configure('evenrow', background="white")
        self.tree_upiti.column("#0", width=5, minwidth=10)
        self.tree_upiti.column("#1", width=50, minwidth=100)
        self.tree_upiti.column("#2", width=50, minwidth=100)
        self.tree_upiti.column("#3", width=50, minwidth=100)
        self.tree_upiti.column("#4", width=50, minwidth=100)
        self.tree_upiti.column("#5", width=50, minwidth=100)
        self.tree_upiti.column("#6", width=50, minwidth=100)
        self.tree_upiti.column("#7", width=50, minwidth=100)
        self.tree_upiti.column("#8", width=50, minwidth=100)
        self.tree_upiti.column("#9", width=50, minwidth=100)
        self.tree_upiti.heading('#0', text='')
        self.tree_upiti.heading('#1', text='Datum')
        self.tree_upiti.heading("#2", text='Ime')
        self.tree_upiti.heading("#3", text="Kategorija")
        self.tree_upiti.heading("#4", text="Pod kategorija")
        self.tree_upiti.heading("#5", text="Vrsta transakcije")
        self.tree_upiti.heading("#6", text="Vrsta placanja")
        self.tree_upiti.heading("#7", text="Primaoc/Platioc")
        self.tree_upiti.heading("#8", text="Kontakt")
        self.tree_upiti.heading("#9", text="Iznos")
        self.tree_upiti["displaycolumns"] = (
            "#0", "#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9")


        Label(self.tab4, font=15, bg="#2b306e", fg="white",
              text="Izaberi opciju i vrednosti te opcije da bi\n video imena u toj vrednosti ").grid(
            row=1, column=1, pady=10)
        Label(self.tab4, font=15, bg="#2b306e", fg="white",
              text="Izaberi opciju i vrednost te opcije i onda\n MIN ili MAX da vidis najmanju ili najvecu vrednosti ").grid(
            row=5, column=1, pady=10)
        Label(self.tab4, font=15, bg="#2b306e", fg="white",
              text="Izaberi opciju i vrednosti te opcije da bi u \ntabeli video koliko puta se vrednost unela u tabelu").grid(
            row=2, column=1, pady=10)
        self.opcija_prihod_rashod7 = ttk.Combobox(self.tab4, value=ras_pri,
                                                  width=8, state='readonly')
        self.opcija_prihod_rashod7.current(newindex=0)
        self.opcija_prihod_rashod7.grid(row=1, column=0, pady=5, padx=5)
        CreateToolTip(self.opcija_prihod_rashod7, "Izaberi tabelu")
        self.opcija_prihod_rashod9 = ttk.Combobox(self.tab4, value=ras_pri,
                                                  width=8, state='readonly')
        self.opcija_prihod_rashod9.current(newindex=0)
        self.opcija_prihod_rashod9.grid(row=2, column=0, pady=5, padx=5)
        CreateToolTip(self.opcija_prihod_rashod9, "Izaberi tabelu")
        self.opcija_prihod_rashod11 = ttk.Combobox(self.tab4, value=ras_pri,
                                                   width=8, state='readonly')
        self.opcija_prihod_rashod11.current(newindex=0)
        self.opcija_prihod_rashod11.grid(row=5, column=0, pady=5, padx=5)
        CreateToolTip(self.opcija_prihod_rashod11, "Izaberi tabelu")
        # Pravljenje listbox-a u kojoj su prikazani rezultati upita
        self.list = Listbox(self.tab4, font=45, height=13, width=20)
        self.treescrollbar_list = ttk.Scrollbar(self.tab4, orient="vertical",
                                                command=self.list.yview)
        self.scrollbarhoriz_list = ttk.Scrollbar(self.tab4,
                                                 orient="horizontal",
                                                 command=self.list.xview)
        self.scrollbarhoriz_list.grid(row=7, column=2, columnspan=3,
                                      sticky=W + S + E)
        self.treescrollbar_list.grid(row=7, column=4, sticky=S + E + N)
        self.list.configure(yscrollcommand=self.treescrollbar_list.set,
                            xscrollcommand=self.scrollbarhoriz_list.set)
        self.list.grid(row=7, column=2, columnspan=3, pady=10,
                       sticky=S + W + E + N)

        self.upit_opcija5 = ttk.Combobox(self.tab4, width=15, state='readonly',
                                         value=opc)
        self.upit_opcija5.bind("<<ComboboxSelected>>", self.combo_opcija5)
        self.upit_opcija5.grid(row=1, column=2, padx=5)
        CreateToolTip(self.upit_opcija5, "Izaberi opciju")
        self.upit_vrednosti1 = AutocompleteCombobox(self.tab4, width=15)
        self.upit_vrednosti1.grid(row=1, column=3, padx=5)
        CreateToolTip(self.upit_vrednosti1, "Unesi ili izaberi vrednost")
        Button(self.tab4, text="Potvrdi", command=self.upit6,
               image=self.slika_dugme).grid(row=1, column=4)

        self.upit_opcija6 = ttk.Combobox(self.tab4, width=15, state='readonly',
                                         value=opc)
        self.upit_opcija6.bind("<<ComboboxSelected>>", self.combo_opcija6)
        self.upit_opcija6.grid(row=5, column=2, pady=10, padx=5)
        CreateToolTip(self.upit_opcija6, "Izaberi opciju")
        self.upit_vrednosti2 = AutocompleteCombobox(self.tab4, width=15)
        self.upit_vrednosti2.grid(row=5, column=3, sticky=W, pady=10, padx=5)
        CreateToolTip(self.upit_vrednosti2, "Unesi ili izaberi vrednost")
        self.minimum = IntVar()
        self.maximum = IntVar()
        self.min = Checkbutton(self.tab4, text='MIN', variable=self.minimum,
                               onvalue=1, offvalue=0, width=4,command=lambda:self.check_opcija1(True))
        self.min.grid(row=5, column=4, pady=10, padx=5)
        CreateToolTip(self.min, "Izaberi minimum")
        self.max = Checkbutton(self.tab4, text='MAX', variable=self.maximum,
                               onvalue=1, offvalue=0, width=4,command=lambda:self.check_opcija1(True))
        self.max.grid(row=5, column=5, pady=10, padx=5)
        CreateToolTip(self.max, "Izaberi maksimum")
        Button(self.tab4, text="Potvrdi", command=self.upit7,
               image=self.slika_dugme).grid(row=5, column=6)
        self.upit_opcija7 = ttk.Combobox(self.tab4, width=15, state='readonly',
                                         value=opc)
        self.upit_opcija7.bind("<<ComboboxSelected>>", self.combo_opcija7)
        self.upit_opcija7.grid(row=2, column=2, padx=5)
        CreateToolTip(self.upit_opcija7, "Izaberi opciju")
        self.upit_vrednosti3 = AutocompleteCombobox(self.tab4, width=15)
        self.upit_vrednosti3.grid(row=2, column=3, sticky=W, padx=5)
        CreateToolTip(self.upit_vrednosti3, "Unesi ili izaberi vrednost")
        Button(self.tab4, text="Potvrdi", command=self.upit8,
               image=self.slika_dugme).grid(row=2, column=4)
        Label(self.tab4, font=15, bg="#2b306e", fg="white",
              text="Izaberi mesec i MIN ili MAX da vidis minimalan  i maksimalan\n"
                   "iznos za izabrani mesec").grid(row=4, column=1, pady=10)
        self.opcija_prihod_rashod14 = ttk.Combobox(self.tab4, value=ras_pri,
                                                   state='readonly', width=8)
        self.opcija_prihod_rashod14.current(newindex=0)
        self.opcija_prihod_rashod14.grid(row=4, column=0, pady=5, padx=5)
        CreateToolTip(self.opcija_prihod_rashod14, "Izaberi tabelu")
        self.upit_mesec3 = ttk.Combobox(self.tab4, state='readonly', width=13,
                                        value=self.meseci)
        self.upit_mesec3.grid(row=4, column=2, pady=10, padx=5)
        CreateToolTip(self.upit_mesec3, "Izaberi mesec")
        self.check_var1 = IntVar()
        self.check_var2 = IntVar()
        # Opcija da se cekira ili ne odredjena promenljiva
        self.upit_min = Checkbutton(self.tab4, width=4, text="MIN",
                                    variable=self.check_var1, onvalue=1,
                                    offvalue=0,command=lambda:self.check_opcija(True))
        self.upit_min.grid(row=4, column=3, pady=10, sticky=W)
        CreateToolTip(self.upit_min, "Izaberi minimum")
        self.upit_max = Checkbutton(self.tab4, width=4, text="MAX",
                                    variable=self.check_var2, onvalue=1,
                                    offvalue=0,command=lambda:self.check_opcija(True))
        self.upit_max.grid(row=4, column=3, pady=10, sticky=E)
        CreateToolTip(self.upit_max, "Izaberi maksimum")
        Button(self.tab4, text="Potvrdi", command=self.upit14,
               image=self.slika_dugme).grid(row=4, column=4, pady=10, padx=5)

        Label(self.tab4, font=15, bg="#2b306e", fg="white",
              text="Izaberi mesec i opciju i pogledaj vrednosti opcije za izabrani mesec").grid(
            row=3, column=1, pady=10)
        self.opcija_prihod_rashod15 = ttk.Combobox(self.tab4, state='readonly',
                                                   value=ras_pri, width=8)
        self.opcija_prihod_rashod15.current(newindex=0)
        self.opcija_prihod_rashod15.grid(row=3, column=0, padx=5, pady=5)
        CreateToolTip(self.opcija_prihod_rashod15, "Izaberi tabelu")
        self.upit_mesec4 = ttk.Combobox(self.tab4, value=self.meseci,
                                        state='readonly', width=15)
        self.upit_mesec4.grid(row=3, column=2, pady=10, padx=5)
        CreateToolTip(self.upit_mesec4, "Izaberi mesec")
        self.upit_opcija10 = ttk.Combobox(self.tab4, state='readonly',
                                          value=opc, width=15)
        self.upit_opcija10.grid(row=3, column=3, pady=10, padx=5)
        CreateToolTip(self.upit_opcija10, "Izaberi opciju")
        Button(self.tab4, text="Potvrdi", command=self.upit15,
               image=self.slika_dugme).grid(row=3, column=4, pady=10)

        Label(self.tab5, font=15, bg="#2b306e", fg="white",
              text="Pogledaj razliku izmedju dve tabele").grid(row=1, column=1,
                                                               pady=10)
        Button(self.tab5, text="Potvrdi", command=self.upit16,
               image=self.slika_dugme).grid(row=1, column=2, pady=10)

        Label(self.tab5, font=15, bg="#2b306e", fg="white",
              text="Izaberi opcije i njihove vrednosti da bi video razliku izmedju njih ").grid(
            row=2, column=1, rowspan=2, pady=10)
        self.upit_opcija11 = ttk.Combobox(self.tab5, value=opc,
                                          state="readonly", width=15)
        self.upit_opcija11.bind("<<ComboboxSelected>>", self.combo_opcija8)
        self.upit_opcija11.grid(row=2, column=2, rowspan=2, pady=10, padx=5)
        self.upit_vrednosti4 = AutocompleteCombobox(self.tab5, width=15)
        self.upit_vrednosti4.grid(row=2, column=3, pady=10, padx=5)
        CreateToolTip(self.upit_vrednosti4, "Unesi ili izaberi vrednost")
        self.upit_vrednosti5 = AutocompleteCombobox(self.tab5, width=15)
        self.upit_vrednosti5.grid(row=3, column=3, pady=10, padx=5)
        CreateToolTip(self.upit_vrednosti5, "Unesi ili izaberi vrednost")
        Button(self.tab5, text="Potvrdi", command=self.upit17,
               image=self.slika_dugme).grid(row=2, column=4, rowspan=2,
                                            pady=10)

        Label(self.tab5, font=15, bg="#2b306e", fg="white",
              text="Izaberi datume i pogledaj razliku izmedju "
        "tabela za izabrane datume").grid(row=4, column=1, pady=10)
        self.upit_datum2 = ttk.Combobox(self.tab5, width=10)
        self.upit_datum2['value'] = self.daj_upit(
            "SELECT datum from rashod group by datum")
        self.upit_datum2.grid(row=4, column=2, pady=10, padx=5)
        CreateToolTip(self.upit_datum2, "Unesi ili izaberi datum")
        self.upit_datum3 = ttk.Combobox(self.tab5, width=10)
        self.upit_datum3['value'] = self.daj_upit(
            "SELECT datum from prihod group by datum")
        self.upit_datum3.grid(row=4, column=3, pady=10, padx=5)
        CreateToolTip(self.upit_datum3, "Unesi ili izaberi datum")
        Button(self.tab5, text="Potvrdi", command=self.upit18,
               image=self.slika_dugme).grid(row=4, column=4, pady=10)

        Label(self.tab5, font=15, bg="#2b306e", fg="white",
              text="Izaberi opciju i vrednosti iz obe tabele i "
    "pogledaj njene ukupne \n i prosecne vrednosti po mesecu").grid(row=5,
                                                column=1, rowspan=2, pady=10)
        self.upit_opcija13 = ttk.Combobox(self.tab5, state="readonly",
                                          value=opc, width=15)
        self.upit_opcija13.bind("<<ComboboxSelected>>", self.combo_opcija9)
        self.upit_opcija13.grid(row=5, rowspan=2, column=2, pady=10, padx=5)
        CreateToolTip(self.upit_opcija13, "Izaberi opciju")
        self.upit_vrednosti6 = AutocompleteCombobox(self.tab5, width=15)
        self.upit_vrednosti6.grid(row=5, column=3, pady=10, padx=5)
        CreateToolTip(self.upit_vrednosti6, "Unesi ili izaberi vrednost")
        self.upit_vrednosti7 = AutocompleteCombobox(self.tab5, width=15)
        self.upit_vrednosti7.grid(row=6, column=3, pady=10, padx=5)
        CreateToolTip(self.upit_vrednosti7, "Unesi ili izaberi vrednost")
        Button(self.tab5, text="AVG", command=self.upit19).grid(row=5,
                                                                column=4,
                                                                rowspan=2,
                                                                pady=10,
                                                                padx=5)
        Button(self.tab5, text="SUM", command=self.upit20).grid(row=5,
                                                                column=5,
                                                                rowspan=2,
                                                                pady=10,
                                                                padx=5)
        Label(self.tab5, font=15, bg="#2b306e", fg="white",
              text="Izaberi opciju unesi vrednosti i izaberi "
                   "mesec da vidis razliku \nizmedju"
                   " vrednosti prema mesecima").grid(row=8, column=1,rowspan=2,
                                                     pady=10, padx=5)
        self.upit_opcija14 = ttk.Combobox(self.tab5, state='readonly',
                                          value=opc, width=15)
        self.upit_opcija14.bind("<<ComboboxSelected>>", self.combo_opcija10)
        self.upit_opcija14.grid(row=8, column=2, rowspan=2, pady=10, padx=5)
        CreateToolTip(self.upit_opcija14, "Izaberi opciju")
        self.upit_vrednosti8 = AutocompleteCombobox(self.tab5, width=15)
        self.upit_vrednosti8.grid(row=8, column=3, pady=10, padx=5)
        CreateToolTip(self.upit_vrednosti8, "Unesi i izaberi vrednost")
        self.upit_vrednosti9 = AutocompleteCombobox(self.tab5, width=15)
        self.upit_vrednosti9.grid(row=9, column=3, pady=10, padx=5)
        CreateToolTip(self.upit_vrednosti8, "Unesi i izaberi vrednost")
        self.upit_mesec5 = ttk.Combobox(self.tab5, state='readonly',
                                        value=self.meseci, width=13)
        self.upit_mesec5.grid(row=8, column=4, pady=10, padx=5)
        CreateToolTip(self.upit_mesec5, "Izaberi mesec")
        self.upit_mesec6 = ttk.Combobox(self.tab5, state='readonly',
                                        value=self.meseci, width=13)
        self.upit_mesec6.grid(row=9, column=4, pady=10, padx=5)
        CreateToolTip(self.upit_mesec6, "Izaberi mesec")
        Button(self.tab5, text="Potvrdi", command=self.upit21,
               image=self.slika_dugme).grid(row=8, rowspan=2, column=5,
                                            pady=10)

        self.autofil()
        self.wind2.configure(bg="#001c4d")
        self.wind2.mainloop()

    def autofil(self):
        # funkcija koja ucitava podatke i baze i vrsi autokomplit
        # ucitava se baza koja se zove po korisnickom imenu korisnika koji
        # se ulogovao
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute("SELECT datum from rashod group by datum")
            lista_datum =c.fetchall()
            lista_datum2 = [item[0] for item in lista_datum]
            self.datum_autofil = tuple(map(str,lista_datum2))
            # upit da izbaci vrednosti iz ove tabele
            c.execute("SELECT ime from rashod group by ime")
            # promenljiva koja preuzima rezultate upita
            lista_ime = c.fetchall()
            #promenljiva koja preuzima nabrajanjem preuzima vrednosti iz upita
            lista_ime2 = [item[0] for item in lista_ime]
            # promenljiva koja preuzima vrednosti kao string koji su
            # konvertovani iz liste u string
            self.imena = tuple(map(str, lista_ime2))
            c.execute("SELECT kategorija from rashod group by kategorija")
            lista_kategorija = c.fetchall()
            lista_kategorija2 = [item[0] for item in lista_kategorija]
            self.kategorija_autofil = tuple(map(str, lista_kategorija2))
            c.execute(
                "SELECT podkategorija from rashod group by podkategorija")
            lista_podkategorija = c.fetchall()
            lista_podkategorija2 = [item[0] for item in lista_podkategorija]
            self.podkategorija_autofil = tuple(map(str, lista_podkategorija2))
            c.execute("SELECT primaoc from rashod group by primaoc ")
            lista_primaoc = c.fetchall()
            lista_primaoc2 = [item[0] for item in lista_primaoc]
            self.primaoc_autofil = tuple(map(str, lista_primaoc2))

            c.execute("SELECT ime from prihod group by ime")
            lista_ime = c.fetchall()
            lista_ime2 = [item[0] for item in lista_ime]
            self.imena1 = tuple(map(str, lista_ime2))
            c.execute("SELECT kategorija from prihod group by kategorija")
            lista_kategorija = c.fetchall()
            lista_kategorija2_1 = [item[0] for item in lista_kategorija]
            self.kategorija_autofil1 = tuple(map(str, lista_kategorija2_1))
            c.execute(
                "SELECT podkategorija from prihod group by podkategorija")
            lista_podkategorija = c.fetchall()
            lista_podkategorija2_1 = [item[0] for item in lista_podkategorija]
            self.podkategorija_autofil1 = tuple(
                map(str, lista_podkategorija2_1))
            c.execute("SELECT platioc from prihod group by platioc ")
            lista_platioc = c.fetchall()
            lista_platioc2_1 = [item[0] for item in lista_platioc]
            self.platioc_autofil = tuple(map(str, lista_platioc2_1))

            c.execute("SELECT kontakt from rashod group by kontakt")
            lista_kontakt= c.fetchall()
            lista_kontakt2 = [item[0] for item in lista_kontakt]
            self.kontakt_autofil = tuple(map(str ,lista_kontakt2))

            c.execute("SELECT datum from prihod group by datum")
            lista_datum = c.fetchall()
            lista_datum2 = [item[0] for item in lista_datum]
            self.datum_autofil1 = tuple(map(str,lista_datum2))
            c.execute(
                "SELECT ime from rashod group by ime union all SELECT ime from prihod group by ime")
            lista_imena = c.fetchall()
            lista_imena2 = [item[0] for item in lista_imena]
            self.lista_imena = tuple(map(str, lista_imena2))

            c.execute(
                "SELECT kategorija from rashod group by kategorija union all SELECT kategorija from prihod group by kategorija")
            lista_kategorija = c.fetchall()
            lista_kategorija2 = [item[0] for item in lista_kategorija]
            self.lista_kategorija = tuple(map(str, lista_kategorija2))

            c.execute(
                "SELECT podkategorija from rashod group by podkategorija union all SELECT podkategorija from prihod group by podkategorija")
            lista_podkategorija = c.fetchall()
            lista_podkategorija2 = [item[0] for item in lista_podkategorija]
            self.lista_podkategorija = tuple(map(str, lista_podkategorija2))

            c.execute(
                "SELECT primaoc from rashod group by primaoc union all SELECT platioc from prihod group by platioc")
            lista_primaoc_platioc = c.fetchall()
            lista_primaoc_platioc2 = [item[0] for item in
                                      lista_primaoc_platioc]
            self.lista_primaoc_platioc = tuple(
                map(str, lista_primaoc_platioc2))
            c.execute("SELECT kontakt from prihod group by kontakt")
            lista_kontakt =c.fetchall()
            lista_kontakt2 = [item[0] for item in lista_kontakt]
            self.kontakt_autofil1 = tuple(map(str,lista_kontakt2))

            c.execute("SELECT datum from rashod group by datum union all SELECT datum from prihod group by datum")
            lista_datumi = c.fetchall()
            lista_datumi2 = [item[0] for item in lista_datumi]
            self.datumi_autofil = tuple(map(str,lista_datumi2))

            c.execute("SELECT kontakt from rashod group by kontakt union all SELECT kontakt from prihod group by kontakt")
            lista_kontakti = c.fetchall()
            lista_kontakt2 = [item[0] for item in lista_kontakti]
            self.kontakti = tuple(map(str,lista_kontakt2))

    def reset(self):
        #funkcija koja  resetuje sve vrednosti nakon dodavanja , menjanja ili
        #brisanja vrednosti u upitima gde su vrednosti izabrane da se pokrene
        # odredjeni upit

        self.upit_opcija1.set("")
        self.upitdatum1.set("")
        self.upit_opcija1_1.set("")
        self.upit_opcija2.set("")
        # self.upit_vrednost2.delete(0,END)
        # self.upit_vrednost2.set("")
        self.upit_opcija3.set("")
        self.upit_vrednost3.delete(0, END)
        self.upit_vrednost3.set("")
        self.upit_godina1.delete(0, END)
        self.upit_opcija4.set("")
        self.upit_vrednost14.delete(0, END)
        self.upit_vrednost14.set("")

        self.upit_opcija8.set("")
        self.upit_vrednost4.set("")
        self.upit_vrednost4.delete(0, END)
        self.upit_mesec1.set("")
        self.upit_opcija9.set("")
        self.upit_vrednost5.delete(0, END)
        self.upit_vrednost5.set("")
        self.upit_vrednost6.delete(0, END)
        self.upit_vrednost6.set("")
        self.znak.set("")
        self.unos_iznos.delete(0, END)
        self.znak1.set("")
        self.upit_godina2.delete(0, END)
        self.upit_mesec2.set("")

        self.upit_opcija5.set("")
        self.upit_vrednosti1.set("")
        self.upit_vrednosti1.delete(0, END)
        self.upit_opcija6.set("")
        self.upit_vrednosti2.set("")
        self.upit_vrednosti2.delete(0, END)
        self.upit_opcija7.set("")
        self.upit_vrednosti3.set("")
        self.upit_vrednosti3.delete(0, END)
        self.upit_mesec3.set("")
        self.upit_mesec4.set("")
        self.upit_opcija10.set("")

        self.upit_opcija11.set("")
        self.upit_vrednosti4.delete(0, END)
        self.upit_vrednosti4.set("")
        self.upit_vrednosti5.delete(0, END)
        self.upit_vrednosti5.set("")
        self.upit_datum2.set("")
        self.upit_datum3.set("")
        self.upit_opcija13.set("")
        self.upit_vrednosti6.set("")
        self.upit_vrednosti6.delete(0, END)
        self.upit_vrednosti7.set("")
        self.upit_vrednosti7.delete(0, END)
        self.upit_opcija14.set("")
        self.upit_vrednosti8.set("")
        self.upit_vrednosti8.delete(0, END)
        self.upit_vrednosti9.set("")
        self.upit_vrednosti9.delete(0, END)
        self.upit_mesec5.set("")
        self.upit_mesec6.set("")

    def live_prikaz(self):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute("SELECT SUM(iznos) from prihod ")
            row = c.fetchall()
            pri = []
            [pri.append(i[0]) for i in row]
            pri1 = ''.join(map(str, pri))
            try:
                self.sumpri1 = float(pri1)
            except ValueError:
                self.sumpri1 = float(0)

            c.execute("SELECT SUM(iznos) from rashod ")
            row = c.fetchall()
            ras = []
            [ras.append(i[0]) for i in row]
            ras1 = ''.join(map(str, ras))
            try:
                self.sumras1 = float(ras1)
            except ValueError:
                self.sumras1 = float(0)

            self.label_prihod["text"] = str(self.sumpri1)
            self.label_rashod["text"] = str(self.sumras1)
            broj1 = self.sumras1
            broj2 = self.sumpri1
            if broj1 > broj2:
                rez = broj1 - broj2
                self.suficit_deficit[
                    'text'] = "  Deficit:              " + str(rez)
                self.suficit_deficit["fg"] = "orange"
            if broj2 > broj1:
                rez = broj2 - broj1
                self.suficit_deficit[
                    'text'] = "  Suficit:              " + str(rez)
                self.suficit_deficit['fg'] = "#05ff3f"
            if broj1 == 0 and broj2 == 0:
                var = self.suficit_deficit[
                    'text'] = 'Suficit/Deficit:               0.0'
                self.suficit_deficit['fg'] = "white"
                self.suficit_deficit.grid(row=8, column=1, )

    def pokreni_upit(self, upit, parametri=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(upit, parametri)
            conn.commit()

        return result

    def daj_upit(self, upit):
        res = []
        result_query = self.pokreni_upit(upit)
        for row in result_query.fetchall():
            res.append(row[0])
        return res

    def reklama_funkcija(self):
        if (self.brojac >= len(self.reklama)):
            self.brojac = 0
            self.text = ""
            self.label_reklama.config(text=self.text)
        else:
            self.text = self.text + self.reklama[self.brojac]
            self.label_reklama.config(text=self.text)
            self.brojac += 1
        self.label_reklama.after(200, self.reklama_funkcija)

    def reklama_boje(self):
        colors = ["white", 'silver', 'orange', '#eb9234', 'green', '#daff0a',
                  'yellow', 'pink', 'red2', 'gold2', "#70ff0a", "#8c006e",
                  "#4b2a87", "#2a873a"]
        boje = random.choice(colors)
        self.label_reklama.config(fg=boje)
        self.label_reklama.after(2, self.reklama_boje)
    def check_opcija(self,flag=False):
        if flag:
            if self.check_var1.get():
                self.check_var2.set(0)
            elif self.check_var2.get():
                self.check_var1.set(0)
            else:
                pass
    def check_opcija1(self,flag=False):
        if flag:
            if self.minimum.get():
                self.maximum.set(0)
            elif self.maximum.get():
                self.minimum.set(0)


    def dodaj(self):
        self.dodaj_prozor = Tk()
        self.dodaj_prozor.title("Dodavanje vrednosti")
        self.dodaj_prozor.geometry("500x500")
        self.dodaj_prozor.wm_iconbitmap('slike/emblem-money-2.ico')
        self.menubar = Menu(self.dodaj_prozor)
        self.dodaj_prozor.config(menu=self.menubar)
        self.tab_control = ttk.Notebook(self.dodaj_prozor)
        self.tab1 = Frame(self.tab_control, bg="#2b306e")
        self.tab2 = Frame(self.tab_control, bg="#2b306e")
        self.tab1.pack(expand=1, fill="both")
        self.tab2.pack(expand=1, fill="both")
        self.tab_control.add(self.tab1, text="Rashod")
        self.tab_control.add(self.tab2, text="Prihod")
        self.tab_control.pack(expand=1, fill="both")
        self.autofil()
        Label(self.tab1, text="Unesi datum", font=15, bg="#2b306e",
              fg="white").grid(row=0, column=1, columnspan=2, pady=5)
        self.datum = AutocompleteCombobox(self.tab1, width=12)
        self.datum.set_completion_list(self.datum_autofil)
        self.datum['value']=self.daj_upit("SELECT datum from rashod group by datum")
        self.datum.grid(row=0, column=3, pady=5)
        Label(self.tab1,text="Godina", font=15, bg="#2b306e",
              fg="white").grid(row=1,column=1)
        self.unos_godina = Entry(self.tab1,width=6)
        self.unos_godina.bind('<Key>', lambda event: self.datumunost(event))
        self.unos_godina.grid(row=2,column=1)
        Label(self.tab1,text="Mesec", font=15, bg="#2b306e",
              fg="white").grid(row=1,column=2)
        self.unos_meseca= ttk.Combobox(self.tab1,width=13,value=self.meseci,state='readonly')
        self.unos_meseca.bind("<<ComboboxSelected>>",self.dani)
        self.unos_meseca.bind('<Key>', lambda event: self.datumunost(event))
        self.unos_meseca.grid(row=2,column=2)
        dani = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                '11', '12', '13', '14', '15', '16', '17',
                '18',
                '19', '20', '21',
                '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
        Label(self.tab1,text="Dan", font=15, bg="#2b306e",
              fg="white").grid(row=1,column=3)
        self.unos_dana = ttk.Combobox(self.tab1,width=3,state='readonly',value=dani)
        self.unos_dana.bind('<Key>', lambda event: self.datumunost(event))
        self.unos_dana.grid(row=2,column=3)
        Button(self.tab1,text="OK",command=self.datum_unesen,width=6).grid(row=2,column=4)
        Label(self.tab1, text="Unesi ime", font=15, bg="#2b306e",
              fg="white").grid(row=3, column=1, columnspan=2, pady=5)
        self.ime = AutocompleteCombobox(self.tab1, width=15)
        self.ime.set_completion_list(self.imena)
        self.ime.grid(row=3, column=3, pady=5)
        CreateToolTip(self.ime, "Unesi ili izaberi ime")
        Label(self.tab1, text="Unesi kategoriju", font=15, bg="#2b306e",
              fg="white").grid(row=4, column=1, columnspan=2, pady=5)
        self.kategorija = AutocompleteCombobox(self.tab1, width=15)
        self.kategorija.set_completion_list(self.kategorija_autofil)
        self.kategorija.grid(row=4, column=3, pady=5)
        CreateToolTip(self.kategorija, "Unesi ili izaberi kategoriju")
        Label(self.tab1, text="Unesi podkategoriju", font=15, bg="#2b306e",
              fg="white").grid(row=5, column=1, columnspan=2, pady=5)
        self.podkategorija = AutocompleteCombobox(self.tab1, width=15)
        self.podkategorija.set_completion_list(self.podkategorija_autofil)
        self.podkategorija.grid(row=5, column=3, pady=5)
        CreateToolTip(self.podkategorija, "Unesi ili izaberi podkategoriju")
        Label(self.tab1, text="Izaberi vrstu transakcije", font=15,
              bg="#2b306e", fg="white").grid(row=6, column=1, columnspan=2,
                                             pady=5)
        self.vrsta_transakcije = ttk.Combobox(self.tab1, width=15)
        self.vrsta_transakcije['value'] = "Kupovina", "Pozajmica"
        self.vrsta_transakcije.current(newindex=0)
        self.vrsta_transakcije.grid(row=6, column=3, pady=5)
        CreateToolTip(self.vrsta_transakcije, "Izaberi vrstu transakcije")
        Label(self.tab1, text="Izaberi vrstu placanja", font=15, bg="#2b306e",
              fg="white").grid(row=7, column=1, columnspan=2, pady=5)
        self.vrsta_placanja = ttk.Combobox(self.tab1, width=15,
                                           state='readonly')
        self.vrsta_placanja['value'] = "Gotovina"
        self.vrsta_placanja.current(newindex=0)
        self.vrsta_placanja[
            'value'] = "Gotovina", "Cek", "Kreditna kartica", "Nalog za uplatu"
        self.vrsta_placanja.grid(row=7, column=3, pady=5)
        CreateToolTip(self.vrsta_placanja, "Izaberi vrstu placanja")
        Label(self.tab1, text="Unesi primaoca", font=15, bg="#2b306e",
              fg="white").grid(row=8, column=1, columnspan=2, pady=5)
        self.primaoc = AutocompleteCombobox(self.tab1, width=15)
        self.primaoc.set_completion_list(self.primaoc_autofil)
        self.primaoc.grid(row=8, column=3, pady=5)
        CreateToolTip(self.primaoc, "Unesi ili izaberi primaoca vrednosti")
        Label(self.tab1, text="Unesi kontakt", font=15, bg="#2b306e",
              fg="white").grid(row=9, column=1, columnspan=2, pady=5)
        self.kontakt =AutocompleteCombobox(self.tab1, width=15)
        self.kontakt.set_completion_list(self.kontakt_autofil)
        self.kontakt.grid(row=9, column=3, pady=5)
        CreateToolTip(self.kontakt, "Unesi ili izaberi kontakt")
        Label(self.tab1, text="Unesi iznos", font=15, bg="#2b306e",
              fg="white").grid(row=10, column=1, columnspan=2, pady=5)
        self.iznos = Entry(self.tab1, width=15,bd=4)
        self.iznos.grid(row=10, column=3, pady=5)
        CreateToolTip(self.iznos, "Unesi iznos")
        ttk.Button(self.tab1, width=15,text="Potvrdi",
                   command=self.validnost).grid(row=11, column=1,
                                                            columnspan=2,
                                                            pady=5)

        ###########################################################
        # Prihod tab
        Label(self.tab2, text="Unesi datum", font=15, bg="#2b306e",
              fg="white").grid(row=0, column=1, columnspan=2, pady=5)
        self.datum_prihod = AutocompleteCombobox(self.tab2, width=12)
        self.datum_prihod.set_completion_list(self.datum_autofil1)
        self.datum_prihod.grid(row=0, column=3, pady=5)
        Label(self.tab2,text="Godina", font=15, bg="#2b306e",
              fg="white").grid(row=1,column=1)
        self.unos_godina1 = Entry(self.tab2, width=6)
        self.unos_godina1.bind('<Key>', lambda event: self.datumunost_prihod(event))
        self.unos_godina1.grid(row=2, column=1)
        Label(self.tab2, text="Mesec", font=15, bg="#2b306e",
              fg="white").grid(row=1, column=2)
        self.unos_meseca1 = ttk.Combobox(self.tab2, width=13, value=self.meseci,
                                        state='readonly')
        self.unos_meseca1.bind('<Key>', lambda event: self.datumunost_prihod(event))
        self.unos_meseca1.grid(row=2, column=2)
        Label(self.tab2, text="Dan", font=15, bg="#2b306e",
              fg="white").grid(row=1, column=3)
        dani = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                '11', '12', '13', '14', '15', '16', '17',
                '18',
                '19', '20', '21',
                '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
        self.unos_dana1 = ttk.Combobox(self.tab2, width=3, state='readonly',value=dani)
        self.unos_dana1.bind('<Key>', lambda event: self.datumunost_prihod(event))
        self.unos_dana1.grid(row=2, column=3)
        Button(self.tab2,text="OK",width=6,command=self.datumunost_prihod).grid(row=2,column=4)
        Label(self.tab2, text="Unesi ime", font=15, bg="#2b306e",
              fg="white").grid(row=3, column=1, columnspan=2, pady=5)
        self.ime_prihod = AutocompleteCombobox(self.tab2, width=15)
        self.ime_prihod.set_completion_list(self.imena1)
        self.ime_prihod.grid(row=3, column=3, pady=5)
        CreateToolTip(self.ime_prihod, "Unesi ili izaberi ime")
        Label(self.tab2, text="Unesi kategoriju", font=15, bg="#2b306e",
              fg="white").grid(row=4, column=1, columnspan=2, pady=5)
        self.kategorija_prihod = AutocompleteCombobox(self.tab2, width=15)
        self.kategorija_prihod.set_completion_list(self.kategorija_autofil1)
        self.kategorija_prihod.grid(row=4, column=3, pady=5)
        CreateToolTip(self.kategorija_prihod, "Unesi ili izaberi kategoriju")
        Label(self.tab2, text="Unesi podkategoriju", font=15, bg="#2b306e",
              fg="white").grid(row=5, column=1, columnspan=2, pady=5)
        self.podkategorija_prihod = AutocompleteCombobox(self.tab2, width=15)
        self.podkategorija_prihod.set_completion_list(
            self.podkategorija_autofil1)
        self.podkategorija_prihod.grid(row=5, column=3, pady=5)
        CreateToolTip(self.podkategorija_prihod,
                      "Unesi ili izaberi podkategoriju")
        Label(self.tab2, text="Izaberi vrstu transakcije", font=15,
              bg="#2b306e", fg="white").grid(row=6, column=1, columnspan=2,
                                             pady=5)
        self.vrsta_transakcije_prihod = ttk.Combobox(self.tab2, width=15,
                                                     state='readonly')
        self.vrsta_transakcije_prihod['value'] = "Prodaja", "Pozajmica"
        self.vrsta_transakcije_prihod.current(newindex=0)
        self.vrsta_transakcije_prihod.grid(row=6, column=3, pady=5)
        CreateToolTip(self.vrsta_transakcije_prihod,
                      "Izaberi vrstu transakcije")
        Label(self.tab2, text="Izaberi vrstu placanja", font=15, bg="#2b306e",
              fg="white").grid(row=7, column=1, columnspan=2, pady=5)
        self.vrsta_placanja_prihod = ttk.Combobox(self.tab2, width=15,
                                                  state='readonly')

        self.vrsta_placanja_prihod[
            'value'] = "Gotovina", "Cek", "Kreditna kartica", "Nalog za uplatu"
        self.vrsta_placanja_prihod.grid(row=7, column=3, pady=5)
        CreateToolTip(self.vrsta_placanja_prihod, "Izaberi vrstu placanja")
        Label(self.tab2, text="Unesi platioca", font=15, bg="#2b306e",
              fg="white").grid(row=8, column=1, columnspan=2, pady=5)
        self.platioc = AutocompleteCombobox(self.tab2, width=15)
        self.platioc.set_completion_list(self.platioc_autofil)
        self.platioc.grid(row=8, column=3, pady=5)
        CreateToolTip(self.platioc, "Unesi ili izaberi platioca vrednosti")
        Label(self.tab2, text="Unesi kontakt", font=15, bg="#2b306e",
              fg="white").grid(row=9, column=1, columnspan=2, pady=5)
        self.kontakt_prihod = AutocompleteCombobox(self.tab2, width=15)
        self.kontakt_prihod.set_completion_list(self.kontakt_autofil1)
        self.kontakt_prihod.grid(row=9, column=3, pady=5)
        CreateToolTip(self.kontakt_prihod, "Unesi ili izaberi kontakt")
        Label(self.tab2, text="Unesi iznos", font=15, bg="#2b306e",
              fg="white").grid(row=10, column=1, columnspan=2, pady=5)
        self.iznos_prihod = Entry(self.tab2, width=15)
        self.iznos_prihod.grid(row=10, column=3, pady=5)
        CreateToolTip(self.iznos_prihod, "Unesi iznos")
        ttk.Button(self.tab2, text="Potvrdi",
                   command=self.validnost1).grid(row=11, column=1,
                                                            columnspan=2,
                                                            pady=5)

        self.dodaj_prozor.mainloop()
    def dani(self,event):
        tridesetjedan = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                '18',
                '19', '20', '21',
                '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
        trideset =['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                '18',
                '19', '20', '21',
                '22', '23', '24', '25', '26', '27', '28', '29', '30']
        dvadesetdevet = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                '18',
                '19', '20', '21',
                '22', '23', '24', '25', '26', '27', '28', '29']
        if self.unos_meseca.get()=="Januar" or self.unos_meseca.get()=="Mart" or self.unos_meseca.get()=="Maj" or self.unos_meseca.get()=="Jul" or self.unos_meseca.get()=="Avgust" or self.unos_meseca.get()=="Oktobar" or self.unos_meseca.get()=="Decembar":
            self.unos_dana['value']=tridesetjedan
        if self.unos_meseca.get()=="April" or self.unos_meseca.get()=="Jul" or self.unos_meseca.get()=="Septembar" or self.unos_meseca.get()=="Novembar":
            self.unos_dana['value']=trideset
        if self.unos_meseca.get()=="Februar":
            self.unos_dana['value']=dvadesetdevet
        if self.unos_meseca1.get() == "Januar" or self.unos_meseca1.get() == "Mart" or self.unos_meseca1.get() == "Maj" or self.unos_meseca1.get() == "Jul" or self.unos_meseca1.get() == "Avgust" or self.unos_meseca1.get() == "Oktobar" or self.unos_meseca1.get() == "Decembar":
            self.unos_dana1['value'] = tridesetjedan
        if self.unos_meseca1.get() == "April" or self.unos_meseca1.get() == "Jul" or self.unos_meseca1.get() == "Septembar" or self.unos_meseca1.get() == "Novembar":
            self.unos_dana1['value'] = trideset
        if self.unos_meseca1.get() == "Februar":
            self.unos_dana1['value'] = dvadesetdevet



    def datumunost(self, event=None):
        if self.datum.get():
            self.datum.delete(0, END)
        if len(self.unos_godina.get()) >= 5:
            messagebox.showerror('greska', 'Godina mora imati 4 broja',
                                 icon='error')
            self.unos_godina.delete(0,END)
        broj = 0
        if self.unos_meseca.get() == "Januar":
            broj = '01'
        elif self.unos_meseca.get() == 'Februar':
            broj = '02'
        elif self.unos_meseca.get() == 'Mart':
            broj = '03'
        elif self.unos_meseca.get() == 'April':
            broj = '04'
        elif self.unos_meseca.get() == 'Maj':
            broj = '05'
        elif self.unos_meseca.get() == 'Jun':
            broj = '06'
        elif self.unos_meseca.get() == 'Jul':
            broj = '07'
        elif self.unos_meseca.get() == 'Avgust':
            broj = '08'
        elif self.unos_meseca.get() == 'Septembar':
            broj = '09'
        elif self.unos_meseca.get() == 'Oktobar':
            broj = '10'
        elif self.unos_meseca.get() == 'Novembar':
            broj = '11'
        elif self.unos_meseca.get() == 'Decembar':
            broj = '12'

        unos = (str(self.unos_godina.get()) + "-" + str(broj) + "-" + str(
            self.unos_dana.get()))
        self.datum.insert(0,unos)
        self.autofil()
    def datumunost_prihod(self, event=None):
        if self.datum_prihod.get():
            self.datum_prihod.delete(0, END)
        if len(self.unos_godina1.get()) >= 5:
            messagebox.showerror('greska', 'Godina mora imati 4 broja',
                                 icon='error')
            self.unos_godina1.delete(0,END)
            self.unos_godina1.delete(0,END)
        broj = 0
        if self.unos_meseca1.get() == "Januar":
            broj = '01'
        elif self.unos_meseca1.get() == 'Februar':
            broj = '02'
        elif self.unos_meseca1.get() == 'Mart':
            broj = '03'
        elif self.unos_meseca1.get() == 'April':
            broj = '04'
        elif self.unos_meseca1.get() == 'Maj':
            broj = '05'
        elif self.unos_meseca1.get() == 'Jun':
            broj = '06'
        elif self.unos_meseca1.get() == 'Jul':
            broj = '07'
        elif self.unos_meseca1.get() == 'Avgust':
            broj = '08'
        elif self.unos_meseca1.get() == 'Septembar':
            broj = '09'
        elif self.unos_meseca1.get() == 'Oktobar':
            broj = '10'
        elif self.unos_meseca1.get() == 'Novembar':
            broj = '11'
        elif self.unos_meseca1.get() == 'Decembar':
            broj = '12'

        unos = (str(self.unos_godina1.get()) + "-" + str(broj) + "-" + str(
            self.unos_dana1.get()))
        self.datum_prihod.insert(0,unos)
        self.autofil()
    def datum_unesen(self):
        if self.datum.get():
            self.datum.delete(0, END)
        if len(self.unos_godina.get()) >= 5:
            messagebox.showerror('greska', 'Godina mora imati 4 broja',
                                 icon='error')
            self.unos_godina.delete(0,END)
        broj = 0
        if self.unos_meseca.get() == "Januar":
            broj = '01'
        elif self.unos_meseca.get() == 'Februar':
            broj = '02'
        elif self.unos_meseca.get() == 'Mart':
            broj = '03'
        elif self.unos_meseca.get() == 'April':
            broj = '04'
        elif self.unos_meseca.get() == 'Maj':
            broj = '05'
        elif self.unos_meseca.get() == 'Jun':
            broj = '06'
        elif self.unos_meseca.get() == 'Jul':
            broj = '07'
        elif self.unos_meseca.get() == 'Avgust':
            broj = '08'
        elif self.unos_meseca.get() == 'Septembar':
            broj = '09'
        elif self.unos_meseca.get() == 'Oktobar':
            broj = '10'
        elif self.unos_meseca.get() == 'Novembar':
            broj = '11'
        elif self.unos_meseca.get() == 'Decembar':
            broj = '12'

        unos = (str(self.unos_godina.get()) + "-" + str(broj) + "-" + str(
            self.unos_dana.get()))
        self.datum.insert(0, unos)
        self.autofil()
    def datum_unesen1(self):
        if self.datum_prihod.get():
            self.datum_prihod.delete(0, END)
        if len(self.unos_godina1.get()) >= 5:
            messagebox.showerror('greska', 'Godina mora imati 4 broja',
                                 icon='error')
            self.unos_godina1.delete(0,END)
        broj = 0
        if self.unos_meseca1.get() == "Januar":
            broj = '01'
        elif self.unos_meseca1.get() == 'Februar':
            broj = '02'
        elif self.unos_meseca1.get() == 'Mart':
            broj = '03'
        elif self.unos_meseca1.get() == 'April':
            broj = '04'
        elif self.unos_meseca1.get() == 'Maj':
            broj = '05'
        elif self.unos_meseca1.get() == 'Jun':
            broj = '06'
        elif self.unos_meseca1.get() == 'Jul':
            broj = '07'
        elif self.unos_meseca1.get() == 'Avgust':
            broj = '08'
        elif self.unos_meseca1.get() == 'Septembar':
            broj = '09'
        elif self.unos_meseca1.get() == 'Oktobar':
            broj = '10'
        elif self.unos_meseca1.get() == 'Novembar':
            broj = '11'
        elif self.unos_meseca1.get() == 'Decembar':
            broj = '12'

        unos = (str(self.unos_godina1.get()) + "-" + str(broj) + "-" + str(
            self.unos_dana1.get()))
        self.datum_prihod.insert(0, unos)
        self.autofil()

    def prikaz_tabela(self):
        if self.opcija3.get() == "Tabela Rashod":
            self.prikazi_vrednosti()
        elif self.opcija3.get() == "Tabela Prihod":
            self.prikazi_vrednosti2()

    def prikazi_vrednosti(self):
        # cleaning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        upit = 'SELECT * FROM rashod'
        db_rows = self.pokreni_upit(upit)
        i = 0
        for row in db_rows:
            if i % 2 == 0:
                self.tree.insert('', 0, text=row[0], values=(row[1:20]),
                                 tags=('evenrow',))
            else:
                self.tree.insert('', 0, text=row[0], values=(row[1:20]),
                                 tags=('oddrow',))
            i += 1

    def prikazi_vrednosti2(self):
        # cleaning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        upit = 'SELECT * FROM prihod'
        db_rows = self.pokreni_upit(upit)
        i = 0
        for row in db_rows:
            if i % 2 == 0:
                self.tree.insert('', 0, text=row[0], values=(row[1:20]),
                                 tags=('evenrow',))
            else:
                self.tree.insert('', 0, text=row[0], values=(row[1:20]),
                                 tags=('oddrow',))
            i += 1

    def dodaj_vrednost_prihod(self):
        try:
            potvrda = messagebox.askquestion("Pitanje", "Sacuvaj vrednosti",
                                             icon="question")
            if potvrda == "yes":
                upit = """INSERT INTO prihod VALUES(NULL,?,?,?,?,?,?,?,?,?) """
                parametri = (self.datum_prihod.get(), self.ime_prihod.get(),
                             self.kategorija_prihod.get(),
                             self.podkategorija_prihod.get(),
                             self.vrsta_transakcije_prihod.get(),
                             self.vrsta_placanja_prihod.get(),
                             self.platioc.get(), self.kontakt_prihod.get(),
                             self.iznos_prihod.get())
                self.pokreni_upit(upit, parametri)
                self.reset()
                self.dodaj_prozor.destroy()

            elif potvrda == "no":
                pass
        except:
            pass
        if self.opcija3.get() == "Tabela Rashod":
            self.prikazi_vrednosti()
        elif self.opcija3.get() == "Tabela Prihod":
            self.prikazi_vrednosti2()
        else:
            pass
        self.autofil()
        self.live_prikaz()
    def validnost(self):
        try:
            iznos = float(self.iznos.get())
        except ValueError:
            iznos = 0
        if len(self.kontakt.get()) == 0:
            self.kontakt.set("Nema kontakt")
        else:
            pass

        if len(self.datum.get()) == 10:
            if len(self.ime.get()) >= 1:
                if len(self.kategorija.get()) >= 1:
                    if len(self.vrsta_transakcije.get()) >= 1:
                        if len(self.vrsta_placanja.get()) >= 1:
                           if len(self.primaoc.get()) >= 1:

                                if iznos > 0:
                                       return self.dodaj_vrednost_rashod()
                                else:
                                        messagebox.showerror("Greska",
                                                             "Nisi uneo iznos ili je on 0\nIznos mora biti veci od 0",
                                                             icon='error')
                           else:
                                    messagebox.showerror("Greska",
                                                         "Nisi upisao ime primaoca\nMoras uneti ime  primaoca ",
                                                         icon='error')

                        else:
                            messagebox.showerror("Greska",
                                                 "Nisi izabrao vrstu placanja\nMoras izabrati vrstu placanja ",
                                                 icon='error')
                    else:
                        messagebox.showerror("Greska",
                                             "Nisi izabrao transkciju\nMoras izabrati transakciju ",
                                             icon='error')
                else:
                    messagebox.showerror("Greska",
                                         "Nisi uneo kategoriju\nMoras uneti kategoriju",
                                         icon='error')
            else:
                messagebox.showerror("Greska",
                                     "Nisi uneo ime\nMoras uneti ime",
                                     icon='error')
        else:
            messagebox.showerror("Greska",
                                 "Nisi uneo datum ili je datum lose unesen ",
                                 icon='error')
    def validnost1(self):
        try:
            iznos = float(self.iznos_prihod.get())
        except ValueError:
            iznos = 0
        if len(self.kontakt.get()) == 0:
            self.kontakt_prihod.set("Nema kontakt")
        else:
            pass

        if len(self.datum_prihod.get()) == 10:
            if len(self.ime_prihod.get()) >= 1:
                if len(self.kategorija_prihod.get()) >= 1:
                    if len(self.vrsta_transakcije_prihod.get()) >= 1:
                        if len(self.vrsta_placanja_prihod.get()) >= 1:
                           if len(self.platioc.get()) >= 1:

                                if iznos > 0:
                                       return self.dodaj_vrednost_prihod()
                                else:
                                        messagebox.showerror("Greska",
                                                             "Nisi uneo iznos ili je on 0\nIznos mora biti veci od 0",
                                                             icon='error')
                           else:
                                    messagebox.showerror("Greska",
                                                         "Nisi upisao ime primaoca\nMoras uneti ime  primaoca ",
                                                         icon='error')

                        else:
                            messagebox.showerror("Greska",
                                                 "Nisi izabrao vrstu placanja\nMoras izabrati vrstu placanja ",
                                                 icon='error')
                    else:
                        messagebox.showerror("Greska",
                                             "Nisi izabrao transkciju\nMoras izabrati transakciju ",
                                             icon='error')
                else:
                    messagebox.showerror("Greska",
                                         "Nisi uneo kategoriju\nMoras uneti kategoriju",
                                         icon='error')
            else:
                messagebox.showerror("Greska",
                                     "Nisi uneo ime\nMoras uneti ime",
                                     icon='error')
        else:
            messagebox.showerror("Greska",
                                 "Nisi uneo datum ili je datum lose unesen ",
                                 icon='error')

    def dodaj_vrednost_rashod(self):
        try:
            potvrda = messagebox.askquestion("Pitanje",
                                             "Da li zelis da sacuvas vrednost?",
                                             icon="info")
            if potvrda == "yes":

                upit = """INSERT INTO rashod  VALUES(NULL,?,?,?,?,?,?,?,?,?) """
                parametri = (
                    self.datum.get(), self.ime.get(), self.kategorija.get(),
                    self.podkategorija.get(), self.vrsta_transakcije.get(),
                    self.vrsta_placanja.get(), self.primaoc.get(),
                    self.kontakt.get(),
                    self.iznos.get())
                self.pokreni_upit(upit, parametri)
                self.dodaj_prozor.destroy()
                self.reset()

                # self.dodaj_prozor.destroy()
            elif potvrda == "no":
                pass
        except:
            pass
        if self.opcija3.get() == "Tabela Rashod":
            self.prikazi_vrednosti()
        elif self.opcija3.get() == "Tabela Prihod":
            self.prikazi_vrednosti2()
        else:
            pass
        self.autofil()
        self.live_prikaz()

    def izbrisi_vrednosti(self):
        try:
            var = self.tree.item(self.tree.selection())["text"]
            var = self.tree.item(self.tree.selection())["values"][0]
        except IndexError as e:
            messagebox.showerror("Upozorenje",
                                 "Nisi izabrao vrednost koju brises",
                                 icon="error")
            return
        id = self.tree.item(self.tree.selection())["text"]
        if self.opcija3.get() == "Tabela Rashod":
            upit = ("DELETE  FROM {} WHERE id =? ").format('rashod')
            self.pokreni_upit(upit, (id,))
            self.prikazi_vrednosti()
        elif self.opcija3.get() == "Tabela Prihod":
            upit = ("DELETE  FROM {} WHERE id =? ").format('prihod')
            self.pokreni_upit(upit, (id,))
            self.prikazi_vrednosti2()
        else:
            pass
        self.autofil()
        self.live_prikaz()
        self.reset()

    def promeni_vrednosti(self):
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            messagebox.showwarning("Upozorenje ",
                                   "Nisi izabrao kolonu koju menjas",
                                   icon='warning')
            return
        self.prozor_promeni = Tk()
        self.prozor_promeni.title("Promeni vrednosti")
        self.prozor_promeni.geometry("600x400")
        self.prozor_promeni.wm_iconbitmap('slike/emblem-money-2.ico')
        self.prozor_promeni.configure(bg="#2b306e")
        idi = self.tree.item(self.tree.selection())["text"]
        Label(self.prozor_promeni, text="Broj ID-a koji je izabran").grid(
            row=22, column=0)
        self.broj = Entry(self.prozor_promeni,
                          textvariable=StringVar(self.prozor_promeni, value=
                          self.tree.item(self.tree.selection())["text"]),
                          state="readonly")
        self.broj.grid(row=24, column=1)
        staro = self.tree.item(self.tree.selection())['values'][0]
        staro1 = self.tree.item(self.tree.selection())['values'][1]
        staro2 = self.tree.item(self.tree.selection())['values'][2]
        staro3 = self.tree.item(self.tree.selection())['values'][3]
        staro4 = self.tree.item(self.tree.selection())['values'][4]
        staro5 = self.tree.item(self.tree.selection())['values'][5]
        staro6 = self.tree.item(self.tree.selection())['values'][6]
        staro7 = self.tree.item(self.tree.selection())['values'][7]
        staro8 = self.tree.item(self.tree.selection())['values'][8]

        Label(self.prozor_promeni, text="Datum", font=15, bg="#2b306e",
              fg="white").grid(row=0, column=4)
        Label(self.prozor_promeni, text="Ime", font=15, bg="#2b306e",
              fg="white").grid(row=3, column=4)
        Label(self.prozor_promeni, text="Kategorija", font=15, bg="#2b306e",
              fg="white").grid(row=4, column=4)
        Label(self.prozor_promeni, text="Podkategorija", font=15, bg="#2b306e",
              fg="white").grid(row=5, column=4)
        Label(self.prozor_promeni, text="Vrsta transkacije", font=15,
              bg="#2b306e", fg="white").grid(row=6, column=4)
        Label(self.prozor_promeni, text="Vrsta placanja", font=15,
              bg="#2b306e", fg="white").grid(row=7, column=4)
        Label(self.prozor_promeni, text="Primaoc/Platioc", font=15,
              bg="#2b306e", fg="white").grid(row=8, column=4)
        Label(self.prozor_promeni, text="Kontakt", font=15, bg="#2b306e",
              fg="white").grid(row=9, column=4)
        Label(self.prozor_promeni, text="Iznos", font=15, bg="#2b306e",
              fg="white").grid(row=10, column=4)

        Entry(self.prozor_promeni,
              textvariable=StringVar(self.prozor_promeni, value=staro),
              state='readonly').grid(row=0, column=5)
        Entry(self.prozor_promeni,
              textvariable=StringVar(self.prozor_promeni, value=staro1),
              state='readonly').grid(row=3, column=5)
        Entry(self.prozor_promeni,
              textvariable=StringVar(self.prozor_promeni, value=staro2),
              state='readonly').grid(row=4, column=5)
        Entry(self.prozor_promeni,
              textvariable=StringVar(self.prozor_promeni, value=staro3),
              state='readonly').grid(row=5, column=5)
        Entry(self.prozor_promeni,
              textvariable=StringVar(self.prozor_promeni, value=staro4),
              state='readonly').grid(row=6, column=5)
        Entry(self.prozor_promeni,
              textvariable=StringVar(self.prozor_promeni, value=staro5),
              state='readonly').grid(row=7, column=5)
        Entry(self.prozor_promeni,
              textvariable=StringVar(self.prozor_promeni, value=staro6),
              state='readonly').grid(row=8, column=5)
        Entry(self.prozor_promeni,
              textvariable=StringVar(self.prozor_promeni, value=staro7),
              state='readonly').grid(row=9, column=5)
        Entry(self.prozor_promeni,
              textvariable=StringVar(self.prozor_promeni, value=staro8),
              state='readonly').grid(row=10, column=5)
        Label(self.prozor_promeni, text="Novi datum", font=15, bg="#2b306e",
              fg="white").grid(row=0, column=0, pady=5, sticky=W)
        self.datum_promena = AutocompleteCombobox(self.prozor_promeni, width=12)
        self.datum_promena.set_completion_list(self.datumi_autofil)
        self.datum_promena['value']=self.daj_upit("SELECT datum from rashod group by datum union all SELECT datum from prihod group by datum")
        self.datum_promena.grid(row=0, column=1, pady=5, sticky=W)
        Label(self.prozor_promeni, text="Godina", font=15, bg="#2b306e",
              fg="white").grid(row=1, column=0,sticky=W)
        self.unos_godina_promena = Entry(self.prozor_promeni, width=6)
        self.unos_godina_promena.bind('<Key>', lambda event: self.datumunost_promena(event))
        self.unos_godina_promena.grid(row=2, column=0,sticky=W)
        Label(self.prozor_promeni, text="Mesec", font=15, bg="#2b306e",
              fg="white").grid(row=1, column=0,padx=10,sticky=E)
        self.unos_meseca_promena = ttk.Combobox(self.prozor_promeni, width=13, value=self.meseci,
                                        state='readonly')
        #self.unos_meseca_promena.bind("<<ComboboxSelected>>", self.dani)
        self.unos_meseca_promena.bind('<Key>', lambda event: self.datumunost_promena(event))
        self.unos_meseca_promena.grid(row=2, column=0,sticky=E)
        dani = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                '11', '12', '13', '14', '15', '16', '17',
                '18',
                '19', '20', '21',
                '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
        Label(self.prozor_promeni,text="Dan",font=15, bg="#2b306e",
              fg="white").grid(row=1,column=1,sticky=W)
        self.unos_dana_promena = ttk.Combobox(self.prozor_promeni, width=3, state='readonly',
                                       value=dani)
        self.unos_dana_promena.bind('<Key>', lambda event: self.datumunost_promena(event))
        self.unos_dana_promena.grid(row=2, column=1,sticky=W,padx=10)
        Button(self.prozor_promeni,text="Ok",width=6,command=self.datum_unesen_promena).grid(row=2,column=1,sticky=E)
        Label(self.prozor_promeni, text="Novo ime", font=15, bg="#2b306e",
              fg="white").grid(row=3, column=0, pady=5, sticky=W)
        self.ime_promena = AutocompleteCombobox(self.prozor_promeni, width=15)
        self.ime_promena.set_completion_list(self.lista_imena)
        self.ime_promena.grid(row=3, column=1, pady=5, sticky=W)
        CreateToolTip(self.ime_promena, "Unesi ili izaberi ime")
        Label(self.prozor_promeni, text="Nova kategorija", font=15,
              bg="#2b306e", fg="white").grid(row=4, column=0, pady=5,
                                             sticky=W)
        self.kategorija_promena = AutocompleteCombobox(self.prozor_promeni,
                                                       width=15)
        self.kategorija_promena.set_completion_list(self.lista_kategorija)
        self.kategorija_promena.grid(row=4, column=1, pady=5, sticky=W)
        CreateToolTip(self.kategorija_promena, "Unesi ili izaberi kategoriju")
        Label(self.prozor_promeni, text="Nova podkategorija", font=15,
              bg="#2b306e", fg="white").grid(row=5, column=0, pady=5,
                                             sticky=W)
        self.podkategorija_promena = AutocompleteCombobox(self.prozor_promeni,
                                                          width=15)
        self.podkategorija_promena.set_completion_list(
            self.lista_podkategorija)
        self.podkategorija_promena.grid(row=5, column=1, pady=5, sticky=W)
        CreateToolTip(self.podkategorija_promena,
                      "Unesi ili izaberi podkategoriju")
        Label(self.prozor_promeni, text="Nova vrsta transakcije", font=15,
              bg="#2b306e", fg="white").grid(row=6, column=0,
                                             pady=5, sticky=W)
        self.vrsta_transakcije_promena = ttk.Combobox(self.prozor_promeni,
                                                      width=15,
                                                      state='readonly')
        self.vrsta_transakcije_promena[
            'value'] = "Kupovina", "Prodaja", "Pozajmica"
        self.vrsta_transakcije_promena.current(newindex=0)
        self.vrsta_transakcije_promena.grid(row=6, column=1, pady=5, sticky=W)
        CreateToolTip(self.vrsta_transakcije_promena,
                      "Izaberi vrstu transakcije")
        Label(self.prozor_promeni, text="Nova vrsta placanja", font=15,
              bg="#2b306e", fg="white").grid(row=7, column=0, pady=5,
                                             sticky=W)
        self.vrsta_placanja_promena = ttk.Combobox(self.prozor_promeni,
                                                   width=15, state='readonly')
        self.vrsta_placanja_promena[
            'value'] = "Gotovina", "Cek", "Kreditna kartica", "Nalog za uplatu"
        self.vrsta_placanja_promena.current(newindex=0)
        self.vrsta_placanja_promena.grid(row=7, column=1, pady=5, sticky=W)
        CreateToolTip(self.vrsta_placanja_promena, "Izaberi vrstu placanja")
        Label(self.prozor_promeni, text="Novi primaoc/platioc", font=15,
              bg="#2b306e", fg="white").grid(row=8, column=0,
                                             pady=5, sticky=W)
        self.primaoc_promena = AutocompleteCombobox(self.prozor_promeni,
                                                    width=15)
        self.primaoc_promena.set_completion_list(self.lista_primaoc_platioc)
        self.primaoc_promena.grid(row=8, column=1, pady=5, sticky=W)
        CreateToolTip(self.primaoc_promena,
                      "Unesi ili izaberi primaoca vrednost")
        Label(self.prozor_promeni, text="Novi kontakt", font=15, bg="#2b306e",
              fg="white").grid(row=9, column=0, pady=5,
                               sticky=W)
        self.kontakt_promena = AutocompleteCombobox(self.prozor_promeni, width=15)
        self.kontakt_promena.set_completion_list(self.kontakti)
        self.kontakt_promena.grid(row=9, column=1, pady=5, sticky=W)
        CreateToolTip(self.kontakt_promena, "Unesi ili izaberi kontakt")
        Label(self.prozor_promeni, text="Novi iznos", font=15, bg="#2b306e",
              fg="white").grid(row=10, column=0, pady=5, sticky=W)
        self.iznos_promena = Entry(self.prozor_promeni, width=15)
        self.iznos_promena.grid(row=10, column=1, pady=5, sticky=W)
        CreateToolTip(self.iznos_promena, "Unesi iznos")

        ttk.Button(self.prozor_promeni, text="Promeni",
                   command=self.validnost_promena).grid(row=12, column=0, pady=15)
        self.prozor_promeni.mainloop()

    def promeni(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = messagebox.askquestion("Sacuvaj vrednosti",
                                            "Da li zelis da sacuvas vrednosti?",
                                            icon='info')

            if result == 'yes':
                if self.opcija3.get() == "Tabela Rashod":
                    cursor.execute(
                        'UPDATE rashod SET datum = ? , ime = ? , kategorija = ?'
                        ' , podkategorija = ? ,vrstatransakcije = ? ,'
                        ' vrstaplacanja = ? , primaoc = ? , kontakt = ? ,'
                        ' iznos = ? WHERE id = ?', (
                            self.datum_promena.get(), self.ime_promena.get(),
                            self.kategorija_promena.get(),
                            self.podkategorija_promena.get(),
                            self.vrsta_transakcije_promena.get(),
                            self.vrsta_placanja_promena.get(),
                            self.primaoc_promena.get(),
                            self.kontakt_promena.get(),
                            self.iznos_promena.get(),
                            self.broj.get()))
                    self.prozor_promeni.destroy()
                    self.reset()
                    cursor.fetchall()
                    cursor.close()
                elif self.opcija3.get() == "Tabela Prihod":
                    cursor.execute(
                        'UPDATE prihod SET datum = ? , ime = ? , kategorija = ? , podkategorija = ? ,'
                        'vrstatransakcije = ? , vrstaplacanja = ? , platioc = ? , kontakt = ? , iznos = ?'
                        ' WHERE id = ?', (
                            self.datum_promena.get(), self.ime_promena.get(),
                            self.kategorija_promena.get(),
                            self.podkategorija_promena.get(),
                            self.vrsta_transakcije_promena.get(),
                            self.vrsta_placanja_promena.get(),
                            self.primaoc_promena.get(),
                            self.kontakt_promena.get(),
                            self.iznos_promena.get(),
                            self.broj.get()))
                    self.prozor_promeni.destroy()
                    self.reset()

                    cursor.fetchall()
                    cursor.close()
            else:
                pass
        if self.opcija3.get() == "Tabela Rashod":
            self.prikazi_vrednosti()
        elif self.opcija3.get() == "Tabela Prihod":
            self.prikazi_vrednosti2()
        else:
            pass
        self.autofil()

        self.live_prikaz()
    def validnost_promena(self):
        try:
            iznos = float(self.iznos_promena.get())
        except ValueError:
            iznos = 0
        if len(self.kontakt_promena.get()) == 0:
            self.kontakt_promena.set("Nema kontakt")
        else:
            pass

        if len(self.datum_promena.get()) == 10:
            if len(self.ime_promena.get()) >= 1:
                if len(self.kategorija_promena.get()) >= 1:
                    if len(self.vrsta_transakcije_promena.get()) >= 1:
                        if len(self.vrsta_placanja_promena.get()) >= 1:
                           if len(self.primaoc_promena.get()) >= 1:

                                if iznos > 0:
                                       return self.promeni()
                                else:
                                        messagebox.showerror("Greska",
                                                             "Nisi uneo iznos ili je on 0\nIznos mora biti veci od 0",
                                                             icon='error')
                           else:
                                    messagebox.showerror("Greska",
                                                         "Nisi upisao ime primaoca\nMoras uneti ime  primaoca ",
                                                         icon='error')

                        else:
                            messagebox.showerror("Greska",
                                                 "Nisi izabrao vrstu placanja\nMoras izabrati vrstu placanja ",
                                                 icon='error')
                    else:
                        messagebox.showerror("Greska",
                                             "Nisi izabrao transkciju\nMoras izabrati transakciju ",
                                             icon='error')
                else:
                    messagebox.showerror("Greska",
                                         "Nisi uneo kategoriju\nMoras uneti kategoriju",
                                         icon='error')
            else:
                messagebox.showerror("Greska",
                                     "Nisi uneo ime\nMoras uneti ime",
                                     icon='error')
        else:
            messagebox.showerror("Greska",
                                 "Nisi uneo datum ili je datum lose unesen ",
                                 icon='error')

    def export_csv_file(self):
        ff = filedialog.asksaveasfilename()
        gg = self.tree.get_children()
        datum, ime, kategorija, podkategorija, vrsta_transakcije, vrsta_placanja, primaoc, kontakt, iznos = [], [], [], [], [], [], [], [], [],
        for i in gg:
            content = self.tree.item(i)
            pp = content['values']
            datum.append(pp[0]), ime.append(pp[1]), kategorija.append(
                pp[2]), podkategorija.append(
                pp[3]), vrsta_transakcije.append(pp[4]), vrsta_placanja.append(
                pp[5]), primaoc.append(pp[6]), kontakt.append(
                pp[7]), iznos.append(pp[8])
        dd = ['Datum', 'Ime', 'Kategorija', 'Podkategorija',
              'Vrsta_transakcije', 'Vrsta_placanja', 'Primaoc', 'Kontakt',
              'Iznos']
        df = pandas.DataFrame(list(
            zip(datum, ime, kategorija, podkategorija, vrsta_transakcije,
                vrsta_placanja,
                primaoc, kontakt, iznos)),
            columns=dd)
        paths = r'{}.csv'.format(ff)

        df.to_csv(paths, index=False)
        messagebox.showinfo('Obavestenje',
                            'Sacuvan je csv fajl {}'.format(paths),
                            icon="info")


    def datumunost_promena(self, event=None):
        if self.datum_promena.get():
            self.datum_promena.delete(0, END)
        if len(self.unos_godina_promena.get()) >= 5:
            messagebox.showerror('greska', 'Godina mora imati 4 broja',
                                 icon='error')
            self.unos_godina_promena.delete(0,END)
        broj = 0
        if self.unos_meseca_promena.get() == "Januar":
            broj = '01'
        elif self.unos_meseca_promena.get() == 'Februar':
            broj = '02'
        elif self.unos_meseca_promena.get() == 'Mart':
            broj = '03'
        elif self.unos_meseca_promena.get() == 'April':
            broj = '04'
        elif self.unos_meseca_promena.get() == 'Maj':
            broj = '05'
        elif self.unos_meseca_promena.get() == 'Jun':
            broj = '06'
        elif self.unos_meseca_promena.get() == 'Jul':
            broj = '07'
        elif self.unos_meseca_promena.get() == 'Avgust':
            broj = '08'
        elif self.unos_meseca_promena.get() == 'Septembar':
            broj = '09'
        elif self.unos_meseca_promena.get() == 'Oktobar':
            broj = '10'
        elif self.unos_meseca_promena.get() == 'Novembar':
            broj = '11'
        elif self.unos_meseca_promena.get() == 'Decembar':
            broj = '12'

        unos = (str(self.unos_godina_promena.get()) + "-" + str(broj) + "-" + str(
            self.unos_dana_promena.get()))
        self.datum_promena.insert(0, unos)
        self.autofil()
    def datum_unesen_promena(self):
        if self.datum_promena.get():
            self.datum_promena.delete(0, END)
        if len(self.unos_godina_promena.get()) >= 5:
            messagebox.showerror('greska', 'Godina mora imati 4 broja',
                                 icon='error')
            self.unos_godina_promena.delete(0,END)
        broj = 0
        if self.unos_meseca_promena.get() == "Januar":
            broj = '01'
        elif self.unos_meseca_promena.get() == 'Februar':
            broj = '02'
        elif self.unos_meseca_promena.get() == 'Mart':
            broj = '03'
        elif self.unos_meseca_promena.get() == 'April':
            broj = '04'
        elif self.unos_meseca_promena.get() == 'Maj':
            broj = '05'
        elif self.unos_meseca_promena.get() == 'Jun':
            broj = '06'
        elif self.unos_meseca_promena.get() == 'Jul':
            broj = '07'
        elif self.unos_meseca_promena.get() == 'Avgust':
            broj = '08'
        elif self.unos_meseca_promena.get() == 'Septembar':
            broj = '09'
        elif self.unos_meseca_promena.get() == 'Oktobar':
            broj = '10'
        elif self.unos_meseca_promena.get() == 'Novembar':
            broj = '11'
        elif self.unos_meseca_promena.get() == 'Decembar':
            broj = '12'

        unos = (str(self.unos_godina_promena.get()) + "-" + str(broj) + "-" + str(
            self.unos_dana_promena.get()))
        self.datum_promena.insert(0, unos)
        self.autofil()


    def combo_opcija1(self, event):
        if self.upit_opcija2.get() == "Kategorija":
            self.upit_vrednost2.delete(0, END)
            self.upit_vrednost2['state'] = 'normal'
            if self.opcija_prihod_rashod2.get() == "Rashod":
                self.upit_vrednost2.set_completion_list(
                    self.kategorija_autofil)
            if self.opcija_prihod_rashod2.get() == "Prihod":
                self.upit_vrednost2.set_completion_list(
                    self.kategorija_autofil1)
        elif self.upit_opcija2.get() == "Vrsta Transakcije":
            self.upit_vrednost2.delete(0, END)
            self.upit_vrednost2['state'] = 'readonly'
            if self.opcija_prihod_rashod2.get() == "Rashod":
                self.upit_vrednost2['value'] = "Kupovina", "Pozajmica"
            if self.opcija_prihod_rashod2.get() == "Prihod":
                self.upit_vrednost2['value'] = "Prodaja", "Pozajmica"
        elif self.upit_opcija2.get() == "Vrsta placanja":
            self.upit_vrednost2.delete(0, END)
            self.upit_vrednost2['state'] = 'readonly'
            self.upit_vrednost2[
                'value'] = "Gotovina", "Cek", "Kreditna kartica", "Nalog za uplatu"
        if self.opcija_prihod_rashod2.get() == "Rashod" and self.upit_opcija2.get() == "Primaoc/Platioc":
            self.upit_vrednost2.delete(0, END)
            self.upit_vrednost2['state'] = 'normal'
            self.upit_vrednost2.set_completion_list(self.primaoc_autofil)
        if self.opcija_prihod_rashod2.get() == "Prihod" and self.upit_opcija2.get() == "Primaoc/Platioc":
            self.upit_vrednost2.delete(0, END)
            self.upit_vrednost2['state'] = 'normal'
            self.upit_vrednost2.set_completion_list(self.platioc_autofil)

    def combo_opcija2(self, event):
        if self.upit_opcija3.get() == "Kategorija":
            self.upit_vrednost3.delete(0, END)
            self.upit_vrednost3['state'] = 'normal'
            if self.opcija_prihod_rashod3.get() == "Rashod":
                self.upit_vrednost3.set_completion_list(
                    self.kategorija_autofil)
            if self.opcija_prihod_rashod3.get() == "Prihod":
                self.upit_vrednost3.set_completion_list(
                    self.kategorija_autofil1)
        elif self.upit_opcija3.get() == "Vrsta Transakcije":
            self.upit_vrednost3.delete(0, END)
            self.upit_vrednost3['state'] = 'readonly'
            if self.opcija_prihod_rashod3.get() == "Rashod":
                self.upit_vrednost3['value'] = "Kupovina", "Pozajmica"
            if self.opcija_prihod_rashod3.get() == "Prihod":
                self.upit_vrednost3['value'] = "Prodaja", "Pozajmica"
        elif self.upit_opcija3.get() == "Vrsta placanja":
            self.upit_vrednost3.delete(0, END)
            self.upit_vrednost3['state'] = 'readonly'
            self.upit_vrednost3[
                'value'] = "Gotovina", "Cek", "Kreditna kartica", "Nalog za uplatu"
        if self.opcija_prihod_rashod3.get() == "Rashod" and self.upit_opcija3.get() == "Primaoc/Platioc":
            self.upit_vrednost3.delete(0, END)
            self.upit_vrednost3['state'] = 'normal'
            self.upit_vrednost3.set_completion_list(self.primaoc_autofil)
        if self.opcija_prihod_rashod3.get() == "Prihod" and self.upit_opcija3.get() == "Primaoc/Platioc":
            self.upit_vrednost3.delete(0, END)
            self.upit_vrednost3['state'] = 'normal'
            self.upit_vrednost3.set_completion_list(self.platioc_autofil)

    def combo_opcija3(self, event):
        if self.upit_opcija8.get() == "Kategorija":
            self.upit_vrednost4.delete(0, END)
            self.upit_vrednost4['state'] = 'normal'
            if self.opcija_prihod_rashod10.get() == "Rashod":
                self.upit_vrednost4.set_completion_list(
                    self.kategorija_autofil)
            if self.opcija_prihod_rashod10.get() == "Prihod":
                self.upit_vrednost4.set_completion_list(
                    self.kategorija_autofil1)
        elif self.upit_opcija8.get() == "Vrsta Transakcije":
            self.upit_vrednost4.delete(0, END)
            self.upit_vrednost4['state'] = 'readonly'
            if self.opcija_prihod_rashod10.get() == "Rashod":
                self.upit_vrednost4['value'] = "Kupovina", "Pozajmica"
            if self.opcija_prihod_rashod10.get() == "Prihod":
                self.upit_vrednost4['value'] = "Prodaja", "Pozajmica"
        elif self.upit_opcija8.get() == "Vrsta placanja":
            self.upit_vrednost4.delete(0, END)
            self.upit_vrednost4['state'] = 'readonly'
            self.upit_vrednost4[
                'value'] = "Gotovina", "Cek", "Kreditna kartica", "Nalog za uplatu"
        if self.opcija_prihod_rashod10.get() == "Rashod" and self.upit_opcija8.get() == "Primaoc/Platioc":
            self.upit_vrednost4.delete(0, END)
            self.upit_vrednost4['state'] = 'normal'
            self.upit_vrednost4.set_completion_list(self.primaoc_autofil)
        if self.opcija_prihod_rashod10.get() == "Prihod" and self.upit_opcija8.get() == "Primaoc/Platioc":
            self.upit_vrednost4.delete(0, END)
            self.upit_vrednost4['state'] = 'normal'
            self.upit_vrednost4.set_completion_list(self.platioc_autofil)

    def combo_opcija4(self, event):
        if self.upit_opcija9.get() == "Kategorija":
            self.upit_vrednost5.delete(0, END)
            self.upit_vrednost5['state'] = 'normal'
            if self.opcija_prihod_rashod8.get() == "Rashod":
                self.upit_vrednost5.set_completion_list(
                    self.kategorija_autofil)
            if self.opcija_prihod_rashod8.get() == "Prihod":
                self.upit_vrednost5.set_completion_list(
                    self.kategorija_autofil1)
        elif self.upit_opcija9.get() == "Vrsta Transakcije":
            self.upit_vrednost5.delete(0, END)
            self.upit_vrednost5['state'] = 'readonly'
            if self.opcija_prihod_rashod8.get() == "Rashod":
                self.upit_vrednost5['value'] = "Kupovina", "Pozajmica"
            if self.opcija_prihod_rashod8.get() == "Prihod":
                self.upit_vrednost5['value'] = "Prodaja", "Pozajmica"
        elif self.upit_opcija9.get() == "Vrsta placanja":
            self.upit_vrednost5.delete(0, END)
            self.upit_vrednost5['state'] = 'readonly'
            self.upit_vrednost5[
                'value'] = "Gotovina", "Cek", "Kreditna kartica", "Nalog za uplatu"
        if self.opcija_prihod_rashod8.get() == "Rashod" and self.upit_opcija9.get() == "Primaoc/Platioc":
            self.upit_vrednost5.delete(0, END)
            self.upit_vrednost5['state'] = 'normal'
            self.upit_vrednost5.set_completion_list(self.primaoc_autofil)
        if self.opcija_prihod_rashod8.get() == "Prihod" and self.upit_opcija9.get() == "Primaoc/Platioc":
            self.upit_vrednost5.delete(0, END)
            self.upit_vrednost5['state'] = 'normal'
            self.upit_vrednost5.set_completion_list(self.platioc_autofil)

    def combo_opcija5(self, event):
        if self.upit_opcija5.get() == "Kategorija":
            self.upit_vrednosti1.delete(0, END)
            self.upit_vrednosti1['state'] = 'normal'
            if self.opcija_prihod_rashod7.get() == "Rashod":
                self.upit_vrednosti1.set_completion_list(
                    self.kategorija_autofil)
            if self.opcija_prihod_rashod7.get() == "Prihod":
                self.upit_vrednosti1.set_completion_list(
                    self.kategorija_autofil1)
        elif self.upit_opcija5.get() == "Vrsta Transakcije":
            self.upit_vrednosti1.delete(0, END)
            self.upit_vrednosti1['state'] = 'readonly'
            if self.opcija_prihod_rashod7.get() == "Rashod":
                self.upit_vrednosti1['value'] = "Kupovina", "Pozajmica"
            if self.opcija_prihod_rashod7.get() == "Prihod":
                self.upit_vrednosti1['value'] = "Prodaja", "Pozajmica"
        elif self.upit_opcija5.get() == "Vrsta placanja":
            self.upit_vrednosti1.delete(0, END)
            self.upit_vrednosti1['state'] = 'readonly'
            self.upit_vrednosti1[
                'value'] = "Gotovina", "Cek", "Kreditna kartica", "Nalog za uplatu"
        if self.opcija_prihod_rashod7.get() == "Rashod" and self.upit_opcija5.get() == "Primaoc/Platioc":
            self.upit_vrednosti1.delete(0, END)
            self.upit_vrednosti1['state'] = 'normal'
            self.upit_vrednosti1.set_completion_list(self.primaoc_autofil)
        if self.opcija_prihod_rashod7.get() == "Prihod" and self.upit_opcija5.get() == "Primaoc/Platioc":
            self.upit_vrednosti1.delete(0, END)
            self.upit_vrednosti1['state'] = 'normal'
            self.upit_vrednosti1.set_completion_list(self.platioc_autofil)

    def combo_opcija6(self, event):
        if self.upit_opcija6.get() == "Kategorija":
            self.upit_vrednosti2.delete(0, END)
            self.upit_vrednosti2['state'] = 'normal'
            if self.opcija_prihod_rashod11.get() == "Rashod":
                self.upit_vrednosti2.set_completion_list(
                    self.kategorija_autofil)
            if self.opcija_prihod_rashod11.get() == "Prihod":
                self.upit_vrednosti2.set_completion_list(
                    self.kategorija_autofil1)
        elif self.upit_opcija6.get() == "Vrsta Transakcije":
            self.upit_vrednosti2.delete(0, END)
            self.upit_vrednosti2['state'] = 'readonly'
            if self.opcija_prihod_rashod11.get() == "Rashod":
                self.upit_vrednosti2['value'] = "Kupovina", "Pozajmica"
            if self.opcija_prihod_rashod11.get() == "Prihod":
                self.upit_vrednosti2['value'] = "Prodaja", "Pozajmica"
        elif self.upit_opcija6.get() == "Vrsta placanja":
            self.upit_vrednosti2.delete(    0, END)
            self.upit_vrednosti2['state'] = 'readonly'
            self.upit_vrednosti2[
                'value'] = "Gotovina", "Cek", "Kreditna kartica", "Nalog za uplatu"
        if self.opcija_prihod_rashod11.get() == "Rashod" and self.upit_opcija6.get() == "Primaoc/Platioc":
            self.upit_vrednosti2.delete(0, END)
            self.upit_vrednosti2['state'] = 'normal'
            self.upit_vrednosti2.set_completion_list(self.primaoc_autofil)
        if self.opcija_prihod_rashod11.get() == "Prihod" and self.upit_opcija6.get() == "Primaoc/Platioc":
            self.upit_vrednosti2.delete(0, END)
            self.upit_vrednosti2['state'] = 'normal'
            self.upit_vrednosti2.set_completion_list(self.platioc_autofil)

    def combo_opcija7(self, event):
        if self.upit_opcija7.get() == "Kategorija":
            self.upit_vrednosti3.delete(0, END)
            self.upit_vrednosti3['state'] = 'normal'
            if self.opcija_prihod_rashod9.get() == "Rashod":
                self.upit_vrednosti3.set_completion_list(
                    self.kategorija_autofil)
            if self.opcija_prihod_rashod9.get() == "Prihod":
                self.upit_vrednosti3.set_completion_list(
                    self.kategorija_autofil1)
        elif self.upit_opcija7.get() == "Vrsta Transakcije":
            self.upit_vrednosti3.delete(0, END)
            self.upit_vrednosti3['state'] = 'readonly'
            if self.opcija_prihod_rashod9.get() == "Rashod":
                self.upit_vrednosti3['value'] = "Kupovina", "Pozajmica"
            if self.opcija_prihod_rashod9.get() == "Prihod":
                self.upit_vrednosti3['value'] = "Prodaja", "Pozajmica"
        elif self.upit_opcija7.get() == "Vrsta placanja":
            self.upit_vrednosti3.delete(0, END)
            self.upit_vrednosti3['state'] = 'readonly'
            self.upit_vrednosti3[
                'value'] = "Gotovina", "Cek", "Kreditna kartica", "Nalog za uplatu"
        if self.opcija_prihod_rashod9.get() == "Rashod" and self.upit_opcija7.get() == "Primaoc/Platioc":
            self.upit_vrednosti3.delete(0, END)
            self.upit_vrednosti3['state'] = 'normal'
            self.upit_vrednosti3.set_completion_list(self.primaoc_autofil)
        if self.opcija_prihod_rashod9.get() == "Prihod" and self.upit_opcija7.get() == "Primaoc/Platioc":
            self.upit_vrednosti3.delete(0, END)
            self.upit_vrednosti3['state'] = 'normal'
            self.upit_vrednosti3.set_completion_list(self.platioc_autofil)

    def combo_opcija8(self, event):
        if self.upit_opcija11.get() == "Kategorija":
            self.upit_vrednost4.delete(0, END)
            self.upit_vrednost5.delete(0, END)
            self.upit_vrednost4['state'] = 'normal'
            self.upit_vrednost5['state'] = 'normal'
            self.upit_vrednosti4.set_completion_list(self.kategorija_autofil)
            self.upit_vrednosti5.set_completion_list(self.kategorija_autofil1)
        elif self.upit_opcija11.get() == "Vrsta Transakcije":
            self.upit_vrednosti4.delete(0, END)
            self.upit_vrednosti5.delete(0, END)
            self.upit_vrednosti4['state'] = 'readonly'
            self.upit_vrednosti5['state'] = 'readonly'
            self.upit_vrednosti4['value'] = "Kupovina", "Pozajmica"
            self.upit_vrednosti5['value'] = "Prodaja", "Pozajmica"

        elif self.upit_opcija11.get() == "Vrsta placanja":
            self.upit_vrednosti4.delete(0, END)
            self.upit_vrednosti5.delete(0, END)
            self.upit_vrednosti4['state'] = 'readonly'
            self.upit_vrednosti5['state'] = 'readonly'
            self.upit_vrednosti4[
                'value'] = "Gotovina", "Cek", "Kreditna kartica", "Nalog za uplatu"
            self.upit_vrednosti5[
                'value'] = "Gotovina", "Cek", "Kreditna kartica", "Nalog za uplatu"
        elif self.upit_opcija11.get() == "Primaoc/Platioc":
            self.upit_vrednosti4.delete(0, END)
            self.upit_vrednosti5.delete(0, END)
            self.upit_vrednosti4['state'] = 'normal'
            self.upit_vrednosti5['state'] = 'normal'
            self.upit_vrednosti4.set_completion_list(self.primaoc_autofil)
            self.upit_vrednosti5.set_completion_list(self.platioc_autofil)

    def combo_opcija9(self, event):
        if self.upit_opcija13.get() == "Kategorija":
            self.upit_vrednosti6['state'] = 'normal'
            self.upit_vrednosti7['state'] = 'normal'
            self.upit_vrednosti6.delete(0, END)
            self.upit_vrednosti7.delete(0, END)
            self.upit_vrednosti6.set_completion_list(self.kategorija_autofil)
            self.upit_vrednosti7.set_completion_list(self.kategorija_autofil1)
        elif self.upit_opcija13.get() == "Vrsta Transakcije":
            self.upit_vrednosti6.delete(0, END)
            self.upit_vrednosti7.delete(0, END)
            self.upit_vrednosti6['state'] = 'readonly'
            self.upit_vrednosti7['state'] = 'readonly'
            self.upit_vrednosti6['value'] = "Kupovina", "Pozajmica"
            self.upit_vrednosti7['value'] = "Prodaja", "Pozajmica"
        elif self.upit_opcija13.get() == "Vrsta placanja":
            self.upit_vrednosti6.delete(0, END)
            self.upit_vrednosti7.delete(0, END)
            self.upit_vrednosti6['state'] = 'readonly'
            self.upit_vrednosti7['state'] = 'readonly'
            self.upit_vrednosti6[
                'value'] = "Gotovina", "Cek", "Kreditna kartica", "Nalog za uplatu"
            self.upit_vrednosti7[
                'value'] = "Gotovina", "Cek", "Kreditna kartica", "Nalog za uplatu"
        elif self.upit_opcija13.get() == "Primaoc/Platioc":
            self.upit_vrednosti6.delete(0, END)
            self.upit_vrednosti7.delete(0, END)
            self.upit_vrednosti6['state'] = 'normal'
            self.upit_vrednosti7['state'] = 'normal'
            self.upit_vrednosti6.set_completion_list(self.primaoc_autofil)
            self.upit_vrednosti7.set_completion_list(self.platioc_autofil)

    def combo_opcija10(self, event):
        if self.upit_opcija14.get() == "Kategorija":
            self.upit_vrednosti8.delete(0, END)
            self.upit_vrednosti9.delete(0, END)
            self.upit_vrednosti8['state'] = 'normal'
            self.upit_vrednosti9['state'] = 'normal'
            self.upit_vrednosti8.set_completion_list(self.kategorija_autofil)
            self.upit_vrednosti9.set_completion_list(self.kategorija_autofil1)
        elif self.upit_opcija14.get() == "Vrsta Transakcije":
            self.upit_vrednosti8.delete(0, END)
            self.upit_vrednosti9.delete(0, END)
            self.upit_vrednosti8['state'] = 'readonly'
            self.upit_vrednosti9['state'] = 'readonly'
            self.upit_vrednosti8['value'] = "Kupovina", "Pozajmica"
            self.upit_vrednosti9['value'] = "Prodaja", "Pozajmica"
        elif self.upit_opcija14.get() == "Vrsta placanja":
            self.upit_vrednosti8.delete(0, END)
            self.upit_vrednosti9.delete(0, END)
            self.upit_vrednosti8['state'] = 'readonly'
            self.upit_vrednosti9['state'] = 'readonly'
            self.upit_vrednosti8[
                'value'] = "Gotovina", "Cek", "Kreditna kartica", "Nalog za uplatu"
            self.upit_vrednosti9[
                'value'] = "Gotovina", "Cek", "Kreditna kartica", "Nalog za uplatu"
        if self.upit_opcija14.get() == "Primaoc/Platioc":
            self.upit_vrednosti8.delete(0, END)
            self.upit_vrednosti9.delete(0, END)
            self.upit_vrednosti8['state'] = 'normal'
            self.upit_vrednosti9['state'] = 'normal'
            self.upit_vrednosti8.set_completion_list(self.primaoc_autofil)
            self.upit_vrednosti9.set_completion_list(self.platioc_autofil)

    def combo_opcija11(self, event):
        if self.upit_opcija4.get() == "Kategorija":
            self.upit_vrednost14.delete(0, END)
            self.upit_vrednost14['state'] = 'normal'
            if self.opcija_prihod_rashod4.get() == "Rashod":
                self.upit_vrednost14.set_completion_list(
                    self.kategorija_autofil)
            elif self.opcija_prihod_rashod4.get() == "Prihod":
                self.upit_vrednost14.set_completion_list(
                    self.kategorija_autofil1)
        if self.upit_opcija4.get() == "Vrsta Transakcije":
            self.upit_vrednost14.delete(0, END)
            self.upit_vrednost14['state']='readonly'
            if self.opcija_prihod_rashod4.get() == "Rashod":
                self.upit_vrednost14.delete(0, END)
                self.upit_vrednost14['state'] = "readonly"
                self.upit_vrednost14['value'] = "Kupovina", "Pozajmica"
            if self.opcija_prihod_rashod4.get() == "Prihod":
                self.upit_vrednost14['value'] = "Prodaja", "Pozajmica"
                self.upit_vrednost14.delete(0, END)
                self.upit_vrednost14['state'] = "readonly"
        if self.upit_opcija4.get() == "Vrsta placanja":
            self.upit_vrednost14.delete(0, END)
            self.upit_vrednost14['state'] = "readonly"
            self.upit_vrednost14[
                'value'] = "Gotovina", "Cek", "Kreditna kartica", "Nalog za uplatu"
        if self.upit_opcija4.get() == "Primaoc/Platioc" and self.opcija_prihod_rashod4.get() == "Rashod":
            self.upit_vrednost14.delete(0, END)
            self.upit_vrednost14['state'] = 'normal'
            self.upit_vrednost14.set_completion_list(self.primaoc_autofil)
        if self.upit_opcija4.get() == "Primaoc/Platioc" and self.opcija_prihod_rashod4.get() == "Prihod":
            self.upit_vrednost14.delete(0, END)
            self.upit_vrednost14['state'] = 'normal'
            self.upit_vrednost14.set_completion_list(self.platioc_autofil)

    def upit1(self):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            try:
                if self.upit_opcija1.get() == "Kategorija":
                    opcija = "kategorija"
                elif self.upit_opcija1.get() == "Vrsta Transakcije":
                    opcija = "vrstatransakcije"
                elif self.upit_opcija1.get() == "Vrsta placanja":
                    opcija = "vrstaplacanja"
                if self.opcija_prihod_rashod.get() == "Rashod":
                    tabela = "rashod"
                    if self.upit_opcija1.get() == "Primaoc/Platioc":
                        opcija = "primaoc"
                if self.opcija_prihod_rashod.get() == "Prihod":
                    tabela = "prihod"
                    if self.upit_opcija1.get() == "Primaoc/Platioc":
                        opcija = "platioc"

                cur.execute(
                    "SELECT  SUM(iznos),"
                    + opcija
                    + " FROM "
                    + tabela
                    + "  group  by "
                    + opcija
                    + "")
                row = cur.fetchall()
                objects = []
                target = []
                [objects.append(i[0]) for i in row]
                [target.append(i[1]) for i in row]
                fig1, axt1 = plt.subplots()
                axt1.pie(objects, labels=objects, autopct='%1.1f%%',
                         shadow=True)
                axt1.axis("equal")
                plt.legend(target)
                plt.show()
            except UnboundLocalError:
                messagebox.showerror("Greska", "Nisi izabrao opciju",
                                     icon="error")

    def upit2(self):
        if self.upitdatum1.get() == "Januar":
            broj = '01'
        elif self.upitdatum1.get() == 'Februar':
            broj = '02'
        elif self.upitdatum1.get() == 'Mart':
            broj = '03'
        elif self.upitdatum1.get() == 'April':
            broj = '04'
        elif self.upitdatum1.get() == 'Maj':
            broj = '05'
        elif self.upitdatum1.get() == 'Jun':
            broj = '06'
        elif self.upitdatum1.get() == 'Jul':
            broj = '07'
        elif self.upitdatum1.get() == 'Avgust':
            broj = '08'
        elif self.upitdatum1.get() == 'Septembar':
            broj = '09'
        elif self.upitdatum1.get() == 'Oktobar':
            broj = '10'
        elif self.upitdatum1.get() == 'Novembar':
            broj = '11'
        elif self.upitdatum1.get() == 'Decembar':
            broj = '12'
        else:
            messagebox.showerror('Greska', 'Nisi izabrao mesec', icon='error')

        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            if self.upit_opcija1_1.get() == "Kategorija":
                opcija = "kategorija"
            elif self.upit_opcija1_1.get() == "Vrsta Transakcije":
                opcija = "vrstatransakcije"
            elif self.upit_opcija1_1.get() == "Vrsta placanja":
                opcija = "vrstaplacanja"
            if self.opcija_prihod_rashod1.get() == "Prihod":
                tabela = "prihod"
            if self.opcija_prihod_rashod1.get() == "Rashod":
                tabela = "rashod"
            if self.opcija_prihod_rashod1.get() == "Rashod" and self.upit_opcija1_1.get() == "Primaoc/Platioc":
                opcija = "primaoc"
            if self.opcija_prihod_rashod1.get() == "Prihod" and self.upit_opcija1_1.get() == "Primaoc/Platioc":
                opcija = "platioc"
            try:
                cur.execute(
                    "SELECT  SUM(iznos)," + opcija + " FROM " + tabela + " where datum LIKE " + "'%-" + broj + "-%'  group  by " + opcija + "")
                row = cur.fetchall()
                objects = []
                target = []
                [objects.append(i[0]) for i in row]
                [target.append(i[1]) for i in row]
                label = (target)
                size = (target)
                fig1, axt1 = plt.subplots()
                axt1.pie(objects, labels=objects, autopct='%1.1f%%',
                         shadow=True)
                # axt1.pie(objects, labels=label, autopct="%1.1f%%", shadow=True, startangle=90)
                axt1.axis("equal")
                plt.legend(target)
                plt.show()
            except UnboundLocalError:
                messagebox.showerror("Greska", "Nisi izabrao opciju",
                                     icon="error")

    def upit3(self):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            if self.upit_opcija2.get() == "Kategorija":
                opcija = "kategorija"
            if self.upit_opcija2.get() == "Vrsta Transakcije":
                opcija = "vrstatransakcije"
            elif self.upit_opcija2.get() == "Vrsta placanja":
                opcija = "vrstaplacanja"
            if self.opcija_prihod_rashod2.get() == "Rashod":
                tabela = "rashod"
            if self.opcija_prihod_rashod2.get() == "Prihod":
                tabela = "prihod"
            if self.opcija_prihod_rashod2.get() == "Rashod" and self.upit_opcija2.get() == "Primaoc/Platioc":
                opcija = "primaoc"
            if self.opcija_prihod_rashod2.get() == "Prihod" and self.upit_opcija2.get() == "Primaoc/Platioc":
                opcija = "platioc"
            if len(self.upit_vrednost2.get()) <= 0:
                plt.close()
            else:
                try:
                    c.execute(
                        "SELECT  iznos,datum," + opcija + " from " + tabela + " where " + opcija + " ='" + self.upit_vrednost2.get() + "' order by datum")
                    objects = []
                    targets = []
                    datum = []
                    for row in c.fetchall():
                        objects.append(row[0])
                        targets.append(row[2])
                        datum.append(row[1])
                    r = (cbook.get_sample_data('goog.npz', np_load=True)[
                             'price_data']
                         .view(np.recarray))
                    fig, (ax1) = plt.subplots(ncols=1, figsize=(8, 4))
                    ax1.plot(datum, objects, 'o-')
                    ax1.set_title(
                        self.upit_opcija2.get() + ": " + self.upit_vrednost2.get())
                    fig.autofmt_xdate()
                    N = len(r)
                    ind = np.arange(N)
                    plt.show()
                except UnboundLocalError:
                    messagebox.showerror("Greska", "Nisi izabrao opciju",
                                         icon="error")


    def upit4(self):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            try:
                if self.upit_opcija3.get() == "Kategorija":
                    opcija = "kategorija"
                if self.upit_opcija3.get() == "Vrsta Transakcije":
                    opcija = "vrstatransakcije"
                elif self.upit_opcija3.get() == "Vrsta placanja":
                    opcija = "vrstaplacanja"
                if self.opcija_prihod_rashod3.get() == "Rashod":
                    tabela = "rashod"
                if self.opcija_prihod_rashod3.get() == "Prihod":
                    tabela = "prihod"
                if self.upit_opcija3.get() == "Primaoc/Platioc" and self.opcija_prihod_rashod3.get() == "Rashod":
                    opcija = "primaoc"
                if self.upit_opcija3.get() == "Primaoc/Platioc" and self.opcija_prihod_rashod3.get() == "Prihod":
                    opcija = "platioc"

                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE'%-01-%' AND " + opcija + " = '" + self.upit_vrednost3.get() + "'")
                row = c.fetchall()
                januarsum = []
                januaravg = []
                [januarsum.append(i[0]) for i in row]
                [januaravg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from  " + tabela + " where datum LIKE'%-02-%' AND " + opcija + " = '" + self.upit_vrednost3.get() + "'")
                row = c.fetchall()
                februarsum = []
                februaravg = []
                [februarsum.append(i[0]) for i in row]
                [februaravg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE'%-03-%' AND " + opcija + " = '" + self.upit_vrednost3.get() + "'")
                row = c.fetchall()
                martsum = []
                martavg = []
                [martsum.append(i[0]) for i in row]
                [martavg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE'%-04-%' AND " + opcija + " = '" + self.upit_vrednost3.get() + "'")
                row = c.fetchall()
                aprilsum = []
                aprilavg = []
                [aprilsum.append(i[0]) for i in row]
                [aprilavg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE'%-05-%' AND " + opcija + " = '" + self.upit_vrednost3.get() + "'")
                row = c.fetchall()
                majsum = []
                majavg = []
                [majsum.append(i[0]) for i in row]
                [majavg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE'%-06-%' AND " + opcija + " = '" + self.upit_vrednost3.get() + "'")
                row = c.fetchall()
                junsum = []
                junavg = []
                [junsum.append(i[0]) for i in row]
                [junavg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE'%-07-%' AND " + opcija + " = '" + self.upit_vrednost3.get() + "'")
                row = c.fetchall()
                julsum = []
                julavg = []
                [julsum.append(i[0]) for i in row]
                [julavg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE'%-08-%' AND " + opcija + " = '" + self.upit_vrednost3.get() + "'")
                row = c.fetchall()
                avgsum = []
                avgavg = []
                [avgsum.append(i[0]) for i in row]
                [avgavg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE'%-09-%' AND " + opcija + " = '" + self.upit_vrednost3.get() + "'")
                row = c.fetchall()
                sepsum = []
                sepavg = []
                [sepsum.append(i[0]) for i in row]
                [sepavg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE'%-10-%' AND " + opcija + " = '" + self.upit_vrednost3.get() + "'")
                row = c.fetchall()
                oktsum = []
                oktavg = []
                [oktsum.append(i[0]) for i in row]
                [oktavg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE'%-11-%' AND " + opcija + " = '" + self.upit_vrednost3.get() + "'")
                row = c.fetchall()
                novsum = []
                novavg = []
                [novsum.append(i[0]) for i in row]
                [novavg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE'%-12-%' AND " + opcija + " = '" + self.upit_vrednost3.get() + "'")
                row = c.fetchall()
                decsum = []
                decavg = []
                [decsum.append(i[0]) for i in row]
                [decavg.append(i[1]) for i in row]

                jan1 = ''.join(map(str, januarsum))
                jan2 = ''.join(map(str, januaravg))
                feb1 = ''.join(map(str, februarsum))
                feb2 = ''.join(map(str, februaravg))
                mar1 = ''.join(map(str, martsum))
                mar2 = ''.join(map(str, martavg))
                apr1 = ''.join(map(str, aprilsum))
                apr2 = ''.join(map(str, aprilavg))
                maj1 = ''.join(map(str, majsum))
                maj2 = ''.join(map(str, majavg))
                jun1 = ''.join(map(str, junsum))
                jun2 = ''.join(map(str, junavg))
                jul1 = ''.join(map(str, julsum))
                jul2 = ''.join(map(str, julavg))
                avg1 = ''.join(map(str, avgsum))
                avg2 = ''.join(map(str, avgavg))
                sep1 = ''.join(map(str, sepsum))
                sep2 = ''.join(map(str, sepavg))
                okt1 = ''.join(map(str, oktsum))
                okt2 = ''.join(map(str, oktavg))
                nov1 = ''.join(map(str, novsum))
                nov2 = ''.join(map(str, novavg))
                dec1 = ''.join(map(str, decsum))
                dec2 = ''.join(map(str, decavg))

                try:
                    sumjan1 = float(jan1)
                except ValueError:
                    sumjan1 = 0
                try:
                    sumjan2 = float(jan2)
                except ValueError:
                    sumjan2 = 0
                try:
                    sumfeb1 = float(feb1)
                except ValueError:
                    sumfeb1 = 0
                try:
                    sumfeb2 = float(feb2)
                except ValueError:
                    sumfeb2 = 0
                try:
                    summar1 = float(mar1)
                except ValueError:
                    summar1 = 0
                try:
                    summar2 = float(mar2)
                except ValueError:
                    summar2 = 0
                try:
                    sumapr1 = float(apr1)
                except ValueError:
                    sumapr1 = 0
                try:
                    sumapr2 = float(apr2)
                except ValueError:
                    sumapr2 = 0
                try:
                    summaj1 = float(maj1)
                except ValueError:
                    summaj1 = 0
                try:
                    summaj2 = float(maj2)
                except ValueError:
                    summaj2 = 0
                try:
                    sumjun1 = float(jun1)
                except ValueError:
                    sumjun1 = 0
                try:
                    sumjun2 = float(jun2)
                except ValueError:
                    sumjun2 = 0
                try:
                    sumjul1 = float(jul1)
                except ValueError:
                    sumjul1 = 0
                try:
                    sumjul2 = float(jul2)
                except ValueError:
                    sumjul2 = 0
                try:
                    sumavg1 = float(avg1)
                except ValueError:
                    sumavg1 = 0
                try:
                    sumavg2 = float(avg2)
                except ValueError:
                    sumavg2 = 0
                try:
                    sumsep1 = float(sep1)
                except ValueError:
                    sumsep1 = 0
                try:
                    sumsep2 = float(sep2)
                except ValueError:
                    sumsep2 = 0
                try:
                    semokt1 = float(okt1)
                except ValueError:
                    semokt1 = 0
                try:
                    semokt2 = float(okt2)
                except ValueError:
                    semokt2 = 0
                try:
                    semnov1 = float(nov1)
                except ValueError:
                    semnov1 = 0
                try:
                    sumnov2 = float(nov2)
                except ValueError:
                    sumnov2 = 0
                try:
                    semdec1 = float(dec1)
                except ValueError:
                    semdec1 = 0
                try:
                    semdec2 = float(dec2)
                except ValueError:
                    semdec2 = 0

                labels = ['Januar', 'Februar', 'Mart', 'April', 'Maj', 'Jun',
                          'Jul', 'Avgust', 'Septembar', 'Oktobar',
                          'Novembar', 'Decembar']
                men_means = [sumjan1, sumfeb1, summar1, sumapr1, summaj1,
                             sumjun1, sumjul1, sumavg1, sumsep1, semokt1,
                             semnov1, semdec1]
                women_means = [sumjan2, sumfeb2, summar2, sumapr2, summaj2,
                               sumjun2, sumjul2, sumavg2, sumsep2, semokt2,
                               sumnov2, semdec2]

                x = np.arange(len(labels))  # the label locations
                width = 0.49  # the width of the bars

                fig, ax = plt.subplots(figsize=(14, 6))
                rects1 = ax.bar(x - width / 2, men_means, width, label='Sum')
                rects2 = ax.bar(x + width / 2, women_means, width, label='Avg')

                # Add some text for labels, title and custom x-axis tick labels, etc.

                ax.set_xticks(x)
                ax.set_xticklabels(labels)
                ax.legend()
                ax.bar_label(rects1, padding=3)
                ax.bar_label(rects2, padding=3)

                fig.tight_layout()
                plt.show()
            except UnboundLocalError:
                messagebox.showerror("Greska", "Nisi izabrao opciju ",
                                     icon="error")

        pass

    def upit5(self):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            if self.opcija_prihod_rashod4.get() == "Rashod":
                tabela = "rashod"
            elif self.opcija_prihod_rashod4.get() == "Prihod":
                tabela = "prihod"
            if self.upit_opcija4.get() == "Kategorija":
                opcija = "kategorija"
            if self.upit_opcija4.get() == "Vrsta transakcije":
                opcija = "vrstatransakcije"
            if self.upit_opcija4.get() == "Vrsta placanja":
                opcija = "vrstaplacanja"
            if self.opcija_prihod_rashod4.get() == "Rashod" and self.upit_opcija4.get() == "Primaoc/Platioc":
                opcija = "primaoc"
            if self.opcija_prihod_rashod4.get() == "Prihod" and self.upit_opcija4.get() == "Primaoc/Platioc":
                opcija = "platioc"
            try:
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE" + "'" + self.upit_godina1.get() + "-01-%' AND " + opcija + "=" + "'" + self.upit_vrednost14.get() + "'")
                row = c.fetchall()
                januarsum = []
                januaravg = []
                [januarsum.append(i[0]) for i in row]
                [januaravg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE" + "'" + self.upit_godina1.get() + "-02-%' AND  " + opcija + "=" + "'" + self.upit_vrednost14.get() + "'")
                row = c.fetchall()
                februarsum = []
                februaravg = []
                [februarsum.append(i[0]) for i in row]
                [februaravg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE" + "'" + self.upit_godina1.get() + "-03-%' AND  " + opcija + "=" + "'" + self.upit_vrednost14.get() + "'")
                martsum = []
                martavg = []
                [martsum.append(i[0]) for i in row]
                [martavg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE" + "'" + self.upit_godina1.get() + "-04-%' AND  " + opcija + "=" + "'" + self.upit_vrednost14.get() + "'")
                row = c.fetchall()
                aprilsum = []
                aprilavg = []
                [aprilsum.append(i[0]) for i in row]
                [aprilavg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE" + "'" + self.upit_godina1.get() + "-05-%' AND  " + opcija + "=" + "'" + self.upit_vrednost14.get() + "'")
                row = c.fetchall()
                majsum = []
                majavg = []
                [majsum.append(i[0]) for i in row]
                [majavg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE" + "'" + self.upit_godina1.get() + "-06-%' AND  " + opcija + "=" + "'" + self.upit_vrednost14.get() + "'")
                row = c.fetchall()
                junsum = []
                junavg = []
                [junsum.append(i[0]) for i in row]
                [junavg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE" + "'" + self.upit_godina1.get() + "-07-%' AND  " + opcija + "=" + "'" + self.upit_vrednost14.get() + "'")
                row = c.fetchall()
                julsum = []
                julavg = []
                [julsum.append(i[0]) for i in row]
                [julavg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE" + "'" + self.upit_godina1.get() + "-08-%' AND  " + opcija + "=" + "'" + self.upit_vrednost14.get() + "'")
                row = c.fetchall()
                avgsum = []
                avgavg = []
                [avgsum.append(i[0]) for i in row]
                [avgavg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE" + "'" + self.upit_godina1.get() + "-09-%' AND  " + opcija + "=" + "'" + self.upit_vrednost14.get() + "'")
                row = c.fetchall()
                sepsum = []
                sepavg = []
                [sepsum.append(i[0]) for i in row]
                [sepavg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE" + "'" + self.upit_godina1.get() + "-10-%' AND  " + opcija + "=" + "'" + self.upit_vrednost14.get() + "'")
                row = c.fetchall()
                oktsum = []
                oktavg = []
                [oktsum.append(i[0]) for i in row]
                [oktavg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE" + "'" + self.upit_godina1.get() + "11-%' AND  " + opcija + "=" + "'" + self.upit_vrednost14.get() + "'")
                row = c.fetchall()
                novsum = []
                novavg = []
                [novsum.append(i[0]) for i in row]
                [novavg.append(i[1]) for i in row]
                c.execute(
                    "SELECT SUM(iznos),AVG(iznos) from " + tabela + " where datum LIKE" + "'" + self.upit_godina1.get() + "-12-%' AND  " + opcija + "=" + "'" + self.upit_vrednost14.get() + "'")
                row = c.fetchall()
                decsum = []
                decavg = []
                [decsum.append(i[0]) for i in row]
                [decavg.append(i[1]) for i in row]

                jan1 = ''.join(map(str, januarsum))
                jan2 = ''.join(map(str, januaravg))
                feb1 = ''.join(map(str, februarsum))
                feb2 = ''.join(map(str, februaravg))
                mar1 = ''.join(map(str, martsum))
                mar2 = ''.join(map(str, martavg))
                apr1 = ''.join(map(str, aprilsum))
                apr2 = ''.join(map(str, aprilavg))
                maj1 = ''.join(map(str, majsum))
                maj2 = ''.join(map(str, majavg))
                jun1 = ''.join(map(str, junsum))
                jun2 = ''.join(map(str, junavg))
                jul1 = ''.join(map(str, julsum))
                jul2 = ''.join(map(str, julavg))
                avg1 = ''.join(map(str, avgsum))
                avg2 = ''.join(map(str, avgavg))
                sep1 = ''.join(map(str, sepsum))
                sep2 = ''.join(map(str, sepavg))
                okt1 = ''.join(map(str, oktsum))
                okt2 = ''.join(map(str, oktavg))
                nov1 = ''.join(map(str, novsum))
                nov2 = ''.join(map(str, novavg))
                dec1 = ''.join(map(str, decsum))
                dec2 = ''.join(map(str, decavg))

                try:
                    sumjan1 = float(jan1)
                except ValueError:
                    sumjan1 = 0
                try:
                    sumjan2 = float(jan2)
                except ValueError:
                    sumjan2 = 0
                try:
                    sumfeb1 = float(feb1)
                except ValueError:
                    sumfeb1 = 0
                try:
                    sumfeb2 = float(feb2)
                except ValueError:
                    sumfeb2 = 0
                try:
                    summar1 = float(mar1)
                except ValueError:
                    summar1 = 0
                try:
                    summar2 = float(mar2)
                except ValueError:
                    summar2 = 0
                try:
                    sumapr1 = float(apr1)
                except ValueError:
                    sumapr1 = 0
                try:
                    sumapr2 = float(apr2)
                except ValueError:
                    sumapr2 = 0
                try:
                    summaj1 = float(maj1)
                except ValueError:
                    summaj1 = 0
                try:
                    summaj2 = float(maj2)
                except ValueError:
                    summaj2 = 0
                try:
                    sumjun1 = float(jun1)
                except ValueError:
                    sumjun1 = 0
                try:
                    sumjun2 = float(jun2)
                except ValueError:
                    sumjun2 = 0
                try:
                    sumjul1 = float(jul1)
                except ValueError:
                    sumjul1 = 0
                try:
                    sumjul2 = float(jul2)
                except ValueError:
                    sumjul2 = 0
                try:
                    sumavg1 = float(avg1)
                except ValueError:
                    sumavg1 = 0
                try:
                    sumavg2 = float(avg2)
                except ValueError:
                    sumavg2 = 0
                try:
                    sumsep1 = float(sep1)
                except ValueError:
                    sumsep1 = 0
                try:
                    sumsep2 = float(sep2)
                except ValueError:
                    sumsep2 = 0
                try:
                    semokt1 = float(okt1)
                except ValueError:
                    semokt1 = 0
                try:
                    semokt2 = float(okt2)
                except ValueError:
                    semokt2 = 0
                try:
                    semnov1 = float(nov1)
                except ValueError:
                    semnov1 = 0
                try:
                    sumnov2 = float(nov2)
                except ValueError:
                    sumnov2 = 0
                try:
                    semdec1 = float(dec1)
                except ValueError:
                    semdec1 = 0
                try:
                    semdec2 = float(dec2)
                except ValueError:
                    semdec2 = 0

                labels = ['Januar', 'Februar', 'Mart', 'April', 'Maj', 'Jun',
                          'Jul', 'Avgust', 'Septembar', 'Oktobar',
                          'Novembar', 'Decembar']
                men_means = [sumjan1, sumfeb1, summar1, sumapr1, summaj1,
                             sumjun1, sumjul1, sumavg1, sumsep1, semokt1,
                             semnov1, semdec1]
                women_means = [sumjan2, sumfeb2, summar2, sumapr2, summaj2,
                               sumjun2, sumjul2, sumavg2, sumsep2, semokt2,
                               sumnov2, semdec2]
                x = np.arange(len(labels))  # the label locations
                width = 0.49  # the width of the bars
                fig, ax = plt.subplots(figsize=(14, 6))
                rects1 = ax.bar(x - width / 2, men_means, width, label='Sum')
                rects2 = ax.bar(x + width / 2, women_means, width, label='Avg')
                ax.set_xticks(x)
                ax.set_xticklabels(labels)
                ax.legend()
                ax.bar_label(rects1, padding=3)
                ax.bar_label(rects2, padding=3)
                fig.tight_layout()
                plt.show()
            except UnboundLocalError:
                messagebox.showerror("Greska", "Nisi izabrao opciju",
                                     icon="error")

    def upit6(self):
        with sqlite3.connect(self.db_name) as conn:
            self.list.delete(0, END)
            if self.opcija_prihod_rashod7.get() == "Rashod":
                tabela = "rashod"
            elif self.opcija_prihod_rashod7.get() == "Prihod":
                tabela = "prihod"
            if self.upit_opcija5.get() == "Kategorija":
                opcija = "kategorija"
            elif self.upit_opcija5.get() == "Vrsta Transakcije":
                opcija = "vrstatransakcije"
            elif self.upit_opcija5.get() == "Vrsta placanja":
                opcija = "vrstaplacanja"
            if self.upit_opcija5.get() == "Primaoc/Platioc" and self.opcija_prihod_rashod7.get() == "Rashod":
                opcija = "primaoc"
            if self.upit_opcija5.get() == "Primaoc/Platioc" and self.opcija_prihod_rashod7.get() == "Prihod":
                opcija = "platioc"
            cur = conn.cursor()
            try:
                cur.execute(
                    "SELECT  DISTINCT ime from " + tabela + " where " + opcija + "= '" + self.upit_vrednosti1.get() + "'")
                row = cur.fetchall()
                objects = []
                [objects.append(i[0]) for i in row]
                for i in objects:
                    self.list.insert(0, i)
            except UnboundLocalError:
                messagebox.showerror("Greska", "Nisi izabrao opciju",
                                     icon="error")

    def upit7(self):
        with sqlite3.connect(self.db_name) as conn:
            self.list.delete(0, END)
            if self.opcija_prihod_rashod11.get() == "Rashod":
                tabela = "rashod"
            elif self.opcija_prihod_rashod11.get() == "Prihod":
                tabela = "prihod"
            if self.upit_opcija6.get() == "Kategorija":
                opcija = "kategorija"
            if self.upit_opcija6.get() == "Vrsta Transakcije":
                opcija = "vrstatransakcije"
            if self.upit_opcija6.get() == "Vrsta placanja":
                opcija = "vrstaplacanja"
            if self.upit_opcija6.get() == "Primaoc/Platioc" and self.opcija_prihod_rashod11.get() == "Rashod":
                opcija = "primaoc"
            if self.upit_opcija6.get() == "Primaoc/Platioc" and self.opcija_prihod_rashod11.get() == "Prihod":
                opcija = "platioc"
            cur = conn.cursor()
            if self.minimum.get():
                try:
                    cur.execute(
                        "SELECT MIN(iznos)  from " + tabela + " where " + opcija + " = '" + self.upit_vrednosti2.get() + "'")
                    row = cur.fetchall()
                    objects = []
                    [objects.append(i[0]) for i in row]
                    self.list.delete(0, END)
                    for i in objects:
                        self.list.insert(0, i)
                except UnboundLocalError:
                    messagebox.showerror("Greska", "Nisi izabrao opciju",
                                         icon="error")

            if self.maximum.get():
                try:
                    cur.execute(
                        "SELECT MAX(iznos)  from " + tabela + " where " + opcija + " = '" + self.upit_vrednosti2.get() + "'")
                    row = cur.fetchall()
                    objects = []
                    [objects.append(i[0]) for i in row]
                    self.list.delete(0, END)
                    for i in objects:
                        self.list.insert(0, i)
                except UnboundLocalError:
                    messagebox.showerror("Greska", "Nisi izabrao opciju",
                                         icon="error")


    def upit8(self):
        with sqlite3.connect(self.db_name) as conn:
            self.list.delete(0, END)
            cur = conn.cursor()
            if self.opcija_prihod_rashod9.get() == "Rashod":
                tabela = "rashod"
            elif self.opcija_prihod_rashod9.get() == "Prihod":
                tabela = "prihod"
            if self.upit_opcija7.get() == "Kategorija":
                opcija = "kategorija"
            elif self.upit_opcija7.get() == "Vrsta Transakcije":
                opcija = "vrstatransakcije"
            elif self.upit_opcija7.get() == "Vrsta placanja":
                opcija = "vrstaplacanja"
            if self.opcija_prihod_rashod9.get() == "Rashod" and self.upit_opcija7.get() == "Primaoc/Platioc":
                opcija = "primaoc"
            if self.opcija_prihod_rashod9.get() == "Prihod" and self.upit_opcija7.get() == "Primaoc/Platioc":
                opcija = "platioc"
            try:
                cur.execute(
                    "SELECT COUNT(" + opcija + ") from " + tabela + " where " + opcija + " ='" + self.upit_vrednosti3.get() + "'")  # "+opcija+" = '" + self.upit_vrednosti3.get() + "'")
                rows = cur.fetchall()
                objects = []
                [objects.append(i[0]) for i in rows]
                for res in objects:
                    self.list.insert(0, res)
            except UnboundLocalError:
                messagebox.showerror("Greska", "Nisi izabrao opciju",
                                     icon="error")

    def upit9(self):
        if self.upit_mesec1.get() == "Januar":
            broj = '01'
        elif self.upit_mesec1.get() == 'Februar':
            broj = '02'
        elif self.upit_mesec1.get() == 'Mart':
            broj = '03'
        elif self.upit_mesec1.get() == 'April':
            broj = '04'
        elif self.upit_mesec1.get() == 'Maj':
            broj = '05'
        elif self.upit_mesec1.get() == 'Jun':
            broj = '06'
        elif self.upit_mesec1.get() == 'Jul':
            broj = '07'
        elif self.upit_mesec1.get() == 'Avgust':
            broj = '08'
        elif self.upit_mesec1.get() == 'Septembar':
            broj = '09'
        elif self.upit_mesec1.get() == 'Oktobar':
            broj = '10'
        elif self.upit_mesec1.get() == 'Novembar':
            broj = '11'
        elif self.upit_mesec1.get() == 'Decembar':
            broj = '12'
        else:
            messagebox.showerror('Greska', 'Nisi izabrao mesec', icon='error')
        records = self.tree_upiti.get_children()
        for element in records:
            self.tree_upiti.delete(element)
        if self.opcija_prihod_rashod10.get() == "Rashod":
            tabela = "rashod"
        elif self.opcija_prihod_rashod10.get() == "Prihod":
            tabela = "prihod"
        if self.upit_opcija8.get() == "Kategorija":
            opcija = "kategorija"
        elif self.upit_opcija8.get() == "Vrsta Transakcije":
            opcija = "vrstatransakcije"
        elif self.upit_opcija8.get() == "Vrsta placanja":
            opcija = "vrstaplacanja"
        if self.upit_opcija8.get() == "Primaoc/Platioc" and self.opcija_prihod_rashod10.get() == "Rashod":
            opcija = "primaoc"
        if self.upit_opcija8.get() == "Primaoc/Platioc" and self.opcija_prihod_rashod10.get() == "Prihod":
            opcija = "platioc"
        try:
            upit = "SELECT * from " + tabela + " where datum LIKE " + "'%-" + broj + "-%' and " + opcija + " =" + "'" + self.upit_vrednost4.get() + "'"
            db_rows = self.pokreni_upit(upit)
            i = 0
            for row in db_rows:
                if i % 2 == 0:
                    self.tree_upiti.insert('', 0, text=row[0],
                                           values=(row[1:20]),
                                           tags=('evenrow',))
                else:
                    self.tree_upiti.insert('', 0, text=row[0],
                                           values=(row[1:20]),
                                           tags=('oddrow',))
                i += 1
        except UnboundLocalError:
            messagebox.showerror("Greska", "Nisi izabrao opciju", icon="error")

    def upit10(self):
        records = self.tree_upiti.get_children()
        for element in records:
            self.tree_upiti.delete(element)
        if self.opcija_prihod_rashod8.get() == "Rashod":
            tabela = "rashod"
        elif self.opcija_prihod_rashod8.get() == "Prihod":
            tabela = "prihod"
        if self.upit_opcija9.get() == "Kategorija":
            opcija = "kategorija"
        elif self.upit_opcija9.get() == "Vrsta Transakcije":
            opcija = "vrstatransakcije"
        elif self.upit_opcija9.get() == "Vrsta placanja":
            opcija = "vrstaplacanja"
        if self.upit_opcija9.get() == "Primaoc/Platioc" and self.opcija_prihod_rashod8.get() == "Rashod":
            opcija = "primaoc"
        if self.upit_opcija9.get() == "Primaoc/Platioc" and self.opcija_prihod_rashod8.get() == "Prihod":
            opcija = "platioc"
        try:
            upit = "SELECT * from " + tabela + " where " + opcija + " = '" + self.upit_vrednost5.get() + "'"
            db_rows = self.pokreni_upit(upit)
            i = 0
            for row in db_rows:
                if i % 2 == 0:
                    self.tree_upiti.insert('', 0, text=row[0],
                                           values=(row[1:20]),
                                           tags=('evenrow',))
                else:
                    self.tree_upiti.insert('', 0, text=row[0],
                                           values=(row[1:20]),
                                           tags=('oddrow',))
                i += 1
        except UnboundLocalError:
            messagebox.showerror("Greska", "Nisi izabrao opciju", icon="error")

    def upit11(self):
        records = self.tree_upiti.get_children()
        for element in records:
            self.tree_upiti.delete(element)
        if self.opcija_prihod_rashod6.get() == "Rashod":
            tabela = "rashod"
        if self.opcija_prihod_rashod6.get() == "Prihod":
            tabela = "prihod"
        try:
            upit = "SELECT * from " + tabela + " where datum " + self.znak.get() + "'" + self.upit_vrednost6.get() + "'"
            db_rows = self.pokreni_upit(upit)
            i = 0
            for row in db_rows:
                if i % 2 == 0:
                    self.tree_upiti.insert('', 0, text=row[0],
                                           values=(row[1:20]),
                                           tags=('evenrow',))
                else:
                    self.tree_upiti.insert('', 0, text=row[0],
                                           values=(row[1:20]),
                                           tags=('oddrow',))
                i += 1
        except sqlite3.OperationalError:
            messagebox.showerror("Greska", "Nisi izabrao datum,znak ili oba",
                                 icon='error')

    def upit12(self):
        records = self.tree_upiti.get_children()
        for element in records:
            self.tree_upiti.delete(element)
        if self.opcija_prihod_rashod12.get() == "Rashod":
            try:
                upit = upit = "SELECT * from rashod where iznos " + self.znak1.get() + "" + self.unos_iznos.get() + ""
                db_rows = self.pokreni_upit(upit)
                i = 0
                for row in db_rows:
                    if i % 2 == 0:
                        self.tree_upiti.insert('', 0, text=row[0],
                                               values=(row[1:20]),
                                               tags=('evenrow',))
                    else:
                        self.tree_upiti.insert('', 0, text=row[0],
                                               values=(row[1:20]),
                                               tags=('oddrow',))
                    i += 1
            except sqlite3.OperationalError:
                pass

        elif self.opcija_prihod_rashod12.get() == "Prihod":
            upit = upit = "SELECT * from prihod where iznos " + self.znak1.get() + "" + self.unos_iznos.get() + ""
            db_rows = self.pokreni_upit(upit)
            i = 0
            for row in db_rows:
                if i % 2 == 0:
                    self.tree_upiti.insert('', 0, text=row[0],
                                           values=(row[1:20]),
                                           tags=('evenrow',))
                else:
                    self.tree_upiti.insert('', 0, text=row[0],
                                           values=(row[1:20]),
                                           tags=('oddrow',))
                i += 1

    def upit13(self):
        if self.upit_mesec2.get() == "Januar":
            broj = '01'
        elif self.upit_mesec2.get() == 'Februar':
            broj = '02'
        elif self.upit_mesec2.get() == 'Mart':
            broj = '03'
        elif self.upit_mesec2.get() == 'April':
            broj = '04'
        elif self.upit_mesec2.get() == 'Maj':
            broj = '05'
        elif self.upit_mesec2.get() == 'Jun':
            broj = '06'
        elif self.upit_mesec2.get() == 'Jul':
            broj = '07'
        elif self.upit_mesec2.get() == 'Avgust':
            broj = '08'
        elif self.upit_mesec2.get() == 'Septembar':
            broj = '09'
        elif self.upit_mesec2.get() == 'Oktobar':
            broj = '10'
        elif self.upit_mesec2.get() == 'Novembar':
            broj = '11'
        elif self.upit_mesec2.get() == 'Decembar':
            broj = '12'

        records = self.tree_upiti.get_children()
        for element in records:
            self.tree_upiti.delete(element)
        if self.opcija_prihod_rashod13.get() == "Rashod":
            tabela = "rashod"
        elif self.opcija_prihod_rashod13.get() == "Prihod":
            tabela = "prihod"
        try:
            upit = "SELECT * from " + tabela + " where datum LIKE " + "'" + \
                   self.upit_godina2.get() + "-" + broj + "-%' "
            db_rows = self.pokreni_upit(upit)
            i = 0
            for row in db_rows:
                if i % 2 == 0:
                    self.tree_upiti.insert('', 0, text=row[0],
                                           values=(row[1:20]),
                                           tags=('evenrow',))
                else:
                    self.tree_upiti.insert('', 0, text=row[0],
                                           values=(row[1:20]),
                                           tags=('oddrow',))
                i += 1
        except UnboundLocalError:
            messagebox.showerror('Greska', 'Nisi izabrao mesec', icon='error')

    def upit14(self):
        if self.upit_mesec3.get() == "Januar":
            broj = '01'
        elif self.upit_mesec3.get() == 'Februar':
            broj = '02'
        elif self.upit_mesec3.get() == 'Mart':
            broj = '03'
        elif self.upit_mesec3.get() == 'April':
            broj = '04'
        elif self.upit_mesec3.get() == 'Maj':
            broj = '05'
        elif self.upit_mesec3.get() == 'Jun':
            broj = '06'
        elif self.upit_mesec3.get() == 'Jul':
            broj = '07'
        elif self.upit_mesec3.get() == 'Avgust':
            broj = '08'
        elif self.upit_mesec3.get() == 'Septembar':
            broj = '09'
        elif self.upit_mesec3.get() == 'Oktobar':
            broj = '10'
        elif self.upit_mesec3.get() == 'Novembar':
            broj = '11'
        elif self.upit_mesec3.get() == 'Decembar':
            broj = '12'
        else:
            messagebox.showerror('Greska', 'Nisi izabrao mesec', icon='error')
        with sqlite3.connect(self.db_name) as conn:
            self.list.delete(0, END)
            cur = conn.cursor()
            if self.opcija_prihod_rashod14.get() == "Rashod":
                tabela = "rashod"
            elif self.opcija_prihod_rashod14.get() == "Prihod":
                tabela = "prihod"
            if self.check_var1.get():
                try:
                    cur.execute(
                        "SELECT MIN(iznos) from " + tabela + " where datum LIKE '%-" + broj + "-%'")
                    rows = cur.fetchall()
                    objects = []
                    [objects.append(i[0]) for i in rows]
                    for res in objects:
                        self.list.insert(0, res)
                except UnboundLocalError:
                    messagebox.showerror("Greska","Nisi izabrao mesec!!!",icon="error")
            elif self.check_var2.get():
                try:
                    cur.execute(
                        "SELECT MAX(iznos) from " + tabela + " where datum LIKE '%-" + broj + "-%'")
                    rows = cur.fetchall()
                    objects = []
                    [objects.append(i[0]) for i in rows]
                    for res in objects:
                        self.list.insert(0, res)
                except UnboundLocalError:
                    messagebox.showerror("Greska","Nisi izabrao mesec!!!",icon="error")


    def upit15(self):
        with sqlite3.connect(self.db_name) as conn:
            self.list.delete(0, END)
            cur = conn.cursor()
            if self.upit_mesec4.get() == "Januar":
                broj = '01'
            elif self.upit_mesec4.get() == 'Februar':
                broj = '02'
            elif self.upit_mesec4.get() == 'Mart':
                broj = '03'
            elif self.upit_mesec4.get() == 'April':
                broj = '04'
            elif self.upit_mesec4.get() == 'Maj':
                broj = '05'
            elif self.upit_mesec4.get() == 'Jun':
                broj = '06'
            elif self.upit_mesec4.get() == 'Jul':
                broj = '07'
            elif self.upit_mesec4.get() == 'Avgust':
                broj = '08'
            elif self.upit_mesec4.get() == 'Septembar':
                broj = '09'
            elif self.upit_mesec4.get() == 'Oktobar':
                broj = '10'
            elif self.upit_mesec4.get() == 'Novembar':
                broj = '11'
            elif self.upit_mesec4.get() == 'Decembar':
                broj = '12'
            else:
                messagebox.showerror('Greska', 'Nisi izabrao mesec',
                                     icon='error')
            if self.opcija_prihod_rashod15.get() == "Rashod":
                tabela = "rashod"
            elif self.opcija_prihod_rashod15.get() == "Prihod":
                tabela = "prihod"
            if self.upit_opcija10.get() == "Kategorija":
                opcija = "kategorija"
            elif self.upit_opcija10.get() == "Vrsta Transakcije":
                opcija = "vrstatransakcije"
            elif self.upit_opcija10.get() == "Vrsta placanja":
                opcija = "vrstaplacanja"
            elif self.upit_opcija10.get() == "Primaoc/Platioc" and self.opcija_prihod_rashod15.get() == "Rashod":
                opcija = "primaoc"
            elif self.upit_opcija10.get() == "Primaoc/Platioc" and self.opcija_prihod_rashod15.get() == "Prihod":
                opcija = "platioc"
            try:
                cur.execute(
                    "SELECT " + opcija + " from " + tabela + " where datum LIKE '%-" + broj + "-%'")
                rows = cur.fetchall()
                objects = []
                [objects.append(i[0]) for i in rows]
                for res in objects:
                    self.list.insert(0, res)
            except UnboundLocalError:
                messagebox.showerror("Greska", "Nisi izabrao opciju",
                                     icon="error")

    def upit16(self):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT SUM(iznos) from rashod union all SELECT SUM(iznos) from prihod")
            row = cur.fetchall()
            objects = []
            [objects.append(i[0]) for i in row]
            fig1, axt1 = plt.subplots()
            axt1.pie(objects, labels=objects, autopct='%1.1f%%', shadow=True)
            axt1.axis("equal")
            plt.legend()
            plt.show()

    def upit17(self):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            if self.upit_opcija11.get() == "Kategorija":
                opcija = "kategorija"
                opcija1 = "kategorija"
            elif self.upit_opcija11.get() == "Vrsta Transakcije":
                opcija = "vrstatransakcije"
                opcija1 = "vrstatransakcije"
            elif self.upit_opcija11.get() == "Vrsta placanja":
                opcija = "vrstaplacanja"
                opcija1 = "vrstaplacanja"
            if self.upit_opcija11.get() == "Primaoc/Platioc":
                opcija = "primaoc"
                opcija1 = "platioc"
            try:
                cur.execute(
                    "SELECT SUM(iznos)," + opcija + " from rashod where " + opcija + " = '" + self.upit_vrednosti4.get() + "' union all SELECT SUM(iznos)," + opcija1 + " from prihod where " + opcija1 + "= '" + self.upit_vrednosti5.get() + "'")
                row = cur.fetchall()
                objects = []
                target = []
                [objects.append(i[0]) for i in row]
                [target.append(i[1]) for i in row]
                label = (objects)
                # print(objects,target)
                size = (target)
                fig1, axt1 = plt.subplots()
                try:
                   axt1.pie(objects, labels=objects, autopct='%1.1f%%',
                         shadow=True)


                # axt1.pie(objects, labels=label, autopct="%1.1f%%", shadow=True, startangle=90)
                   axt1.axis("equal")
                   plt.legend(target)
                   plt.show()

                except ValueError:
                    messagebox.showerror("Greska", "Nisi izabrao vrednosti\n"
                                   "ili jedna od vrednosti nije validna")
                    plt.close()
            except UnboundLocalError:
                messagebox.showerror("Greska","Nisi izabrao opciju!!!",icon="error")



    def upit18(self):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            try:
                cur.execute(
                    "SELECT SUM(iznos),datum from rashod where datum = '" + self.upit_datum2.get() + "' union all SELECT SUM(iznos),datum from prihod where datum = '" + self.upit_datum3.get() + "'")
                row = cur.fetchall()
                objects = []
                target = []
                [objects.append(i[0]) for i in row]
                [target.append(i[1]) for i in row]
                fig1, axt1 = plt.subplots()
                axt1.pie(objects, labels=objects, autopct='%1.1f%%',
                         shadow=True)
                axt1.axis("equal")
                plt.legend(target)
                plt.show()
            except ValueError:
                messagebox.showerror("Greska",
                                     "Nisi izabrao datum ili datume!",
                                     icon="error")
                plt.close()


    def upit19(self):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            if self.upit_opcija13.get() == "Kategorija":
                opcija = "kategorija"
                opcija1 = "kategorija"
            elif self.upit_opcija13.get() == "Vrsta Transakcije":
                opcija = "vrstatransakcije"
                opcija1 = "vrstatransakcije"
            elif self.upit_opcija13.get() == "Vrsta placanja":
                opcija = "vrstaplacanja"
                opcija1 = "vrstaplacanja"
            if self.upit_opcija13.get() == "Primaoc/Platioc":
                opcija = "primaoc"
                opcija1 = "platioc"
            try:
                c.execute(
                    "SELECT AVG(iznos) from rashod where datum LIKE'%-01-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                januaravg = []
                [januaravg.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from prihod where datum LIKE'%-01-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                januaravg1 = []
                [januaravg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from rashod where datum LIKE'%-02-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                februaravg = []
                [februaravg.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from prihod where datum LIKE'%-02-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                februaravg1 = []
                [februaravg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from rashod where datum LIKE'%-03-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                martavg = []
                [martavg.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from prihod where datum LIKE'%-03-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                martavg1 = []
                [martavg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from rashod where datum LIKE'%-04-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                aprilavg = []
                [aprilavg.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from prihod where datum LIKE'%-04-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                aprilavg1 = []
                [aprilavg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from rashod where datum LIKE'%-05-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                majavg = []
                [majavg.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from prihod where datum LIKE'%-05-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                majavg1 = []
                [majavg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from rashod where datum LIKE'%-06-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                junavg = []
                [junavg.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from prihod where datum LIKE'%-06-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                junavg1 = []
                [junavg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from rashod where datum LIKE'%-07-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                julavg = []
                [julavg.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from prihod where datum LIKE'%-07-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                julavg1 = []
                [julavg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from rashod where datum LIKE'%-08-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                avgustavg = []
                [avgustavg.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from prihod where datum LIKE'%-08-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                avgustavg1 = []
                [avgustavg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from rashod where datum LIKE'%-09-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                septembaravg = []
                [septembaravg.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from prihod where datum LIKE'%-09-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                septembaravg1 = []
                [septembaravg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from rashod where datum LIKE'%-10-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                oktobaravg = []
                [oktobaravg.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from prihod where datum LIKE'%-10-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                oktobaravg1 = []
                [oktobaravg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from rashod where datum LIKE'%-11-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                novembaravg = []
                [novembaravg.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from prihod where datum LIKE'%-11-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                novembaravg1 = []
                [novembaravg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from rashod where datum LIKE'%-12-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                decembaravg = []
                [decembaravg.append(i[0]) for i in row]
                c.execute(
                    "SELECT AVG(iznos) from prihod where datum LIKE'%-12-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                decembaravg1 = []
                [decembaravg1.append(i[0]) for i in row]

                jan = ''.join(map(str, januaravg))
                jan1 = ''.join(map(str, januaravg1))
                feb = ''.join(map(str, februaravg))
                feb1 = ''.join(map(str, februaravg1))
                mar = ''.join(map(str, martavg))
                mar1 = ''.join(map(str, martavg1))
                apr = ''.join(map(str, aprilavg))
                apr1 = ''.join(map(str, aprilavg1))
                maj = ''.join(map(str, majavg))
                maj1 = ''.join(map(str, majavg1))
                jun = ''.join(map(str, junavg))
                jun1 = ''.join(map(str, junavg1))
                jul = ''.join(map(str, julavg))
                jul1 = ''.join(map(str, julavg1))
                avg = ''.join(map(str, avgustavg))
                avg1 = ''.join(map(str, avgustavg1))
                sep = ''.join(map(str, septembaravg))
                sep1 = ''.join(map(str, septembaravg1))
                okt = ''.join(map(str, oktobaravg))
                okt1 = ''.join(map(str, oktobaravg1))
                nov = ''.join(map(str, novembaravg))
                nov1 = ''.join(map(str, novembaravg1))
                dec = ''.join(map(str, decembaravg))
                dec1 = ''.join(map(str, decembaravg1))

                try:
                    avgjan = float(jan)
                except ValueError:
                    avgjan = 0
                try:
                    avgjan1 = float(jan1)
                except ValueError:
                    avgjan1 = 0
                try:
                    avgfeb = float(feb)
                except ValueError:
                    avgfeb = 0
                try:
                    avgfeb1 = float(feb1)
                except ValueError:
                    avgfeb1 = 0
                try:
                    avgmar = float(mar)
                except ValueError:
                    avgmar = 0
                try:
                    avgmar1 = float(mar1)
                except ValueError:
                    avgmar1 = 0
                try:
                    avgapr = float(apr)
                except ValueError:
                    avgapr = 0
                try:
                    avgapr1 = float(apr1)
                except ValueError:
                    avgapr1 = 0
                try:
                    avgmaj = float(maj)

                except ValueError:
                    avgmaj = 0
                try:
                    avgmaj1 = float(maj1)
                except ValueError:
                    avgmaj1 = 0
                try:
                    avgjun = float(jun)
                except ValueError:
                    avgjun = 0
                try:
                    avgjun1 = float(jun1)
                except ValueError:
                    avgjun1 = 0
                try:
                    avgjul = float(jul)
                except ValueError:
                    avgjul = 0
                try:
                    avgjul1 = float(jul1)
                except ValueError:
                    avgjul1 = 0
                try:
                    avgavg = float(avg)
                except ValueError:
                    avgavg = 0
                try:
                    avgavg1 = float(avg1)
                except ValueError:
                    avgavg1 = 0
                try:
                    avgsep = float(sep)
                except ValueError:
                    avgsep = 0
                try:
                    avgsep1 = float(sep1)
                except ValueError:
                    avgsep1 = 0
                try:
                    avgokt = float(okt)
                except ValueError:
                    avgokt = 0
                try:
                    avgokt1 = float(okt1)
                except ValueError:
                    avgokt1 = 0
                try:
                    avgnov = float(nov)
                except ValueError:
                    avgnov = 0
                try:
                    avgnov1 = float(nov1)
                except ValueError:
                    avgnov1 = 0
                try:
                    avgdec = float(dec)
                except ValueError:
                    avgdec = 0
                try:
                    avgdec1 = float(dec1)
                except ValueError:
                    avgdec1 = 0

                labels = ['Januar', 'Februar', 'Mart', 'April', 'Maj', 'Jun',
                          'Jul', 'Avgust', 'Septembar', 'Oktobar',
                          'Novembar', 'Decembar']
                prosek = [avgjan, avgfeb, avgmar, avgapr, avgmaj, avgjun,
                          avgjul, avgavg, avgsep, avgokt, avgnov, avgdec]
                prosek1 = [avgjan1, avgfeb1, avgmar1, avgapr1, avgmaj1,
                           avgjun1,
                           avgjul1, avgavg1, avgsep1, avgokt1, avgnov1,
                           avgdec1]
                x = np.arange(len(labels))  # the label locations
                width = 0.49  # the width of the bars

                fig, ax = plt.subplots(figsize=(14, 6))
                rects1 = ax.bar(x - width / 2, prosek, width,
                                label='Avg rashod')
                rects2 = ax.bar(x + width / 2, prosek1, width,
                                label='Avg prihod')

                # Add some text for labels, title and custom x-axis tick labels, etc.
                ax.set_ylabel('')
                ax.set_title('Rezultati')
                ax.set_xticks(x)
                ax.set_xticklabels(labels)
                ax.legend()
                ax.bar_label(rects1, padding=3)
                ax.bar_label(rects2, padding=3)

                fig.tight_layout()

                plt.show()
            except UnboundLocalError:
                messagebox.showerror("Greska",
                                     "Nisi izabrao opciju ili opcije",
                                     icon="error")

    def upit20(self):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            if self.upit_opcija13.get() == "Kategorija":
                opcija = "kategorija"
                opcija1 = "kategorija"
            elif self.upit_opcija13.get() == "Vrsta Transakcije":
                opcija = "vrstatransakcije"
                opcija1 = "vrstatransakcije"
            elif self.upit_opcija13.get() == "Vrsta placanja":
                opcija = "vrstaplacanja"
                opcija1 = "vrstaplacanja"
            if self.upit_opcija13.get() == "Primaoc/Platioc":
                opcija = "primaoc"
                opcija1 = "platioc"
            try:
                c.execute(
                    "SELECT SUM(iznos) from rashod where datum LIKE'%-01-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                januaravg = []
                [januaravg.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from prihod where datum LIKE'%-01-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                januaravg1 = []
                [januaravg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from rashod where datum LIKE'%-02-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                februaravg = []
                [februaravg.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from prihod where datum LIKE'%-02-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                februaravg1 = []
                [februaravg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from rashod where datum LIKE'%-03-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                martavg = []
                [martavg.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from prihod where datum LIKE'%-03-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                martavg1 = []
                [martavg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from rashod where datum LIKE'%-04-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                aprilavg = []
                [aprilavg.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from prihod where datum LIKE'%-04-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                aprilavg1 = []
                [aprilavg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from rashod where datum LIKE'%-05-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                majavg = []
                [majavg.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from prihod where datum LIKE'%-05-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                majavg1 = []
                [majavg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from rashod where datum LIKE'%-06-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                junavg = []
                [junavg.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from prihod where datum LIKE'%-06-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                junavg1 = []
                [junavg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from rashod where datum LIKE'%-07-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                julavg = []
                [julavg.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from prihod where datum LIKE'%-07-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                julavg1 = []
                [julavg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from rashod where datum LIKE'%-08-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                avgustavg = []
                [avgustavg.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from prihod where datum LIKE'%-08-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                avgustavg1 = []
                [avgustavg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from rashod where datum LIKE'%-09-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                septembaravg = []
                [septembaravg.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from prihod where datum LIKE'%-09-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                septembaravg1 = []
                [septembaravg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from rashod where datum LIKE'%-10-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                oktobaravg = []
                [oktobaravg.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from prihod where datum LIKE'%-10-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                oktobaravg1 = []
                [oktobaravg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from rashod where datum LIKE'%-11-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                novembaravg = []
                [novembaravg.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from prihod where datum LIKE'%-11-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                novembaravg1 = []
                [novembaravg1.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from rashod where datum LIKE'%-12-%' and " + opcija + "= '" + self.upit_vrednosti6.get() + "'")
                row = c.fetchall()
                decembaravg = []
                [decembaravg.append(i[0]) for i in row]
                c.execute(
                    "SELECT SUM(iznos) from prihod where datum LIKE'%-12-%' and " + opcija1 + "= '" + self.upit_vrednosti7.get() + "'")
                row = c.fetchall()
                decembaravg1 = []
                [decembaravg1.append(i[0]) for i in row]

                jan = ''.join(map(str, januaravg))
                jan1 = ''.join(map(str, januaravg1))
                feb = ''.join(map(str, februaravg))
                feb1 = ''.join(map(str, februaravg1))
                mar = ''.join(map(str, martavg))
                mar1 = ''.join(map(str, martavg1))
                apr = ''.join(map(str, aprilavg))
                apr1 = ''.join(map(str, aprilavg1))
                maj = ''.join(map(str, majavg))
                maj1 = ''.join(map(str, majavg1))
                jun = ''.join(map(str, junavg))
                jun1 = ''.join(map(str, junavg1))
                jul = ''.join(map(str, julavg))
                jul1 = ''.join(map(str, julavg1))
                avg = ''.join(map(str, avgustavg))
                avg1 = ''.join(map(str, avgustavg1))
                sep = ''.join(map(str, septembaravg))
                sep1 = ''.join(map(str, septembaravg1))
                okt = ''.join(map(str, oktobaravg))
                okt1 = ''.join(map(str, oktobaravg1))
                nov = ''.join(map(str, novembaravg))
                nov1 = ''.join(map(str, novembaravg1))
                dec = ''.join(map(str, decembaravg))
                dec1 = ''.join(map(str, decembaravg1))

                try:
                    avgjan = float(jan)
                except ValueError:
                    avgjan = 0
                try:
                    avgjan1 = float(jan1)
                except ValueError:
                    avgjan1 = 0
                try:
                    avgfeb = float(feb)
                except ValueError:
                    avgfeb = 0
                try:
                    avgfeb1 = float(feb1)
                except ValueError:
                    avgfeb1 = 0
                try:
                    avgmar = float(mar)
                except ValueError:
                    avgmar = 0
                try:
                    avgmar1 = float(mar1)
                except ValueError:
                    avgmar1 = 0
                try:
                    avgapr = float(apr)
                except ValueError:
                    avgapr = 0
                try:
                    avgapr1 = float(apr1)
                except ValueError:
                    avgapr1 = 0
                try:
                    avgmaj = float(maj)

                except ValueError:
                    avgmaj = 0
                try:
                    avgmaj1 = float(maj1)
                except ValueError:
                    avgmaj1 = 0
                try:
                    avgjun = float(jun)
                except ValueError:
                    avgjun = 0
                try:
                    avgjun1 = float(jun1)
                except ValueError:
                    avgjun1 = 0
                try:
                    avgjul = float(jul)
                except ValueError:
                    avgjul = 0
                try:
                    avgjul1 = float(jul1)
                except ValueError:
                    avgjul1 = 0
                try:
                    avgavg = float(avg)
                except ValueError:
                    avgavg = 0
                try:
                    avgavg1 = float(avg1)
                except ValueError:
                    avgavg1 = 0
                try:
                    avgsep = float(sep)
                except ValueError:
                    avgsep = 0
                try:
                    avgsep1 = float(sep1)
                except ValueError:
                    avgsep1 = 0
                try:
                    avgokt = float(okt)
                except ValueError:
                    avgokt = 0
                try:
                    avgokt1 = float(okt1)
                except ValueError:
                    avgokt1 = 0
                try:
                    avgnov = float(nov)
                except ValueError:
                    avgnov = 0
                try:
                    avgnov1 = float(nov1)
                except ValueError:
                    avgnov1 = 0
                try:
                    avgdec = float(dec)
                except ValueError:
                    avgdec = 0
                try:
                    avgdec1 = float(dec1)
                except ValueError:
                    avgdec1 = 0

                labels = ['Januar', 'Februar', 'Mart', 'April', 'Maj', 'Jun',
                          'Jul', 'Avgust', 'Septembar', 'Oktobar',
                          'Novembar', 'Decembar']
                prosek = [avgjan, avgfeb, avgmar, avgapr, avgmaj, avgjun,
                          avgjul, avgavg, avgsep, avgokt, avgnov, avgdec]
                prosek1 = [avgjan1, avgfeb1, avgmar1, avgapr1, avgmaj1,
                           avgjun1, avgjul1, avgavg1, avgsep1, avgokt1,
                           avgnov1, avgdec1]
                x = np.arange(len(labels))  # the label locations
                width = 0.49  # the width of the bars

                fig, ax = plt.subplots(figsize=(14, 6))
                rects1 = ax.bar(x - width / 2, prosek, width,
                                label='sum rashod')
                rects2 = ax.bar(x + width / 2, prosek1, width,
                                label='sum prihod')

                # Add some text for labels, title and custom x-axis tick labels, etc.
                ax.set_ylabel('')
                ax.set_title('Rezultati')
                ax.set_xticks(x)
                ax.set_xticklabels(labels)
                ax.legend()
                ax.bar_label(rects1, padding=3)
                ax.bar_label(rects2, padding=3)

                fig.tight_layout()

                plt.show()
            except UnboundLocalError:
                messagebox.showerror("Greska", "Nisi izabrao opciju",
                                     icon="error")

    def upit21(self):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            if self.upit_mesec5.get() == "Januar":
                broj = '01'
            elif self.upit_mesec5.get() == 'Februar':
                broj = '02'
            elif self.upit_mesec5.get() == 'Mart':
                broj = '03'
            elif self.upit_mesec5.get() == 'April':
                broj = '04'
            elif self.upit_mesec5.get() == 'Maj':
                broj = '05'
            elif self.upit_mesec5.get() == 'Jun':
                broj = '06'
            elif self.upit_mesec5.get() == 'Jul':
                broj = '07'
            elif self.upit_mesec5.get() == 'Avgust':
                broj = '08'
            elif self.upit_mesec5.get() == 'Septembar':
                broj = '09'
            elif self.upit_mesec5.get() == 'Oktobar':
                broj = '10'
            elif self.upit_mesec5.get() == 'Novembar':
                broj = '11'
            elif self.upit_mesec5.get() == 'Decembar':
                broj = '12'
            else:
                messagebox.showerror('Greska', 'Nisi izabrao mesec',
                                     icon='error')
            if self.upit_mesec6.get() == "Januar":
                broj1 = '01'
            elif self.upit_mesec6.get() == 'Februar':
                broj1 = '02'
            elif self.upit_mesec6.get() == 'Mart':
                broj1 = '03'
            elif self.upit_mesec6.get() == 'April':
                broj1 = '04'
            elif self.upit_mesec6.get() == 'Maj':
                broj1 = '05'
            elif self.upit_mesec6.get() == 'Jun':
                broj1 = '06'
            elif self.upit_mesec6.get() == 'Jul':
                broj1 = '07'
            elif self.upit_mesec6.get() == 'Avgust':
                broj1 = '08'
            elif self.upit_mesec6.get() == 'Septembar':
                broj1 = '09'
            elif self.upit_mesec6.get() == 'Oktobar':
                broj1 = '10'
            elif self.upit_mesec6.get() == 'Novembar':
                broj1 = '11'
            elif self.upit_mesec6.get() == 'Decembar':
                broj1 = '12'
            else:
                messagebox.showerror('Greska', 'Nisi izabrao mesec',
                                     icon='error')
            if self.upit_opcija14.get() == "Kategorija":
                opcija = "kategorija"
            elif self.upit_opcija14.get() == "Vrsta Transakcije":
                opcija = "vrstatransakcije"
            elif self.upit_opcija14.get() == "Vrsta placanja":
                opcija = "vrstaplacanja"
            try:
                cur.execute(
                    "SELECT SUM(iznos),"+opcija+" from rashod  where datum LIKE '%-" + broj + "-%' and  " + opcija + " = '" + self.upit_vrednosti8.get() + "' union all SELECT SUM(iznos),"+opcija+" from prihod where datum LIKE '%-" + broj1 + "-%' and " + opcija + "= '" + self.upit_vrednosti9.get() + "'")
                row = cur.fetchall()
                objects = []
                target = []
                [objects.append(i[0]) for i in row]
                [target.append(i[1]) for i in row]
                fig1, axt1 = plt.subplots()
                axt1.pie(objects, labels=objects, autopct='%1.1f%%',
                         shadow=True)
                axt1.axis("equal")
                plt.legend(target)
                plt.show()
            except ValueError:
                messagebox.showerror("Greska",
                                     "Nisi uneo ili izabrao vrednost/i \nNisi izabrao mesec/e koji su validni",
                                     icon='error')
                plt.close()
            except UnboundLocalError:
                messagebox.showerror("Greska", "Nisi izabrao opciju \n ili nisi izabrao vrednost/i opcije",
                                     icon='error')



if __name__ == '__main__':
    Diplomski().meni()

""" if self.unos_meseca_promena.get() == "Januar" or self.unos_meseca_promena.get() == "Mart" or self.unos_meseca_promena.get() == "Maj" or self.unos_meseca_promena.get() == "Jul" or self.unos_meseca_promena.get() == "Avgust" or self.unos_meseca_promena.get() == "Oktobar" or self.unos_meseca_promena.get() == "Decembar":
            self.unos_dana_promena['value'] = tridesetjedan
        if self.unos_meseca_promena.get() == "April" or self.unos_meseca_promena.get() == "Jul" or self.unos_meseca_promena.get() == "Septembar" or self.unos_meseca_promena.get() == "Novembar":
            self.unos_dana_promena['value'] = trideset
        if self.unos_meseca_promena.get() == "Februar":
            self.unos_dana_promena['value'] = dvadesetdevet"""  #na liniji 1505 vratiti