import subprocess
import os
import argparse
import sys
parser = argparse.ArgumentParser(description='Making backbone file')
parser.add_argument('-nameorg', type=str, help='way', required=True)
parser.add_argument('-dirname', type=str, help='dirname', required=True)
args = parser.parse_args()

#check path of your files 
path = '/Users/danilkr/orgs/' + '{}'.format(args.dirname) + '/'
#important '()' invalid syntax
rep = '/applications/Mauve.app/Contents/MacOS/progressivemauve --backbone-output=/Users/danilkr/backbones/' + '{}'.format(args.nameorg) + '.backbone' + ' {}'.format(path).join(os.listdir('/Users/danilkr/orgs/' + '{}'.format(args.dirname)))
print(rep)
subprocess.call(rep, shell=True)