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
#Change your path 
path = '/Users/danilkr/orgs/' + '{}'.format(args.dirname) + '/'
if SK == 'Mauve':
    rep = '/applications/Mauve.app/Contents/MacOS/progressivemauve --backbone-output=/Users/danilkr/backbones/{}.backbone /Users/danilkr/orgs/{}/'.format(
        args.nameorg, args.nameorg) + ' {}'.format(
            path).join(
                [f for f in os.listdir ('/Users/danilkr/orgs/{}'.format(
                args.dirname)) if '.DS_Store' not in f  and '.sslist' not in f])

#Change your path 
elif SK == 'Sibelia':
    
    rep ='/Users/danilkr/Sibelia/./sibelia -s loose -o /Users/danilkr/Sib_coord/{}.txt /Users/danilkr/orgs/{}/'.format(args.nameorg, args.nameorg) + ' {}'.format( 
        path).join(
            [f for f in os.listdir ('/Users/danilkr/orgs/{}'.format(
                args.dirname)) if '.DS_Store' not in f and '.sslist' not in f])
else:
    print('Programm is not suppurted!\n Skript uses only Mauve and Sibelia')

print(rep)
subprocess.call(rep, shell=True)