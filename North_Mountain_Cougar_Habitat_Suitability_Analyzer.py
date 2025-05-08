#
# Program: Assignment1: North Mountain Cougar Habitat Suitability Analysis
# Purpose: Calculate the suitability of forest stands in a NSDNR dataset for the
#           North Mountain Cougar habitat. Run in QGIS.
# Programmer: Colin DeCoste
# Date: October 15, 2024
#

# Set imported data as active layer
forestlyr = iface.activeLayer()

# Clear selected features
forestlyr.removeSelection()

# Create species list
forestlyr.selectAll()
unique_species = []

for currspecies in forestlyr.selectedFeatures():
    species = currspecies['SP1']
    try:
         position = unique_species.index(species)
    except:
        unique_species.append(species)

unique_species.remove(NULL)


def main1():
    
    # Pop-up species selector
    qI = QInputDialog()
    title = 'SP1 Selection'
    label = 'Select SP1'
    mode = QLineEdit.Normal
    SPone,okSP1 = QInputDialog.getItem(qI, title, label,unique_species)
    print("SP1 selected: ", SPone)
    print("User clicked okay button: ", okSP1)
    
    # Selection process
    expression1 = '"SP1" = \'%s\'' % SPone

    forestlyr.selectByExpression(expression1,QgsVectorLayer.SetSelection)

    forsel = forestlyr.selectedFeatures()

    # Define variables
    height_rat = 0
    dia_rat = 0
    cov_rat = 0
    suit_rat = 0

    low_suit_poly_count = 0
    low_suit_min_area = 0
    low_suit_max_area = 0
    low_suit_tot_area = 0
    low_suit_ave_area = 0

    med_suit_poly_count = 0
    med_suit_min_area = 0
    med_suit_max_area = 0
    med_suit_tot_area = 0
    med_suit_ave_area = 0

    hi_suit_poly_count = 0
    hi_suit_min_area = 0
    hi_suit_max_area = 0
    hi_suit_tot_area = 0
    hi_suit_ave_area = 0

    # Classify polygons
    for currfeature in forsel:
        if currfeature['HEIGHT'] < 10:
            height_rat = 1.25
        elif currfeature['Height'] > 20:
            height_rat = 3.75
        else:
            height_rat = 2.5
        
        if currfeature['AVDI'] < 20:
            dia_rat = 0.75
        elif currfeature['AVDI'] > 30:
            dia_rat = 2.5
        else:
            dia_rat = 1.75
            
        if currfeature['COVER_TYPE'] == 2:
            cov_rat = 1
        elif currfeature['COVER_TYPE'] == 5:
             cov_rat = 2
        else:
             cov_rat = 3.75
             
        suit_rat = height_rat + dia_rat + cov_rat
        
    # Low Suitability Polygon Properties
        if suit_rat < 5:
            low_suit_poly_count += 1
            
            low_suit_tot_area += currfeature['SHAPE_AREA']
            
            low_ave = low_suit_tot_area/low_suit_poly_count
            
            if low_suit_poly_count == 1:
                low_suit_min_area = currfeature['SHAPE_AREA']
                low_suit_max_area = currfeature['SHAPE_AREA']
                
            elif currfeature['SHAPE_AREA'] < low_suit_min_area:
                low_suit_min_area = currfeature['SHAPE_AREA']
            
            elif currfeature['SHAPE_AREA'] < low_suit_max_area:
                low_suit_max_area = currfeature['SHAPE_AREA']
     
    # High Suitability Polygon Properties 
        elif suit_rat > 8:
            hi_suit_poly_count += 1
            
            hi_suit_tot_area += currfeature['SHAPE_AREA']
            
            hi_suit_ave_area = hi_suit_tot_area/hi_suit_poly_count
            
            if hi_suit_poly_count == 1:
                hi_suit_min_area = currfeature['SHAPE_AREA']
                hi_suit_max_area = currfeature['SHAPE_AREA']
            
            if currfeature['SHAPE_AREA'] < hi_suit_min_area:
                hi_suit_min_area = currfeature['SHAPE_AREA']
                
            if currfeature['SHAPE_AREA'] > hi_suit_max_area:
                hi_suit_max_area = currfeature['SHAPE_AREA']
     
    # Medium Suitability Polygon Properties 
        else:
            med_suit_poly_count += 1
            
            med_suit_tot_area += currfeature['SHAPE_AREA']
            
            med_suit_ave_area = med_suit_tot_area/med_suit_poly_count
            
            if med_suit_poly_count == 1:
                med_suit_min_area = currfeature['SHAPE_AREA']
                med_suit_max_area = currfeature['SHAPE_AREA']
            
            if currfeature['SHAPE_AREA'] < med_suit_min_area:
                med_suit_min_area = currfeature['SHAPE_AREA']
            if currfeature['SHAPE_AREA'] < med_suit_max_area:
                med_suit_max_area = currfeature['SHAPE_AREA']
                
    # Print Report
    print('='*70)
    print('\t\tNorth Mountain Cougar Habitat Suitability Analysis')
    print('\t\t\t%i  of %s Polygons in Study Area' % (len(forsel),SPone))
    print('='*70)
    print('Low Suitability:')
    print('\t\t\t\t- Number of polygons  :         %3i' % low_suit_poly_count)
    print('\t\t\t\t- Minimum polygon area:       %9.3f' % low_suit_min_area)
    print('\t\t\t\t- Maximum poylgon area:       %9.3f' % low_suit_max_area)
    print('\t\t\t\t- Total area          :      %10.3f' % low_suit_tot_area)
    print('\t\t\t\t- Average polygon area:       %9.3f'% low_suit_ave_area)
    print()
    print('Medium Suitability:')
    print('\t\t\t\t- Number of polygons  :         %3i' % med_suit_poly_count)
    print('\t\t\t\t- Minimum polygon area:       %9.3f' % med_suit_min_area)
    print('\t\t\t\t- Maximum poylgon area:       %9.3f' % med_suit_max_area)
    print('\t\t\t\t- Total area          :      %10.3f' % med_suit_tot_area)
    print('\t\t\t\t- Average polygon area:       %9.3f' % med_suit_ave_area)
    print()
    print('High Suitability:')
    print('\t\t\t\t- Number of polygons  :         %3i' % hi_suit_poly_count)
    print('\t\t\t\t- Minimum polygon area:       %9.3f' % hi_suit_min_area)
    print('\t\t\t\t- Maximum poylgon area:       %9.3f' % hi_suit_max_area)
    print('\t\t\t\t- Total area          :      %10.3f' % hi_suit_tot_area)
    print('\t\t\t\t- Average polygon area:       %9.3f' % hi_suit_ave_area)
    print('='*70)

# While loop to run again or no
YesNo = "Y"
while YesNo[0] != "N":
    
    main1()
    
    choice1 = ["Yes","No"]
    qJ = QInputDialog()
    title2 = 'Run Program Again?'
    label2 = 'Yes or No:'
    mode = QLineEdit.Normal
    YesNo,okYesNo = QInputDialog.getItem(qJ, title2,label2,choice1)
    if okYesNo == False:
        YesNo = "N"
    
print("\n"," ---- Good Bye"*4, "----")


