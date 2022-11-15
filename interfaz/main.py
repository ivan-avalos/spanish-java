import gi, sys, subprocess
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
        self.crear_paneles()

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
        
        return

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

    def crear_paneles(self):
        # Área de mensajes
        notebook1 = Gtk.Notebook()
        self.grid.attach(notebook1, 0, 1, 2, 1)

        scrolled_msg = Gtk.ScrolledWindow()
        scrolled_msg.set_hexpand(True)
        scrolled_msg.set_min_content_height(150)
        
        self.msgbuf = GtkSource.Buffer()
        self.msgview = GtkSource.View.new_with_buffer(self.msgbuf)
        self.msgview.set_editable(False)
        scrolled_msg.set_child(self.msgview)
        notebook1.append_page(scrolled_msg, Gtk.Label.new('Mensajes'))

        # Tabla de símbolos
        notebook2 = Gtk.Notebook()
        self.grid.attach(notebook2, 1, 0, 1, 1)

        scrolled_tabla = Gtk.ScrolledWindow()
        scrolled_tabla.set_vexpand(True)
        scrolled_tabla.set_min_content_width(300)
        
        self.tablabuf = GtkSource.Buffer()
        self.tablaview = GtkSource.View.new_with_buffer(self.tablabuf)
        self.tablaview.set_editable(False)
        scrolled_tabla.set_child(self.tablaview)
        notebook2.append_page(scrolled_tabla, Gtk.Label.new('Símbolos'))

    def abrir_archivo(self, button):
        print('abrir_archivo()')
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
        if self.input_file:
            result = subprocess.run([
                'python', compilador_dir,
                '-i', self.input_file,
                '-o', self.output_file
            ], stdout=subprocess.PIPE)
            output = result.stdout.decode('utf-8')
            self.msgbuf.set_text(output)

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

    
app = App(application_id='mx.rgg.spanishjava')
app.run(sys.argv)
