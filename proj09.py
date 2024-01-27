'''
CSE 231
Project 09

This project will take the .csv files from the user that they input and convert
it into data sets that will be organized and displayed for the user. The user may
search by country name, plot the country, and compare two countries at the same time.

'''

import csv
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt

#Function combines the dictionaries
def combine_dictionaries(year, subD, superD):
    superD[year] = subD
    return superD
#Function opens the read file
def open_file(year_str):
    filename = year_str + '.csv'
    try:
        fp = open(filename, 'r')
        return fp
    except:
        return None
#The function allows the user to input and search by inquiry 
def search_by_country(country1, superD, print_boolean):
    lst = []
    lst2 = []
    d = superD
    #Condition statement
    if print_boolean == True:
        #Series of conditions
        for year, dictionaries in d.items():
            for val in dictionaries.values():
                for country, vals in val.items():
                    if country in country1:
                        #Tuple
                        rank = vals[0][0]
                        score = vals[0][1]
                        family = vals[2][0]
                        health = vals[2][1]
                        freedom = vals[2][2]
                        #Print Body
                        print()
                        print('{:<10s}{:<s}'.format('Year:', year))
                        print('{:<10s}{:<s}'.format('Country:', country))
                        print('{:<10s}{:<5d}'.format('Rank:', rank))
                        print('{:<10s}{:<5.2f}'.format('Score:', score))
                        print('{:<10s}{:<5.2f}'.format('Family:', family))
                        print('{:<10s}{:<5.2f}'.format('Health:', health))
                        print('{:<10s}{:<5.2f}'.format('Freedom:', freedom))
                        print('-'*20)

    
    else:
        for key, val in d.items():
            year = key
            dictionaries = val
            for keys, values in dictionaries.items():
                for countries, tuples in values.items():
                    if country1 in countries:
                        lst.append(tuples)
                    else:
                        pass
        #First Tuple        
        hs = lst[0][0][1]
        f = lst[0][2][0]
        h = lst[0][2][1]
        free = lst[0][2][2]
        tup = (hs, f, h, free)
        #Second tuple
        hs_ = lst[1][0][1]
        f_ = lst[1][2][0]
        h_ = lst[1][2][1]
        free_ = lst[1][2][2]
        tup_ = (hs_, f_, h_, free_)
        #appends the tuples to the list
        lst2.append(tup)
        lst2.append(tup_)
        return lst2
#Function builds dictionary
def build_dictionary(fp):
    D = {}
    reader = csv.reader(fp)
    #Skips headerline
    next(reader,None)
    for line in reader:
        try:
            region = line[1]; country = line[0]; rank = line[2]; happy = line[3]; economy = line[5]; trust = line[9]; family = line[6]; health = line[7]; freedom = line[8]
            if region not in D:
                D[region] = {country:((int(rank), float(happy)), (float(economy), float(trust)), (float(family), float(health), float(freedom)))}
            else:
                D[region][country] = ((int(rank), float(happy)), (float(economy), float(trust)), (float(family), float(health), float(freedom)))
        #Fixes Error
        except ValueError:
            continue 
        #Fixes Error    
        except KeyError:
            continue
    fp.close()
    return D
#Function takes the countries and organizes them by ranks
def print_ranks(superD, list1, list2, year_one, year_two):
    print("\n{:<15s} {:>7s} {:>7s} {:>12s}".format("Country ",str(year_one),str(year_two),"Avg.H.Score"))
    for i in range(len(list1)):
        C=list1[i][0]
        rank_one, rank_two = search_by_country(C, superD, False)[0][0], search_by_country(C, superD, False)[1][0]
        
        Average_Rank = (rank_one+rank_two)/2
        print("{:<15s} {:>7d} {:>7d} {:>12.2f}".format(C, list1[i][1], list2[i][1], Average_Rank))
#The Function is the prequsite for the bar_plot
#It creates a list the that has tuples appended to it
def prepare_plot(country1, country2, superD):
    print_boolean = False
    prep = []
    #Tuple 1 and is later appended to the prep list
    country1 = search_by_country(country1, superD, print_boolean)
    #Tuple 2 is later appended to the prep list
    country2 = search_by_country(country2, superD, print_boolean)

    prep.append(country1[0])
    prep.append(country2[0])

    return prep
#Function takes the top ten countries and lists them in order
def top_10_ranks_across_years(superD, year_one, year_two):
    result_one, result_two = [], []
    for region_one in superD[year_one]:
        for country_one in superD[year_one][region_one]:
            country_one_data = superD[year_one][region_one][country_one]; position = int(country_one_data[0][0])
            result_one.append((country_one, position))
        result_one.sort(key=lambda x: x[1])
        result_one = result_one[0:10]
    for year_one_result in result_one:
        for region_two in superD[year_two]:
            for country_two in superD[year_two][region_two]:
                if country_two == year_one_result[0]:
                    position = int(superD[year_two][region_two][country_two][0][0])
                    result_two.append((country_two, position))
    return [result_one, result_two]

