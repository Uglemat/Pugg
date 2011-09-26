#!/usr/bin/env python
"""
    This program is called Pugg, and is used to learn new languages.
    Copyright (C) 2011  Mattias Ugelvik

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import pygtk
import gtk
import random
import pango
pygtk.require('2.0')

class win:
  def __init__(self):
    self.version = "0.1"

    mb = gtk.MenuBar()

    filemenu = gtk.Menu()
    filem = gtk.MenuItem("File")
    filem.set_submenu(filemenu)
    exit = gtk.MenuItem("Exit")
    exit.connect("activate", gtk.main_quit)
    filemenu.append(exit)
    mb.append(filem)


    vbox = gtk.VBox(False, 2)
    vbox.pack_start(mb, False, False, 0)
    vbox.show_all()

    self.splits = "!;!" # What the words are seperated by in the dictionary. If you wanna use csv files, just change to ",".

    self.attr = pango.AttrList()
    size = pango.AttrSize(20000, 0, -1)
    self.attr.insert(size)

    f = open("dicts.pugg","r")
    dicts = f.readlines()
    f.close()
    self.parsed_dicts = []
    for line in dicts:
      self.parsed_dicts.append(line[:-1].split(self.splits)) # Creates a list of all the .pugg files listed in dicts.pugg, and their title.

    self.cb = gtk.combo_box_new_text()
    self.cb.connect("changed", self.on_changed)

    for d in self.parsed_dicts:
      self.cb.append_text(d[1])

    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    #self.window.set_border_width(10)
    self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(16400, 16400, 16440))

    self.window.connect("destroy", lambda w: gtk.main_quit())
    self.word = gtk.Label()  # The label to hold the word to guess
    self.word.set_attributes(self.attr)
    self.word.set_size_request(100,48)

    self.nbutt = gtk.Button(label="Next word")
    self.showbutt = gtk.Button(label="Show answer")
    self.answerlabel = gtk.Label(" ") # The label to show the answer, and to show wether the answer was correct
    self.guess = gtk.Entry() # The entry to guess the answer
    self.vbox = gtk.VBox()
    self.hbox = gtk.HBox()
    between = gtk.HSeparator()
    between.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(16400, 16400, 16440))
    self.hbox.pack_start(self.guess)
    self.hbox.pack_start(between,padding=10)
    self.hbox.pack_start(self.nbutt)
    #self.hbox.pack_start(image)
    self.vbox.pack_start(self.word)
    self.vbox.pack_start(self.hbox,padding=5)
    self.vbox.pack_start(self.showbutt)
    self.vbox.pack_start(self.answerlabel)
    self.window.set_position(gtk.WIN_POS_CENTER)
    self.window.show()

    self.showbutt.connect("clicked", self.showanswer)

    #self.mainvbox = gtk.VBox()
    self.contentvbox = gtk.VBox()
    self.selecthbox = gtk.HBox()

    markup = "<span foreground='white'>Select dictionary:  </span>"
    self.selectlabel = gtk.Label()
    self.selectlabel.set_markup(markup)

    fixed = gtk.Fixed()
    fixed.put(self.cb, 150,0)
    fixed.put(self.selectlabel,0,8)
    self.label = gtk.Label("")
    fixed.put(self.label,0,0)

    #self.selecthbox.pack_start(self.selectlabel)
    self.selecthbox.pack_start(fixed) # The widget that holds the combobox

    #self.contentvbox.pack_start(vbox)
    self.contentvbox.pack_start(self.selecthbox)

    self.contentvbox.show_all()
    self.contentvbox.set_border_width(10)
    self.contentvbox.pack_start(self.vbox)


    vbox.pack_start(self.contentvbox)
    vbox.show()

    self.window.add(vbox)
    self.window.set_title("Pugg - "+ self.version)

    self.nbutt.connect("clicked", self.nextindex)
    self.guess.connect("activate", self.guessword)

  def main(self):
    gtk.main()

  def nextindex(self, next=1): # Function to chose the next word to guess, and make sure the program doesn't crash while doing it.
    if next:
        self.index += 1
    try:
      self.word.set_text(self.currentwords[self.index].capitalize())
    except IndexError:
      self.index = 0
      self.word.set_text(self.currentwords[self.index].capitalize())
    #print self.index
    markup = "<span foreground='white'>"+ self.word.get_text() +"</span>"
    self.word.set_markup(markup)
    self.guess.set_text("")
    self.answerlabel.set_text(" ")
    self.showbutt.set_label("Show answer")
    self.showbutt.show()
    self.window.set_focus(self.guess)

  def guessword(self,guess): # Does what you would expect
    if guess.get_text().upper() == self.current[self.currentwords[self.index]].upper(): # Guess is correct
      self.showbutt.hide()
      markup = "<span foreground='green'>Correct!</span>"
      self.answerlabel.set_markup(markup)
      self.window.set_focus(self.nbutt)
    else: # Guess is not correct
      markup = "<span foreground='red'>Not correct!</span>"
      self.answerlabel.set_markup(markup)
    #print guess.get_text().upper() + " : " + self.current[self.currentwords[self.index]].upper()

  def read_in_dict(self,fil): # Funtion to return a dictionary with all the words in a file, the first word is the key to the second for each line.
    f = open(fil)
    words = f.readlines()
    f.close()
    retlist = []
    dic = {}
    for line in words:
      retlist.append(line[:-1].split(self.splits))
    for i in retlist:
      dic[i[0]] = i[1]
    return dic


  def select(self,pdics,wanted): # Function that return the requested dictionary, "wanted" is the dictionary title, which is defined in column two in dicts.pugg
    for i in pdics:
      if i[1] == wanted:
        return self.read_in_dict(i[0])

  def on_changed(self,s): # A function that loads a new dictionary when a new dict is selected from the combobox, and randomly sorts a list of all the dict keys.
    self.index = 0
    self.current = self.select(self.parsed_dicts,self.cb.get_active_text())
    #print "current:",
    #print self.current

    self.currentwords = self.current.keys()
    random.shuffle(self.currentwords)
    #print self.currentwords
    self.nextindex(0)
    self.contentvbox.show_all()

  def showanswer(self,ob): # Does what you would expect
    if self.answerlabel.get_text() == " " or self.answerlabel.get_text() == "Not correct!":
      self.answerlabel.set_text(self.current[self.currentwords[self.index]].capitalize())
      self.showbutt.set_label("Hide answer")
      self.window.set_focus(self.nbutt)
    else:
      self.answerlabel.set_text(" ")
      self.showbutt.set_label("Show answer")
    markup = "<span foreground='white'>" + self.answerlabel.get_text() + "</span>"
    self.answerlabel.set_markup(markup)


if __name__ == "__main__":
  wind = win()
  wind.main()
