import unittest
import math as m
from Vecteur import Vecteur as vect

class TestClassVecteur(unittest.TestCase):
	def test_vect_is_vect(self):
		v = vect(4,4)
		self.assertIsInstance(v, vect)
	
	def test_calcNorm_is_good(self):
		v  = vect(4,4)
		v1 = vect(15, -1)
		v2 = vect(-5, 90)
		v3 = vect(0,0)
		v4 = vect(5.68, 7.687)
		
		self.assertAlmostEqual(v.calcNorm(), 4*m.sqrt(2))
		self.assertAlmostEqual(v1.calcNorm(), m.sqrt(226))
		self.assertAlmostEqual(v2.calcNorm(), 25*m.sqrt(13))
		self.assertAlmostEqual(v3.calcNorm(), 0)
		self.assertAlmostEqual(v4.calcNorm(), 9.55784332367925)

	def test_produitScalaire(self):
		v  = vect(4,4)
		v1 = vect(15, -1)
		v2 = vect(-5, 90)
		v3 = vect(0,0)
		v4 = vect(5.68, 7.687)
		v6 = vect(-15.6, 4.81)

		self.assertEqual(v.produitScalaire(v1), 56)
		self.assertEqual(v2.produitScalaire(v3), 0)
		self.assertAlmostEqual(v4.produitScalaire(v6), -51.6335299999)
	
	def test_calculerAngle(self):
		v  = vect(4,4)
		v1 = vect(15, -1)
		v2 = vect(-5, 90)
		v3 = vect(0,0)
		v4 = vect(5.68, 7.687)
		v6 = vect(-15.6, 4.81)

		self.assertEqual(v.calculerAngle(v1), 48)
		self.assertEqual(v.calculerAngle(v), 0.0)
		#self.assertEqual(v2.calculerAngle(v3), 90.0)
		self.assertEqual(v4.calculerAngle(v6), 109)

	def test_rotationAngle(self):
		v  = vect(10,0)
		v1 = vect(15, -1)
		v2 = vect(-5, 90)
		v3 = vect(0,0)
		v4 = vect(5.68, 7.687)
		v6 = vect(-15.6, 4.81)
		v.rotationAngle(-90)
		print((v.x,v.y))






if __name__ == '__main__':
	unittest.main()