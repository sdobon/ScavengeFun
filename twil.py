from flask import Flask, request, redirect
import twilio.twiml
import ScavengerHunt
from predict import get_tags

app = Flask(__name__)

setup = True
game = None

@app.route("/", methods = ['GET', 'POST'])
def game1():
	global setup
	global game
	test = True
	from_number = request.values.get('From', None)
	msg_body = request.values.get('Body', None).split('\n')
	response = ""
	if setup:
		if game and from_number == game.host_num:
			test = False
			if str(msg_body[0]) == "Start":
				setup = False
				response = "The game has started"
			if str(msg_body[0]) == "Status":
				response = "The players in this game are: \n"
				for num in game.players:
					response += game.players[num].name + "\n"

		if msg_body[0] == "Create":
			game = ScavengerHunt.ScavengerHunt(from_number, msg_body[1], msg_body[2:])
			response = "Game Created!\nYour code is " + game.code + "\nEnter 'Status' to view the players or 'Start' to begin the game"

		elif msg_body[0] == 'Join':
			if msg_body[2] == game.code:
				game.addPlayer(from_number, msg_body[1])
				response = "You have been added.\nThe items you are looking for are:\n"
				for item in game.returnItems():
					response += item + "\n"

			else:
				response = "Invalid code. Please enter a valid code."

		elif test:
			response = "Invalid format. blah blah"

	else:
		if from_number in game.players:
			media_url = request.values.get('MediaUrl0', None)
			if media_url != None:
				print "check2"
				tags = get_tags(media_url)
				found = False
				for key in game.keywords:
					for tag in tags:
						if found == False:
							if str(tag) == key.lower() and key not in game.players[from_number].found:
								response = "Congradulations! You found the " + key
								game.players[from_number].found.append(key)
								found = True
							elif key in game.players[from_number].found:
								response = "You already found the " + key
				if found == False:
					response = "Your picture didn't match any of the objects"

			elif msg_body[0] == "Status":
				response = "You found: \n"
				for item in game.players[from_number].found:
					response += item + "\n"
				response += "\nYou still need to find: \n"
				for item in game.keywords:
					if item not in game.players[from_number].found:
						response += item + "\n"

			else:
				response = "Invalid command. Please submit a picture or 'Status'"

		else:
			response = "Number not found in game"

	print "TO: " + str(from_number) + "\n" + response
	resp = twilio.twiml.Response()
	resp.message(response)
	return str(resp)



if __name__ == "__main__":
	app.run(debug=True)