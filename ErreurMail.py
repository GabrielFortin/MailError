# Import de packages
# Import de 4 éléments faisant partie de la librairie tkinter (librairie d'interfaces graphiques)
from tkinter import Tk, Label, Button, messagebox
# Import de la libraire os, permettant des actions sur le système d'exploitation, dans notre cas, la lecture de fichiers
import os
# Import de la librairie regex, nous permettant de trouver des patterns dans des chaînes de caractères
import re
# Import de pip (Pip Install Packages) permettant d'installer des packages (libraires)
import pip

# Fonction permettant d'installer un package
def install(package):
	if hasattr(pip, 'main'):
		pip.main(['install', package])
	else:
		pip._internal.main(['install', package])

# Essaie d'importer le package extract_msg (pour lire les fichiers .msg) et l'installe si introuvable
try:
	import extract_msg
except:
	install('extract-msg')
	import extract_msg

# Classe représentant l'interface utilisateur
class ErreurMail:
	# Fonction d'initialisation qui prend en paramètre un processus Tkinter
	def __init__(self, master):
		self.master = master
		master.title("ErreurMail")

		# Création d'un label
		self.title = Label(master, text="Bienvenue dans ErreurMail")
		# Ajout du label dans l'interface
		self.title.pack()

		# Création d'un autre label et ajout dans l'interface
		self.label = Label(master, text="Appuyer sur le bouton pour lire les fichiers.")
		self.label.pack()

		# Création d'un bouton et ajout dans l'interface qui appelle la fonction parse lorsqu'enfoncés
		self.greet_button = Button(master, text="Obtenir les adresses", command=self.parse)
		self.greet_button.pack()

	# Fonction qui lit chaque fichier et extrait les adresses erronées
	def parse(self):
		# Liste de tous les fichiers dans le dossier
		fichiers = os.listdir('.')

		# Liste qui va contenir les adresses erronées
		bad_addresses = []

		# On parcourt chaque fichier dans la liste intitulée fichiers
		for fichier in fichiers:
			# S'il s'agit d'un fichier .msg, on effectue la logique ci-dessous
			if '.msg' in fichier:
				msg = extract_msg.Message(fichier)
				msg_message = msg.body

				# Cas #1: Failed Recipients
				if re.findall('Failed+\s+Recipient+:+.+', msg_message):
					address = re.findall('Failed+\s+Recipient+:+.+', msg_message)[0]
					address = address.replace('Failed Recipient: ', '')

					if '<' in address:
						address = address.replace('<', '')

				# Cas #2: *@*
				elif re.findall('\(+.+\@+.+\)', msg_message):
					address = re.findall('\(+.+\@+.+\)', msg_message)[0]
					address = address.replace('(', '').replace(')', '')

				# Si aucun cas, on passe au fichier suivant et on log l'erreur
				else:
					print("Le fichier nommé " + str(fichier) + " a été sauté puisque le programme n'a pas pu trouver d'adresse courriel erronée.")
					continue

				# On enlève les espaces, retour à la ligne et autres
				address = address.replace('"', '').replace(' ', '')
				address = address.replace('\n', '').replace('\r', '')

				# On ajoute l'adresse nouvellement trouvée à notre liste
				bad_addresses.append(address)

			# Sinon, on passe au fichier suivant
			else:
				continue

		# On ouvre le fichier de sortie en mode écriture (write) en le nommant file
		with open('Addresses_erronees.txt', 'w') as file:
			# On crée une nouvelle chaîne de caractères vide
			to_write = ""

			# Pour chaque adresse erronée, on l'ajoute dans la chaîne de caractères nouvellement créée, et on ajoute un retour à la ligne
			for address in bad_addresses:
					to_write += address
					if '\n' not in address and '\r' not in address:
						to_write += '\n'

			# On écrit cette chaîne de caractères dans le fichier
			file.write(to_write)

		# Lorsque l'écriture est terminée, on affiche une fenêtre d'informations dans l'interface.
		messagebox.showinfo(title="Terminé", message="Tous les fichiers ont été parcourus. Un fichier nommé 'Adresses erronées' a été créé dans le dossier où se trouve le programme.")

# Fonction main
if __name__ == '__main__':
	# On crée un processus tkinter (librairie d'interface utilisateur)
	root = Tk()

	# On crée une instance de notre classe en lui donnant en paramètre notre processus tkinter nouvellement créé
	erreurMail = ErreurMail(root)

	# On définit les dimensions de la fenêtre
	root.geometry("500x200")

	# On démarre l'interface utilisateur dans une boucle infinie (fonction de la librairie tkinter)
	root.mainloop()
