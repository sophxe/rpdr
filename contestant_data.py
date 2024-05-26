import requests, bs4, re, csv, urllib.parse
 
        
def get_contestant_data(first_season,last_season):

    urls = ["https://en.wikipedia.org/wiki/RuPaul%27s_Drag_Race_season_{}",
           #"https://en.wikipedia.org/wiki/RuPaul's_Drag_Race_All_Stars_season_{}", needs different logic, todo
           "https://en.wikipedia.org/wiki/RuPaul%27s_Drag_Race_UK_series_{}",
           "https://en.wikipedia.org/wiki/Canada's_Drag_Race_season_{}",
           "https://en.wikipedia.org/wiki/Drag_Race_Belgique_season_{}",
           "https://en.wikipedia.org/wiki/RuPaul%27s_Drag_Race_Down_Under_season_{}",
           "https://en.wikipedia.org/wiki/Drag_Race_Espa%C3%B1a_season_{}",
           "https://en.wikipedia.org/wiki/Drag_Race_Italia_season_{}",
           "https://en.wikipedia.org/wiki/Drag_Race_Brasil_season_{}",
           "https://en.wikipedia.org/wiki/Drag_Race_Philippines_season_{}",
           "https://en.wikipedia.org/wiki/Drag_Race_Germany_season_{}",
           "https://en.wikipedia.org/wiki/Drag_Race_M%C3%A9xico_season_{}",
           "https://en.wikipedia.org/wiki/Drag_Race_France_season_{}",
           "https://en.wikipedia.org/wiki/Drag_Race_Thailand_season_{}",
           "https://en.wikipedia.org/wiki/Drag_Race_Sverige"]
    
    contestant_data = []
    contestant_data_header = ['contestant_name', 'contestant_govt_name', 'contestant_season', 'contestant_franchise', 'contestant_dob', 'contestant_age_at_airing', 'contestant_town', 'contestant_region', 'contestant_position', 'contestant_entrance_position']
    contestant_data.append(contestant_data_header)

    for url in urls:
    
        for num in range(1,17): # because there are no more than 16 seasons of any franchise at this time
            scrape_url = url.format(num)
            request = requests.get(scrape_url)
            
            if request.status_code == 200: 
                soup = bs4.BeautifulSoup(request.text, 'html.parser')
                queen_data = soup.find_all('table',{'class': 'wikitable sortable'}) # get the table with the queens in
                if queen_data:
                    queen_data = queen_data[0] # reassign queen_table to the first item in the queen_data list, so we can treat it like a bs4 object rather than a list
                    rows = queen_data.find_all('tr') # get all the rows which contain the queen data
                    rows.pop(0) # first row is just headers
            
                    for row_num, row in enumerate(rows): # have to do this to keep track of rows in order to handle merged cells, see phiphi ohara who doesn't have a cell [2]
                    # create a separate list for each queen
                        queen = []
                        queen_names = row.select('th')
                        queen_name = queen_names[0].text.strip('\n')
                        queen_remaining_data = row.find_all('td') # all the other data is within a td rather than th
                        queen_govt_name = ''
                        queen_season = num
                        # get the queen franchise from the url because it is inconsistently present in the infobox data
                        match = re.search(r'/wiki/(.*?)(?=_season|_series|\{\}|$)',url)
                        if match:
                            franchise = match.group(1)
                            franchise = urllib.parse.unquote(franchise)
                            queen_franchise = franchise.replace("_", " ")
                        queen_dob = ''
                        queen_entrance_position = ''
                
                        for td in queen_remaining_data:
                            queen_age_at_airing = queen_remaining_data[0].text.strip('\n').lower()
                            queen_location = queen_remaining_data[1].text.strip('\n').split(',')
                            queen_town = queen_location[0]
                            try:
                                queen_region = queen_location[1].lstrip(' ')
                            except IndexError:
                                queen_region = queen_location[0]
                            try:
                                queen_position = queen_remaining_data[2].text.strip("\n").lower()
                            except IndexError:
                                queen_position = queen_position # use the last known queen position
                            if 'runners-up' in queen_position:
                                queen_position = 'runner-up'
                        
                        # append all the above to the queen list
                        queen.extend([queen_name, queen_govt_name, queen_season, queen_franchise, queen_dob, queen_age_at_airing, queen_town, queen_region,queen_position, queen_entrance_position])

                        # append the queen to the contestant_data
                        contestant_data.append(queen)
                    
                else:
                    continue
            else:
                continue
            if 'Sverige' in url: # because the sverige url doesn't follow the same format, so we need to break out of the loop 
                break

            # clean up contestant_data for any odd characters like [a], [b] etc

            for i, queen in enumerate(contestant_data): # need to use enumerate() to keep track of the index so the list can be updated
                for j, list_item in enumerate(queen):
                    for match in re.finditer(r'\[\w\]$',str(list_item)): 
                        contestant_data[i][j] = re.sub(r'\[\w\]$', '', list_item) # substitue the pattern match with an empty string
                
    return contestant_data

def write_to_csv(contestant_data):
    file = open('contestant_data_test_multiple.csv', mode='w', newline='',encoding='utf-8')
    csv_writer = csv.writer(file,delimiter=',')
    for row in contestant_data:
        csv_writer.writerow(row)
    file.close()
    
if __name__ == '__main__':
    contestant_data = get_contestant_data(1,17)
    write_to_csv(contestant_data)
