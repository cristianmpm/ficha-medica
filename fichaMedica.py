from tkinter import *
from tkinter import ttk
import sqlite3

class FichaMedica:

    dbName = 'database.db'

    def __init__(self, window):
        self.wind = Toplevel(window)
        self.wind.title('Ficha Medica')

        # Se crea el contenedor frame
        frame = LabelFrame(self.wind, text = 'Buscar ficha de paciente')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        Label(frame, text = 'Rut del paciente: ').grid(row = 1, column = 0)
        self.rut = Entry(frame)
        self.rut.grid(row = 1, column = 1)

        #boton para crear producto
        Button(frame, text = 'Buscar ficha ', command=self.getFile).grid(row = 2, columnspan = 2, sticky = W + E)

        #tabla de vista
        # define las columnas 
        columns = ('diagnostico', 'anemesis', 'date')
        self.tree = ttk.Treeview(self.wind, height = 20, columns = columns, show='headings')
        self.tree.grid(row=3, column=0, sticky='nsew')
        # define los titulos de las columnas 
        self.tree.heading('diagnostico', text='Diagnóstico')
        self.tree.heading('anemesis', text='Anémesis')
        self.tree.heading('date', text='Fecha')

         #boton para agregar diagnostico
        Button(self.wind, text = 'Agregar diagnóstico', command=self.viewDiagnostico).grid(row = 4, column=0, columnspan = 2, sticky = W + E)

    def runQuery(self, query, parameters = ()):
        with sqlite3.connect(self.dbName) as conn :
            cursor = conn.cursor()
            result = cursor.execute(query, parameters) 
            conn.commit()
        return result
    
    def validation(self):
        return len(self.rut.get()) != 0   
    
    def getFile(self):
         # limpiando la tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # obteniendo la data
        query = 'SELECT Ficha.id_ficha,  Persona.nombre, Persona.apellido_paterno, Persona.rut, Paciente.prevision, personaMedico.nombre, personaMedico.apellido_paterno, especialidad.especialidad FROM FICHA INNER JOIN PACIENTE ON PACIENTE.ID_PACIENTE = FICHA.ID_PACIENTE INNER JOIN PERSONA ON PACIENTE.ID_PERSONA = PERSONA.ID_PERSONA INNER JOIN MEDICO ON MEDICO.ID_MEDICO = FICHA.ID_MEDICO INNER JOIN ESPECIALIDAD ON MEDICO.ID_ESPECIALIDAD = ESPECIALIDAD.ID_ESPECIALIDAD INNER JOIN PERSONA AS personaMedico ON MEDICO.ID_PERSONA = personaMedico.ID_PERSONA WHERE PERSONA.rut = ?'
        parameters = (self.rut.get(),)
        dbRows = self.runQuery(query,parameters)
        # seteando la data
        pacientes = []
        for row in dbRows:
            frame = LabelFrame(self.wind, text = 'Información')
            frame.grid(row = 1, column = 0, columnspan = 3, pady = 20)
            self.idFicha = row[0]
            Label(frame, text = 'Nombre del paciente: ' + row[1] + ' ' + row[2]).grid(row = 1, column = 0)
            Label(frame, text = 'RUT del paciente: ' + row[3]).grid(row = 2, column = 0)
            Label(frame, text = 'Previsión del paciente: ' + row[4]).grid(row = 3, column = 0)
            Label(frame, text = 'Nombre del médico: ' + row[5] + ' ' + row[6]).grid(row = 4, column = 0)
            Label(frame, text = 'Especialidad del médico: ' + row[7]).grid(row = 5, column = 0)
           
            query = 'SELECT * FROM Diagnostico WHERE Diagnostico.id_ficha = ?' 
            dbRowsFicha = self.runQuery(query, (row[0],))
        for row in dbRowsFicha:
            pacientes.append((f'{row[1]}', f'{row[2]}', f'{row[4]}'))
        for paciente in pacientes:
            self.tree.insert('', END, values=paciente)

    def viewDiagnostico(self):
        self.add = Toplevel()
       # Se crea el contenedor frame
        frameTwo = LabelFrame(self.add, text = 'Agregar diagnóstico')
        frameTwo.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        Label(frameTwo, text = 'Diagnóstico: ').grid(row = 1, column = 0)
        self.diagnosis = Entry(frameTwo)
        self.diagnosis.grid(row = 1, column = 1)

        Label(frameTwo, text = 'Anemesis: ').grid(row = 2, column = 0)
        self.anemesis = Entry(frameTwo)
        self.anemesis.grid(row = 2, column = 1)

        Label(frameTwo, text = 'Fecha: ').grid(row = 3, column = 0)
        self.date = Entry(frameTwo)
        self.date.grid(row = 3, column = 1)

        #boton para agregar
        Button(frameTwo,text = 'Agregar', command=self.addDiagnostico).grid(row = 4, column=0, columnspan = 2, sticky = W + E)

    def addDiagnostico(self): 
        if len(self.diagnosis.get()) != 0 and len(self.anemesis.get()) != 0 and len(self.date.get()) != 0 : 
            query = "INSERT INTO DIAGNOSTICO VALUES(NULL, ?, ?, ?, ?)"
            parameters = (self.diagnosis.get(), self.anemesis.get(), self.idFicha, self.date.get())
            response = self.runQuery(query, parameters)
            self.getFile()
        else:
            print("campos vacios")
            

    
        
        
        


