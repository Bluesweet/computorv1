import re
import sys
import main

equation = ''

if len(sys.argv) == 1:
	print "\033[1;30m(Tapez 'exit' pour quitter le programme.)"
	while 1:
		main.rawinput(equation)
elif len(sys.argv) != 2:
	print "\033[1;31mUsage: python computor.py to launch in standalone or python computor.py <equation> to directly do the shit\a"
	exit()
else:
	equation = sys.argv[1]
	main.rawinput(equation)
