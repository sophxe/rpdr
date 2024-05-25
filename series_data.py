def get_drag_race_titles_all():

    import requests, bs4, csv
    # url will need updating depending on franchise
  
    url = "https://en.wikipedia.org/wiki/RuPaul's_Drag_Race_season_{}" 
    episode_info = []

    # loop through each series - num will need updating depending on how many seasons are within a franchise
    for num in range(1,17):
        scrape_url = url.format(num)
        request = requests.get(scrape_url)
        soup = bs4.BeautifulSoup(request.text, 'lxml')
        episode_name = soup.select('.wikiepisodetable .summary')
        episode_air_date = soup.select('.wikiepisodetable .bday.dtstart.published.updated.itvstart')
        for number in range(0,len(episode_name)):
            # return everything between"
            episode_number = number + 1
            episode_information = f"{str(num+53)},{episode_number},{episode_air_date[number].text},{episode_name[number].text[1:-1]}"
            episode_info.append(episode_information)
  
    # print resulting data - for testing purposes
    for episode in episode_info:
        print(episode)
        
  # write resulting data into csv  
    with open('episode_data_us.csv', 'w', encoding='utf-8') as file:
        header = ['series_key', 'episode_number', 'episode_date', 'episode_name']
        file_writer = csv.writer(file)
        file_writer.writerow(item for item in header)
        for episode in episode_info:
            if episode.strip():
                episode_row = episode.split(',')
                file_writer.writerow(episode_row)

# run script
if __name__ == "__main__":
    get_drag_race_titles_all()
