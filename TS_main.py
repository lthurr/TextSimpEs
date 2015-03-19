#!/usr/bin/python
# -*- coding:utf-8 -*-

from sys import argv
from math import floor
import utils
from jinja2 import Template
import codecs

MODEL = "Language_Model/ngram_count_corpus_ordered.txt"
UMBRAL = 0

def show_help():
	return """\nUsage:\n""" + \
		"""TS_main.py file_to_parse.txt n m\n""" + \
		"""where n is the n-gram argument default:3"""

def pre_process_corpus(st):
	st = st.lower()
	st = utils.separate_punt_marks(st)
	st = utils.tag_numbers(st)
	return st

def match_ngrams(ngram_model, ngram_input):
	assert len(ngram_model) == len(ngram_input)
	b = True
	for (e1, e2) in zip(ngram_model, ngram_input):
		b = e1 == e2 and b
	return b

def mean_ngram(n_gram_len):
	model = open(MODEL, 'r')
	model = list(model)
	ki = 0
	n = 0
	for line in model:
		n_gram_set, amount = line.split('\t')
		n_gram_list = n_gram_set.split()
		if len(n_gram_list) == n_gram_len: #Is an unigram
			n+=1
			ki+=int(amount)
	return ki//n

def umbral_0():
	return 5

def umbral_1():
	return mean_ngram(1)

def umbral_2(p_adjust):
	return int(floor(umbral_1()*p_adjust))

def umbral_3():
	m1 = mean_ngram(1)
	m2 = mean_ngram(2)
	m3 = mean_ngram(3)
	return m1+m2+m3

def count_ngrams(text_to_analyse, n_gram_argument):
	model = open(MODEL, 'r')
	model = list(model)
	result = dict()
	with open(text_to_analyse, 'r') as input_txt:
		input_list = pre_process_corpus(input_txt.read()).split()
		for i in range(1, n_gram_argument + 1):
			n_gram_input = utils.find_ngrams(input_list, i)
			for n_gram in n_gram_input:
				n_gram_amout = 0
				for line in model:
					n_gram_set, amount = line.split('\t')
					n_gram_list = n_gram_set.split()
					if len(n_gram_list) == i:
						if match_ngrams(n_gram, n_gram_list):
							n_gram_amout = int(amount)
							#print "INFO: N-gram: (%s), amount: %s" % (', '.join(n_gram), n_gram_amout)
							break
				if n_gram_amout == 0:
					#print "INFO: N-gram: (%s), amount: 0" % ', '.join(n_gram)
					pass
				result[', '.join(n_gram)] = n_gram_amout
	return result

def neighbors(input_list, i, ngram_count):
	assert len(input_list) >= 5
	if ngram_count == 1:
		return [input_list[i:i+1]]
	elif i == 0:
		if ngram_count == 2:
			return [input_list[i:i+1], input_list[i:i+2]]
		elif ngram_count == 3:
			return [input_list[i:i+1], input_list[i:i+2], input_list[i:i+3]]
	elif i == 1:
		if ngram_count == 2:
			return [input_list[i-1:i+1], input_list[i:i+1], input_list[i:i+2]]
		elif ngram_count == 3:
			return [input_list[i-1:i+1], input_list[i:i+1], input_list[i:i+2], input_list[i:i+3]]
	elif i == len(input_list)-1:
		if ngram_count == 2:
			return [input_list[i-1:i+1], input_list[i:i+1]]
		elif ngram_count == 3:
			return [input_list[i-2:i+1], input_list[i-1:i+1], input_list[i:i+1]]
	elif i == len(input_list)-2:
		if ngram_count == 2:
			return [input_list[i-1:i+1], input_list[i:i+1], input_list[i:i+2]]
		elif ngram_count == 3:
			return [input_list[i-2:i+1], input_list[i-1:i+1], input_list[i:i+1], input_list[i:i+2]]
	else:
		if ngram_count == 2:
			return [input_list[i-1:i+1], input_list[i:i+1], input_list[i:i+2]]
		elif ngram_count == 3:
			return [input_list[i-2:i+1], input_list[i-1:i+1], input_list[i:i+1], input_list[i:i+2], input_list[i:i+3]]


def render_template(text_to_analyse, complex_words, output="output.html"):
	jinja_temp = codecs.open('template.html', 'r', 'utf-8').read()
	template = Template(jinja_temp)
	template_vars = {
		"original_text": text_to_analyse,
		"complex_words": complex_words
	}
	with codecs.open(output, 'wb', 'utf-8') as output_file:
		output_file.write(template.render(template_vars))

if __name__ == '__main__':
	args = argv[1:]
	assert len(args) <= 2 and len(args) > 0, show_help()
	assert args[0].endswith('.txt'), show_help()
	n_gram_argument = 3
	UMBRAL = umbral_1()
	print "Umbral usado %d" % UMBRAL
	text_to_analyse = args[0]
	if len(args) == 2:
		n_gram_argument = int(args[1])
	counts_ngram_from_input = count_ngrams(text_to_analyse, n_gram_argument)
	with open(text_to_analyse, 'r') as input_txt:
		input_list = pre_process_corpus(input_txt.read()).split()
		result = []
		for i in range(len(input_list)):
			list_of_neighbors = neighbors(input_list, i, n_gram_argument)
			total = 0
			for neighbor in list_of_neighbors:
				query = ', '.join(neighbor)
				total += counts_ngram_from_input[query]
			if total < UMBRAL:
				result.append(input_list[i])
	print "Palabras complejas: ", ', '.join(result)
	#render_template(open(text_to_analyse, 'r').read(), result)
