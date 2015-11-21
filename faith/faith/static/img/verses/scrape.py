import urllib
import urllib2

base = 'http://legacy.quran.com/images/ayat_retina/'
for s in range(1,115):
	for a in range(1,300):
		print str(s) + ':' + str(a)
		try:
			urllib2.urlopen(base + str(s) + '_' + str(a) + '.png')
			urllib.urlretrieve(base + str(s) + '_' + str(a) + '.png', str(s) + '-' + str(a) + '.png')
		except:
			pass
