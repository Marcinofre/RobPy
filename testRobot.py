from Robot import Robot as r
from Vecteur import Vecteur as vec
import random as rand
import unittest

class Robot(unittest.TestCase) :
	
	def test_avancerRobot(self):
		robot = r(0,0,0,0)
		robot.vectD = vec(0.1, 0)
		
		
		robot.scalVitesse = 2.0
		for time in range(10):
			robot.avancerRobot()

		self.assertEqual(robot.posCenter, (round(2.0*0.1*10, 2), 0.0))
		
		robot.scalVitesse = 0
		robot.posCenter = (0.0,0.0)
		for time in range(10):
			robot.avancerRobot()
		self.assertEqual(robot.posCenter, (0.0, 0.0))

		robot.scalVitesse = 15
		robot.posCenter = (0.0,0.0)
		robot.vectD = vec(0.1, -4)
		for time in range(5):
			robot.avancerRobot()
		self.assertEqual(robot.posCenter, (7.5, -300.0))

	def test_reculerRobot(self):
		robot = r(0,0,0,0)
		
		startx = rand.randint(0,160)
		starty = rand.randint(0,160)
		robot.posCenter = (startx,starty)
		robot.scalVitesse = rand.randint(0,10)
		robot.vectD = vec(rand.random(),rand.random())
		it = rand.randint(0,142)
		for count in range(it):
			robot.reculerRobot()
		for count in range(it):
			robot.avancerRobot()
		
		self.assertEqual(robot.posCenter, (startx,starty))
	
	def test_tournerRobot(self):
		
		robot = r(0,0,0,0)
		
		robot.vectD = vec(0,0)
		robot.tournerRobot(15)
		x = robot.vectD.x
		y = robot.vectD.y
		self.assertEqual((x,y), (0,0))

		robot.vectD = vec(1,1)
		robot.tournerRobot(180)
		x = robot.vectD.x
		y = robot.vectD.y
		self.assertEqual((x,y), (-1,-1))

		robot.vectD = vec(0.1,0.1)
		robot.tournerRobot(90)
		x = robot.vectD.x
		y = robot.vectD.y
		self.assertEqual((x,y), (-0.1,0.1))

		robot.vectD = vec(0.1,0.1)
		robot.tournerRobot(-90)
		x = robot.vectD.x
		y = robot.vectD.y
		self.assertEqual((x,y), (0.1,-0.1))

	def test_readInstruction(self):
		robot = r(0,0,0,0)

		#Doit pouvoir lever une exeption si le fichier est introuvable ou inexistant
		with self.assertRaises(Exception):
			genText = robot.readInstruction("fichier qui n'existe pas")
			next(genText)
		

		#Doit rendre un string
		genText = robot.readInstruction("CompteRendu/cr1.md")
		self.assertIsInstance(next(genText), str)

	def test_parsingInstruction(self):
		robot = r(0,0,0,0)

		with self.assertRaises(ValueError):
			robot.parsingInstruction("instruction: sans nombre")
			robot.parsingInstruction("malformaté: d 5 v 2")
			robot.parsingInstruction("reculer: ")
			robot.parsingInstruction("AvANcer:5 2")

		
		self.assertTupleEqual(robot.parsingInstruction("AvANcer:d5 v2"), ("avancer", {"duree":5, "vitesse":2}))
		self.assertTupleEqual(robot.parsingInstruction("RECULER:g5 l2"), ("reculer", {}))

	def test_executeInstruction(self):
		robot = r(0,0,0,0)

		with self.assertRaises():




	
		



		


if __name__ == "__main__":
	unittest.main() 