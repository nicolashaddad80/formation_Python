class Navire:

   def __init__(self, nom, couleur, puis_tir, resistance, kilometrage=0, pdv=100):
      self.nom = nom
      self.couleur = couleur
      self.puis_tir = puis_tir
      self.resistance = resistance
      self.kilometrage = kilometrage
      self.pdv = pdv

   def is_en_vie(self):
      return self.pdv > 0


   def afficher_infos(self):
      return f"[ {self.nom.upper()} ]\n" \
         f"{self.couleur} – {self.kilometrage} NM \n" \
         f"Puissance de tir : {self.puis_tir} \n" \
         f"Résistance : {self.resistance} \n" \
         f"Points de vie : {self.pdv}/100 \n" \
         f"Etat : {'En vie' if self.is_en_vie() else 'Détruit'} \n" \
         f"------------------------- \n"


   def naviguer(self, distance):
      self.kilometrage += distance
      print(f"{self.nom} navigue, {distance} NM parcourus, km actuel : {self.kilometrage} NM")


   def subir_degats(self, degats):
      self.pdv = max([0, self.pdv - degats])
      print(f"{self.nom} subit {degats} dégâts, pts de vie : {self.pdv}")
      

if __name__ == '__main__':

   nav1 = Navire("Le titan", "Gris", 80.0, 75.0)
   nav2 = Navire("Le terrible", "Noir", 75.0, 75.0)
   nav3 = Navire("Le terrifiant", "Blanc", 70.0, 75.0)

   print(nav1.afficher_infos())

   nav2.naviguer(4000)
   nav2.naviguer(4000)

   nav3.subir_degats(40)
   nav3.subir_degats(80)