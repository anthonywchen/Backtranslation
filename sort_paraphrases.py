import argparse


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('source_file', help='path to file with sentences to parapharse (backtranslate)')
	parser.add_argument('forward_file', help='path to file with forward translations')
	parser.add_argument('back_file', help='path to file with backtranslations')
	parser.add_argument('beam_size', help='beam size of forward and back translations')

	args = parser.parse_args()

	source_path = args.source_file
	forward_path = args.forward_file
	back_path = args.back_file
	beam_size = int(args.beam_size)

	source_file = open(source_path)
	forward_file =  open(forward_path)
	back_file = open(back_path)

	output_file = open(back_path+'.sorted', 'w')

	for source_line in source_file:    
	    source_line = source_line.strip()
	    back_lines = []
	    
	    # Get the next beam_size lines from forward file
	    for _ in range(beam_size):
	        forward_line = next(forward_file)
	        _, forward_translated, forward_score = forward_line.strip().split('|||')
	        
	        # For each forward translated line, get the next beam_size lines from backtranslation file
	        for _ in range(beam_size):
	            back_line = next(back_file)
	            _, back_translated, back_score = back_line.strip().split('|||')
	            
	            # Append the backtranslation along with forward*backward score
	            back_lines.append((back_translated, float(back_score)*float(forward_score)))
	    
	    # Sort backtranslations by forward*backward score
	    back_lines.sort(key=lambda tup: tup[1])
	    back_lines = [(e[0].strip(), round(e[1], 2)) for e in back_lines]

	    output_file.write(source_line + '\t' + back_lines.__repr__() + '\n')