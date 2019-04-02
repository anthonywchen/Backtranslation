#!/bin/bash

# this sample script translates a test set, including
# preprocessing (tokenization, truecasing, and subword segmentation),
# and postprocessing (merging subword units, detruecasing, detokenization).

# instructions: set paths to mosesdecoder, subword_nmt, and nematus,
# then run "./paraphrase.sh input_file target_language_suffix beam_size"

input_file=$(realpath $1)

SRC=en # suffix of source language
TRG=$2 # suffix of target language
BEAM_SIZE=$3

mosesdecoder=$(realpath "mosesdecoder")				 	# path to moses decoder: https://github.com/moses-smt/mosesdecoder
subword_nmt=$(realpath "subword-nmt")				 	# path to subword segmentation scripts: https://github.com/rsennrich/subword-nmt
nematus=$(realpath "nematus") 							# path to nematus ( https://www.github.com/rsennrich/nematus )

FORWARD="$nematus/wmt16_systems/$SRC-$TRG"				# path to source to target translation models and parameters
BACKWARD="$nematus/wmt16_systems/$TRG-$SRC"				# path to target to source translation models and parameters

################################
# Forward translate
################################

# preprocess
tmpfile=$(realpath "tmpfile.txt")

$mosesdecoder/scripts/tokenizer/normalize-punctuation.perl -l $SRC | \
$mosesdecoder/scripts/tokenizer/tokenizer.perl -l $SRC -penn | \
$mosesdecoder/scripts/recaser/truecase.perl -model $FORWARD/truecase-model.$SRC | \
$subword_nmt/apply_bpe.py -c $FORWARD/$SRC$TRG.bpe < $input_file > $tmpfile &

sleep 1

# forward translate
forward_file=$input_file.$TRG.forward
(cd $FORWARD && cat $tmpfile | python $nematus/nematus/translate.py -m $FORWARD/model-ens1.tf -k $BEAM_SIZE --n-best) > $forward_file

rm $tmpfile

# strip out line numbers and scores for backtranslation
cut -d"|" -f4 < $forward_file > $forward_file.stripped

################################
# Backtranslate
################################
backtranslated_file=$input_file.$TRG.backtranslated
(cd $BACKWARD && cat $forward_file.stripped | python $nematus/nematus/translate.py -m $BACKWARD/model-ens1.tf -k $BEAM_SIZE --n-best) > $backtranslated_file

# remove BPE tokens
sed -r 's/(@@ )|(@@ ?$)//g' < $backtranslated_file > $backtranslated_file.tmp
mv $backtranslated_file.tmp $backtranslated_file

################################
# Sort backtranslations by forward*backward score
################################
python sort_paraphrases.py $input_file $forward_file $backtranslated_file $BEAM_SIZE


rm $forward_file
rm $forward_file.stripped
rm $backtranslated_file