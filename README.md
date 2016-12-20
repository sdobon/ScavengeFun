# ScavengeFun

DOCUMENTATION: A twilio/clarifai based scavenger hunt
Created by Theodore Bisdikian, Sebastian Dobon, Will Lundgren, Elana Stettin

run twil.py on a remote host or a local host tunneled to a remote host.

Our project is a sms/mms based scavenger hunt. To play, a host first tests the following to the host number (224)265-4689
Create
Your name
A list of objects to be found, separated by line breaks

A 5 letter code will be sent back to the host. This will be used by other players to join using the following format:
Join
Your name
code

Then the host may insert "Status" to view the current players' names, or "Start" to begin the scavenger hunt.
Once the game has started, all users can text in pictures of items to the number. The system will test the picture using clarifai 
in order to see whether the picture matches any of the object descriptions.

Users may also type "Status" to see what objects they've found and what objects they have yet to find.
