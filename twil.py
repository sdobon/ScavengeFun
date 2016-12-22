from flask import Flask, request, redirect
import twilio.twiml
import ScavengerHunt
from predictImage import get_tags

app = Flask(__name__)


games = []

@app.route("/", methods = ['GET', 'POST'])
def allocateInput():
	from_number = request.values.get('From', None)
	msg_body = request.values.get('Body', None).split('\n')
	response = ""

	for hunt in games:
		if from_number in hunt.players or from_number == hunt.host_num:
			return handleInput(hunt, from_number, msg_body)
	else:
		return handleUnknownNumber(from_number, msg_body)

def handleUnknownNumber(from_number, msg_body):
	if msg_body[0].strip().lower() == "create":
		print "pass1"
		hunt = ScavengerHunt.ScavengerHunt(from_number, msg_body[1], msg_body[2:])
		response = "Game Created!\nYour code is " + hunt.code + "\nEnter 'Status' to view the players or 'Start' to begin the game"
		games.append(hunt)

	elif msg_body[0].strip().lower() == 'join':
		#if no code match
		response = "No matching game found for that join code."
		for hunt in games:
			if msg_body[2].strip().lower() == hunt.code:
				hunt.addPlayer(from_number, msg_body[1])
				response = "You have been added.\nThe items you are looking for are:\n"
				for item in hunt.returnItems():
					response += item + "\n"

	else:
		response = "Improper format to create or join a game."

	# ------ Twilio response block. Takes the variable "response" and sends it back at the from_number -------

	print "TO: " + str(from_number) + "\n" + response
	resp = twilio.twiml.Response()
	resp.message(response)
	return str(resp)

	#---------------------------------------------------------------------------------------------------------


def handleInput(hunt, from_number, msg_body):
	if hunt.setup:
		response = "Game hasn't started yet."
		if from_number == hunt.host_num:
			if str(msg_body[0]) == "Start":
				hunt.setup = False
				response = "The game has started"
			if str(msg_body[0]) == "Status":
				response = "The players in this game are: \n"
				for num in hunt.players:
					response += hunt.players[num].name + "\n"
	else:
		if from_number in hunt.players:
			media_url = request.values.get('MediaUrl0', None)
			if media_url != None:
				tags = get_tags(media_url)
				found = False
				print tags
				for key in hunt.keywords:
					for tag in tags:
						if found == False:
							if str(tag) == key.lower() and key not in hunt.players[from_number].found:
								response = "Congradulations! You found the " + key
								hunt.players[from_number].found.append(key)
								found = True
							elif key in hunt.players[from_number].found:
								response = "You already found the " + key
				if found == False:
					response = "Your picture didn't match any of the objects"

			elif msg_body[0] == "Status":
				response = "You found: \n"
				for item in hunt.players[from_number].found:
					response += item + "\n"
				response += "\nYou still need to find: \n"
				for item in hunt.keywords:
					if item not in hunt.players[from_number].found:
						response += item + "\n"

			else:
				response = "Invalid command. Please submit a picture or 'Status'"

		else:
			response = "Number not found in game"

	# ------ Twilio response block. Takes the variable "response" and sends it back at the from_number -------

	print "TO: " + str(from_number) + "\n" + response
	resp = twilio.twiml.Response()
	resp.message(response)
	return str(resp)

	#---------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
#
# setup = True
# game = None
#
#
# @app.route("/", methods = ['GET', 'POST'])
# def game1():
# 	global setup
# 	global game
# 	test = True
# 	from_number = request.values.get('From', None)
# 	msg_body = request.values.get('Body', None).split('\n')
# 	response = ""
# 	if setup:
# 		if game and from_number == game.host_num:
# 			test = False
# 			if str(msg_body[0]) == "Start":
# 				setup = False
# 				response = "The game has started"
# 			if str(msg_body[0]) == "Status":
# 				response = "The players in this game are: \n"
# 				for num in game.players:
# 					response += game.players[num].name + "\n"
#
# 		if msg_body[0] == "Create":
# 			game = ScavengerHunt.ScavengerHunt(from_number, msg_body[1], msg_body[2:])
# 			response = "Game Created!\nYour code is " + game.code + "\nEnter 'Status' to view the players or 'Start' to begin the game"
#
# 		elif msg_body[0] == 'Join':
# 			if msg_body[2] == game.code:
# 				game.addPlayer(from_number, msg_body[1])
# 				response = "You have been added.\nThe items you are looking for are:\n"
# 				for item in game.returnItems():
# 					response += item + "\n"
#
# 			else:
# 				response = "Invalid code. Please enter a valid code."
#
# 		elif test:
# 			response = "Invalid format. blah blah"
#
# 	else:
# 		if from_number in game.players:
# 			media_url = request.values.get('MediaUrl0', None)
# 			if media_url != None:
# 				print "check2"
# 				tags = get_tags(media_url)
# 				found = False
# 				for key in game.keywords:
# 					for tag in tags:
# 						if found == False:
# 							if str(tag) == key.lower() and key not in game.players[from_number].found:
# 								response = "Congradulations! You found the " + key
# 								game.players[from_number].found.append(key)
# 								found = True
# 							elif key in game.players[from_number].found:
# 								response = "You already found the " + key
# 				if found == False:
# 					response = "Your picture didn't match any of the objects"
#
# 			elif msg_body[0] == "Status":
# 				response = "You found: \n"
# 				for item in game.players[from_number].found:
# 					response += item + "\n"
# 				response += "\nYou still need to find: \n"
# 				for item in game.keywords:
# 					if item not in game.players[from_number].found:
# 						response += item + "\n"
#
# 			else:
# 				response = "Invalid command. Please submit a picture or 'Status'"
#
# 		else:
# 			response = "Number not found in game"
#
# 	# ------ Twilio response block. Takes the variable "response" and sends it back at the from_number -------
#
# 	print "TO: " + str(from_number) + "\n" + response
# 	resp = twilio.twiml.Response()
# 	resp.message(response)
# 	return str(resp)
#
# 	#---------------------------------------------------------------------------------------------------------
#


if __name__ == "__main__":
	app.run(debug=True)
