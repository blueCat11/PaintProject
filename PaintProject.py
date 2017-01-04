#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as tk
from tkColorChooser import askcolor
import tkMessageBox
import tkSimpleDialog
import tkFileDialog
from PIL import Image, ImageTk, ImageDraw
import numpy as np

class PaintGui(object):
	def __init__(self, root):
		self.penThickness = 1
		self.root = root
		self.root.title("Mini-Paint")
		self.imageSize = 240, 200
		self.root.minsize(width = 600, height = 500)
		self.currentPaintColor = (0,0,0)
		self.menuBar()
		self.paintImage = Image.new("RGB", (self.imageSize[0], self.imageSize[1]), "white")
		self.draw = ImageDraw.Draw(self.paintImage)
		self.lifePhotoImage = ImageTk.PhotoImage(self.paintImage)
		self.lifeImageLabel = tk.Label(root, image=self.lifePhotoImage, borderwidth=0, cursor="cross")
		self.lifeImageLabel.bind("<B1-Motion>", self.mouseMove)
		self.lifeImageLabel.bind("<ButtonPress-1>", self.mouseDown)
		self.lifeImageLabel.bind("<ButtonRelease-1>", self.mouseUp)
		self.lifeImageLabel.bind("<Configure>", lambda(e): self.showImage())
		self.lifeImageLabel.pack(side="top", fill="both", expand=True)
		self.file_opt = options = {}
		options['filetypes'] = [('PNG Datei', '.png')]
	@property
	def screenSize(self):
		return self.lifeImageLabel.winfo_width(), self.lifeImageLabel.winfo_height()
	def mousePosition(self, event):
		currentScreenSize = self.screenSize
		return event.x * self.imageSize[0] / currentScreenSize[0], event.y * self.imageSize[1] / currentScreenSize[1]
	def mouseDown(self, event):
		self.mouseX, self.mouseY = self.mousePosition(event)
		self.penColor = self.currentPaintColor if self.paintImage.getpixel((self.mouseX, self.mouseY)) != (0,0,0) else (255,255,255)  
		print self.penThickness
		self.draw.line((self.mouseX, self.mouseY, self.mouseX, self.mouseY), fill=self.penColor, width = self.penThickness)
		self.showImage()
	def mouseUp(self, event):
		self.mouseX , self.mouseY = -1, -1
	def mouseMove(self, event):
		currentMousePosition = self.mousePosition(event)
		if currentMousePosition != (self.mouseX, self.mouseY):
			self.draw.line((self.mouseX, self.mouseY, currentMousePosition[0], currentMousePosition[1]), fill=self.penColor)
			self.mouseX, self.mouseY = currentMousePosition
			self.showImage()
	def showImage(self):
		self.resizedImage = self.paintImage.resize(self.screenSize, Image.NEAREST)
		self.lifePhotoImage = ImageTk.PhotoImage(self.resizedImage)
		self.lifeImageLabel.config(image=self.lifePhotoImage)
	def setImageSize(self, size):
		self.imageSize = size
		self.paintImage = Image.new("RGB", (self.imageSize[0], self.imageSize[1]), "white")
		self.draw = ImageDraw.Draw(self.paintImage)
		self.showImage()
	def save(self):
		name = tkFileDialog.asksaveasfilename(**self.file_opt)
		if name is None or name is "":
			tkMessageBox.showinfo("Speicherabbruch", "Ihr Bild wurde noch nicht gespeichert")
		else:
			self.paintImage.save(name+".png")
			tkMessageBox.showinfo("Speichern", "Ihr Bild wurde gespeichert")
	def open(self):
		name = tkFileDialog.askopenfilename(**self.file_opt)
		if name is None or name is "":
			tkMessageBox.showinfo("Abbruch", "Es wurde kein Bild zum Öffnen ausgewählt") 
		else:
			self.paintImage = Image.open(name)
			self.draw = ImageDraw.Draw(self.paintImage)
			self.showImage()
	def chooseColor(self):
		color = askcolor() 
		self.currentPaintColor = color[0]
	def erase(self):
		self.currentPaintColor = (255, 255, 255)
	def changePenThickness(self, pen):
		print pen
		self.penThickness = pen
	def menuBar(self):
		menuMain = tk.Menu(self.root)
		menuHelp = tk.Menu(menuMain, tearoff=0)
		menuPenThickness = tk.Menu(menuMain, tearoff = 0)
		self.rules = tk.IntVar()
		self.rules.set(0)
		menuMain.add_command(label="Neu", underline=1, command = lambda: self.setImageSize((240, 200)))
		menuMain.add_command(label="Öffnen", command=self.open)
		menuMain.add_command(label="Speichern", underline=1, command = self.save)
		menuMain.add_command(label="Farbe", command = self.chooseColor)
		menuMain.add_command(label="Radieren", command = self.erase)
		menuMain.add_cascade(label = "Hilfe", underline=0, menu = menuHelp)
		menuMain.add_cascade(label = "Stiftdicke", menu = menuPenThickness)
		menuHelp.add_command(label="Über", underline=0, command = lambda: tkMessageBox.showinfo("Paint", "Wählen Sie eine Farbe und zeichnen Sie auf den Canvas\nRadieren Sie\nSpeichern Sie Ihr Werk ab"))
		menuPenThickness.add_command(label = "dünn", command = self.changePenThickness(pen =1))
		menuPenThickness.add_command(label="normal", command = self.changePenThickness(pen =5))
		#menuPenThickness.add_command(label = "dick", command = self.changePenThickness(pen =10))
		self.root.config(menu=menuMain)

root = tk.Tk()
mainWindow = PaintGui(root)
root.mainloop()
