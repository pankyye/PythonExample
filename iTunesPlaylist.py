import re, argparse
import sys
from matplotlob import pyplot
import plistlib
import numpy as np

def findCommonTracks(fileNames):
	"""
	find common tracks in given playlist files, and save them to 
	common.txt
	"""
	trackNamesSets=[]
	for fileName in fileNames:
		trackNames=set()
		plist=plistlib.readPlist(fileName)
		tracks=plist['Tracks']
		for trackId,track in tracks.items():
			try:
				trackNames.add(track['Name'])
			except:
				pass
		trackNameSets.append(trackNames)

	commonTracks=set.intersection(*trackNameSets)

	if len(commonTracks)>0:
		f=open('common.txt','wb')
		for val in commonTracks:
			s='%s\n' %val
			f.write(s.encode('UTF-8'))
		f.close()
		print('%d commin tracks found.'
			'track names written to common.txt' % len(commonTracks))
	else:
		print('No common tracks')

def plotStats(fileName):
	'''
	Plot some statistics by readin track information from playlist
	'''
	plist=plistlib.readPlist(fileName)
	tracks=plist['Tracks']
	ratings=[]
	durations=[]
	for trackId,track in tracks.items():
		try:
			ratings.append(track['album rating'])
			durations.append(track['total time'])
		except:
			pass 
	if ratings==[] or durations==[]:
		print('No valid album rating/total time data in %s.' %fileName)
		return

	x = np.array(durations, np.int32)
    # convert to minutes
    x = x/60000.0
    y = np.array(ratings, np.int32)
    pyplot.subplot(2, 1, 1)
    pyplot.plot(x, y, 'o')
    pyplot.axis([0, 1.05*np.max(x), -1, 110])
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Track rating')

    # plot histogram
    pyplot.subplot(2, 1, 2)
    pyplot.hist(x, bins=20)
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Count')

    # show plot
    pyplot.show()


def findDuplicates(fileName):
	'''
	find duplicate tracks in given playlist
	'''

	print('finding duplicate tracks in %s...' % fileName)
	plist=plistlib.readPlist(fileName)
	tracks=plist['Tracks']
	trackNames={}
	for trackId,track in tracks.items():
		try:
			name=track['Name']
			duration=track['total time']
			if name in trackNames:
				if duration//1000==trackNames[name][0]//1000:
					count=trackNames[name][1]
					trackNames[name]=(duration,count+1)
			else:
				trackNames[name]=(duration,1)
		except:
			pass 
	# store duplicates as (name, count) tuples
	dups=[]
	for k,v in trackNames.items():
		if v[1]>1:
			dups.append((v[1],k))
	if len(dups)>0:
		print('found %d duplicates. track names saved to dup.txt' % len(dups))
	else:
		print('no duplicate tracks found')
	f=open('dups.txt','w')
	for val in dups:
		f.write('[%d]%s\n' %(val[0],val[1]))
	f.close()

def main():
	parser=argparse.ArgumentParser(description=descStr)
	group=parser.add_mutually_exclusive_group()
	# add expected arguments
	group.add_argument('--common',narg='*',dest='plFiles',required=False)
	group.add_argument('--stats',dest='plFile',required=False)
	group.add_argument('--dup',dest='plFileD',required=False)

	#parse args
	args=parser.parse_args()

	if args.plFiles:
		findCommonTracks(args.plFiles)
	elif args.plFiles:
		plotStats(args.plFiles)
	elif args.plFileD:
		findDuplicates(args.plFileD)
	else:
		print('these are not the tracks you are looking for.')

if __name__='__main__':
	main()





























