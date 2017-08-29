# encoding: utf-8

from bs4 import BeautifulSoup
from fpdf import FPDF
from Tkinter import *
from PyRTF import *
import PyRTF
import tkFileDialog
import tkMessageBox
import requests
import Tkinter
import urllib2
import urllib
import Image
import sys
import os

sys.path.append( '../' )

class simpleapp_tk(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()
	
	def initialize(self):
		self.grid()
		
		popup = Menu(self, tearoff=0)
		popup.add_command(label="Next") # , command=next) etc...
		popup.add_command(label="Previous")
		popup.add_separator()
		popup.add_command(label="Home")

		def do_popup(event):
			# display the popup menu
			try:
				popup.tk_popup(event.x_root, event.y_root, 0)
			finally:
				# make sure to release the grab (Tk 8.0a1 only)
				popup.grab_release()
		
		#url
		self.entry1Variable = Tkinter.StringVar()
		self.entry1 = Tkinter.Entry(self,textvariable=self.entry1Variable,width=70)
		self.entry1.grid(column=0,row=0,columnspan=5,sticky='w')
		button1 = Tkinter.Button(self,text=u"Vnos",command=self.Vnos,width=5)
		button1.grid(column=5,row=0, sticky='ew')
		
		#ime
		self.label1Variable = Tkinter.StringVar()
		label1 = Tkinter.Label(self,textvariable=self.label1Variable,anchor="w",width=5)
		label1.grid(column=0,row=1, sticky='w')
		self.label1Variable.set(u"Ime:")
		self.entry2Variable = Tkinter.StringVar()
		self.entry2 = Tkinter.Entry(self,textvariable=self.entry2Variable,width=70)
		self.entry2.grid(column=1,row=1,columnspan=5,sticky='w')
		
		#kopis
		self.label2Variable = Tkinter.StringVar()
		label2 = Tkinter.Label(self,textvariable=self.label2Variable,anchor="w",width=10)
		label2.grid(column=0,row=2,columnspan=2,sticky='w')
		self.label2Variable.set(u"Kratek opis:")
		
		self.text1 = Tkinter.Text(self, width=61, height=3,wrap='word')
		self.text1.grid(column=0,row=3,columnspan=6,sticky='w')
		self.scrollbar1 = Tkinter.Scrollbar(self, command=self.text1.yview)
		self.text1.config(yscrollcommand=self.scrollbar1.set)
		self.scrollbar1.grid(column=0,row=3,columnspan=6,sticky='ens')
		
		#cena
		self.label3Variable = Tkinter.StringVar()
		label3 = Tkinter.Label(self,textvariable=self.label3Variable,anchor="w",width=5)
		label3.grid(column=0,row=4, sticky='w')
		self.label3Variable.set(u"Cena:")
		self.entry3Variable = Tkinter.StringVar()
		self.entry3 = Tkinter.Entry(self,textvariable=self.entry3Variable,width=70)
		self.entry3.grid(column=1,row=4,columnspan=5,sticky='ew')
		
		#opis
		self.label4Variable = Tkinter.StringVar()
		label4 = Tkinter.Label(self,textvariable=self.label4Variable,anchor="w",width=7)
		label4.grid(column=0,row=5, sticky='w')
		self.label4Variable.set(u"Opis:")
		
		self.text2 = Tkinter.Text(self, width=61, height=10,wrap='word')
		self.text2.grid(column=0,row=6,columnspan=6,sticky='w')
		self.scrollbar2 = Tkinter.Scrollbar(self, command=self.text2.yview)
		self.text2.config(yscrollcommand=self.scrollbar2.set)
		self.scrollbar2.grid(column=0,row=6,columnspan=6,sticky='ens')

		#gumbi
		button6 = Tkinter.Button(self,text=u"SE brez vira",command=lambda v=False, se=True: self.makePDF(v, se),width=10)
		button6.grid(column=2,row=9, sticky='ew')
		button7 = Tkinter.Button(self,text=u"SE z virom",command=lambda v=True, se=True: self.makePDF(v, se),width=10)
		button7.grid(column=3,row=9, sticky='ew')
		
		button9 = Tkinter.Button(self,text=u"EPS brez vira",command=lambda v=False, se=False: self.makePDF(v, se),width=10)
		button9.grid(column=2,row=10, sticky='ew')
		button10 = Tkinter.Button(self,text=u"EPS z virom",command=lambda v=True, se=False: self.makePDF(v, se),width=10)
		button10.grid(column=3,row=10, sticky='ew')
		
		button11 = Tkinter.Button(self,text=u"RTF SE",command=lambda se=1: self.MakeRTF(se),width=10)
		button11.grid(column=2,row=11, columnspan=1, sticky='ew')
		button12 = Tkinter.Button(self,text=u"RTF EPS",command=lambda se=2: self.MakeRTF(se),width=10)
		button12.grid(column=3,row=11, columnspan=1, sticky='ew')
		button13 = Tkinter.Button(self,text=u"RTF prazen",command=lambda se=0: self.MakeRTF(se),width=10)
		button13.grid(column=2,row=12, columnspan=2, sticky='ew')
		
		button14 = Tkinter.Button(self,text=u"Briši",command=self.Brisi,width=10)
		button14.grid(column=2,row=13, columnspan=2, sticky='ew')
		
		self.grid_columnconfigure(0,weight=1)
		self.resizable(False,False)
		self.update()
		self.geometry(self.geometry())	   
		self.entry1.focus_set()
		self.entry1.selection_range(0, Tkinter.END)

	def Brisi(self):
		self.entry1.delete(0,Tkinter.END)
		self.entry2.delete(0,Tkinter.END)
		self.entry3.delete(0,Tkinter.END)
		self.text1.delete('1.0', Tkinter.END)
		self.text2.delete('1.0', Tkinter.END)
		img = []
		
	def Vnos(self): #vnese podatke z nepremicnine.net
		url = self.entry1Variable.get()
		if url[0:7] != 'http://':
			url = 'http://'+url
		request = urllib2.Request(url)
		request.add_header('Accept-Encoding', 'utf-8')
		response = urllib2.urlopen(request)
		soup = BeautifulSoup(response)
		tabela = soup.find_all('table', attrs={'border':'1'})[0]
		tentries = tabela.find_all('tr')
		global vrsta
		vrsta = unicode(tentries[1].find_all('td')[0].get_text())
		global velikost
		velikost = unicode(tentries[5].find_all('td')[0].get_text())
		global img
		if soup.find(class_ = "rsImg") != None:
			img = soup.find_all(class_="rsImg")
		if soup.find(class_ = "web-opis") != None:
			wopis = unicode(soup.find_all(class_="web-opis")[0].get_text())
			wopis = wopis[13:len(wopis)]
		kopis = unicode(soup.find_all(class_="kratek")[0].get_text())
		global nasl
		nasl = unicode(soup.find_all(class_="kratek")[0].strong.get_text())
		global cena
		cena = unicode(soup.find_all(class_="cena")[0].get_text())
		global pime
		pime =''
		global ptel
		ptel=''
		if soup.find(class_ = "prodajalec") != None:
			pime = unicode(soup.find_all(class_="prodajalec")[0].h2.get_text())
		if soup.find(class_ = "tel") != None:
			ptel = unicode(soup.find_all(class_="tel")[0].get_text())
		self.entry2.delete(0,Tkinter.END)
		self.entry2.insert(0,nasl)
		self.text1.delete('1.0', Tkinter.END)
		self.text1.insert('1.0', kopis[len(nasl)+2:len(kopis)-len(cena)-8])
		self.entry3.delete(0,Tkinter.END)
		self.entry3.insert(0,cena[1:len(cena)])
		self.text2.delete('1.0', Tkinter.END)
		if soup.find(class_ = "web-opis") != None:
			self.text2.insert('1.0', wopis)
		
	def makePDF(self, virbool, se):
		if se:
			pdf=SE()
			pdnm='pdf/se'
		else:
			pdf=EPS()
			pdnm='pdf/eps'
		pdf.alias_nb_pages()
		pdf.add_page()
		pdf.add_font('DejaVu', '', 'resources/DejaVuSansCondensed.ttf', uni=True)
		pdf.add_font('DejaVu', 'B', 'resources/DejaVuSansCondensed-Bold.ttf', uni=True)
		pdf.set_font('DejaVu','B',10)
		a = pdf.get_string_width(self.entry2.get())
		pdf.cell(a,5,self.entry2.get(),0,0)
		pdf.ln()
		pdf.set_font('DejaVu','',10)
		pdf.multi_cell(0,5,self.text1.get("1.0",'end-1c'),0,1)
		pdf.set_font('DejaVu','B',10)
		pdf.cell(0,5,self.entry3.get(),0,1)
		pdf.set_font('DejaVu','',10)
		pdf.ln()
		pdf.multi_cell(0,5,self.text2.get("1.0",'end-1c'),0,1)
		pdf.ln()
		imgv=[]
		imgh=[]
		hbool = True
		vbool = True
		hrat = 0 
		vrat = 0
		for s in img:
			fname = "resources/"+str(s.get('href')).split('/')[-1]
			urllib.urlretrieve(s.get('href'), fname)
			imgf = Image.open(fname)
			sizes = imgf.size # (width,height) tuple
			w = sizes[0]
			h = sizes[1]
			#horizontal
			if w > h:
				if h/w != 0.66:
					if int(0.66*w) <= h:
						imgf.crop((0, 0, w, int(0.66*w))).save(fname)
					else:
						imgf.crop((0, 0, int(h/0.66), h)).save(fname)
				imgh.append(fname)
			#vertical
			elif w < h:
				if w/h != 0.66:
					if int(0.66*h) <= w:
						imgf.crop((0, 0, int(0.66*h), h)).save(fname)
					else:
						imgf.crop((0, 0, w, int(w/0.66))).save(fname)
				imgv.append(fname)
			imgf.load()
		imghn = len(imgh)
		imgvn = len(imgv)
		remh = imghn%2
		rowsh = imghn//2
		remv = imgvn%3
		rowsv = imgvn//3
		cy = pdf.get_y()
		pagewidth = pdf.w - pdf.r_margin - pdf.x
		pageheight = pdf.h - pdf.t_margin - pdf.b_margin
		hpos = (pagewidth - 68) / 2.0 + pdf.l_margin
		vpos = (pagewidth - 46) / 2.0 + pdf.l_margin
		for s in range(0, rowsv):
			cy = pdf.get_y()
			if pageheight-cy < 60:
				pdf.add_page()
				cy = pdf.get_y()
			pdf.image(imgv[len(imgv)-imgvn], y=pdf.get_y(), x=vpos-50.5, w=46)
			pdf.image(imgv[len(imgv)-imgvn+1], y=cy, x=vpos, w=46)
			pdf.image(imgv[len(imgv)-imgvn+2], y=cy, x=vpos+50.5, w=46)
			imgvn = imgvn-3
			pdf.ln(76)			
		for s in range(0,rowsh):
			cy = pdf.get_y()
			if pageheight-cy < 50:
				pdf.add_page()
				cy = pdf.get_y()
			pdf.image(imgh[len(imgh)-imghn], y=pdf.get_y(),x=hpos-37.5, w=68)
			pdf.image(imgh[len(imgh)-imghn+1], y=cy, x=hpos+37.5, w=68)
			imghn = imghn-2
			pdf.ln(50)	
		if remv == 2:
			cy = pdf.get_y()
			if pageheight-cy < 60:
				pdf.add_page()
				cy = pdf.get_y()
			pdf.image(imgv[len(imgv)-imgvn], y=pdf.get_y(),x=vpos-26.5, w=46)
			pdf.image(imgv[len(imgv)-imgvn+1], y=cy, x=vpos+26.5, w=46)
			imgvn = imgvn-2
			pdf.ln(76)
		if remh == 1:
			cy = pdf.get_y()
			if pageheight-cy < 50:
				pdf.add_page()
				cy = pdf.get_y()
			cy = pdf.get_y()
			pdf.image(imgh[len(imgh)-imghn], y=pdf.get_y(),x=hpos, w=68)
			pdf.ln(50)
		if remv == 1:
			cy = pdf.get_y()
			if pageheight-cy < 50:
				pdf.add_page()
				cy = pdf.get_y()
			cy = pdf.get_y()
			pdf.image(imgv[len(imgv)-imgvn], y=pdf.get_y(),x=vpos, w=46)
			pdf.ln(76)
		if virbool:
			pdf.ln(10)
			pdf.set_text_color(0,0,255)
			pdf.set_font('DejaVu','U',10)
			pdf.cell(0,5, self.entry1Variable.get(),0,1,'L',0, self.entry1Variable.get())
			pdf.set_text_color(0,0,0)
			pdf.set_font('DejaVu','',10)
			a = max(pdf.get_string_width(pime), pdf.get_string_width(ptel))
			pdf.multi_cell(a+5,5, pime+'\ntel: '+ptel,0,'L', 0)
			pdf.output(pdnm+'_'+nasl+'_'+vrsta+'_'+velikost+'_'+cena+'_'+self.entry1Variable.get()[len('http://www.nepremicnine.net/nepremicnine.html?id='):len(self.entry1Variable.get())]+'_v.pdf','F')
		else:
			pdf.output(pdnm+'_'+nasl+'_'+vrsta+'_'+velikost+'_'+cena+'_'+self.entry1Variable.get()[len('http://www.nepremicnine.net/nepremicnine.html?id='):len(self.entry1Variable.get())]+'.pdf','F')
		
		#fix dis ting
		for s in imgv:
			os.remove(s)
		for s in imgh:
			os.remove(s)
		tkMessageBox.showinfo("Status", "Končano")
		
	def MakeRTF(self, se) :
		doc     = Document()
		ss      = doc.StyleSheet
		section = Section()
		doc.Sections.append( section )

		#header
		# fix image size
		head = ParagraphPS()
		head.SetAlignment(TabPS.CENTER)
		p = Paragraph( ss.ParagraphStyles.Normal, head )
		
		if (se == 1):
			image = PyRTF.Image( 'resources/sertf.png' )
		elif (se == 2):
			image = PyRTF.Image( 'resources/epsrtf.png' )
		if (se > 0):
			p.append( image )
			section.Header.append( p )
			section.Header.append( '' )
		
		#footer
		
		pod = ''
		#convert to utf8
		if (se == 1):
			for char in unicode('Novi list d.o.o., Žabjak 2, 1000 Ljubljana, Slovenija, GSM: +386 (0)51 622 444\ninfo@sloveniaestates.com, www.sloveniaestates.com','utf-8'):
				pod = pod + '\\' + 'u' + str(ord(char)) + '?'
		elif (se == 2):
			for char in unicode('Agencija Elite d.o.o., Žabjak 2, 1000 Ljubljana, Slovenija, GSM: +386 (0)51 299 065\ninfo@elitepropertyslovenia.com, www.elitepropertyslovenia.com','utf-8'):
				pod = pod + '\\' + 'u' + str(ord(char)) + '?'
		if (se > 0):
			foot = ParagraphPS()
			foot.SetAlignment(TabPS.CENTER)
			p = Paragraph( ss.ParagraphStyles.Normal, foot )
			p.append( pod )
			section.Footer.append( p )
		
		#title
		rtftitle = ""
		for char in unicode(self.entry2.get()):
			rtftitle = rtftitle + '\\' + 'u' + str(ord(char)) + '?'
		p = Paragraph( ss.ParagraphStyles.Normal )
		p.append(TEXT( rtftitle, bold=True ))
		section.append(p)

		#kopis
		rtfkopis=""
		#convert to utf8
		for char in unicode(self.text1.get("1.0",'end-1c')):
			rtfkopis = rtfkopis + '\\' + 'u' + str(ord(char)) + '?'
		p = Paragraph( ss.ParagraphStyles.Normal )
		p.append(TEXT( rtfkopis, bold=False ))
		section.append( p )
		
		#cena
		rtfcena = ""
		for char in unicode(self.entry3.get()):
			rtfcena = rtfcena + '\\' + 'u' + str(ord(char)) + '?'
		p = Paragraph()
		p.append(TEXT( rtfcena, bold=True ))
		section.append( p )
		
		section.append( '' )
		
		#opis
		# utf8 converter
		rtfopis=""
		#convert to utf8
		for char in unicode(self.text2.get("1.0",'end-1c')):
			rtfopis = rtfopis + '\\' + 'u' + str(ord(char)) + '?'
		p = Paragraph( ss.ParagraphStyles.Normal )
		p.append(TEXT( rtfopis, bold=False ))
		section.append( p )

		section.append( '' )

		pslike = ParagraphPS()
		pslike.SetAlignment(TabPS.CENTER)
		p = Paragraph( ss.ParagraphStyles.Normal, pslike )
		
		imgv=[]
		imgh=[]
		hbool = True
		vbool = True
		hrat = 0 
		vrat = 0
		for s in img:
			fname = "resources/"+str(s.get('href')).split('/')[-1]
			urllib.urlretrieve(s.get('href'), fname)
			
			imgf = Image.open(fname)
			sizes = imgf.size # (width,height) tuple
			w = sizes[0]
			h = sizes[1]
			
			#horizontal
			if w > h:
				if h/w != 0.66:
					if int(0.66*w) <= h:
						imgf.crop((0, 0, w, int(0.66*w)))					
					else:
						imgf.crop((0, 0, int(h/0.66), h))
				basewidth = 230
				wpercent = (basewidth/float(imgf.size[0]))
				hsize = int((float(imgf.size[1])*float(wpercent)))
				imgf.thumbnail((basewidth,hsize), Image.ANTIALIAS)
				imgf.save(fname)
				imgh.append(fname)
			
			#vertical
			elif w < h:
				if w/h != 0.66:
					if int(0.66*h) <= w:
						imgf.crop((0, 0, int(0.66*h), h))
					else:
						imgf.crop((0, 0, w, int(w/0.66)))
				basewidth = 155
				wpercent = (basewidth/float(imgf.size[0]))
				hsize = int((float(imgf.size[1])*float(wpercent)))
				imgf.thumbnail((basewidth,hsize), Image.ANTIALIAS)
				imgf.save(fname)
				
				imgv.append(fname)
			
			imgf.load()

		imghn = len(imgh)
		imgvn = len(imgv)
		remh = imghn%2
		rowsh = imghn//2
		remv = imgvn%3
		rowsv = imgvn//3

		for s in range(0, rowsv):
			i1 = PyRTF.Image(imgv[len(imgv)-imgvn])
			i2 = PyRTF.Image(imgv[len(imgv)-imgvn+1])
			i3 = PyRTF.Image(imgv[len(imgv)-imgvn+2])
			p.append( i1 )
			p.append(" ")
			p.append( i2 )
			p.append(" ")
			p.append( i3 )
			imgvn = imgvn-3	
		
		for s in range(0,rowsh):
			i1 = PyRTF.Image(imgh[len(imgh)-imghn])
			i2 = PyRTF.Image(imgh[len(imgh)-imghn+1])
			p.append( i1 )
			p.append(" ")
			p.append( i2 )
			imghn = imghn-2	

		if remv == 2:
			i1 = PyRTF.Image(imgv[len(imgv)-imgvn])
			i2 = PyRTF.Image(imgv[len(imgv)-imgvn+1])
			p.append( i1 )
			p.append(" ")
			p.append( i2 )
			imgvn = imgvn-2

		if remh == 1:
			i1 = PyRTF.Image(imgh[len(imgh)-imghn])
			p.append( i1 )

		if remv == 1:
			i1 = PyRTF.Image(imgv[len(imgv)-imgvn])
			section.append( Paragraph( i1 ) )
		
		section.append( p )
		if (se == 1):
			rtn = 'se_'
		elif (se == 2):
			rtn = 'eps_'
		else:
			rtn = 'blank_'
		namertf = rtn+nasl+'_'+vrsta+'_'+velikost+'_'+cena+'_'+self.entry1Variable.get()[len('http://www.nepremicnine.net/nepremicnine.html?id='):len(self.entry1Variable.get())]
		
		DR.Write( doc, OpenFile( namertf ) )
		
		for s in imgv:
			os.remove(s)
		for s in imgh:
			os.remove(s)
			
		tkMessageBox.showinfo("Status", "Končano")
			
class EPS(FPDF):
		def header(this):
				# Logo
				pagewidth = this.w - this.r_margin - this.x
				xpos = (pagewidth - 50) / 2.0 + this.l_margin
				this.image('resources/eps.jpg', xpos, 8, 50, 0)
				# Line break
				this.ln(30)

		# Page footer
		def footer(this):
				# Position at 1.5 cm from bottom
				this.set_y(-15)
				# Arial italic 8
				this.add_font('DejaVu', '', 'resources/DejaVuSansCondensed.ttf', uni=True)
				this.set_font('DejaVu','',10)
				# Page number
				this.line(10,282,200,282)
				this.cell(0, 5, u'Agencija Elite d.o.o., Žabjak 2, 1000 Ljubljana, Slovenija, GSM: +386 (0)51 299 065',0,1,'C',0)
				this.set_text_color(0,0,255)
				this.set_font('DejaVu','U',10)
				a = this.get_string_width(u'info@elitepropertyslovenia.com')
				b = this.get_string_width(u', ')
				c = this.get_string_width(u'www.elitepropertyslovenia.com')
				d = this.get_string_width(u'info@selitepropertyslovenia.com, www.elitepropertyslovenia.com')
				pagewidth = this.w - this.r_margin - this.x
				hpos = (pagewidth - d) / 2.0
				this.cell(hpos)
				this.cell(a,5, u'info@elitepropertyslovenia.com',0,0, 'L', 0, 'mailto:info@elitepropertyslovenia.com')
				this.set_text_color(0,0,0)
				this.set_font('DejaVu','',10)
				this.cell(b,5, u', ',0,0, 'L', 0)
				this.set_text_color(0,0,255)
				this.set_font('DejaVu','U',10)
				this.cell(c,5, u'www.elitepropertyslovenia.com',0,1,'L',0, 'http://www.elitepropertyslovenia.com')
			
class SE(FPDF):
		def header(this):
				# Logo
				pagewidth = this.w - this.r_margin - this.x
				xpos = (pagewidth - 50) / 2.0 + this.l_margin
				this.image('resources/logo.png', xpos, 8, 50, 0)
				# Line break
				this.ln(30)

		# Page footer
		def footer(this):
				# Position at 1.5 cm from bottom
				this.set_y(-15)
				# Arial italic 8
				this.add_font('DejaVu', '', 'resources/DejaVuSansCondensed.ttf', uni=True)
				this.set_font('DejaVu','',10)
				# Page number
				this.line(10,282,200,282)
				this.cell(0, 5, u'Novi list d.o.o., Žabjak 2, 1000 Ljubljana, Slovenija, GSM: +386 (0)51 622 444',0,1,'C',0)
				this.set_text_color(0,0,255)
				this.set_font('DejaVu','U',10)
				a = this.get_string_width(u'info@sloveniaestates.com')
				b = this.get_string_width(u', ')
				c = this.get_string_width(u'www.sloveniaestates.com')
				d = this.get_string_width(u'info@sloveniaestates.com, www.sloveniaestates.com')
				pagewidth = this.w - this.r_margin - this.x
				hpos = (pagewidth - d) / 2.0
				this.cell(hpos)
				this.cell(a,5, u'info@sloveniaestates.com',0,0, 'L', 0, 'mailto:info@sloveniaestates.com')
				this.set_text_color(0,0,0)
				this.set_font('DejaVu','',10)
				this.cell(b,5, u', ',0,0, 'L', 0)
				this.set_text_color(0,0,255)
				this.set_font('DejaVu','U',10)
				this.cell(c,5, u'www.sloveniaestates.com',0,1,'L',0, 'http://www.sloveniaestates.com')

def rClicker(e):
    try:
        def rClick_Copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')

        def rClick_Cut(e):
            e.widget.event_generate('<Control-x>')

        def rClick_Paste(e):
            e.widget.event_generate('<Control-v>')

        e.widget.focus()

        nclst=[
               (' Cut', lambda e=e: rClick_Cut(e)),
               (' Copy', lambda e=e: rClick_Copy(e)),
               (' Paste', lambda e=e: rClick_Paste(e)),
               ]

        rmenu = Menu(None, tearoff=0, takefocus=0)

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")

    except TclError:
        print ' - rClick menu, something wrong'
        pass

    return "break"

def rClickbinder(r):
	try:
		for b in [ 'Text', 'Entry', 'Listbox', 'Label']: #
			r.bind_class(b, sequence='<Button-3>',
						func=rClicker, add='')
	except TclError:
		print ' - rClickbinder, something wrong'
		pass
		
def OpenFile( name ) :
		return file( 'pdf/%s.rtf' % name, 'w' )
		
if __name__ == "__main__":
	# sys.stdout = open('resources/info.log', 'w')
	# sys.stderr = open('resources/err.log', 'w')
	DR = Renderer()
	app = simpleapp_tk(None)
	app.title('Nepremicnine.net')
	rClickbinder(app)
	app.mainloop()
