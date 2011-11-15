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
from string import capitalize
pygtk.require('2.0')

class win:
  def __init__(self):

    self.score = 0 # The score
    self.guessed = 0
    self.allowscore = 1 # Score will only increase if allowscore is 1, when you show the answer it becomes 0
    self.reset_score_if_false_guess = 0

    self.version = "0.2.2"

##################################################################
                      ## Menu Stuff ##
    mb = gtk.MenuBar()

    filemenu = gtk.Menu()
    filem = gtk.MenuItem("File")
    filem.set_submenu(filemenu)
    exit = gtk.MenuItem("Exit")
    exit.connect("activate", gtk.main_quit)
    filemenu.append(exit)
    mb.append(filem)

    settingsmenu = gtk.Menu()
    settingsm = gtk.MenuItem("Settings")
    settingsm.set_submenu(settingsmenu)
    setbackscore = gtk.MenuItem("Reset score")
    falseguessreset = gtk.CheckMenuItem("False guess will reset score")
    falseguessreset.connect("toggled", self.falsetoggle)
    setbackscore.connect("activate", self.resetscore)
    settingsmenu.append(setbackscore)
    settingsmenu.append(falseguessreset)
    mb.append(settingsm)

    helpmenu = gtk.Menu()
    helpm = gtk.MenuItem("Help")
    helpm.set_submenu(helpmenu)
    about = gtk.MenuItem("About")
    about.connect("activate",self.aboutdialog)
    helpmenu.append(about)
    mb.append(helpm)
                       ## Menu stuff end ##
