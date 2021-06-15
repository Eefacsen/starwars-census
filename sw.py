import os
import re
import json
import pandas as pd
import matplotlib.pyplot as plt

# FUNCTIONS
def openFile():
    try:
        filePath = './files/starWars.json'
        with open(filePath, 'r') as myFile: 
            # The file swFile gets opened as a list of dictionaries
            swFile = json.load(myFile)
            # I needed to remove once level of dictionay so I built a new list from key 'fields'
            newFields = []
            for item in swFile: # prepare data for pandas and json use
                newFields.append(item['fields'])
            
            # I use the .from_dict() function in pandas as 'newFields' is a list of Dictionaries
            df2 = pd.DataFrame.from_dict(newFields)
            # I created a general clean that I send the data through
            df = genClean(df2)
            return(df)
    except Exception as e:
        print('error in openFile : {}'.format(e))

def getFileInfo(op):
    df = openFile()
    # Here I am just using all diferent Dataframe reporting options to see info in the DataFrame    
    if op == 1:
        print('')
        print(df.info())
        input('Press enter to continue')
    elif op == 2:
        print('')
        print(df.head())
        input('Press enter to continue')
    elif op == 3:
        print('')
        print(df.tail())
        input('Press enter to continue')
    elif op == 4:
        print('')
        print(df.to_string())
        input('Press enter to continue')
    elif op == 5:
        try:
            print('\nEnter the row you wish to print from\n')
            opRow1 = int(input('--> : '))
            print('\nEnter the row you wish to print to\n')
            opRow2 = int(input('--> : '))
            if opRow1 != '' and opRow2 != '':
                print('')
                print(df.loc[opRow1:opRow2])
            else:
                print('\nINVALID INPUT FOR ROW SELETION\n')
        except Exception as e:
            print('Error in getFileInfo op == 5 : {}'.format(e))
    else:
        print('Error in getFileInfo')

def age():
    global df
    formatAge()
    
    print('\nAt the Battle of Yamin, ')
    oldest = df.loc[df['birth_year'].idxmax()]
    #oldest = df.idxmax()
    print('The oldest known Charactor was:')
    print('{} years - {}'.format(oldest['birth_year'],oldest['name']))
    youngest = df.loc[df['birth_year'].idxmin()]
    print('The youngest known Charactor was:')
    print('{} years - {}'.format(youngest['birth_year'],youngest['name']))
    avgAge = df['birth_year'].mean()
    avgAge = round(avgAge, 2)
    print('The average age of charactors was:')
    print('{} years'.format(avgAge))
    input('\nPress enter to continue')

    # I make a new dataframe from selected age data to report in a graph using matplotlib.pyplot
    ageDct = {youngest['name']:youngest['birth_year'], 'Average Age':avgAge, oldest['name']:oldest['birth_year']}
    ageDF = pd.DataFrame(ageDct, index=[0])
    
    ageDF.plot.barh()
    plt.show()

def height():
    formatHeight()

    # report general stats
    print('\nAt the Battle of Yamin, ')
    tallest = df.loc[df['height'].idxmax()]
    print('The tallest known Charactor was:')
    print('{} cm - {}'.format(tallest['height'],tallest['name']))
    shortest = df.loc[df['height'].idxmin()]
    print('The shortest known Charactor was:')
    print('{} cm - {}'.format(shortest['height'],shortest['name']))
    avgHeight = df['height'].mean()
    avgHeight = round(avgHeight, 2)
    print('The average Height of charactors was:')
    print('{} cm'.format(avgHeight))
    input('\nPress enter to continue')

    # create a new Dataframe fro plotting
    ageDct = {shortest['name']:shortest['height'],'Average Height':avgHeight,tallest['name']:tallest['height']}
    ageDF = pd.DataFrame(ageDct, index=[0])
    
    ageDF.plot.bar()
    plt.show()
    # can also make chart from Dct - https://stackoverflow.com/questions/16010869/plot-a-bar-using-matplotlib-using-a-dictionary

def mass():
    formatMass()

    # report general stats
    print('\nAt the Battle of Yamin, ')
    heaviest = df.loc[df['mass'].idxmax()]
    print('The heaviest known Charactor was:')
    print('{} kg - {}'.format(heaviest['mass'],heaviest['name']))
    lightest = df.loc[df['mass'].idxmin()]
    print('The lightest known Charactor was:')
    print('{} kg - {}'.format(lightest['mass'],lightest['name']))
    avgMass = df['mass'].mean()
    avgMass = round(avgMass, 2)
    print('The average weight of charactors was:')
    print('{} kg'.format(avgMass))
    input('\nPress enter to continue')

    # create new dataframe for plotting
    ageDct = {lightest['name']:lightest['mass'],'Average Weight':avgMass,heaviest['name']:heaviest['mass']}
    ageDF = pd.DataFrame(ageDct, index=[0])
    
    ageDF.plot.bar()
    plt.show()

