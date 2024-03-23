import unittest
import math as m
from utils.vecteur import Vecteur as vect

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

	def test_produitVectoriel(self):
		v  = vect(4,4)
		v1 = vect(15, -1)
		v2 = vect(-5, 90)
		v3 = vect(0,0)
		self.assertEqual(v.produitVectoriel(v1), -64)
		self.assertEqual(v2.produitVectoriel(v3), 0)

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
		v = vect(1,0)
		v1 = vect(0,1)
		v2 = vect(1,1)
		v3 = vect(0,-1)
		v4 = vect(-1,0)
		v5 = vect(0,0)
		v6 = vect(-1,-1)


		self.assertEqual(v.calculerAngle(v), 0)
		self.assertEqual(v.calculerAngle(v1), 90)
		self.assertEqual(v.calculerAngle(v2), 45)
		self.assertEqual(v.calculerAngle(v3), 90)
		self.assertEqual(v.calculerAngle(v4), 180)
		self.assertEqual(v.calculerAngle(v5), 90)
		self.assertEqual(v.calculerAngle(v6), 135)
		self.assertEqual(v2.calculerAngle(v6), 180)


	def test_rotationAngle(self):
		
		v1 = vect(0,1)
		v3 = vect(0,-1)
		v4 = vect(-1,0)
		
		v = vect(1,0)
		v.rotationAngle(90)
		self.assertEqual((v.x, v.y), (v1.x, v1.y))
		
		v = vect(1,0)
		v.rotationAngle(180)
		self.assertEqual((v.x, v.y), (v4.x, v4.y))

		v = vect(1,0)
		v.rotationAngle(45)
		self.assertEqual((v.x, v.y), (0.7, 0.7))

		v = vect(1,0)
		v.rotationAngle(-90)
		self.assertEqual((v.x, v.y), (v3.x, v3.y))

		







if __name__ == '__main__':
	unittest.main()