########################################################################

    vbox = gtk.VBox(False, 2)
    vbox.pack_start(mb, False, False, 0)
    vbox.show_all()

    self.splits = "!;!" # What the words are separated by in the dictionary. If you wanna use csv files, just change to ",".

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

    self.window.connect("destroy", lambda w: gtk.main_quit())
    self.word = gtk.Label()  # The label to hold the word to guess
    self.word.set_attributes(self.attr)
    self.word.set_size_request(100,48)

    self.nbutt = gtk.Button(label="Next word")
    self.showbutt = gtk.Button(label="Show answer")
    self.showbutt.set_size_request(332,40)
    self.answerlabel = gtk.Label(" ") # The label to show the answer, and to show wether the answer was correct
    self.answerlabel.set_line_wrap(True)
    self.answerlabel.set_size_request(300,50)
    self.guess = gtk.Entry() # The entry to guess the answer
    self.guess.set_size_request(250,30)

    self.vbox = gtk.VBox()
    self.hbox = gtk.HBox()

    entry_nbutt_hbox = gtk.HBox()
    entry_nbutt_hbox.pack_start(self.guess,padding=5)
    entry_nbutt_hbox.pack_start(self.nbutt,padding=5)
    self.hbox.pack_start(entry_nbutt_hbox,1,0)

    showbutthbox = gtk.HBox()
    showbutthbox.pack_start(self.showbutt,1,0,10)

    self.vbox.pack_start(self.word,0,0,10)
    self.vbox.pack_start(self.hbox,1,1,padding=10)
    self.vbox.pack_start(showbutthbox,1,1)
    self.vbox.pack_start(self.answerlabel)
    self.window.set_position(gtk.WIN_POS_CENTER)
    self.window.show()

    self.showbutt.connect("clicked", self.showanswer)

    self.contentvbox = gtk.VBox()
    self.selecthbox = gtk.HBox()
    markup = "<span>Select dictionary:  </span>"
    self.selectlabel = gtk.Label()
    self.selectlabel.set_markup(markup)

    fixed = gtk.Fixed()
    fixed.put(self.cb, 150,5)
    fixed.put(self.selectlabel,5,13)
    self.label = gtk.Label("")
    fixed.put(self.label,0,0)

    self.selecthbox.pack_start(fixed) 

    self.contentvbox.pack_start(self.selecthbox)

    self.contentvbox.show_all()
    self.contentvbox.pack_start(self.vbox,1,0)


    vbox.pack_start(self.contentvbox)
    vbox.show()

    self.statusbar = gtk.Statusbar()
    self.statusbar.show()
    self.statusbar.set_has_resize_grip(False)

    self.statusbar.push(1,"Correct guesses in a row: " + str(self.score))

    vbox.pack_start(self.statusbar,False,True,0)

    self.window.add(vbox)
    self.window.set_size_request(340,300)
    self.window.set_title("Pugg - "+ self.version)

    self.nbutt.connect("clicked", self.nextindex)
    self.guess.connect("activate", self.guessword)


  def nextindex(self, next=1): # Function to chose the next word to guess, and make sure the program doesn't crash while doing it.
    if next:
      self.index += 1
    try:
      self.word.set_text(self.currentwords[self.index].capitalize())
    except IndexError:
      self.index = 0
      self.word.set_text(self.currentwords[self.index].capitalize())

    markup = "<span>"+ self.word.get_text() +"</span>"
    self.word.set_markup(markup)
    self.guess.set_text("")
    self.answerlabel.set_text(" ")
    self.showbutt.set_label("Show answer")
    self.showbutt.set_sensitive(True)
    self.window.set_focus(self.guess)
    if not self.guessed:
      self.setscore(0)
    self.allowscore = 1
    self.guessed = 0

  def guessword(self,guess): # Does what you would expect
    if guess.get_text().upper() in self.current[self.currentwords[self.index]]: # Guess is correct
      self.showbutt.set_sensitive(False)
      #markup = "<span foreground='darkgreen'>Correct!</span>"
      #self.answerlabel.set_markup(markup)
      self.showanswer(0,guess.get_text().capitalize())
      self.window.set_focus(self.nbutt)
      self.setscore(1)
      self.guessed = 1
    else: # Guess is not correct
      markup = "<span foreground='red'>Not correct!</span>" # Don't change, will have effect on self.showanswer
      self.answerlabel.set_markup(markup)
      if self.reset_score_if_false_guess:
        self.setscore(0)

  def on_changed(self,s): # A function that loads a new dictionary when a new dict is selected from the combobox, and randomly sorts a list of all the dict keys.
    self.index = 0
    self.current = self.select(self.parsed_dicts,self.cb.get_active_text())

    self.currentwords = self.current.keys()
    random.shuffle(self.currentwords)
    self.nextindex(0)
    self.contentvbox.show_all()

  def capital(self,ize):
    n = ize.find(">")
    if n is -1:
      return ize.capitalize()
    else:
      return ize[:n]+ize[n].capitalize()+ize[n+1:]

  def showanswer(self,ob,correctguess=0): # Does what you would expect
    if self.answerlabel.get_text() == " " or self.answerlabel.get_text() == "Not correct!":
      orr = "<span foreground=\"darkblue\"> or </span>"
      comma = "<span foreground=\"darkblue\">, </span>"

      if correctguess: # If showanswer is called from self.guessword
        for i in range(len(self.current[self.currentwords[self.index]])):
          if self.current[self.currentwords[self.index]][i] == correctguess.upper():
            self.current[self.currentwords[self.index]][i] = "<span foreground=\"darkgreen\"><b>"+self.current[self.currentwords[self.index]][i].capitalize()+"</b></span>"
      else:
        self.setscore(0)

      text = orr.join([comma.join(map(self.capital,self.current[self.currentwords[self.index]][:-1])),
                                  self.capital(self.current[self.currentwords[self.index]][-1])])
      if text.startswith(orr):
        text = text[len(orr):]

      self.answerlabel.set_text(text)
      self.showbutt.set_label("Hide answer")
      self.window.set_focus(self.nbutt)
    else:
      self.answerlabel.set_text(" ")
      self.showbutt.set_label("Show answer")
    markup = "<span>" + self.answerlabel.get_text() + "</span>"
    self.answerlabel.set_markup(markup)

  def setscore(self,correct=0):
    if correct and self.allowscore:
      self.score += 1
      self.allowscore = 0
    else:
      self.score = 0
      self.allowscore = 0
    self.statusbar.push(1,"Correct guesses in a row: " + str(self.score))

  def resetscore(self,omg):
    self.score = 0
    self.statusbar.push(1,"Correct guesses in a row: " + str(self.score))

  def falsetoggle(self,omg):
    if omg.active:
      self.reset_score_if_false_guess = 1
    else:
      self.reset_score_if_false_guess = 0

  def read_in_dict(self,fil): # Funtion to return a dictionary with all the words in a file, the first word is the key to the second for each line.
    f = open(fil)
    words = f.readlines()
    f.close()
    retlist = []
    dic = {}
    for line in words:
      uline = line.upper()
      retlist.append(uline[:-1].split(self.splits))
    for i in retlist:
      try:
        dic[i[0]] = i[1].split("!-!")
      except IndexError:
        print "Invalid line in dictionary, continuing without it."
    return dic

  def select(self,pdics,wanted): # Function that return the requested dictionary, "wanted" is the dictionary title, which is defined in column two in dicts.pugg
    for i in pdics:
      if i[1] == wanted:
        return self.read_in_dict(i[0])

  def aboutdialog(self, widget):
    about = gtk.AboutDialog()
    about.set_program_name("Putt")
    about.set_version(self.version)
    about.set_copyright("Copyright (c) 2011 Mattias Ugelvik <smartestviking@gmail.com>")
    about.set_comments("Pugg is a tool to memorize words from other languages")
    about.set_website("http://smartviking.github.com/Pugg/")
    about.set_logo(gtk.AboutDialog().render_icon(gtk.STOCK_DIALOG_INFO,gtk.ICON_SIZE_DIALOG))
    about.set_license(open("gpl.txt").read())
    about.set_authors(["Mattias Ugelvik <smartestviking@gmail.com>"])
    about.set_documenters(["Mattias Ugelvik <smartestviking@gmail.com>"])
    about.run()
    about.destroy()

  def main(self):
    gtk.main()

if __name__ == "__main__":
  wind = win()
  wind.main()
