from tkinter import *
from tkinter import ttk
import sqlite3

class Ficha:

    dbName = 'database.db'

    def __init__(self, window):
        self.wind = Toplevel(window)
        self.wind.title('Ficha Medica')

        # Se crea los listados de paciente y medico
        Label(self.wind, text = 'Crear ficha de paciente').grid(row = 1, column = 0)
        Label(self.wind, text = 'Seleccionar Paciente: ').grid(row = 2, column = 0)
        self.listPaciente = ttk.Combobox(self.wind )
        self.listPaciente.grid(row = 3, column = 0)

        Label(self.wind, text = 'Seleccionar Médico: ').grid(row = 4, column = 0)
        self.listMedico = ttk.Combobox(self.wind)
        self.listMedico.grid(row = 5, column = 0)

        #boton para crear ficha y eliminar
        Button(self.wind, text = 'Crear ficha ', command=self.addFile).grid(row = 6, columnspan = 2, sticky = W + E)
        Button(self.wind, text = 'Eliminar', command = self.deleteFile).grid(row = 9, column = 0, sticky = W + E)
        
        #Mensajes de error
        self.message = Label(self.wind, text = '', fg = 'red')
        self.message.grid(row = 7, column = 0, columnspan = 2, sticky = W + E)

        #Se obtiene el listado de medicos y pacientes
        self.getMedicos()
        self.getPacientes()

        #tabla de vista
        # define las columnas 
        columns = ('file','namePaciente', 'rutPaciente', 'prevision', 'nameMedico', 'especialidad')
        self.tree = ttk.Treeview(self.wind, height = 20, columns = columns, show='headings')
        self.tree.grid(row=8, column=0, sticky='nsew')
        # define los titulos de las columnas 
        self.tree.heading('file', text='Número de ficha')
        self.tree.heading('namePaciente', text='Nombre paciente')
        self.tree.heading('rutPaciente', text='RUT paciente')
        self.tree.heading('prevision', text='Prevision')
        self.tree.heading('nameMedico', text='Nombre médico')
        self.tree.heading('especialidad', text='Especialidad')

        # busca la informacion en la base de datos y lo pinta en la tabla
        self.getFiles()

    #Conexion y ejecucion de consulta a la base de datos
    def runQuery(self, query, parameters = ()):
        with sqlite3.connect(self.dbName) as conn :
            cursor = conn.cursor()
            result = cursor.execute(query, parameters) 
            conn.commit()
        return result
    
    def validation(self):
        return len(self.rut.get()) != 0   
    
     #Se obtiene el listado de fichas medicas 
    def getFiles(self):
         # limpiando la tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # obteniendo la data
        query = 'SELECT Ficha.id_ficha,  Persona.nombre, Persona.apellido_paterno, Persona.rut, Paciente.prevision, personaMedico.nombre, personaMedico.apellido_paterno, especialidad.especialidad FROM FICHA INNER JOIN PACIENTE ON PACIENTE.ID_PACIENTE = FICHA.ID_PACIENTE INNER JOIN PERSONA ON PACIENTE.ID_PERSONA = PERSONA.ID_PERSONA INNER JOIN MEDICO ON MEDICO.ID_MEDICO = FICHA.ID_MEDICO INNER JOIN ESPECIALIDAD ON MEDICO.ID_ESPECIALIDAD = ESPECIALIDAD.ID_ESPECIALIDAD INNER JOIN PERSONA AS personaMedico ON MEDICO.ID_PERSONA = personaMedico.ID_PERSONA'
        dbRows = self.runQuery(query)
        # seteando la data
        files = []
        for row in dbRows:
            files.append((f'{row[0]}', f'{row[1]} {row[2]}', f'{row[3]}', f'{row[4]}', f'{row[5]} {row[6]}',f'{row[7]}'))
        for file in files:
            self.tree.insert('', END, values=file)

    #Se obtiene el listado de medicos
    def getMedicos(self) :
        query = 'SELECT * FROM MEDICO INNER JOIN PERSONA ON PERSONA.ID_PERSONA = MEDICO.ID_PERSONA'
        dbRows = self.runQuery(query)
        medicos = []
        self.idMedicos = {}
        for row in dbRows:
            medicos.append((f'{row[3]} {row[4]} {row[8]}'))
            self.idMedicos[f'{row[3]} {row[4]} {row[8]}'] = row[0]
        self.listMedico["values"] = medicos
        self.listMedico.current(0)

    #Se obtiene el listado de pacientes
    def getPacientes(self) :
        self.message['text'] = ""
        query = 'SELECT * FROM PACIENTE INNER JOIN PERSONA ON PERSONA.ID_PERSONA = PACIENTE.ID_PERSONA'
        dbRows = self.runQuery(query)
        pacientes = []
        self.idPacientes = {}
        for row in dbRows:
            pacientes.append((f'{row[5]} {row[6]} {row[10]}'))
            self.idPacientes[f'{row[5]} {row[6]} {row[10]}'] = row[0]
        self.listPaciente["values"] = pacientes
        self.listPaciente.current(0)

    #Se crea una nueva ficha medica
    def addFile(self): 
        query = "INSERT INTO FICHA VALUES(NULL, ?, ?)"
        parameters = (int(self.idPacientes[self.listPaciente.get()]), int(self.idMedicos[self.listMedico.get()]))   
        response = self.runQuery(query, parameters)
        self.getFiles()

    #Se elimina una ficha medica
    def deleteFile(self): 
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor seleccione el registro que desea eliminar'
            return
        self.message['text'] = ""
        id_ficha = self.tree.item(self.tree.selection())['values'][0]
        query = 'DELETE FROM FICHA WHERE id_ficha = ?'
        self.runQuery(query, (id_ficha, ))
        self.getFiles()
        
            

    
        
        
        


