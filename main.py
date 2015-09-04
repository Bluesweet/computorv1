import re
import sys

def isFloat(string):
	try:
		float(string)
		return True
	except ValueError:
		return False

def rawinput(equation):
	if equation == '':
		equation = raw_input("\033[1;37mEntrez une equation polynomiale de degre inferieur ou egal a deux : ").lower()
	if equation == 'exit':
		print "\033[1;31mExit.\a"
		exit()
	def parse(text):
		chunks = ['']
		f = '1'
		tab = '0'
		count = 0
		i = 0
		r = 0
		t = 0
		m = 0
		d = 0
		for character in text:
			if character.isdigit():
				d = unicode(chunks[-1])
				if chunks[-1].isdigit():
					chunks[-1] += character
				elif d.isnumeric():
					chunks[-1] += character
				elif chunks[-1] in '^' and r != 0:
					if int(character) >= 3:
						return tab
					else:
						r += 1
						chunks.append(character)
				elif m is None and t != 0:
					m = 0
					chunks[-1] += character
				elif isFloat(chunks[-1]) is True:
					chunks[-1] += character
				else:
					chunks.append(character)
					t += 1
			elif character in '+/*^':
				i += 1
				if character in '^':
					i -= 1
				if chunks[-1] in '+/*^=':
					return f
				chunks.append(character)
			elif character in '-':
				chunks.append(character)
			elif character in '=':
				i += 1
				if chunks[-1] in '+-/*^':
					return f
				chunks.append(character)
				count += 1
			elif character in ',.':
				m = re.search('\d+\.\d+', chunks[-1])
				if m is None:
					chunks[-1] += '.'
				else:
					return f
			elif character.isalpha():
				if chunks[-1].isalpha() or chunks[-1].isdigit():
					return f
				else:
					chunks.append(character)
			if count >= 2:
				return f
		if i == 0:
			return f
		if chunks[-1] in '=+*/-^':
			return f
		return chunks[1:]

	def search_equal(tab):
		i = 0
		pos = 0
		for element in tab:
			if element == '=':
				pos = i
			i += 1
		return pos

	def check_deg(tab):
		poly = []
		i = 0
		pos = search_equal(tab)
		while i < len(tab[:pos + 1]):
			if tab[i - 1] == '^':
				poly.append(tab[i])
			i += 1
		return poly   

	def add_rest(tab1, tab2, tabp):
		i = 0
		j = 0
		pos = search_equal(tab2)
		while j < len(tabp):
			i = 0
			while i < len(tab2[:pos + 1]):
				if tab2[i] == tabp[j] and tab2[i - 1] == '^':
					tab1.extend(tab2[i - 5:i + 1])
				i +=1
			j += 1
		return tab1

	def reduc_equal(tab):
		new_tab = [' ']
		poly = check_deg(tab)
		val = 0
		i = 0
		s = 1
		find = False
		pos = search_equal(tab)
		limit = pos
		while len(tab[pos + 1:]) > 0:
			signe = '+'
			val = tab[pos + 1]
			if val == '+' or val == '-':
				signe = val
				pos += 1
				val = tab[pos + 1]
			deg = tab[pos + 5]
			while i < limit:
				if tab[i] == deg and tab[i - 1] == '^':
					find = True
					poly.remove(deg)
					break
				i += 1
			if find == True:
				if (i - 5) >= 0:
					if tab[i - 5] == '-':
						s = -1;
					else:
						s = 1;
				if signe == '+':
					res = ((float(tab[i - 4]) * s) - float(val))
					if res != 0:
						if res < 0:
							new_tab.append('-')
							new_tab.append(str(res * -1))
						else:
							if new_tab[-1].isdigit():
								new_tab.append('+')
							new_tab.append(str(res))
						new_tab.extend(tab[i - 3:i + 1])
				else:
					res = ((float(tab[i - 4]) * s) + float(val))
					if res != 0:
						if res < 0:
							new_tab.append('-')
							new_tab.append(str(res * -1))
						else:
							if new_tab[-1].isdigit():
								new_tab.append('+')
							new_tab.append(str(res))
						new_tab.extend(tab[i - 3:i + 1])
				pos = search_equal(tab)
				if tab[pos + 1].isdigit():
					del(tab[pos + 1:pos + 6])
				else:
					del(tab[pos + 1:pos + 7])
			else:
				pos = search_equal(tab)
				if tab[pos + 2] != '0':
					if tab[pos + 1] == '+':
						new_tab.append('-')
					else:
						new_tab.append('+')
					new_tab.extend(tab[pos + 2:pos + 7])
				del(tab[pos + 1:pos + 7])
			i = 0    
			find = False
		if len(poly) > 0:
			new_tab = add_rest(new_tab, tab, poly)
		new_tab.extend(['=', '0'])
		return new_tab[1:]

	def max_degree(tab):
		poly = check_deg(tab)
		return max(poly)

	def solution(a, b, c):
		delta = b**2-4*a*c
		if delta < 0:
			print "\033[1;34mL'equation n'admet pas de solution dans R mais deux solutions complexes."
			print "\033[1;36mx1 : %s + i * %s" % ((-b/2*a), (((-delta) ** 0.5) / (2*a)))
			print "\033[1;36mx2 : %s - i * %s" % ((-b/2*a), (((-delta) ** 0.5) / (2*a)))
		elif delta == 0:
			print "\033[1;34mL'equation admet une solution x1 : \033[1;36m%s" % (-b/(2*a))
		else:
			print "\033[1;34mL'equation admet deux solutions." 
			print "\033[1;36mx1 : %s" % ((-b-(-delta ** 0.5))/(2*a))
			print "\033[1;36mx2 : %s" % ((-b+(-delta ** 0.5))/(2*a))

	def resolv_1(tab):
		i = 0
		a = 0
		b = 0
		while i < len(tab):
			if tab[i] == '0' and tab[i - 1] == '^':
				b = float(tab[i - 4])
				if (i - 5) >= 0 and tab[i - 5] == '-':
					b *= -1
			if tab[i] == '1' and tab[i - 1] == '^':
				a = float(tab[i - 4])
				if (i - 5) >= 0 and tab[i - 5] == '-':
					a *= -1
			i += 1
		if a != 0:
			print "\033[1;34mLa solution est : \033[1;36m%s" % (-b/a)
		else:
			if b == 0:
				print "\033[1;34mL'equation est indeterminee."
			else:
				print "\033[1;34mL'equation est impossible."

	def resolv_2(tab):
		i = 0
		a = 0
		b = 0
		c = 0
		while i < len(tab):
			if tab[i] == '0' and tab[i - 1] == '^':
				c = float(tab[i - 4])
				if (i - 5) >= 0 and tab[i - 5] == '-':
					c *= -1
			if tab[i] == '1' and tab[i - 1] == '^':
				b = float(tab[i - 4])
				if (i - 5) >= 0 and tab[i - 5] == '-':
					b *= -1
			if tab[i] == '2' and tab[i - 1] == '^':
				a = float(tab[i - 4])
				if (i - 5) >= 0 and tab[i - 5] == '-':
					a *= -1
			i += 1
		solution(a, b, c)

	tab_equ = parse(equation)
	if tab_equ == '1':
		print "\033[1;31mErreur de syntaxe.\a"
	elif tab_equ == '0':
		print "\033[1;31mLe degre de l'equation est superieur ou egal a 3, je ne peux la resoudre."
	else:
		tab_equ = reduc_equal(tab_equ)
		if	len(tab_equ) == 2:
			print "\033[1;34mIl existe un nombre infini de solutions."
		else:
			print "\033[1;34mForme reduite : %s" % " ".join(tab_equ)
			deg = max_degree(tab_equ)
			print "\033[1;34mLe degree du polynome : %s" % deg
			if int(deg) > 2:
				print "\033[1;34mLe degree de l'equation est superieur a 2, je ne peux pas la resoudre."
			elif deg == '2':
				resolv_2(tab_equ)
			elif deg == '1':
				resolv_1(tab_equ)
			else:
				print "\033[1;34mIl n'existe pas de solution."
