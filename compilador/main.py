import sys, getopt
from tkinter import *
from tkinter import ttk, filedialog
from lexer import *

class Main:
    input_file = None
    output_file = None

    def print_help (self, arg0):
        print("Uso: % s -i entrada.ñ -o salida.ñ" % arg0)
        print("     % s -h" % arg0)

    def main(self, argv):
        try:
            opts, args = getopt.getopt(argv[1:], "hi:o:", ["input=", "output="])
        except getopt.GetoptError as err:
            print(err)
            print_help(argv[0]);
            sys.exit(2)

        for o, a in opts:
            if o == "-h":
                self.print_help (argv[0])
            elif o in ("-i", "--input"):
                self.input_file = a
            elif o in ("-o", "--output"):
                self.output_file = a
            else:
                assert False, "opción desconocida"

        if self.input_file and self.output_file:
            with open(self.input_file) as f:
                data = f.read()
                Lexer(data).inicio()

if __name__ == "__main__":
    Main().main(sys.argv)
