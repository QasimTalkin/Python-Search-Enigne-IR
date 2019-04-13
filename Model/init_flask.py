from flask import Flask, flash, url_for, request, render_template, request, redirect, Response
import random, json, sys
sys.path.append("..")
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, RadioField
from vsm_bol_search import booleanSearch, vsmSearch
from CorpusAccess import corpusAccess
from wtforms.validators import DataRequired



app = Flask(__name__)
app.secret_key = "super secret key"


class SearchBar(Form):
	SearchQuery = TextField('SearchQuery:', validators=[validators.required()], render_kw={"placeholder": "Type you query here!"})
	SearchTopic = TextField('SearchTopics', validators=[validators.required()], render_kw={"placeholder": "Search for topic here"})
#get the query from user and print results!
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	topics = ['copra-cake', 'crude', 'skr', 'palladium', 'livestock', 'nkr', 'dfl', 'sugar', 'lin-oil', 'lin-meal', 'income', 'retail', 'wool', 'pork-belly', 'tea', 'gnp', 'wpi', 'trade', 'soy-oil', 'carcass', 'barley', 'cotton', 'instal-debt', 'lumber', 'austdlr', 'propane', 'corn', 'coffee', 'veg-oil', 'castorseed', 'rape-meal', 'gold', 'rye', 'corn-oil', 'lead', 'groundnut-oil', 'stg', 'reserves', 'money-fx', 'rand', 'lit', 'coconut', 'naphtha', 'soybean', 'orange', 'housing', 'acq', 'platinum', 'ringgit', 'tapioca', 'soy-meal', 'dmk', 'fishmeal', 'copper', 'palmkernel', 'plywood', 'earn', 'sunseed', 'cornglutenfeed', 'sfr', 'coconut-oil', 'sorghum', 'tin', 'interest', 'rice', 'iron-steel', 'hog', 'hk', 'gas', 'zinc', 'lei', 'bop', 'oilseed', 'silver', 'can', 'jobs', 'sun-meal', 'rupiah', 'nat-gas', 'rape-oil', 'saudriyal', 'grain', 'groundnut', 'wheat', 'cpi', 'f-cattle', 'cpu', 'citruspulp', 'bfr', 'potato', 'l-cattle', 'cottonseed', 'oat', 'peseta', 'sun-oil', 'yen', 'nzdlr', 'money-supply', 'dlr', 'fuel', 'dkr', 'red-bean', 'rapeseed', 'pet-chem', 'rubber', 'inventories', 'jet', 'strategic-metal', 'linseed', 'cotton-oil', 'nickel', 'ipi', 'palm-oil', 'castor-oil', 'heat', 'cocoa', 'meal-feed', 'alum', 'ship']
	form = SearchBar(request.form)
	if request.method == 'POST':

		SearchQuery=request.form['SearchQuery']
		search_results = booleanSearch.Search()
		search_results = search_results.query(SearchQuery)
		corpus_access = corpusAccess.CorpusAccess()
		final_results = []
		for i in range(len(search_results)):
			split_results  = search_results[i].split(' : ')
			document_from_corpus = corpus_access.access(split_results[0])
			document_from_corpus['score'] = split_results[1]
			final_results.append(document_from_corpus)
			print(f'Retrived Results Doc ID -> {split_results[0]} and Score -> {split_results[1]}')
		return render_template('results1.html', results=final_results, model="Final Search Engine", query=SearchQuery)
	return render_template('index.html', form=form, topics=topics )


@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/receiver', methods = ['POST'])
def worker():
	# read json + reply
	data = request.get_json(force=True)
	result = ''

	for item in data:
		# loop over every row
		make = str(item['make'])
		if(make == 'Porsche'):
			result += make + ' -- That is a good manufacturer\n'
		else:
			result += make + ' -- That is only an average manufacturer\n'

	return result



@app.route('/result/<doc_id>')
def get_result(doc_id):
	corpus_access = corpusAccess.CorpusAccess()
	print("from init flask ->>>> ", doc_id)
	return render_template('result.html', result=corpus_access.access(doc_id))


if __name__ == "__main__":
	app.run()