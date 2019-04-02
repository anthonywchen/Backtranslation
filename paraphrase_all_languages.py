import argparse
import os
from os.path import join

BEAM_SIZE = 2
TARGET_LANGUAGES = ['cs', 'de', 'ru']
WMT16_PATH = '/home/tony/backtranslation/nematus/wmt16_systems'

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('source_file', help='path to file with sentences to parapharse (backtranslate)')
	args = parser.parse_args()

	source_file = args.source_file

	convert_command = 'python nematus/nematus/theano_tf_convert.py --from_theano --in '
	for tgt in TARGET_LANGUAGES:
		# Convert en-tgt and tgt-en Theano model to TensorFlow model if it hasn't previously been converted
		if os.path.exists(join(WMT16_PATH, 'en-'+tgt, 'model-ens1.tf.json')) == False:
			os.system(convert_command + join(WMT16_PATH, 'en-'+tgt, 'model-ens1.npz') + ' --out ' + join(WMT16_PATH, 'en-'+tgt, 'model-ens1.tf'))

		if os.path.exists(join(WMT16_PATH, tgt+'-en', 'model-ens1.tf.json')) == False:
			os.system(convert_command + join(WMT16_PATH, tgt+'-en', 'model-ens1.npz') + ' --out ' + join(WMT16_PATH, tgt+'-en', 'model-ens1.tf'))

		# Copy the en-tgt and tgt-en JSON files to have a tf extension
		if os.path.exists(join(WMT16_PATH, 'en-'+tgt, 'model-ens1.tf.json')) == False:
			os.system('cp ' + join(WMT16_PATH, 'en-'+tgt, 'model-ens1.npz.json') + ' ' + join(WMT16_PATH, 'en-'+tgt, 'model-ens1.tf.json'))

		if os.path.exists(join(WMT16_PATH, tgt+'-en', 'model-ens1.tf.json')) == False:		
			os.system('cp ' + join(WMT16_PATH, tgt+'-en', 'model-ens1.npz.json') + ' ' + join(WMT16_PATH, tgt+'-en', 'model-ens1.tf.json'))	

		# Call backtranslation script on source document
		os.system('./paraphrase.sh ' + source_file + ' ' + tgt + ' ' + str(BEAM_SIZE))