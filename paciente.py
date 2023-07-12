from tkinter import *
from tkinter import ttk
import sqlite3

class Paciente:

    dbName = 'database.db'

    def __init__(self, window):
        self.wind = Toplevel(window)
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

        Label(frame, text = 'Número de teléfono: ').grid(row = 5, column = 0)
        self.phoneNumber = Entry(frame)
        self.phoneNumber.grid(row = 5, column = 1)

        Label(frame, text = 'E-mail: ').grid(row = 6, column = 0)
        self.email = Entry(frame)
        self.email.grid(row = 6, column = 1)
        
        Label(frame, text = 'Dirección: ').grid(row = 7, column = 0)
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

        Label(frame, text = 'Previsión: ').grid(row = 11, column = 0)
        self.insurance = Entry(frame)
        self.insurance.grid(row = 11, column = 1)

        #boton para crear paciente
        Button(frame, text = 'Agregar paciente ', command=self.addPaciente).grid(row = 12, columnspan = 2, sticky = W + E)

        #Mensajes de error
        self.message = Label(self.wind, text = '', fg = 'red')
        self.message.grid(row = 13, column = 0, columnspan = 2, sticky = W + E)

        #tabla de vista
        # define las columnas 
        columns = ('rut', 'first_name', 'last_name', 'email', 'insurance')
        self.tree = ttk.Treeview(self.wind, height = 10, columns = columns, show='headings')
        self.tree.grid(row=14, column=0, columnspan=2, sticky='nsew')
        # define los titulos de las columnas 
        self.tree.heading('rut', text='RUT')
        self.tree.heading('first_name', text='Nombre')
        self.tree.heading('last_name', text='Apellido')
        self.tree.heading('email', text='Email')
        self.tree.heading('insurance', text='Previsión')

        # busca la informacion en la base de datos y lo pinta en la tabla
        self.getPacientes()
        #boton para editar y eliminar registro 
        Button(self.wind, text = 'Eliminar', command = self.deletePaciente).grid(row = 15, column = 0, sticky = W + E)
        Button(self.wind, text = 'Editar', command = self.viewEditPaciente).grid(row = 15, column = 1, sticky = W + E)
       
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
        query = 'SELECT * FROM PACIENTE INNER JOIN PERSONA ON PACIENTE.ID_PERSONA = PERSONA.ID_PERSONA'
        dbRows = self.runQuery(query=query)
        # seteando la data
        pacientes = []
        for row in dbRows:
            pacientes.append((f'{row[10]}', f'{row[5]}', f'{row[6]}', f'{row[8]}', f'{row[4]}', f'{row[0]}', f'{row[1]}', f'{row[2]}', f'{row[4]}',f'{row[7]}', f'{row[9]}', f'{row[11]}', f'{row[13]}'))
        for paciente in pacientes:
            self.tree.insert('', END, values=paciente)
        self.message['text'] = ""

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
            self.message['text'] = 'Por favor ingrese todos los campos'

    def deletePaciente(self): 
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor seleccione el registro que desea eliminar'
            return
        self.message['text'] = ""
        rut = self.tree.item(self.tree.selection())['values'][0]
        idPaciente = self.tree.item(self.tree.selection())['values'][5]
        query = 'DELETE FROM PERSONA WHERE rut = ?'
        self.runQuery(query, (rut, ))
        query = 'DELETE FROM PACIENTE WHERE id_paciente = ?'
        self.runQuery(query, (idPaciente, ))
        self.getPacientes()
        
    def viewEditPaciente(self): 
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor seleccione el registro que desea editar'
            return
        self.message['text'] = ""
        values = self.tree.item(self.tree.selection())['values']
        editView = Toplevel()
        editView.title = 'Editar Paciente'
        # Datos para agregar paciente
        Label(editView, text = 'Nombre: ').grid(row = 1, column = 0)
        name = Entry(editView)
        name.insert(0, values[1])
        name.focus()
        name.grid(row = 1, column = 1)

        Label(editView, text = 'Apellido paterno: ').grid(row = 2, column = 0)
        lastName = Entry(editView)
        lastName.insert(0, values[2])
        lastName.grid(row = 2, column = 1)
        
        Label(editView, text = 'Apellido materno: ').grid(row = 3, column = 0)
        lastNameTwo = Entry(editView)
        lastNameTwo.insert(0, values[9])
        lastNameTwo.grid(row = 3, column = 1)

        Label(editView, text = 'Rut: ').grid(row = 4, column = 0)
        rut = Entry(editView)
        rut.insert(0, values[0])
        rut.grid(row = 4, column = 1)

        Label(editView, text = 'Número de teléfono: ').grid(row = 5, column = 0)
        phoneNumber = Entry(editView)
        phoneNumber.insert(0, values[10])
        phoneNumber.grid(row = 5, column = 1)

        Label(editView, text = 'E-mail: ').grid(row = 6, column = 0)
        email = Entry(editView)
        email.insert(0, values[3])
        email.grid(row = 6, column = 1)
        
        Label(editView, text = 'Dirección: ').grid(row = 7, column = 0)
        address = Entry(editView)
        address.insert(0, values[11])
        address.grid(row = 7, column = 1)

        Label(editView, text = 'Sexo: ').grid(row = 8, column = 0)
        gender = Entry(editView)
        gender.insert(0, values[12])
        gender.grid(row = 8, column = 1)

        Label(editView, text = 'Edad: ').grid(row = 9, column = 0)
        age = Entry(editView)
        age.insert(0, values[6])
        age.grid(row = 9, column = 1)
        
        Label(editView, text = 'Fecha de nacimiento: ').grid(row = 10, column = 0)
        birthdate = Entry(editView)
        birthdate.insert(0, values[7])
        birthdate.grid(row = 10, column = 1)

        Label(editView, text = 'Previsión: ').grid(row = 11, column = 0)
        insurance = Entry(editView)
        insurance.insert(0, values[8])
        insurance.grid(row = 11, column = 1)
        Button(editView, text = 'Actualizar', command= lambda: self.editPaciente(name.get(), lastName.get(), lastNameTwo.get(), email.get(), phoneNumber.get(), rut.get(), address.get(), gender.get(), values, age.get(), birthdate.get(), insurance.get(), editView)).grid(row = 12, column = 0, columnspan=2, sticky = W + E)

    def editPaciente(self,name, lastName, lastNameTwo, email, phoneNumber, rut, address, gender, values, age, birthdate, insurance, editView) :
        query = "UPDATE PERSONA SET nombre = ?, apellido_materno = ?, apellido_paterno = ?, email = ?, numero_telefono = ?, rut = ?, direccion = ?, sexo = ? WHERE rut = ?"
        parameters = (name, lastName, lastNameTwo, email, phoneNumber, rut, address, gender, values[0])
        response = self.runQuery(query, parameters)
        query = "UPDATE PACIENTE SET edad = ?, fecha_nacimiento = ?, prevision = ? WHERE id_paciente = ?"
        parameters = (age, birthdate, insurance, values[5])
        response = self.runQuery(query, parameters)
        editView.destroy()
        self.getPacientes()




