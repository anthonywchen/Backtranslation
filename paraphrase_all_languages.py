import argparse
from ast import literal_eval
import csv
from jsonlines import Reader
import os
from os.path import join

BEAM_SIZE = 5
TARGET_LANGUAGES = ['cs', 'de', 'ru']
WMT16_PATH = 'nematus/wmt16_systems'

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('source_file', help='path to file with sentences to parapharse (backtranslate)')
	args = parser.parse_args()

	source_file = args.source_file

	convert_command = 'python nematus/nematus/theano_tf_convert.py --from_theano --in '
	for tgt in TARGET_LANGUAGES:
		# Convert en-tgt and tgt-en Theano model to TensorFlow model if it hasn't previously been converted
		if os.path.exists(join(WMT16_PATH, 'en-'+tgt, 'model-ens1.tf.index')) == False:
			os.system(convert_command + join(WMT16_PATH, 'en-'+tgt, 'model-ens1.npz') + ' --out ' + join(WMT16_PATH, 'en-'+tgt, 'model-ens1.tf'))

		if os.path.exists(join(WMT16_PATH, tgt+'-en', 'model-ens1.tf.index')) == False:
			os.system(convert_command + join(WMT16_PATH, tgt+'-en', 'model-ens1.npz') + ' --out ' + join(WMT16_PATH, tgt+'-en', 'model-ens1.tf'))

		# Copy the en-tgt and tgt-en JSON files to have a tf extension
		if os.path.exists(join(WMT16_PATH, 'en-'+tgt, 'model-ens1.tf.json')) == False:
			os.system('cp ' + join(WMT16_PATH, 'en-'+tgt, 'model-ens1.npz.json') + ' ' + join(WMT16_PATH, 'en-'+tgt, 'model-ens1.tf.json'))

		if os.path.exists(join(WMT16_PATH, tgt+'-en', 'model-ens1.tf.json')) == False:		
			os.system('cp ' + join(WMT16_PATH, tgt+'-en', 'model-ens1.npz.json') + ' ' + join(WMT16_PATH, tgt+'-en', 'model-ens1.tf.json'))	

		# Call backtranslation script on source document
		os.system('./paraphrase.sh ' + source_file + ' ' + tgt + ' ' + str(BEAM_SIZE))

	# Merge the backtranslated files from the multiple pivot languages into one file
	translation_files = [csv.reader(open(source_file + '.' + tgt + '.backtranslated.sorted'), delimiter='\t') for tgt in TARGET_LANGUAGES]
	writer = open(source_file + '.backtranslations', 'w')

	while True:
		try:
			lines = [next(e) for e in translation_files]
		except StopIteration:
			break
		head = lines[0][0]
		paraphrases = [f for e in lines for f in literal_eval(e[1])[:]]
		paraphrases.sort(key=lambda tup: tup[1])
		writer.write(head + '\t' + paraphrases.__repr__() + '\n')
	
	writer.close()
