import json
import pickle
import nltk
import numpy as np
import tflearn
from nltk.stem.lancaster import LancasterStemmer
import random

contractions = { 
"ain't": "am not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he's": "he is",
"how'd": "how did",
"how'll": "how will",
"how's": "how is",
"i'd": "i would",
"i'll": "i will",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'll": "it will",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"must've": "must have",
"mustn't": "must not",
"needn't": "need not",
"oughtn't": "ought not",
"shan't": "shall not",
"sha'n't": "shall not",
"she'd": "she would",
"she'll": "she will",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"that'd": "that would",
"that's": "that is",
"there'd": "there had",
"there's": "there is",
"they'd": "they would",
"they'll": "they will",
"they're": "they are",
"they've": "they have",
"wasn't": "was not",
"we'd": "we would",
"we'll": "we will",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"where'd": "where did",
"where's": "where is",
"who'll": "who will",
"who's": "who is",
"won't": "will not",
"wouldn't": "would not",
"you'd": "you would",
"you'll": "you will",
"you're": "you are"
}

ERROR_THRESHOLD = 0.25

def clean_up_sentence(sentence):
	
	sentence_words = []
	
	tokenized_words = nltk.word_tokenize(sentence)
	
	tokenized_words = [stemmer.stem(word.lower()) for word in tokenized_words]
	for word in tokenized_words:
		if word in contractions:
			sentence_words.append(contractions[word])
		else:
			sentence_words.append(word)
	return sentence_words


def bow(sentence, words, show_details=False):
	
	sentence_words = clean_up_sentence(sentence)

	bag = [0]*len(words)  
	for word in sentence_words:
		for index, w in enumerate(words):
			if w == word:
				bag[index] = 1
				if show_details:
					print ("found in bag: %s" % w)

	return(np.array(bag))

def classify(sentence, model):
	model_results = model.predict([bow(sentence, words)])
	results = model_results[0]
	results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
	results.sort(key=lambda x: x[1], reverse=True)
	return_list = []
	for r in results:
		return_list.append((classes[r[0]], r[1]))
	return return_list

def response(sentence, model, userID='123', show_details=False):
	results = classify(sentence, model)
	
	if results:
		while results:
			for i in intents['intents']:
				
				if i['tag'] == results[0][0]:
					return random.choice(i['responses'])

			results.pop(0)


if __name__ == "__main__":

	with open('intents.json') as json_data:
		intents = json.load(json_data)

	
	stemmer = LancasterStemmer()
	
	nltk.download('punkt')

	data = pickle.load(open("training_data", "rb"))
	words = data['words']
	classes = data['classes']
	train_x = data['train_x']
	train_y = data['train_y']
	
	net = tflearn.input_data(shape=[None, len(train_x[0])])
	net = tflearn.fully_connected(net, 8)
	net = tflearn.fully_connected(net, 8)
	net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
	net = tflearn.regression(net)

	model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
	model.load('./model.tflearn')

	intents = response('Is your shop open today ?', model)
	print intents


	


