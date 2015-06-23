import sys

def main(argv):
    print len(argv)
    if(len(argv) == 2):
	print "reading!"
    if(len(argv) == 3):
	print "writing!"

if __name__ == "__main__":
    main(sys.argv[1:])