def gender():
    global df
    # define new counters
    maleCount = 0
    femaleCount = 0
    unknown = 0
    # use the dataframe groupby() function and report back the count by using size()
    newDF = df.groupby(['gender']).size()   

    newDF.plot.pie(y='Gender',figsize=(5,5))
    plt.show()
    # add values to pie chart! using autopct is probably the best way

    """
    #newDF = df[['gender']].groupby(['gender'])
    print(newDF)

    for x in df.index:
        gender = df.loc[x, df['gender']]
    
        if gender == "male":
            maleCount += 1
        elif gender == "female":
            femaleCount += 1
        else:
            unknown += 1
    #genderDct = {'males':maleCount,'females':femaleCount,'unknown':unknown}
    #genderDF = pd.DataFrame(genderDct, index=[0])
    
    y = [maleCount,femaleCount,unknown]
    myLabels = ['males','females','unknown']
    
    print('\nAt the Battle of Yamin,')
    print('There were {} males')
    print('There were {} females')
    print('There were {} without gender')
    print('We can assume these where droids')

    input('\nPress enter to continue')

    plt.pie(y, labels=myLabels)
    plt.show()
    """

def timeVsMass():
    df = openFile()
    formatAge()
    formatMass()

    print('')
    print('Only charactors with both known Age and Weight will be considered\n')
    
    for x in df.index:
        if df['birth_year'][x] > 200:
            print('{} - {} years old removed from DataFrame as exceptional'.format(df['name'][x],df['birth_year'][x]))
            df.drop(x, inplace=True)  
        """
        elif df['mass'][x] > 100:
            print('{} - {} kg removed from DataFrame as exceptional'.format(df['name'][x],df['height'][x]))
            df.drop(x, inplace=True)             
        """
    print('As viewed in our graph - no trend can be drawn between birth year and average population weight')
    input('\nPress enter to continue')

    df.plot(kind = 'scatter', x = 'birth_year', y = 'mass')
    plt.show()

    input('\nPress enter to continue')

def timeVsGrowth():
    df = openFile()
    formatAge()
    formatHeight()
    print('')
    print('Only charactors with both known Age and Height will be considered\n')
    for x in df.index:
        if df['birth_year'][x] > 200:
            print('{} - {} years old removed from DataFrame as exceptional'.format(df['name'][x],df['birth_year'][x]))
            df.drop(x, inplace=True)  

        elif df['height'][x] > 210:
            print('{} - {} cm tall removed from DataFrame as exceptional'.format(df['name'][x],df['height'][x]))
            df.drop(x, inplace=True) 

        elif df['height'][x] < 100:
            print('{} - {} cm tall removed from DataFrame as exceptional'.format(df['name'][x],df['height'][x]))
            df.drop(x, inplace=True)             
    
    print('\nAs viewed in our graph - no trend can be drawn between birth year and average population height')
    input('\nPress enter to continue')

    df.plot(kind = 'scatter', x = 'birth_year', y = 'height')
    plt.show()

    input('\nPress enter to continue')
    timeVsMass()

def genderMass():
    global df
    formatMass()

    maleCount = 0
    femaleCount = 0
    unknown = 0
    
    #newDF = df['gender'] and df['mass']

    newDF = df.groupby(['gender']).agg(['mean'])
    del newDF['homeworld'] 
    print(newDF)
    
    
    newDF.plot.pie(y = newDF['mass'], labels = newDF.index())
    plt.show()

# DATA CLEANING

def genClean(df2):
    # user toggle option to see info or not
    global editingInfo
    # I record the amount of data rows I start with
    bEmpty = len(df2.index)
    # I then remove any entries with empty data cells to avoid complication later
    df2.dropna(inplace = True)
    # I record new amount of data rows after clean
    aEmpty = len(df2.index)
    x = bEmpty - aEmpty 
    if editingInfo:
        print('\n{} rows were removed due to empty data'.format(x))
    
    # I now check for duplicated rows
    # copy is used to reportign during below if statment
    copy = df2.duplicated()
    index = 0
    for item in copy:
        if item == True:
            if editingInfo:
                print('row {} removed from df as a duplicate'.format(index))
        index += 1
    
    # after reporting that duplicates will be removed then drop duplicated using 'inplace=true'
    df2.drop_duplicates(inplace = True)
    # send to remove unwanted columns (different function as this is unique to this file)
    df = dataCorrection(df2)
    return(df)

def dataCorrection(df):
    global editingInfo
    # This function is unique to this databass but wanted for each time we open the file
    # remove unnessisary columns from the df
    del df['edited']
    del df['created']
    if editingInfo:
        print('Removed columns \'edited\' and \'created\'')

    return(df)

def formatHeight():
    global df
    # record amount of dropped data rows
    dropCount3 = 0
    for x in df.index:
        height = df.loc[x, "height"]
        # if the data is a digit then pass over
        if re.match(r"\d", height): 
            pass
        # if data is not a digit drop it from the dataframe
        else:
            df.drop(x, inplace=True)
            dropCount3 += 1
    # report changes made to dataframe
    print('\n{} Height rows purged'.format(dropCount3))
    # convert string to num
    df['height'] = pd.to_numeric(df['height'])
    # no need for a return as we have changed the global dataframe

