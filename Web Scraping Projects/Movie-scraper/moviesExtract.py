import requests
from bs4 import BeautifulSoup
from customLogger import custom_logger_class


custom_logger_obj = custom_logger_class("moviesScraping.log", __name__)
custom_logger=custom_logger_obj.create_custom_logger()


class movies_extract_class:

    def fetch_list_of_movies(self):
        list_of_movies = []
        for page in range(1,4):
            try:
                url = ("https://www.imdb.com/list/ls055265443/?st_dt=&mode=detail&page="
                       +str(page) 
                       +"&sort=release_date,desc")
                custom_logger.info("Connecting to IMDB website")
                page = requests.get(url)
                custom_logger.info("Conncetion Established")
            except Exception as e:
                custom_logger.error(str(e))

            try:
                custom_logger.info("Parsing page content")
                soup = BeautifulSoup(page.content,"html.parser")
                custom_logger.info("Parsing completed")
                custom_logger.info("Finding boxes")
                boxes = soup.find_all("div", class_ = "lister-item mode-detail")
                custom_logger.info("Finding of boxes is completed")
            except Exception as e:
                custom_logger.error(str(e))

            for box in boxes:
                try:
                    movie_dictionary = {}
                    box_content = box.find("div", class_ = "lister-item-content")
                    header = box_content.find("h3", class_ ="lister-item-header")
                    custom_logger.info("Scraping title")
                    title = header.find("a").text
                    movie_dictionary["title"] = title
                    custom_logger.info("Title scraped")
                    custom_logger.info("Scraping year of release")
                    year_of_release = header.find_all("span")[1].text.replace("(","").replace(")","").replace("I","").strip()
                    movie_dictionary["year_of_release"]=year_of_release
                    custom_logger.info("Year of Release scraped")
                except Exception as e:
                    custom_logger.error(str(e))

                try:
                    duration_genre = box_content.find_all("p", class_ = "text-muted text-small")[0]
                    custom_logger.info("Scraping duration")
                    duration = duration_genre.find("span", class_ = "runtime").text
                    movie_dictionary["duration"]=duration
                    custom_logger.info("Duration scraped")
                    custom_logger.info("Scraping genre")
                    genre = duration_genre.find("span", class_ = "genre").text.replace("\n", "").strip()
                    movie_dictionary["genre"] = genre
                    custom_logger.info("Genre scraped")
                except Exception as e:
                    custom_logger.error(str(e))

                try:
                    rating_widget = box_content.find("div", class_ = "ipl-rating-widget")
                    rating_section = rating_widget.find("div", class_ = "ipl-rating-star small")
                    custom_logger.info("Scraping rating")
                    rating = rating_section.find("span", class_ = "ipl-rating-star__rating").text
                    movie_dictionary["rating"] = rating
                    custom_logger.info("Rating scraped")
                    custom_logger.info("Scraping description")
                    description = box_content.find_all("p")[1].text.replace("\n", "").strip()
                    movie_dictionary["description"] = description
                    custom_logger.info("Description scraped")
                except Exception as e:
                    custom_logger.error(str(e))

                try:
                    directors_casts = box_content.find_all("p")[2].text.replace("\n", "").strip()
                    custom_logger.info("Scraping directors")
                    directors = directors_casts.split("|")[0].strip().split(":")[1]
                    movie_dictionary["directors"] = directors
                    custom_logger.info("Directors scraped")
                    custom_logger.info("Scraping casts")
                    casts = directors_casts.split("|")[1].strip().split(":")[1]
                    movie_dictionary["casts"] = casts
                    custom_logger.info("Casts scraped")
                except Exception as e:
                    custom_logger.error(str(e))

                try:
                    image_section = box.find("div", class_ = "lister-item-image ribbonize").find("a")
                    movie_image = image_section.find("img")
                    custom_logger.info("Scraping Image_URL")
                    image_url = movie_image.attrs["loadlate"]
                    movie_dictionary["image_url"] = image_url
                    custom_logger.info("Image_URL scraped")
                    list_of_movies.append(movie_dictionary)
                    custom_logger.info("All the movies have been fetched")
                except Exception as e:
                    custom_logger.error(str(e))
        return list_of_movies
            


