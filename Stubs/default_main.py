'''
A defautl main() that has logging and argparse elements
It must be altered for use, but works as a roadmap
'''
def main():
	#create logger
	logger = logging.getLogger(__name__)
	#logfile format
	formatter = logging.Formatter(
		"%(asctime)s %(name)s : %(levelname)s : \t %(message)s", "%d/%m/%Y %H:%M:%S")
	logger.setLevel(logging.DEBUG)

	#log level screen prints out to
	terminal_format = logging.Formatter("\n%(message)s")
	PR = logging.StreamHandler()
	PR.setLevel(logging.INFO)
	PR.setFormatter(terminal_format)
	logger.addHandler(PR)

	logger.debug('starting up...')

	#create parser options for cli
	parser = argparse.ArgumentParser(description=
	'foobar')
	parser.add_argument('-e', '--extension', help='Select the extention for your file', default='.tsv')
	parser.add_argument('-o','--output', help='Select the file path for your output', required=False)
	parser.add_argument('-i','--input', help= 'Select the file path for your input(s)',required=False)
	#parser options for log file
	parser.add_argument("-v", "--verbose", help="show verbose logger", action="store_true")
	parser.add_argument("-l", "--log", help="log to file", action="store_true")

	arguments = parser.parse_args()

	#set the log levels
	if arguments.verbose:
		PR.setLevel(logging.DEBUG)
	elif arguments.log:
			#don't know if this naming convention will work
			logFilePath = str(_function.__name__)+".log"
			file_handler = logging.FileHandler(logFilePath)
			file_handler.setFormatter(formatter)
			file_handler.setLevel(logging.DEBUG)
			logger.addHandler(file_handler)
	while True:
		#applies if no args given that arent about logging
		if (arguments.output is None and arguments.input is None and arguments.extension is None):
			try:
				response_1 = input(
					"\nPress Y to see a demo otherwise press N or Enter to exit\n")
				response_1 = response_1.lower()
				pass
			except ValueError:
				print ('Sorry, I did not understand that')
				continue
		y = ['y', 'yes', 'yeah']
		n = ['n', 'no', '']
		if response_1 in y:
			Demo_mode(_function)
			break
		elif response_1 in n:
			break
		else:
			_function(arguments)
			break
