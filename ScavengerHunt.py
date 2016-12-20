import string
import random

class ScavengerHunt:
	def __init__(self, host_num, host_name, keywords):
		self.host_num = host_num
		self.host_name = host_name
		self.players = {}
		self.keywords = []
		for word in keywords:
			self.keywords.append(word.strip())
		self.code = createCode()

	def addPlayer(self, player_num, player_name):
		self.players[player_num] = Player(player_num, player_name)

	def returnItems(self):
		r = []
		for item in self.keywords:
			r.append(item)
		return r


class Player:
	def __init__(self, num, name):
		self.num = num
		self.name = name
		self.found = []


def createCode():
	str = ""
	for i in range(5):
		str += random.choice(string.ascii_lowercase)
	return str