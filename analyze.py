from IPython.display import display
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import boto3
import bs4


# Takes the wikipedia link of a basketball and returns of dictionay containing the stats of the player
def get_basketball_stats(link='https://en.wikipedia.org/wiki/Michael_Jordan'):

    """ Gets the statistics of any basketball player through out his carrer"""

    # read the webpage 
    response = requests.get(link)
    # create a BeautifulSoup object to parse the HTML  
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    # the player stats are defined  with the attribute CSS class set to 'wikitable sortable'; 
    #therefore we create a tag object "table"
    table=soup.find(class_='wikitable sortable')

    #the headers of the table are the first table row (tr) we create a tag object that has the first row  
    headers=table.tr
    #the table column names are displayed  as an abbreviation; therefore we find all the abbr tags and returs an Iterator
    titles=headers.find_all("abbr")
    #we create a dictionary  and pass the table headers as the keys 
    data = {title['title']:[] for title in titles}
   #we will store each column as a list in a dictionary, the header of the column will be the dictionary key 

    #we iterate over each table row by fining each table tag tr and assign it to the objed
    for row in table.find_all('tr')[1:]:
    
        #we iterate over each cell in the table, as each cell corresponds to a different column we all obtain the correspondin key corresponding the column n 
        for key,a in zip(data.keys(),row.find_all("td")[2:]):
            # we append each elment and strip any extra HTML contnet 
            data[key].append(''.join(c for c in a.text if (c.isdigit() or c == ".")))

    # we remove extra rows by finding the smallest list     
    Min=min([len(x)  for x in data.values()])
    #we convert the elements in the key to floats 
    for key in data.keys():
    
        data[key]=list(map(lambda x: float(x), data[key][:Min]))
       
    return data


# LIst of names and links of basketball players to be analyzed
links=['https://en.wikipedia.org/wiki/Michael_Jordan'\
       ,'https://en.wikipedia.org/wiki/Kobe_Bryant'\
      ,'https://en.wikipedia.org/wiki/LeBron_James'\
      
      ,'https://en.wikipedia.org/wiki/Stephen_Curry']
names=['Michael Jordan','Kobe Bryant','Lebron James','Stephen Curry']


playersDict = dict()

# For each player, get the statitics of the player, print the name, display the stats table for that player
#  and then plot a graph of "Points per game" on the x axis and "Minutes per game on the y axis"
for i in range(len(links)):
    playersDict[names[i]] = get_basketball_stats(links[i])
    
    currentPlayerDf = pd.DataFrame(playersDict[names[i]])
    print(names[i])
    display(currentPlayerDf)

    plt.plot(currentPlayerDf[['Points per game']], currentPlayerDf[['Minutes per game']])
    plt.legend()
    plt.xlabel('Points per game')
    plt.ylabel('Minutes per game')