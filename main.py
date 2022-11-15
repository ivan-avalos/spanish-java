import sys, getopt
from tkinter import *
from tkinter import ttk, filedialog
from lexer import *

class Main:
    input_file = None
    output_file = None

    # GUI widgets
    text = None
    msgarea = None
    symbols = None

    def abrir_archivo(self):
        self.input_file = filedialog.askopenfilename()
        with open(self.input_file) as f:
            data = f.read()
            self.text.insert(END, data)

    def guardar_archivo(self):
        data = self.text.get('1.0', 'end-1c')
        with open(self.input_file, "r+") as f:
            f.truncate(0)
            f.write(data)

    def compilar_programa(self):
        self.output_file = filedialog.asksaveasfilename()
        data = self.text.get('1.0', 'end-1c')
        Lexer(data).inicio()

    def ejecutar_programa(self):
        print('ejecutar_programa()')

    def salir(self):
        exit(0)

    def main_gui(self, argv):
        root = Tk()
        root.title ("Javañol")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.option_add('*tearOff', FALSE)

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        mainframe.rowconfigure(1, weight=0)

        # Menú
        menubar = Menu(root)
        root['menu'] = menubar

        menu_file = Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='Archivo')
        menu_file.add_command(label='Abrir', command=self.abrir_archivo)
        menu_file.add_command(label='Guardar', command=self.guardar_archivo)
        menu_file.add_command(label='Salir', command=self.salir)

        menu_program = Menu(menubar)
        menubar.add_cascade(menu=menu_program, label='Programa')
        menu_program.add_command(label='Compilar', command=self.compilar_programa)
        menu_program.add_command(label='Ejecutar', command=self.ejecutar_programa)

        # Editor de código
        self.text = Text(mainframe)
        self.text.grid(column=0, row=0, sticky=(N, W, E, S))

        # Área de mensajes
        msgarealf = LabelFrame(mainframe, text='Área de mensajes', height=10)
        msgarealf.grid(column=0, row=1, sticky=(W, E, S))
        
        self.msgarea = Text(msgarealf, height=10)
        self.msgarea.grid(column=0, row=0, sticky=(N, W, E, S))
        self.msgarea.rowconfigure(0, weight=1)
        self.msgarea.columnconfigure(0, weight=1)

        # Tabla de símbolos
        symbolslf = LabelFrame(mainframe, text='Símbolos', width=100)
        symbolslf.grid(column=1, row=0, rowspan=2, sticky=(N, W, E, S))
        
        self.symbols = Text(symbolslf, width=20)
        self.symbols.grid(column=0, row=0, sticky=(N, W, E, S))
        self.msgarea.rowconfigure(0, weight=1)
        self.msgarea.columnconfigure(0, weight=1)

        root.mainloop()
        
if __name__ == "__main__":
    main = Main()
    main.main_gui(sys.argv)
