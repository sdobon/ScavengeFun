# ScavengerFun

An MMS picture based scavenger hunt using Twilio automated sms and ClarifAI image recognition. Forked from a project created at wildhacks2016 by myself, Theodore Bisdikian, Will Lundgren, and Elana Stettin.

-----------------------------------------------------------------------------------------------------

CHANGELOG:

Modularized and cleaned up code for easier updates, Added multiple game functionality - 12/22/2016

Initial commit after wildhacks2016 - 12/19/2016

------------------------------------------------------------------------------------------------------

INSTRUCTIONS:


Run flask.py on a remote host or a local host tunneled to a remote host.

To play, a host first texts the following to the host number (224)265-4689

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
