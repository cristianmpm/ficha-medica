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

        #boton para crear producto
        Button(frame, text = 'Agregar paciente ').grid(row = 9, columnspan = 2, sticky = W + E)

        #tabla de vista
        # define las columnas 
        columns = ('rut', 'first_name', 'last_name', 'email', 'gender')
        self.tree = ttk.Treeview(height = 20, columns = columns, show='headings')
        self.tree.grid(row=10, column=0, sticky='nsew')
        # define los titulos de las columnas 
        self.tree.heading('rut', text='RUT')
        self.tree.heading('first_name', text='Nombre')
        self.tree.heading('last_name', text='Apellido')
        self.tree.heading('email', text='Email')
        self.tree.heading('gender', text='Sexo')
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
            pacientes.append((f'{row[10]}', f'{row[5]}', f'{row[6]}', f'{row[8]}', f'{row[13]}'))
        for paciente in pacientes:
            self.tree.insert('', END, values=paciente)

if __name__ == '__main__':
    window = Tk()
    aplication = Paciente(window)
    window.mainloop()


