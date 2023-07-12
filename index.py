from tkinter import *
from tkinter import ttk
from paciente import * 
from fichaMedica import *
from ficha import *

def goToPaciente():
    paciente = Paciente(window)

def goToFichaMedica():
    fichaMedica = FichaMedica(window)
    
def goToFicha():
    fichaMedica = Ficha(window)

if __name__ == '__main__':
    window = Tk()
    window.title('Kill corona virus')
     # Se crea el contenedor frame
    frame = LabelFrame(window, text= 'Menu')
    frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
    #boton para ir a los pacientes
    Button(frame, text = 'Modulo paciente', command  = goToPaciente).grid(row = 1, columnspan = 2, sticky = W + E)
    #boton para ir a ficha medica
    Button(frame, text = 'Ficha medica', command  = goToFichaMedica).grid(row = 2, columnspan = 2, sticky = W + E)
     #boton para ir al modulo de ficha medica
    Button(frame, text = 'Modulo ficha medica', command  = goToFicha).grid(row = 3, columnspan = 2, sticky = W + E)
   
    window.mainloop()

