names = []
#scrapes through each webpage on billboard.com for top 100 artists per year
def reader():
    counter = 0
    nameIndex = []
    
    year = 2020
    yearstring = str(year)
    filename = "artists"+yearstring+".txt"

    while 2006 <= year:
        counter = 0 
        yearstring = str(year)
        filename = "artists"+yearstring+".txt"
        #grabs index of each artist name
        with open(filename) as f:
            for line in f:
                counter+=1 
                if """<div class="ye-chart-item__title">""" in line:
                    nameIndex.append(counter+2)
        f.close()
        counter = 0
    
        with open(filename) as f:
            for line in f:
                counter+=1
                if counter in nameIndex:
                    line = line.strip()
                    line = line.strip("\n")
                    if line not in names:
                        names.append(line.encode('utf-8'))
        f.close()
        nameIndex=[]
        year -=1

    print(names)