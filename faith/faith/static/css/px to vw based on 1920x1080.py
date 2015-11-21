
txt = open("browse.css")

myStr = txt.read()

writerIndex=0
findIndexPX = myStr.find("vw", writerIndex)

while ((findIndexPX)>-1): #an instance of px has been found
	
	#get the number right before it
	#find the last space or : character
	findIndexSPACE = myStr.rfind(" ",0,findIndexPX)
	findIndexCOLON = myStr.rfind(":",0,findIndexPX)

	#take whichever one is larger i.e. occurs later
	numberStartIndex = max(findIndexCOLON, findIndexSPACE) + 1

	mySubString = myStr[numberStartIndex : findIndexPX]
	myInt = float(mySubString)

	#the calculation
	myReplacement = round( myInt*16 , 0) # to 2 d.p... 19.2 is 1920/100 as a vw is 1% of your viewport = 19.2 pixels

	#replace it in myStr
	myStr = myStr[0: numberStartIndex] + str(myReplacement) + "px" + myStr[findIndexPX+2 : ] 

	writerIndex = findIndexPX
	findIndexPX = myStr.find("vw", writerIndex)



print( myStr )

