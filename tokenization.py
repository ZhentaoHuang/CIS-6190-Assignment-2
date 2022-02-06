"""Author: Zhentao Huang (Github link for this assignment: https://github.com/ZhentaoHuang/CIS-6190-Assignment-1)
This file is used to perform the tokenization task. Some code is taken from the scac_good.py file. Type -h for help.

"""

import ply.lex as lex
import argparse
 
# List of token names, always needed
tokens = (
   'LABEL',
   'WORD',
   'NUMBER',
   'APOSTROPHIZED',
   'HYPHENATED',
   'DELIMITERS',
   'PUNCTUATION'
)

def t_LABEL(t): r'\$DOC.+|\$TITLE|\$TEXT'; return t  #LABEL must be exact "$TITLE", "$TEXT" or start with "$DOC"
def t_APOSTROPHIZED(t): r'[a-zA-Z]+(-[a-zA-Z]+)*\'[a-zA-Z]+(\'[a-zA-Z]+)*'; return t
def t_HYPHENATED(t): r'[a-zA-Z0-9]+-[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*'; return t
def t_WORD(t): r'[+|-]?[a-zA-Z0-9]*[a-zA-Z][a-zA-Z0-9]*'; return t # Word are strings of letters and digits but must have one letters at least
def t_NUMBER(t): r'[+|-]?\d+(\.\d+)?'; return t	# Integers and real numbers, with possible positive and negative signs
def t_DELIMITERS(t): r'[ \t]+'; return t
def t_PUNCTUATION(t): r'.'; return t


# Error handling, always required
def t_error(t):
	print("Shouldn't get here")



def scan(data):
	"""This function is used to build the lexer object and scan the input then transfer to a list of tokens. The original code is taken from scan_good.py

	Args:
		data (string): Input string

	Returns:
		tok_list (list): A list of tokens
	"""
	# Build the lexer
	lexer = lex.lex()

	lexer.input(data)
	tok_list = []
	while True:
		tok = lexer.token()
		if not tok:
			break
		
		tok_list.append(tok)
      
	return tok_list


def update_output_with_delimiters(list, output, delimiters):
	"""This function is used to update the output list with delimiters

	Args:
		list (list): a list of parts of the token
		output (list): a sequence of the tokens for ouput, updated by the function
		delimiters (string): delimiters used to seperate different item
	"""

	for item in list[:-1]:
		output.append(item)
		output.append(delimiters)

	output.append(list[-1])

	return


def postproc_HYPHENATED(input, output):
	"""This function is used to check different situation for HYPHENATED token type, and update the ouput list based on that.

	Args:
		input (token): individual item of token_list acquired from the scan() function
		output (list): a sequence of tokens for ouput, updated by the function
	"""

	parts = input.value.split('-')
				
	#For a HYPHENATED token, it should only contain two or three parts when separated by the hyphens				
	if(len(parts) == 2):
		valid = True
		
	#If there are three parts, the middle part can only have one or two characters
	elif(len(parts) == 3 and (len(parts[1]) == 1 or len(parts[1]) == 2)):
		valid = True

	#Else, split the string into sequences of tokens (add "-")
	else:
		valid = False
		for part in parts[:-1]:
			output.append(part)
			output.append('-')

		# If there is "'" as a suffix, split it as well
		if '\'' in parts[-1]:
			small_parts = parts[-1].split('\'')
			update_output_with_delimiters(small_parts, output, '\'')
			
		else:
			output.append(parts[-1])

	if(valid):
			output.append(input.value)

	return 

def postproc_APOSTROPHIZED(input, output):
	"""This function is used to check different situation for APOSTROPHIZED token type, and update the ouput list based on that.


	Args:
		input (token): individual item of token_list acquired from the scan() function
		output (list): a sequence of tokens for ouput, updated by the function
	"""
	parts = input.value.split('\'')

	if('-' in input.value):
		postproc_HYPHENATED(input, output)
		return
	
	#For an APOSTROPHIZED tokens, it should only contain two or three parts when separated by the apostrophes
	if(len(parts) == 2 ):
		
		# If there are two parts, either the first part contains a single character 
		# and the second part contains more than two characters
		# Or the last part contains the character "s/S"
		if((len(parts[0]) == 1 and len(parts[1]) > 2) or (parts[1] == 's' or parts[1] == 'S')):
			valid = True

		# When spliting an token with two parts, keep the "'" with the second part if it has one or two characters
		elif(len(parts[1])== 1 or len(parts[1]) == 2):
			valid = False
			output.append(parts[0])
			output.append('\'' + parts[1])

		#Otherwise, add spaces on both sides of the "'"
		else:
			valid = False
			update_output_with_delimiters(parts, output, '\'')

	elif(len(parts) == 3):

		# If there are three parts, the first part should contain only one character and the last part contains "s"
		if(len(parts[0]) == 1 and (parts[2] == 's' or parts[2] == 'S')):
			valid = True
		else:
			valid = False
			update_output_with_delimiters(parts, output, '\'')
		
	#Else, split the string into sequences of tokens (add "'")
	else:
		valid = False
		update_output_with_delimiters(parts, output, '\'')

	if(valid):
			output.append(input.value)

	return

def postproc_WORD(input, output):
	"""If there is a "+"/"-"/"_" before the WORD, it would also be reconized as WORD token. 
	This function is used to removed the sign.

	Args:
		input (token): individual item of token_list acquired from the scan() function
		output (list): a sequence of tokens for ouput, updated by the function
	"""

	if (input.value[0] == '+' or input.value[0] == '-' or input.value[0] == '_'):
		output.append(input.value[1:])
	else:
		output.append(input.value)

	return

def tokenize(input, output):
	"""This function is used to perform the tokenization task. It reads the lines and call scan() function each line then call the postprocessing functions.

	Args:
		input (file): input file
        output (file): output file
	"""
	lines = input.readlines()

	for line in lines:

		token_list = scan(line[:-1])
		value_list = []
		for token in token_list:
			
			valid = False
			if(token.type != 'DELIMITERS'):	# Skip the delimiters
				if(token.type == 'HYPHENATED'):
					
					postproc_HYPHENATED(token, value_list)	# Process the HYPHENATED and update the value_list
					
				elif(token.type == 'APOSTROPHIZED'):

					postproc_APOSTROPHIZED(token, value_list) # Process the APOSTROPHIZED and update the value_list

				elif(token.type == 'WORD'):

					postproc_WORD(token, value_list) # Process the WORD and update the value_list
			
				else:
					valid = True
			if(valid):
				value_list.append(token.value)	# Append the string to the value_list if it is valid
			
		output.write(' '.join(value_list) + '\n')	# Write the ouput to the file based on value_list

	input.close()
	output.close()



def arg_parse():
    """This function is used for command line argument parsing. It utilizes the argparse library. It provides the user with file choice at runtime.

    Returns:
        args: command line arguments
    """

    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding optional argument
    parser.add_argument("-i", "--Input", default="samples.splitted", help = "The input file (default: samples.splitted)")
    parser.add_argument("-o", "--Output", default="samples.tokenized", help = "The output file (default: samples.tokenized)")
    
    # Read arguments from command line
    args = parser.parse_args()
    
    print("Input: %s" % args.Input)
    print("Output as: % s" % args.Output)

    return args

def main(args):

    input = open(args.Input, 'r')
    output = open(args.Output, 'w')
    
    tokenize(input, output)

    input.close()
    output.close()

if __name__ == "__main__":

    args = arg_parse()
    main(args)