import gi, sys, subprocess, json
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('GtkSource', '5')
from gi.repository import Gtk, Gdk, Gio, Adw, GtkSource, Pango

compilador_dir = '../compilador/main.py'

class MainWindow(Gtk.ApplicationWindow):
    input_file = None
    output_file = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_title('Javañol para RGG')
        self.set_icon_name('text-editor')
        self.set_default_size(800, 600)

        self.grid = Gtk.Grid()
        self.set_child(self.grid)

        self.crear_headerbar()
        self.crear_textview()
        self.crear_area_mensajes()
        self.crear_tabla_simbolos()

    def crear_headerbar(self):
        header = Gtk.HeaderBar()
        self.set_titlebar(header)

        self.open_button = Gtk.Button(label='Abrir')
        self.open_button.set_icon_name('document-open-symbolic')
        self.open_button.connect('clicked', self.abrir_archivo)
        header.pack_start(self.open_button)
        
        self.save_button = Gtk.Button(label='Guardar')
        self.save_button.set_icon_name('document-save-symbolic')
        self.save_button.connect('clicked', self.guardar_archivo)
        header.pack_start(self.save_button)

        self.run_button = Gtk.Button(label='Ejecutar')
        self.run_button.set_icon_name('media-playback-start-symbolic')
        self.run_button.connect('clicked', self.correr)
        header.pack_end(self.run_button)

    def crear_textview(self):
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_hexpand(True)
        scrolled_win.set_vexpand(True)
        self.grid.attach(scrolled_win, 0, 0, 1, 1)

        self.sourcebuf = GtkSource.Buffer()
        self.sourceview = GtkSource.View.new_with_buffer(self.sourcebuf)
        self.sourceview.set_show_line_numbers(True)
        self.sourceview.set_auto_indent(True)
        self.sourceview.set_indent_width(4)
        self.sourceview.set_insert_spaces_instead_of_tabs(True)
        self.sourceview.set_smart_backspace(True)
        
        scrolled_win.set_child(self.sourceview)

    def crear_area_mensajes(self):
        notebook = Gtk.Notebook()
        self.grid.attach(notebook, 0, 1, 2, 1)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_hexpand(True)
        scrolled.set_min_content_height(150)
        
        self.msgbuf = GtkSource.Buffer()
        self.msgview = GtkSource.View.new_with_buffer(self.msgbuf)
        self.msgview.set_editable(False)
        scrolled.set_child(self.msgview)
        notebook.append_page(scrolled, Gtk.Label.new('Mensajes'))

    def crear_tabla_simbolos(self):
        notebook = Gtk.Notebook()
        self.grid.attach(notebook, 1, 0, 1, 1)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_min_content_width(300)

        self.tablagrid = Gtk.Grid()
        self.tablagrid.set_vexpand(True)
        self.tablagrid.set_row_spacing(8)
        self.tablagrid.set_column_spacing(8)
        self.tablagrid.set_margin_top(8)
        self.tablagrid.set_margin_start(8)
        self.tablagrid.set_margin_end(8)
        self.tablagrid.set_margin_bottom (8)
        scrolled.set_child(self.tablagrid)
        notebook.append_page(scrolled, Gtk.Label.new('Símbolos'))

    def abrir_archivo(self, button):
        self.open_dialog = Gtk.FileChooserNative.new(
            title='Abrir archivo',
            parent=self,
            action=Gtk.FileChooserAction.OPEN)
        self.open_dialog.connect('response', self.abrio_archivo)
        self.open_dialog.show()

    def abrio_archivo(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            file = dialog.get_file()
            self.input_file = file.get_path()
            self.output_file = self.input_file + '.exe'
            with open(self.input_file) as f:
                data = f.read()
                self.sourcebuf.set_text(data)

    def guardar_archivo(self, button):
        if self.input_file:
            start = self.sourcebuf.get_start_iter()
            end = self.sourcebuf.get_end_iter()
            data = self.sourcebuf.get_text(start, end, False)
            with open(self.input_file, 'r+') as f:
                f.truncate(0)
                f.write(data)

    def correr(self, button):
        self.guardar_archivo(None)
        self.limpiar_tabla()
        if self.input_file:
            result = subprocess.run([
                'python', compilador_dir,
                '-i', self.input_file,
                '-o', self.output_file,
                '-t'
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output = result.stdout.decode('utf-8')
            self.msgbuf.set_text(output)

            if result.returncode == 0:
                # Tabla de símbolos
                with open(self.input_file + '.tab', 'r') as f:
                    data = f.read()
                    self.llenar_tabla(data)

    def limpiar_tabla(self):
        for i in range(4):
            self.tablagrid.remove_column(0)

    def llenar_tabla(self, data):
        tabla = json.loads(data)
        label_linea = Gtk.Label.new(None)
        label_linea.set_markup('<b>Línea</b>')
        label_nombre = Gtk.Label.new(None)
        label_nombre.set_markup('<b>Nombre</b>')
        label_valor = Gtk.Label.new(None)
        label_valor.set_markup('<b>Valor</b>')
        label_tipo = Gtk.Label.new(None)
        label_tipo.set_markup('<b>Tipo</b>')
        self.tablagrid.attach(label_linea, 0, 0, 1, 1)
        self.tablagrid.attach(label_tipo, 1, 0, 1, 1)
        self.tablagrid.attach(label_nombre, 2, 0, 1, 1)
        self.tablagrid.attach(label_valor, 3, 0, 1, 1)
        for i, t in enumerate(tabla):
            row = i + 1
            self.tablagrid.attach(Gtk.Label.new(str(t['numlinea'])), 0, row, 1, 1)
            self.tablagrid.attach(Gtk.Label.new(t['tipo']), 1, row, 1, 1)
            self.tablagrid.attach(Gtk.Label.new(t['nombre']), 2, row, 1, 1)
            self.tablagrid.attach(Gtk.Label.new(str(t['valor'])), 3, row, 1, 1)
            

def on_activate(app):
    win = MainWindow()
    win.connect('destroy', Gtk.main_quit)
    win.present()

class App(Adw.Application):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Estilos CSS
        css_provider = Gtk.CssProvider()
        css_provider.load_from_file(
            Gio.File.new_for_path('main.css'))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

if __name__ == "__main__":
    app = App(application_id='mx.rgg.spanishjava')
    app.run(sys.argv)
