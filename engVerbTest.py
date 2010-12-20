# English Verb Test Generator

#non rimuovere!
version = "1.0"

# by PicciMario (mario.piccinelli@gmail.com)
# Semplice script python per generare in modo casuale e automatico testi 
# (in formato PDF, da stampare) di verifiche di inglese sui verbi (regolari 
# e irregolari) per scuole medie/superiori italiane.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Requires: ReportLab PDF Generator
# http://www.reportlab.org/oss/rl-toolkit/download/

import random
import time
import datetime
import getopt
import sys
from reportlab.pdfgen.canvas import Canvas

#parametri di default
numeroPagine = 1
nomeFile = "verifica.pdf"

numVerbiRegolari = 28

#------- help ----------------------------------------------------

def usage():
	print("Opzioni:")
	print("-n num\t\timposta il numero di pagine");
	print("-f nomefile\timposta il file di output");
	print("-h --help\tquesto help");
	print("")

#------- acquisizione dei parametri da riga di comando ------------

print("\nEnglish Verb Test Generator - ver. %s")%version
print("PicciMario <mario.piccinelli@gmail.com>")
print("https://sourceforge.net/projects/verbtestgen/\n")

try:
    opts, args = getopt.getopt(sys.argv[1:], "hhn:f:", ["--help","-h","-n"])
except getopt.GetoptError, err:
    #print("%s\n"%str(err))
    usage()
    sys.exit(2)
    
output = None
for o, a in opts:
    if o == "-n":
    	numeroPagine = int(a)
    elif o in ("-h", "--help"):
    	usage()
        sys.exit()
    elif o in ("-f"):
        nomeFile = a
    else:
        assert False, "Opzione non conosciuta"

print("Richieste %i pagine"%numeroPagine)
print("File di output: %s"%nomeFile)

#acquisizione lista verbi irregolari e regolari
try:
	from engVerbArchive import verbs,regverbs
except:
	print("Errore: Impossibile caricare archivio verbi.\n")
	sys.exit(2)

print("Numero di verbi irregolari: %i (%i da estrarre)"%(len(verbs),numVerbiRegolari))

numeroVerbiRegolari = 0
for element in regverbs:
	numeroVerbiRegolari += len(element)

print("Numero di verbi regolari: %i (%i famiglie, un verbo per famiglia)"%(numeroVerbiRegolari, len(regverbs)))

#creazione canvas PDF
pdf = Canvas(nomeFile)

for pagina in range(1,numeroPagine+1):

	#-------- generazione liste troncate -----------------------

	result = [];
	random.seed()
	random.shuffle(verbs)
	verbiRegolariSelezionati = verbs[0:numVerbiRegolari]
	
	for verb in verbiRegolariSelezionati:
		i = (int)(random.random()*len(verb))
		if i==0:
			result.append(["%s"%(verb[0]),"","",""])
		if i==1:
			result.append(["","%s"%(verb[1]),"",""])		
		if i==2:
			result.append(["","","%s"%(verb[2]),""])		
		if i==3:
			result.append(["","","","%s"%(verb[3])])
	
	for verbfamily in regverbs:
		random.shuffle(verbfamily)
		verb = verbfamily[0]
		if ((int)(random.random()*len(verb)) == 0):
			result.append(["%s"%verb[0],"","",""])
		else:
			result.append(["","","","%s"%verb[1]])
	
	random.shuffle(result)	
	
	#-------- generazione pagina pdf -----------------------
	
	pdf.setStrokeColorRGB(0, 0, 0)
	
	#data e ora
	pdf.setFont("Courier", 10)
	data = datetime.date.today()
	pdf.drawString(50,20,"%s"%data)
	
	#numero pagina
	pdf.setFont("Courier", 10)
	pdf.drawString(480,20,"pagina %i/%i"%(pagina,numeroPagine))
	
	#intestazione
	pdf.setFont("Courier", 20)
	pdf.drawString(180,800,"VERIFICA DI INGLESE")
	
	pdf.setFont("Courier", 12)
	
	pdf.drawString(50,770,"Nome:")
	pdf.line(50+70,770,50+200,770)
	
	pdf.drawString(50,755,"Cognome:")
	pdf.line(50+70,755,50+200,755)
	
	pdf.drawString(50,740,"Classe:")
	pdf.line(50+70,740,50+200,740)
	
	pdf.drawString(50,725,"Data:")
	pdf.line(50+70,725,50+200,725)
	
	x=40
	y=670
	width=127
	height=19
	
	#Intestazioni colonne
	
	pdf.rect(x, y, width, 2*height, stroke = True, fill = False)
	pdf.drawString(x+10, y+15, "Forma Base")
	
	pdf.rect(x+width, y, width, 2*height, stroke = True, fill = False)
	pdf.drawString(x+10+width, y+15, "Passato")
	
	pdf.rect(x+width*2, y, width, 2*height, stroke = True, fill = False)
	pdf.drawString(x+10+width*2, y+25, "Participio")
	pdf.drawString(x+10+width*2, y+10, "Passato")
	
	pdf.rect(x+width*3, y, width, 2*height, stroke = True, fill = False)
	pdf.drawString(x+10+width*3, y+15, "Italiano")
	
	y -= height
	
	#Stampa elementi nel PDF
	
	for verbo in result:
		for i in range(0,4):
			pdf.rect(x+width*i, y, width, height, stroke = True, fill = False)
			pdf.drawString(x+width*i+10, y+7, verbo[i])
		y=y-height
	
	pdf.showPage()
	
	print("Conclusa la pagina %i."%pagina)

pdf.save()

print("Generazione conclusa con successo.\n")
