import random


class Coque:
	"""
	Correspond à la coque d'un navire
	"""

	def __init__(self, matiere, couleur, resistance, pdv=100):
		"""
		Le constructeur
		:param matiere: La matière de la coque
		:param couleur: La couleur de la coque
		:param resistance: La résistance aux tirs, entre 0 et 100
		:param pdv: Les points de vie, entre 0 et 100
		"""
		self.matiere = matiere
		self.couleur = couleur
		self.resistance = resistance
		self.pdv = pdv

	def is_en_vie(self):
		return self.pdv > 0

	def __str__(self):
		return f"{self.matiere} - {self.couleur} \nRésistance : {self.resistance} \nPts de vie : {self.pdv} \n"

	def __repr__(self):
		return str(self.__dict__)

	def subir_degats(self, degats):
		self.pdv = max([0, self.pdv - degats])


class Arme:

	def __init__(self, nom, puis_tir, prix):
		self.nom = nom
		self.puis_tir = puis_tir
		self.prix = prix

	def __str__(self):
		return f"{self.nom} - Puissance : {self.puis_tir} \n"

	def __repr__(self):
		return str(self.__dict__)


class Navire:

	def __init__(self, nom, coque, kilometrage=0):
		if type(self) == Navire:
			raise Exception("Impossible d'instancier la classe Navire")
		self._nom = nom
		self.kilometrage = kilometrage
		self.coque = coque

	nom = property(lambda self: self._nom)

	def is_en_vie(self):
		return self.coque.is_en_vie()

	def __str__(self):
		return f"[ {self._nom.upper()} ]\n" \
			f"{self.kilometrage} NM \n" \
			f"Coque : {self.coque}" \
			f"Etat : {'En vie' if self.is_en_vie() else 'Détruit'} \n"

	def __repr__(self):
		return str(self.__dict__)

	def naviguer(self, distance):
		self.kilometrage += distance
		print(f"{self._nom} navigue, {distance} NM parcourus, km actuel : {self.kilometrage} NM")


class NavireDeGuerre(Navire):

	def __init__(self, nom, coque, arme, kilometrage=0, **kwargs):
		Navire.__init__(self, nom, coque, kilometrage)
		self.arme = arme
		self.__dict__.update(kwargs)

	def __str__(self):
		return Navire.__str__(self) + f"Arme : {self.arme} \n"

	def __gt__(self, other):
		if type(other) != NavireDeGuerre:
			raise TypeError
		return self.coque.pdv > other.coque.pdv

	def tirer_sur(self, ennemi):
		if self != ennemi:
			rdm1 = random.random()
			rdm2 = random.random()
			rdm3 = random.random()

			degats = round((((0.5 + rdm1) * self.arme.puis_tir) - (rdm2 * ennemi.coque.resistance)) * rdm3)

			if degats > 0:
				print(f"{self._nom} tire sur {ennemi.nom}")
				ennemi.coque.subir_degats(degats)
				print(f"{ennemi.nom} subit {degats} dégâts, pts de vie : {ennemi.coque.pdv}")
			else:
				print(f"Le tir de {self._nom} a échoué")
		else:
			print("Impossible de tirer sur soi-même")

	@classmethod
	def classer(cls, *navires):
		# Cast en list pour pouvoir faire un sort()
		liste_navires = list(navires)

		# Le sort() appelle __gt__()
		liste_navires.sort(reverse=True)

		# dict en compréhension : on récupère le nom et les pdv de chaque navire, on récupère les items du dict
		# enumerate() pour faire apapraitre le classement
		return list(enumerate({nav._nom: nav.coque.pdv for nav in liste_navires}.items(), start=1))


class NavireCivil(Navire):

	def __init__(self, nom, coque, capacite, nb_passagers, kilometrage=0, destinations=None):
		Navire.__init__(self, nom, coque, kilometrage)
		self.capacite = capacite
		self._set_nb_passagers(nb_passagers)
		if destinations is None:
			self.destinations = []

	def _set_nb_passagers(self, nb_passagers):
		self._nb_passagers = nb_passagers
		if nb_passagers < 0:
			self._nb_passagers = 0
		if nb_passagers > self.capacite:
			self._nb_passagers = self.capacite

	nb_passagers = property(lambda self: self._nb_passagers, _set_nb_passagers)

	def __str__(self):
		return Navire.__str__(self) + f"Nb. passagers : {self._nb_passagers} / {self.capacite}"

	def debarquer(self, nb_a_debarquer):
		self._set_nb_passagers(self._nb_passagers - nb_a_debarquer)
		print(f"Nombre de passagers actuels : {self.nb_passagers}")

	def embarquer(self, nb_a_embarquer):
		self._set_nb_passagers(self._nb_passagers + nb_a_embarquer)
		print(f"Nombre de passagers actuels : {self.nb_passagers}")


class Hopital:

	def __init__(self, nom, note):
		self._nom = nom
		self.note = note

	nom = property(lambda self: self._nom)

	def soigner(self, pts):
		return pts + (50 * self.note)


class NavireMedical(Navire, Hopital):

	def __init__(self, nom, coque, note, kilometrage=0):
		Navire.__init__(self, nom, coque, kilometrage)
		Hopital.__init__(self, nom, note)

	def soigner(self, navire_a_soigner):
		navire_a_soigner.coque.pdv = min(100, Hopital.soigner(self, navire_a_soigner.coque.pdv))
		print(f"{self._nom} soigne {navire_a_soigner.nom}")


if __name__ == '__main__':

	nav1 = NavireDeGuerre("Le titan", Coque("Métal", "Gris", 75.0), Arme("Canon", 80.0, 100000))
	nav2 = NavireDeGuerre("Le terrible", Coque("Métal", "Noir", 75.0), Arme("Canon", 75.0, 100000))
	nav3 = NavireDeGuerre(
		"Le terrifiant",
		Coque("Métal", "Blanc", 70.0),
		Arme("Canon", 80.0, 100000),
		fabriquant="NavalGroup",
		annee=2021
	)

	nav_civ = NavireCivil("Le pacifique", Coque("Métal", "Gris", 75.0), 3000, 1500)
	nav_civ.nb_passagers = 2000

	print(nav1)
	print(nav2)
	print(nav3)
	print(nav_civ)

	nav2.naviguer(4000)
	nav2.naviguer(4000)

	nav1.tirer_sur(nav3)
	nav2.tirer_sur(nav3)
	nav1.tirer_sur(nav2)
	nav3.tirer_sur(nav1)

	for x in NavireDeGuerre.classer(nav1, nav2, nav3):
		print(x)
