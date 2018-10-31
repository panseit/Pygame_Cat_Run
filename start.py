#Edw ginetai import to menu, apo ekei 9a kalestoun diadoxika to level_selection kai meta to ka9e level.
from menu_libs import menu
from libs import data
import os

def main():
	#fortwnontai ola ta kyriws data tou paixnidiou (aparaithtes arxikopoihseis, eikonidia klp)
	data.load_major_data()
	#fortwma twn ry9misewn
	data.load_settings()
	#fortwma twn stoixeiwn (eikonwn/hxwn klp) tou menu
	data.load_menu_data()
	#emfanish tou menu
	menu.show()
	
if __name__ == '__main__':
	main()