#The function creates a bar plot from the countrues the user has input
def bar_plot(country1, country2, countrylist1, countrylist2):
    ''' Bar plot comparing two countries.'''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    N = 4
    ind = np.arange(N)
    width = 0.25

    rects1 = ax.bar(ind, countrylist1, width,
                    color='black',
                    error_kw=dict(elinewidth=2, ecolor='blue'))

    rects2 = ax.bar(ind + width, countrylist2, width,
                    color='red',
                    error_kw=dict(elinewidth=2, ecolor='red'))

    ax.set_xlim(-width, len(ind) + width)
    ax.set_ylabel('Quantity')
    ax.set_title('Comparison between the two countries')
    xTickMarks = ['Happiness Sc.', 'Family', 'Health', 'Freedom']
    ax.set_xticks(ind + width)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=0, fontsize=10)

    ax.legend((rects1[0], rects2[0]), (country1, country2))
    plt.show()
#Displays the main menu, and allows the user to interact with the program
def main():
    ''' Docstring '''

    BANNER = '''
                    __ooooooooo__
                 oOOOOOOOOOOOOOOOOOOOOOo
             oOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo
          oOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo
        oOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo
      oOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo
     oOOOOOOOOOOO*  *OOOOOOOOOOOOOO*  *OOOOOOOOOOOOo
    oOOOOOOOOOOO      OOOOOOOOOOOO      OOOOOOOOOOOOo
    oOOOOOOOOOOOOo  oOOOOOOOOOOOOOOo  oOOOOOOOOOOOOOo
    oOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo
    oOOOO     OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO     OOOOo
    oOOOOOO OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO OOOOOOo
    *OOOOO  OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO  OOOOO*
    *OOOOOO  *OOOOOOOOOOOOOOOOOOOOOOOOOOOOO*  OOOOOO*
     *OOOOOO  *OOOOOOOOOOOOOOOOOOOOOOOOOOO*  OOOOOO*
      *OOOOOOo  *OOOOOOOOOOOOOOOOOOOOOOO*  oOOOOOO*
        *OOOOOOOo  *OOOOOOOOOOOOOOOOO*  oOOOOOOO*
          *OOOOOOOOo  *OOOOOOOOOOO*  oOOOOOOOO*      
             *OOOOOOOOo           oOOOOOOOO*      
                 *OOOOOOOOOOOOOOOOOOOOO*    
                      ""ooooooooo""
    '''

    MENU = '''
    1. Search by country
    2. Top 10 countries
    3. Compare countries
    x. Exit 
    :'''
    print(BANNER)

    years=input("Input Years comma-separated as A,B: ")
    years=years.split(',')
    year_one=years[0]; year_two= years[1]
    #Creates Dictionary
    superD = {}
    #List 1 construction
    fp1 = open_file('{}'.format(year_one))
    print("Opening Data file for year {}: ".format(year_one))
    d1 = build_dictionary(fp1)
    combine_dictionaries(year_one,d1,superD)
    #List 2 construction
    fp2 = open_file('{}'.format(year_two))
    print("Opening Data file for year {}: ".format(year_two))
    d2 = build_dictionary(fp2)
    combine_dictionaries(year_two,d2,superD)

    #Takes user input 
    user_input = input(MENU)


    while user_input != 'x' or user_input == 'X':
        #Displays the country the user inputs
        if user_input == '1':
            country=input("[ ? ] Please specify the country: ")
            search_by_country(country,superD,True)
        #Displays the Top ten countries
        elif user_input=='2':
            list1 = top_10_ranks_across_years(superD,year_one,year_two)[0]
            list2 = top_10_ranks_across_years(superD,year_one,year_two)[1]
            print_ranks(superD,list1,list2,year_one,year_two)
        #Displays the comparsion of two countries
        elif user_input == '3':
            #User input for country C= Country
            C = input("[ ? ] Please specify the two countries (A,B): ")
            #Splits the two countries into two separate lists
            C = C.split(',')
            data = prepare_plot(C[0],C[1],superD)
            #Country Data 1
            cd=data[0]
            #Country Data 2
            cd2=data[1]
            #Header Print
            print("{:<20s} {:<9s} {:<8s} {:<8s} {:<8s}".format("\nCountry","Hap.Score","Family","Life Ex.","Freedom"))
            #Body Print
            print("{:<20s} {:<9.2f} {:<8.2f} {:<8.2f} {:<8.2f}".format(C[0],cd[0],cd[1],cd[2],cd[3]))
            print("{:<20s} {:<9.2f} {:<8.2f} {:<8.2f} {:<8.2f}".format(C[1],cd2[0],cd2[1],cd2[2],cd2[3]))
            _input_ = input("[ ? ] Plot (y/n)? ")

            #Continues with function
            if _input_ == 'y' or _input_ == 'Y':
                bar_plot(country[0],country[1],cd,cd2)
            #Ends program
            if _input_ == 'n' or _input_ == 'N':
                pass
            #Incorrect input condition
        else:
            print("[ - ] Incorrect input. Try again.")
        #Prompts user with main menu again
        user_input = input(MENU)

if __name__ == '__main__':
    main()
    
