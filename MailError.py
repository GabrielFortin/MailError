from tkinter import Tk, Label, Button, messagebox
import os
import re
import pip

def install(package):
	if hasattr(pip, 'main'):
		pip.main(['install', package])
	else:
		pip._internal.main(['install', package])

try:
	import extract_msg
except:
    try:
        install('extract-msg')
        import extract_msg
    except:
        raise Exception("Nous n'avons pas pu installer extract-msg. S'il vous plait l'installer manuellement.")

class ErreurMail:
	def __init__(self, master):
		self.master = master
		master.title("ErreurMail")

		self.title = Label(master, text="Bienvenue dans ErreurMail")		
		self.title.pack()
		
		self.label = Label(master, text="Mettre les fichiers .msg à lire dans le même dossier que l'exécutable")
		self.label.pack()

		self.label2 = Label(master, text="Appuyer sur le bouton pour lire les fichiers")
		self.label2.pack()
		
		self.greet_button = Button(master, text="Obtenir les adresses", command=self.parse)
		self.greet_button.pack()

	def parse(self):		
		fichiers = os.listdir('.')
		
		bad_addresses = []
		
		for fichier in fichiers:
			
			if '.msg' in fichier:
				msg = extract_msg.Message(fichier)
				msg_message = str(msg.body)
				msg_subj = str(msg.subject)
				
				if 'Delivery Failure' in msg_subj:
					address = re.findall('Failed+\s+Recipient+:+.+', msg_message)[0]
					address = address.replace('Failed Recipient: ', '')
					print(1)

					if '<' in address:
						address = address.replace('<', '')
				
				elif 'Non remis' in msg_subj:
					address = re.findall('\(+[A-z0-9]+\@+.+\)', msg_message)[0]
					address = address.replace('(', '').replace(')', '')
					print(2)

				elif 'This Message was undeliverable due to the following reason' in msg_message:
					address = re.findall('Invalid+\s+recipient+:+.+\@+.+', msg_message)[0]
					address = address.strip('Invalid recipient: <').strip('>')
					print(3)

				elif 'email account that you tried' in msg_message and "wasn't delivered" in msg_message:
					address = re.findall('t+\s+delivered+\s+to+\s+.+\@+.+', msg_message)[0]
					address = address.strip('t delivered to ')
					address = address.split('because')[0]
					print(4)

				elif re.findall('for+\s+\<+.+\@+.+', msg_message) and "We're writing to let you know that the group" in msg_message:
					address = re.findall('for+\s+\<+.+\@+.+', msg_message)[0]
					address = address.split('>')[0]
					address = address.strip('for <')
					print(5)

				elif re.findall('\<+.+\@+.+\>', msg_message) and 'The following addresses had permanent fatal errors' in msg_message:
					address = re.findall('\<+.+\@+.+\>', msg_message)[0]
					address = address.strip('<').strip('>')
					print(6)
				
				else:
					print("Le fichier nommé " + str(fichier) + " a été sauté puisque le programme n'a pas pu trouver d'adresse courriel erronée.")
					continue
				
				address = address.replace('"', '').replace(' ', '')
				address = address.replace('\n', '').replace('\r', '')

				bad_addresses.append(address)
			else:
				continue
		
		with open('Adresses_erronees.txt', 'w') as file:
			to_write = ""
			for address in bad_addresses:
					to_write += address
					if '\n' not in address and '\r' not in address:
						to_write += '\n'
			file.write(to_write)
		messagebox.showinfo(title="Terminé", message="Tous les fichiers ont été parcourus. Un fichier nommé 'Adresses erronées' a été créé dans le dossier où se trouve le programme.")


if __name__ == '__main__':
	root = Tk()
	erreurMail = ErreurMail(root)
	root.geometry("500x200")
	root.mainloop()
