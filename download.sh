# Pull necessary repositories 
git clone https://github.com/EdinburghNLP/nematus.git
git clone https://github.com/rsennrich/subword-nmt.git
git clone https://github.com/moses-smt/mosesdecoder.git

# Pull pretrained translation models
wget -r -e robots=off -nH -np -R index.html* http://data.statmt.org/wmt16_systems/
mv wmt16_systems nematus/