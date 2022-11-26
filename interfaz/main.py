#!/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2022  Iván Alejandro Ávalos Díaz <avalos@disroot.org>
#                     Edgar Alexis López Martínez <edgarmlmp@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from enum import Enum
import gi, sys, os, subprocess, json, math, webbrowser
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('GtkSource', '5')
from gi.repository import Gtk, Gdk, Gio, GLib, Adw, GtkSource, Pango

compilador_dir = '../compilador/main.py'

class Semaforo(Gtk.DrawingArea):
    class Color(Enum):
        NINGUNO = 0
        VERDE = 1
        AMARILLO = 2
        ROJO = 3
    
    def __init__(self, color: Color = Color.NINGUNO):
        super().__init__()
        self.set_content_width(120)
        self.set_content_height(40)
        self.set_color(color)

    def set_color(self, color: Color):
        if color == self.Color.VERDE:
            self.set_draw_func(self.dibujar_sem_verde, None)
        elif color == self.Color.AMARILLO:
            self.set_draw_func(self.dibujar_sem_amarillo, None)
        elif color == self.Color.ROJO:
            self.set_draw_func(self.dibujar_sem_rojo, None)
        else:
            self.set_draw_func(self.dibujar_sem_ninguno, None)

    def dibujar_sem_common(self, c, color: Color):        
        # Verde
        if color == self.Color.VERDE:
            c.set_source_rgba(0, 1, 0, 1)
        else:
            c.set_source_rgba(0, 1, 0, 0.2)
        c.set_line_width(16)
        c.arc(20, 20, 8, 0, 2 * math.pi)
        c.stroke()

        # Amarillo
        if color == self.Color.AMARILLO:
            c.set_source_rgba(1, 1, 0, 1)
        else:
            c.set_source_rgba(1, 1, 0, 0.2)
        c.set_line_width(16)
        c.arc(60, 20, 8, 0, 2 * math.pi)
        c.stroke()

        # Rojo
        if color == self.Color.ROJO:
            c.set_source_rgba(1, 0, 0, 1)
        else:
            c.set_source_rgba(1, 0, 0, 0.2)
        c.set_line_width(16)
        c.arc(100, 20, 8, 0, 2 * math.pi)
        c.stroke()

    def dibujar_sem_verde(self, area, c, w, h, data):
        self.dibujar_sem_common(c, self.Color.VERDE)

    def dibujar_sem_amarillo(self, area, c, w, h, data):
        self.dibujar_sem_common(c, self.Color.AMARILLO)

    def dibujar_sem_rojo(self, area, c, w, h, data):
        self.dibujar_sem_common(c, self.Color.ROJO)

    def dibujar_sem_ninguno(self, area, c, w, h, data):
        self.dibujar_sem_common(c, self.Color.NINGUNO)

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
        self.crear_panel_lateral()

    def crear_headerbar(self):
        header = Gtk.HeaderBar()
        self.set_titlebar(header)

        self.open_button = Gtk.Button(label='Abrir')
        self.open_button.set_icon_name('document-open-symbolic')
        self.open_button.connect('clicked', self.abrir_archivo)
        header.pack_start(self.open_button)
        
        self.save_button = Gtk.Button(label='Guardar')
        self.save_button.set_icon_name('document-save-symbolic')
        self.save_button.set_sensitive(False)
        self.save_button.connect('clicked', self.guardar_archivo)
        header.pack_start(self.save_button)

        self.crear_menu(header)
        
        self.run_button = Gtk.Button(label='Ejecutar')
        self.run_button.set_icon_name('media-playback-start-symbolic')
        self.run_button.set_sensitive(False)
        self.run_button.connect('clicked', self.correr)
        header.pack_end(self.run_button)        

    def crear_menu(self, header):
        action_help = Gio.SimpleAction.new('help', None)
        action_help.connect('activate', self.mostrar_help)
        self.add_action(action_help)
        
        action_about = Gio.SimpleAction.new('about', None)
        action_about.connect('activate', self.mostrar_about)
        self.add_action(action_about)

        menu = Gio.Menu.new()
        menu.append('Ayuda', 'win.help')
        menu.append('Acerca de', 'win.about')

        popover = Gtk.PopoverMenu()
        popover.set_menu_model(menu)

        hamburger = Gtk.MenuButton()
        hamburger.set_popover(popover)
        hamburger.set_icon_name('open-menu-symbolic')

        header.pack_end(hamburger)        

    def crear_textview(self):
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_hexpand(True)
        scrolled_win.set_vexpand(True)
        self.grid.attach(scrolled_win, 0, 0, 1, 1)

        self.sourcebuf = GtkSource.Buffer()
        self.sourcebuf.connect('changed', self.edito_codigo)
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

    def crear_panel_lateral(self):
        notebook = Gtk.Notebook()
        self.grid.attach(notebook, 1, 0, 1, 1)
        
        self.crear_tabla_simbolos(notebook)
        self.crear_semaforo(notebook)

    def crear_tabla_simbolos(self, notebook):
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

    def crear_semaforo(self, notebook):
        semgrid = Gtk.Grid()
        semgrid.set_row_spacing(8)
        semgrid.set_column_spacing(8)
        semgrid.set_margin_top(8)
        semgrid.set_margin_start(8)
        semgrid.set_margin_end(8)
        semgrid.set_margin_bottom (8)
        
        semgrid.attach(Gtk.Label.new('Léxico'), 0, 0, 1, 1)
        semgrid.attach(Gtk.Label.new('Sintáctico'), 0, 1, 1, 1)
        semgrid.attach(Gtk.Label.new('Semántico'), 0, 2, 1, 1)
        
        self.sem_lexico = Semaforo()
        self.sem_sintactico = Semaforo()
        self.sem_semantico = Semaforo()
        semgrid.attach(self.sem_lexico, 1, 0, 1, 1)
        semgrid.attach(self.sem_sintactico, 1, 1, 1, 1)
        semgrid.attach(self.sem_semantico, 1, 2, 1, 1)

        self.btn_lexico = Gtk.Button(label='Análisis léxico')
        self.btn_lexico.set_icon_name('media-playback-start-symbolic')
        self.btn_lexico.set_sensitive(False)
        self.btn_lexico.connect('clicked', self.analisis_lexico)

        self.btn_sintactico = Gtk.Button(label='Análisis sintáctico')
        self.btn_sintactico.set_icon_name('media-playback-start-symbolic')
        self.btn_sintactico.set_sensitive(False)
        self.btn_sintactico.connect('clicked', self.analisis_sintactico)

        self.btn_semantico = Gtk.Button(label='Análisis semántico')
        self.btn_semantico.set_icon_name('media-playback-start-symbolic')
        self.btn_semantico.set_sensitive(False)
        self.btn_semantico.connect('clicked', self.analisis_semantico)

        semgrid.attach(self.btn_lexico, 2, 0, 1, 1);
        semgrid.attach(self.btn_sintactico, 2, 1, 1, 1);
        semgrid.attach(self.btn_semantico, 2, 2, 1, 1);
        
        notebook.append_page(semgrid, Gtk.Label.new('Semáforo'))

    def edito_codigo(self, buffer):
        self.reset_semaforos()

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
                self.save_button.set_sensitive(True)
                self.run_button.set_sensitive(True)
                self.btn_lexico.set_sensitive(True)
                self.sem_lexico.set_color(Semaforo.Color.AMARILLO)

    def guardar_archivo(self, button):
        if self.input_file:
            start = self.sourcebuf.get_start_iter()
            end = self.sourcebuf.get_end_iter()
            data = self.sourcebuf.get_text(start, end, False)
            with open(self.input_file, 'r+') as f:
                f.truncate(0)
                f.write(data)

    def mostrar_help(self, action, param):
        url = 'file://' + os.getcwd() + '/../docs/index.html'
        webbrowser.open(url)

    def mostrar_about(self, action, param):
        self.about_dialog = Gtk.AboutDialog()
        self.about_dialog.set_transient_for(self)
        self.about_dialog.set_modal(self)

        self.about_dialog.set_comments(
            '''Materia: Lenguajes y Autómatas 2
Profesor: I.S.C. Ricardo González González
Tecnológico Nacional de México en Celaya''')
        self.about_dialog.set_authors([
            "Iván Alejandro Ávalos Díaz (18032572)",
            "Edgar Alexis López Martínez (18030817)"
        ])
        self.about_dialog.set_logo_icon_name('applications-development')
        self.about_dialog.set_license(
            '''Copyright (C) 2022  Iván Alejandro Ávalos Díaz <avalos@disroot.org>,
                    Edgar Alexis López Martínez <edgarmlmp@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
            ''')
        self.about_dialog.show()

    def analisis_lexico(self, button):
        self.guardar_archivo(None)
        self.limpiar_tabla()
        self.reset_semaforos()
        result = subprocess.run([
            'python', compilador_dir,
            '-i', self.input_file,
            '-o', self.output_file,
            '-l'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = result.stdout.decode('utf-8')
        self.msgbuf.set_text(output)

        if result.returncode == 0:
            self.sem_lexico.set_color(Semaforo.Color.VERDE)
            self.sem_sintactico.set_color(Semaforo.Color.AMARILLO)
            self.btn_sintactico.set_sensitive(True)
            self.llenar_tabla()
        else:
            self.sem_lexico.set_color(Semaforo.Color.ROJO)

    def analisis_sintactico(self, button):
        self.limpiar_tabla()
        self.sem_semantico.set_color(Semaforo.Color.NINGUNO)
        self.btn_semantico.set_sensitive(False)
        result = subprocess.run([
            'python', compilador_dir,
            '-i', self.input_file,
            '-o', self.output_file,
            '-p'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = result.stdout.decode('utf-8')
        self.msgbuf.set_text(output)

        if result.returncode == 0:
            self.sem_sintactico.set_color(Semaforo.Color.VERDE)
            self.sem_semantico.set_color(Semaforo.Color.AMARILLO)
            self.btn_semantico.set_sensitive(True)
            self.llenar_tabla()
        else:
            self.sem_sintactico.set_color(Semaforo.Color.ROJO)
            self.btn_sintactico.set_sensitive(False)

    def analisis_semantico(self, button):
        self.limpiar_tabla()
        result = subprocess.run([
            'python', compilador_dir,
            '-i', self.input_file,
            '-o', self.output_file,
            '-s'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = result.stdout.decode('utf-8')
        self.msgbuf.set_text(output)

        if result.returncode == 0:
            self.sem_semantico.set_color(Semaforo.Color.VERDE)
            self.llenar_tabla()
        else:
            self.sem_semantico.set_color(Semaforo.Color.ROJO)

    def correr(self, button):
        self.guardar_archivo(None)
        self.reset_semaforos()
        self.limpiar_tabla()
        result = subprocess.run([
            'python', compilador_dir,
            '-i', self.input_file,
            '-o', self.output_file,
            '-t'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = result.stdout.decode('utf-8')
        self.msgbuf.set_text(output)

        if result.returncode == 0:
            self.llenar_tabla()

    def limpiar_tabla(self):
        for i in range(4):
            self.tablagrid.remove_column(0)

    def llenar_tabla(self):
        with open(self.input_file + '.tab', 'r') as f:
            data = f.read()
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

    def reset_semaforos(self):
        if self.input_file:
            self.sem_lexico.set_color(Semaforo.Color.AMARILLO)
            self.btn_lexico.set_sensitive(True)
        else:
            self.sem_lexico.set_color(Semaforo.Color.NINGUNO)
            self.btn_lexico.set_sensitive(False)
        self.sem_sintactico.set_color(Semaforo.Color.NINGUNO)
        self.btn_sintactico.set_sensitive(False)
        self.sem_semantico.set_color(Semaforo.Color.NINGUNO)
        self.btn_semantico.set_sensitive(False)

def on_activate(app):
    win = MainWindow()
    win.connect('destroy', Gtk.main_quit)
    win.present()

class App(Adw.Application):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        GLib.set_application_name("Javañol RGG edition")

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
