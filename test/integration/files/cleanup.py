#!/usr/bin/python
# Script to cleanup regkey emails
# Copy regkey email(s) into a file and pass in input/output files
# Example:
#  python cleanup.py -i <filename of unformated> -o <filename of formated>
import sys
import getopt
import re


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = str(arg)
        elif opt in ("-o", "--ofile"):
            outputfile = str(arg)
    print('Input file is {0}'.format(inputfile))
    print('Output file is {0}'.format(outputfile))
    pattern = re.compile(r'<(\d{4,5})>')
    bigipLicenseRegex = re.compile(r'\w{5}-\w{5}-\w{5}-\w{5}-\w{7}')
    bigipLicense = ""
    for i, line in enumerate(open(inputfile)):
        for match in re.finditer(bigipLicenseRegex, line):
            bigipLicense = (bigipLicense + "\n" + match.group())
            print("Adding:" + match.group())
    f_output = open(outputfile, "a+")
    f_output.write(bigipLicense)
    f_input = open(inputfile, "w")
    f_input.write('')


if __name__ == "__main__":
    main(sys.argv[1:])
