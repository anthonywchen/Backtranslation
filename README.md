# Backtranslation

A repository for generating paraphrases via backtranslation. 

Tested on `Ubuntu 18.04.2 LTS (Bionic Beaver)` and with `TensorFlow 1.13.1`. 

## Steps

Run the following where you want clone the repository:
```
# Clone repository
git clone https://github.com/anthonywchen/Backtranslation.git
cd Backtranslation/

# Create virtualenv
virtualenv --python=python3.6 ENV
source ENV/bin/activate

# Install requirements and downloads pretrained translation models (32 GB)
chmod 700 download.sh
./download.sh
pip install -r requirements.txt

chmod 700 paraphrase.sh
```

For a source file where each line contains a sentence to be paraphrased, run
```
python paraphrase_all_languages.py [source_file]
```
To modify the beam size of the forward and backward translation, modify the variables directly in `paraphrase_all_languages.py`.

## Files
**download.**sh**** 
Downloads repositories for tokenization, byte-pair-encoding, and translation as well as pre-trained translation models.

**requirements.txt**
Python packages to download.

**paraphrase_all_languages.py**
Top level script that creates paraphrases using three different pivot languages. Run this! Creates `BEAM_SIZE^2` number of paraphrases per pivot language. 
Modify `BEAM_SIZE` in this script. 
```
$ python paraphrase_all_languages.py -h
usage: paraphrase_all_languages.py [-h] source_file

positional arguments:
	source_file  path to file with sentences to parapharse (backtranslate)

optional arguments:
	-h, --help   show this help message and exit
```
**paraphrase**.**sh**
Called by `paraphrase_all_languages.py` and is passed the source file, the pivot language, and the beam size. 

**sort_paraphrases.py**
Called by `paraphrase.sh` after the forward and backward translation process. It calculates the score of each backtranslated sentence by multiplying its backward translation score with the forward translation score and rewrites the backtranslated file in a sorted format.
