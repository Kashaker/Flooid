import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import logging


class BoskalisWebScraper:
    """
    Web scraper for organization "Boskalis"
    """
    # Configuring file for logs
    logging.basicConfig(filename='app.log',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        datefmt='%d.%m.%Y %H:%M:%S')

    __projects_url = 'https://boskalis.com/about-us/projects.html#view/list/page'

    def __init__(self, path_to_results):
        """
        Creates the instance of web scraper for organization "Boskalis"
        :param path_to_results: Path to the folder where the results should be
        """
        self.path_to_results = path_to_results + '/Boskalis/'

    def export(self):
        """
        Exports web scraped content to .txt files
        :return: None
        """
        project_links = []
        if not os.path.exists(self.path_to_results):
            os.makedirs(self.path_to_results)

        # Finding all links with projects within page with pagination
        for i in range(1, 30):
            project_links.extend(self.find_links(f'{self.__projects_url}/{i}'))

        # Iterating through unique links from list
        for link in set(project_links):
            try:
                r = requests.get(link)
            except requests.exceptions.ConnectionError:
                print(f'[Boskalis Web Scraper] Error for page <{link}>: connection refused!')
                logging.exception(f'[Boskalis Web Scraper] Error for page <{link}>: connection refused!')
                continue
            except Exception as e:
                print(f'[Boskalis Web Scraper] Error for page {link}: {e}.')
                logging.exception(f'[Boskalis Web Scraper] Error for page {link}: {e}.')
                continue

            soup = BeautifulSoup(r.content, 'html.parser')

            try:
                # Getting project title
                title = soup.find('h1', attrs={'class': 'heading--section'}).text.replace('/', '').replace('\n', '')

                with open(self.path_to_results + f'{title}.txt', 'wt') as f:
                    f.write(soup.get_text(' '))
                with open(self.path_to_results + 'Projects.txt', 'a+') as f1:
                    f1.write(title)

            except Exception as e:
                print(f'[Boskalis Web Scraper] Project <{link}> wasn\'t scraped: {e}.')
                logging.exception(f'[Boskalis Web Scraper] Project <{link}> wasn\'t scraped: {e}.')

        print(f'[Boskalis Web Scraper] {len(set(project_links))} projects were scraped.')
        logging.info(f'[Boskalis Web Scraper] {len(set(project_links))} projects were scraped.')

    @staticmethod
    def find_links(url):
        """
        Finds all links with projects on given page
        :param url: URL for page with list of projects
        :return: list of links with projects
        """
        driver = webdriver.Safari()
        try:
            driver.get(url)
        except Exception as e:
            print(f'[Boskalis Web Scraper] Error while getting links from page <{url}>: {e}.')
            logging.exception(f'[Boskalis Web Scraper] Error while getting links from page <{url}>: {e}.')
            return

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        a_tags = soup.find_all('a', attrs={'target': '_top'})
        to_add = []

        try:
            for a_tag in a_tags:
                # Check if link refers to project
                if 'projects/' in str(a_tag.get('href')):
                    to_add.append((a_tag.get('href')))
        except Exception as e:
            print(f'[Boskalis Web Scraper] Error while extracting links from tags on page <{url}>: {e}.')
            return

        driver.close()
        return to_add
