from tkinter import *
from tkinter import ttk
import sqlite3

class Paciente:

    dbName = 'database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Pacientes')

        # Se crea el contenedor frame
        frame = LabelFrame(self.wind, text = 'Agregar paciente')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Datos para agregar paciente
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        Label(frame, text = 'Apellido paterno: ').grid(row = 2, column = 0)
        self.lastName = Entry(frame)
        self.lastName.grid(row = 2, column = 1)
        
        Label(frame, text = 'Apellido materno: ').grid(row = 3, column = 0)
        self.lastNameTwo = Entry(frame)
        self.lastNameTwo.grid(row = 3, column = 1)

        Label(frame, text = 'Rut: ').grid(row = 4, column = 0)
        self.rut = Entry(frame)
        self.rut.grid(row = 4, column = 1)

        Label(frame, text = 'Numero de telefono: ').grid(row = 5, column = 0)
        self.phoneNumber = Entry(frame)
        self.phoneNumber.grid(row = 5, column = 1)

        Label(frame, text = 'E-mail: ').grid(row = 6, column = 0)
        self.email = Entry(frame)
        self.email.grid(row = 6, column = 1)
        
        Label(frame, text = 'Direccion: ').grid(row = 7, column = 0)
        self.address = Entry(frame)
        self.address.grid(row = 7, column = 1)

        Label(frame, text = 'Sexo: ').grid(row = 8, column = 0)
        self.gender = Entry(frame)
        self.gender.grid(row = 8, column = 1)

        Label(frame, text = 'Edad: ').grid(row = 9, column = 0)
        self.age = Entry(frame)
        self.age.grid(row = 9, column = 1)
        
        Label(frame, text = 'Fecha de nacimiento: ').grid(row = 10, column = 0)
        self.birthdate = Entry(frame)
        self.birthdate.grid(row = 10, column = 1)

        Label(frame, text = 'Prevision: ').grid(row = 11, column = 0)
        self.insurance = Entry(frame)
        self.insurance.grid(row = 11, column = 1)

        #boton para crear producto
        Button(frame, text = 'Agregar paciente ', command=self.addPaciente).grid(row = 12, columnspan = 2, sticky = W + E)

        #tabla de vista
        # define las columnas 
        columns = ('rut', 'first_name', 'last_name', 'email', 'insurance')
        self.tree = ttk.Treeview(height = 20, columns = columns, show='headings')
        self.tree.grid(row=13, column=0, sticky='nsew')
        # define los titulos de las columnas 
        self.tree.heading('rut', text='RUT')
        self.tree.heading('first_name', text='Nombre')
        self.tree.heading('last_name', text='Apellido')
        self.tree.heading('email', text='Email')
        self.tree.heading('insurance', text='Prevision')
        # agrega un scrollbar
        scrollbar = ttk.Scrollbar(orient= VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=10, column=1, sticky='ns')
        # busca la informacion en la base de datos y lo pinta en la tabla
        self.getPacientes()

    def runQuery(self, query, parameters = ()):
        with sqlite3.connect(self.dbName) as conn :
            cursor = conn.cursor()
            result = cursor.execute(query, parameters) 
            conn.commit()
        return result
    
    def validation(self):
        return len(self.name.get()) != 0 and len(self.lastName.get()) != 0 and len(self.lastNameTwo.get()) != 0 and len(self.rut.get()) != 0 and len(self.phoneNumber.get()) != 0 and len(self.email.get()) != 0 and len(self.address.get()) != 0 and len(self.gender.get()) != 0 and len(self.insurance.get()) != 0 and len(self.age.get()) != 0 and len(self.birthdate.get()) != 0 
    
    def getPacientes(self):
         # limpiando la tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # obteniendo la data
        query = 'SELECT * FROM PACIENTE INNER JOIN PERSONA WHERE PACIENTE.ID_PERSONA = PERSONA.ID_PERSONA'
        dbRows = self.runQuery(query=query)
        # seteando la data
        pacientes = []
        for row in dbRows:
            pacientes.append((f'{row[10]}', f'{row[5]}', f'{row[6]}', f'{row[8]}', f'{row[4]}'))
        for paciente in pacientes:
            self.tree.insert('', END, values=paciente)

    def addPaciente(self): 
        validation = self.validation()
        if validation: 
            query = "INSERT INTO PERSONA VALUES(?, ?, ?, ?, ?, ?, ?, NULL, ?)"
            parameters = (self.name.get(), self.lastName.get(), self.lastNameTwo.get(), self.email.get(), self.phoneNumber.get(), self.rut.get(), self.address.get(), self.gender.get())
            response = self.runQuery(query, parameters)
            query = "INSERT INTO PACIENTE VALUES(NULL, ?, ?, ?, ?)"
            parameters = (self.age.get(), self.birthdate.get(), response.lastrowid, self.insurance.get())
            response = self.runQuery(query, parameters)
            self.getPacientes()
        else:
            print("campos vacios")
        


