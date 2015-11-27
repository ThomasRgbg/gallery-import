#!/usr/bin/python -u

from glob import glob
import os
import sys
import shutil
import subprocess

from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS

def getexifdate(image):
    date = None

    exifinfo = image._getexif()
    if exifinfo == None:
        return None
    for tag, value in exifinfo.items():
        decoded = TAGS.get(tag, tag)
        if decoded == 'DateTimeOriginal':
            date = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')

    return date

def create_indexmd(ifilename, title, text=None):
    indexmd = open(ifilename, 'wb')
    indexmd.write('Title: {0}\n'.format(title))
    indexmd.write('\n')
    if text:
	indexmd.write(text + '\n')
    indexmd.close()


def create_neues_indexmd(ifilename, link):
    title='Neue Bilder und Videos'
    text='Hier ist immer nur das neueste Bild, die Bilder des zugehoerigen Monats gibts [hier]({0})'.format(link)
    create_indexmd(ifilename, title, text)


# Workaround for SSH calls from Mac
sys.stderr = sys.stdout

chattext = None

print("---------- autogallery.py - Check if datenserver is mounted")

subprocess.call(['./check_datenserver.sh'], stdout=sys.stdout, stderr=sys.stdout)

print("---------- autogallery.py - Analyse Pictures")

filepattern = ('*.JPG', '*.jpg')

# FIXME: German characters not supported (e.g. Maerz)
monthdict = { 1:'Januar', 2:'Februar', 3:'Maerz', 4:'April', 5:'Mai', 6:'Juni', 7:'Juli', 8:'August', 9:'September', 10:'Oktober', 11:'November', 12:'Dezember'}

neuesdir = 'webgallery/Neues/'

print('Clear Neues')
for filetype in filepattern:
    for filename in glob(neuesdir + filetype):
	os.remove(filename)
for filename in glob(neuesdir + 'index.md'):
	os.remove(neuesdir + 'index.md')

print('Process autogallery directory')
for filetype in filepattern:
    for filename in glob('autogallery/' + filetype):
	print("----------")
        image = Image.open(filename)
	date = getexifdate(image)
	image.close()

        if not date:
	    print 'Datei: {0} No date'.format(filename)
	    break
	else:
	    print 'Datei: {0}, Jahr {1} Monat {2}'.format(filename, date.year, date.month)
	    
	    yearname='Regensburg_{0}'.format(date.year)
	    targetdir = 'webgallery/' + yearname
	    if os.path.exists(targetdir):
		print('Directory for Year exist')
	    else:
		print('Creating Dir for new Year: {0}'.format(targetdir))
		os.mkdir(targetdir)

	    monthname = '{0}_{1:0>2}'.format(date.year,date.month)
	    monthdir = targetdir + '/' + monthname
	    if os.path.exists(monthdir):
		print('Directory for Month exist')
	    else:
		print('Creating Dir for new Month: {0}'.format(monthdir))
		os.mkdir(monthdir)

		print('Creating index.md')
		title = '{0}'.format(monthdict[date.month])
		create_indexmd(monthdir + '/index.md', title)

	    targetfile = monthdir + '/' + os.path.basename(filename)
	    print('Moving {0} to {1}'.format(filename,targetfile))
	    if os.path.isfile(targetfile):
		print('Destination already exist: {0}, removing'.format(targetfile))
		os.remove(targetfile)
	    shutil.move(filename,monthdir)

	    linksrc = '../' + yearname + '/' + monthname + '/' + os.path.basename(filename)
            linkdest = neuesdir + os.path.basename(filename)
	    print('Create link from {0} to {1}'.format(linksrc, linkdest) )
	    os.symlink(linksrc, linkdest)

	#FIXME: does not work for multiple pictures
	#chattext = 'Ein neues Bild bei https://server.de/bilder/Regensburg_{0}/{1}_{2:0>2}/'.format(date.year,date.year,date.month)
	chattext = 'Ein neues Bild bei https://server.de/bilder/Neues'


print('--------- autogallery.py - done analysing pictures')
if chattext:
	print('Create new index.md for Neues')
	create_neues_indexmd( neuesdir + 'index.md', '../Regensburg_2015/{0}'.format(monthname) )

	print('--------- autogallery.py - call Sigal')
	subprocess.call(['sigal','build'], stdout=sys.stdout, stderr=sys.stdout)
	print('--------- autogallery.py - call sync_mailpi.sh')
	subprocess.call(['./sync_mailpi.sh'], stdout=sys.stdout, stderr=sys.stdout)
	print('--------- autogallery.py - call send_client.py')
	subprocess.call(['./send_telegram.py','-m', chattext], stdout=sys.stdout, stderr=sys.stdout)
else:
	print('No new picture found')
print('--------- autogallery.py - End')


