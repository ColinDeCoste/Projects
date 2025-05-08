#
# Program: PROG5000 Assignment 2: Places of the World
# Programmer: Colin DeCoste
# Purpose: Divide the extent of the selection into quadrants, provide a list of
#           point locations, then list the total number of places and total population in 
#           each quadrant. Finally, list the information of the most and least populated
#           places selected.
# Date: November 7, 2024
#

import os

# Edges of the map:
layer = iface.activeLayer()
lyrExtent = layer.extent()
westest = lyrExtent.xMinimum()
eastest = lyrExtent.xMaximum()
southest = lyrExtent.yMinimum()
northest = lyrExtent.yMaximum()

# Midpoint:
xMid = (westest + eastest)/2
yMid = (southest + northest)/2

#Determine if latitude is in northern or southern hemisphere
def getNSHemi(yCoord):
    
    NS_hemi = ''
    
    if yCoord >= yMid:
        NS_hemi = 'North'
    else:
        NS_hemi = 'South'
    return NS_hemi
    
#Determine if longitude is in eastern or western hemisphere    
def getEWHemi(xCoord):
    
    EW_hemi = ''
    
    if xCoord >= xMid:
        EW_hemi = 'western'
    else:
        EW_hemi = 'eastern'
    return EW_hemi

# Printing Report
def main(filename,filepath):
    
    # Variables
    dictionary = {'num_NE': 0, 'pop_NE': 0,\
                  'num_NW': 0, 'pop_NW': 0,\
                  'num_SE': 0, 'pop_SE': 0,\
                  'num_SW': 0, 'pop_SW': 0,\
                  'max_pop_name':'', 'min_pop_name':'',\
                  'max_pop': 0, 'max_pop_place':'',\
                  'min_pop': 0, 'min_pop_place':''}
    list_xCoord = []
    list_yCoord = []
    list_Names = []
    list_NS_Hemi = []
    list_EW_Hemi = []
    list_pop = []
    Quadrant = []
    list_num = 0
    NW_Quad = 0
    NE_Quad = 0
    SW_Quad = 0
    SE_Quad = 0
    NW_pop = 0
    NE_pop = 0
    SW_pop = 0
    SE_pop = 0

    os.chdir(f'{filepath}')
    writefile = open(f'{filename}.txt','w')
    writefile.write('\tQuadrant Report\n')
    writefile.write('='*35)
    writefile.write('\n')

    # Extract data and put in respective lists
    feature = layer.getSelectedFeatures()
    
    for pt in feature:
        
        list_num += 1
        geom = pt.geometry()
        xCoord = geom.asPoint().x()
        yCoord = geom.asPoint().y()
        pop = pt['pop_max']
        Name = pt['nameascii']

        list_Names.append(Name)
        list_xCoord.append(xCoord)
        list_yCoord.append(yCoord)
        list_NS_Hemi.append(getNSHemi(yCoord))
        list_EW_Hemi.append(getEWHemi(xCoord))
        list_pop.append(pop)
        
        if list_EW_Hemi[list_num-1] == 'western' and list_NS_Hemi[list_num-1] == 'North':
            dictionary['num_NW'] +=1
            dictionary['pop_NW'] += pop
            Quadrant.append('Northwest')
            
        elif list_EW_Hemi[list_num-1] == 'western' and list_NS_Hemi[list_num-1] == 'South':
            dictionary['num_SW'] +=1
            dictionary['pop_SW'] += pop
            Quadrant.append('Southwest')
            
        elif list_EW_Hemi[list_num-1]=='eastern' and list_NS_Hemi[list_num-1] == 'North':
            dictionary['num_NE'] +=1
            dictionary['pop_NE'] += pop
            Quadrant.append('Northeast')
            
        elif list_EW_Hemi[list_num-1] == 'eastern' and list_NS_Hemi[list_num-1] == 'South':
            dictionary['num_SE'] +=1
            dictionary['pop_SE'] += pop
            Quadrant.append('Southeast')
        #else: xCoord == xMid and yCoord == yMid:
        #    print('Wow, this point is in the middle of the map!')
            
        writefile.write(f'{list_num}. {Quadrant[list_num-1]}\n')
    
    # Min and Max places:
    dictionary['max_pop'] = max(list_pop)
    maxpos = (list_pop.index(dictionary['max_pop']))
    dictionary['max_pop_name'] = list_Names[maxpos]
    dictionary['max_pop_place'] = ('%s%s' % (list_NS_Hemi[maxpos],list_EW_Hemi[maxpos]))
    
    dictionary['min_pop'] = min(list_pop)
    minpos = (list_pop.index(dictionary['min_pop']))
    dictionary['min_pop_name'] = list_Names[minpos]
    dictionary['min_pop_place'] = ('%s%s' % (list_NS_Hemi[minpos],list_EW_Hemi[minpos]))    
    
    writefile.write('='*35)
    writefile.write('\n')
    writefile.write(f'{dictionary['num_NE']} northeastern places have a total population of {dictionary['pop_NE']}\n')
    writefile.write(f'{dictionary['num_NW']} northwestern places have a total population of {dictionary['pop_NW']}\n')
    writefile.write(f'{dictionary['num_SE']} southeastern places have a total population of {dictionary['pop_SE']}\n')
    writefile.write(f'{dictionary['num_SW']} southwestern places have a total population of {dictionary['pop_SW']}\n')
    writefile.write('='*35)
    writefile.write('\n')
    writefile.write(f'The {dictionary['max_pop_place']} place of {dictionary['max_pop_name']} has the highest population of {dictionary['max_pop']}.\n')
    writefile.write(f'The {dictionary['min_pop_place']} place of {dictionary['min_pop_name']} has the highest population of {dictionary['min_pop']}.\n')

# Setting File Path and Name with validation
def getname(filepath):
    qI = QInputDialog()
    mode = QLineEdit.Normal
    title2 = 'Pick File Name'
    label2 = 'Please name your file:'
    defVal2 = 'QuandrantReportForPeopleWithPoorFileManagement'
        
    filename, filenameok = QInputDialog.getText(qI,title2,label2,mode,defVal2)
        
    if filenameok == True:
        main(filename,filepath)
        print('Enjoy!')
            
    if filenameok == False:
        print("Bye.")
    
    return filename
    
def set_path():
    
    isPath = False
    while isPath == False:

        qI = QInputDialog()
        mode = QLineEdit.Normal
        title1 = 'Define File Path'
        label1 = 'Please define your file path'
        defVal1 = 'C:\\temp'
        
        filepath, filepathok = QInputDialog.getText(qI,title1,label1,mode,defVal1)
        
        if filepathok == True:
            if os.path.isdir(filepath):
                isPath = True
            else:
                print('Invalid file. Please enter a valid file path.')
                
        else:
            print('Bye.')
            break
        
    if isPath == True:
        getname(filepath)
        
    return filepath
    

# Use all features if none selected by user.
if layer.selectedFeatures() == []:
    layer.selectAll()
    set_path()
else:
    set_path()
