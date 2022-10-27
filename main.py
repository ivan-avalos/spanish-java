import sys, getopt
from lexer import *

def inicio (input_file, output_file):
    with open(input_file) as f:
        data = f.read()
        inicio_lexer (data)

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "hi:o:", ["input=", "output="])
    except getopt.GetoptError as err:
        print(err)
        print_help(argv[0]);
        sys.exit(2)

    input_file = None
    output_file = None
    
    for o, a in opts:
        if o == "-h":
            print_help (argv[0])
        elif o in ("-i", "--input"):
            input_file = a
        elif o in ("-o", "--output"):
            output_file = a
        else:
            assert False, "opción desconocida"

    if input_file and output_file:
        inicio (input_file, output_file)

def print_help (arg0):
    print("Uso: % s -i entrada.ñ -o salida.ñ" % arg0)
    print("     % s -h" % arg0)
        
if __name__ == "__main__":
    main(sys.argv)