def formatMass():
    global df
    # record changes
    dropCount2 = 0
    for x in df.index:
        mass = df.loc[x, "mass"]
        
        # check if mass is a number
        if re.search(r"\d", mass):   
            # check if mass has a comma as number spacing                
            if re.search(r',', mass): 
                # remove the comma completely to create clean num
                mass = mass.replace(",","")
                # check that the variable mass starts and ends with a number and that the string is not longer than 5
                if re.match(r'^[0-9]{1,5}$', mass):
                    df.loc[x, "mass"] = mass
                else:
                    df.drop(x, inplace=True)
                    dropCount2 += 1
            # no commas so just check the num format
            elif re.match(r'^[0-9]{1,5}$', mass):
                pass
            else:
                df.drop(x, inplace=True)
                dropCount2 += 1
        else:
            df.drop(x, inplace=True)
            dropCount2 += 1
    # report on dataframe changeds
    print('\n{} Mass rows purged'.format(dropCount2))
    # convert srting to num
    df['mass'] = pd.to_numeric(df['mass'])

def formatAge():
    global df
    # the for loop will remove the BBY(before battle of Yamin) from each birth_year and update the df with a Float value
    changeCount = 0
    dropCount = 0
    for x in df.index:

        # we need to declare the year as a str type or on the 2nd run through the type is a numpy:float and regex will cause an error
        year = str(df.loc[x, "birth_year"])
        # for regex use regex PAL read bottom right for best advice
        if re.match(r"\d", year):
            new_year = year.replace("BBY", "")
            df.loc[x, "birth_year"] = new_year
            changeCount += 1
        # if we run the age function again the BBY will be removed so we seach for only digits and no letters then pass over these
        elif re.match(r"\d+\W", year):
            pass
        else:
            df.drop(x, inplace=True)
            dropCount += 1
    # report on changed data
    print('\n{} Birth year, dates corrected'.format(changeCount))
    print('{} Charactors removed as unknown'.format(dropCount))
    
    # change the formated string data to num to be ploted
    df['birth_year'] = pd.to_numeric(df['birth_year'])
    

def corralation():
    formatAge()
    formatHeight()
    formatMass()

    print('')
    print(df.corr())

# VARIABLES

editingInfo = False

# MAIN LOOPS
def menu3():
    usingMenu3 = True
    while usingMenu3:
        print('\n---------------------------')
        print(' GUINESS BOOK OF STAR WARS')
        print('            MENU 3')
        print('---------------------------\n')

        print('[1] - Age')
        print('[2] - Height')
        print('[3] - Mass')
        print('[4] - Gender')
        print('[5] - Time Vs Growth')
        print('[6] - Gender Mass')
    
        try:
            op = int(input('--> : '))
            
            if op == 999:
                usingMenu3 = False
            elif op == 0:
                # this is an option I hid from my menu to give me the ability to find further matches between the colums in the DataFrame
                corralation()
            elif op == 1:
                age()
            elif op == 2:
                height()
            elif op == 3:
                mass()
            elif op == 4:
                gender()
            elif op == 5:
                timeVsGrowth()
            elif op == 6:
                genderMass()
            else:
                print('INVALID INPUT')

        except Exception as e:
            print('error using menu 1 : {}'.format(e))


def menu2():
    usingMenu2 = True
    while usingMenu2:
        print('\n-------------')
        print(' INFORMATION')
        print('   MENU 2')
        print('-------------\n')

        print('[1] - Summary of file information')
        print('[2] - First info')
        print('[3] - Last info')
        print('[4] - All info')
        print('[5] - Selection of info')
    
        try:
            op = int(input('--> : '))

            if op == 999:
                usingMenu2 = False
            elif op in range(1, 6):
                getFileInfo(op)
            else:
                print('INVALID INPUT')

        except Exception as e:
            print('error using menu 1 : {}'.format(e))



def menu1():
    global editingInfo
    usingMenu1 = True
    while usingMenu1:
        print('------------')
        print(' STAR WARS')
        print('  MENU 1')
        print('------------\n')

        print('[1] - File information')
        print('[2] - Guiness Book of Star Wars')
        print('[3] - Toggle DataFrame editing info text')

        try:
            op = int(input('--> : '))

            if op == 999:
                print('---GOOD BYE---')
                usingMenu1 = False
            elif op == 1:
                # Used to print selected rows in the DataFrame
                menu2()
            elif op == 2:
                # used the Data to generate information tables/graphics
                menu3()
            elif op == 3:
                # use bolean value to establish current stat and toggle on/off
                if editingInfo:
                    editingInfo = False
                    print('DataFrame editing text OFF')
                else:
                    editingInfo = True
                    print('DataFrame editing text ON')
            else:
                print('INVALID INPUT')

        except Exception as e:
            print('error using menu 1 : {}'.format(e))
    
# before anything happens I want to json file opened, cleaned, and stored as a DataFrame    
df = openFile()

if __name__ == '__main__':
    menu1()