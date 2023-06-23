"""
	Description : Lister tous les articles Wikipédia de CIV qui manquent de sources secondaires
	Auteurs : Samuel Guebo & Paul Bouaffou
	Contributeur : Oskhane Boya
	Licence :
"""


import json
import requests


def log_text(filename, text):
	""" Utility for writing in a text file """
	with open(filename, "a", encoding="utf-8") as f:
		f.write(text + "\n")


def print_notice(notice):
	"""Print notice message in yellow """
	print('\033[93m' + notice + '\033[0m')


def run_media_wiki_request(url):
	""" function to give result of url request """
	result_json = requests.get(url).content
	# return the json text
	return result_json
	

def app():
	""" Main entry point for the tool. It gets all articles from CIV archives """
	civ_archives_url = "https://fr.wikipedia.org/w/api.php?action=parse&format=json&page=Projet:C%C3%B4te_d%27Ivoire/Articles_r%C3%A9cents/Archive&prop=links" 

	# convert from plain text to python array, and browse to get items 'parse' and its child 'links' && just the two first items of the array
	links_test = json.loads(run_media_wiki_request(civ_archives_url))['parse']['links'][0:500]

	# initiate counter
	articles_count = 0
	# loop through the small set
	for link in links_test:
		page_title = link['*']
		# build the url 
		page_templates_url = f"https://fr.wikipedia.org/w/api.php?action=parse&format=json&page={page_title}&prop=templates"
		# run a Http request and get the template of each pages
		page_templates = json.loads(run_media_wiki_request(page_templates_url))['parse']['templates']

		# Make sure the list is not empty
		if len(page_templates) > 0:
			# Define which templates are considered problematic
			modele_bandeau = [
				"Modèle:Sources secondaires",
				"Modèle:Sources",
				"Modèle:Méta bandeau d'avertissement",
			]
			
			for template in page_templates:
				if template["*"] in modele_bandeau:
					# save article name into file
					log_text("articles_civ.txt", page_title)
					articles_count += 1
					print(page_title + " has some issues.")

	# Print total
	print_notice("In total, " + str(articles_count) + " articles have issues.")
	if articles_count > 0:
		print_notice("Checkout the logs for more details.")

# Triggering the application
app()
