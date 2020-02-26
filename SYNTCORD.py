#This comined skript, which uses to make mauve_backbone_file and Sibelia_coordinates
import subprocess
import os
import argparse
import sys

parser = argparse.ArgumentParser(description='Making backbone file')
parser.add_argument('-skript', type=str, help='Mauve or Sibelia', required=True)
parser.add_argument('-nameorg', type=str, help='way', required=True)
parser.add_argument('-dirname', type=str, help='dirname', required=True)
args = parser.parse_args()
SK = args.skript
path = '/Users/danilkr/orgs/' + '{}'.format(args.dirname) + '/'
if SK == 'Mauve':
    rep = '/applications/Mauve.app/Contents/MacOS/progressivemauve --backbone-output=/Users/danilkr/backbones/' + '{}'.format(
        args.nameorg) + '.backbone' + ' {}'.format(
            path).join(os.listdir ('/Users/danilkr/orgs/' + '{}'.format(
                args.dirname)))
elif SK == 'Sibelia':
    rep ='/Users/danilkr/Sibelia/./sibelia -s loose -o /Users/danilkr/Sib_coord' + ' {}'.format(
        path).join(
            os.listdir ('/Users/danilkr/orgs/{}'.format(
                args.dirname)))
else:
    print('Programm is not suppurted!\n Skript uses only Mauve and Sibelia')
    sys.exit()

print(rep)
subprocess.call(rep, shell=True)