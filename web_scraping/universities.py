import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
import logging


class TUDelftWebScraper:
    """
    Web scraper for university "TU Delft"
    """

    __projects_url = 'https://www.tudelft.nl/en/innovatie-impact/ontwikkeling-innovatie/innovation-projects?lookup[254940][filter][51][]='

    def __init__(self, years, path_to_results):
        """
        Creates the instance of web scraper for university "TU Delft"
        :param years: List of years from which projects should be web scraped
        :param path_to_results: Path to the folder where the results should be
        """
        self.years = years
        self.path_to_results = path_to_results + '/TUDelft_projects/'

        if not isinstance(years, list):
            print('[TU Delft Web Scraper] Years should be provided as a list!')

    def export_projects(self):
        """
        Exports web scraped projects to .txt files
        :return: None
        """
        project_links = []

        if not os.path.exists(self.path_to_results):
            os.makedirs(self.path_to_results)

        # Iterating through pages with projects from each given year
        for year in self.years:
            url = f'{self.__projects_url}{year}'

            try:
                r = requests.get(url)
            except requests.exceptions.ConnectionError:
                print(f'[TU Delft Web Scraper] Error for page <{url}>: connection refused!')
                logging.exception(f'[TU Delft Web Scraper] Error for page <{url}>: connection refused!')
                continue
            except Exception as e:
                print(f'[TU Delft Web Scraper] Error for page {url}: {e}.')
                logging.exception(f'[TU Delft Web Scraper] Error for page {url}: {e}.')
                continue

            try:
                soup = BeautifulSoup(r.content, 'html.parser')

                # Looking for button 'Last page'
                button_lst_page = soup.find('a', attrs={'aria-label': 'Last page'})

                # If page has button 'Last page'
                if button_lst_page:
                    pos = button_lst_page.get('href').find('Page%5D=')

                    # Find the number of last page
                    last_page = int(button_lst_page.get('href')[pos+8])

                    # Iterating through all pages till the last one
                    for i in range(1, last_page+1):
                        r = requests.get(f'{self.__projects_url}{year}&tx_lookup_results[page-254940][currentPage]={i}')
                        soup = BeautifulSoup(r.content, 'html.parser')
                        a_tags = soup.find_all('a')

                        # Adding links with projects
                        for a_tag in a_tags:

                            # Checking if link refers to project
                            if '/en/innovatie-impact/ontwikkeling-innovatie/innovation-projects/' in a_tag.get('href'):
                                project_links.append('https://www.tudelft.nl' + a_tag.get('href'))

                # If current page is last
                else:
                    a_tags = soup.find_all('a')

                    # Adding links with projects
                    for a_tag in a_tags:

                        # Checking if link refers to project
                        if '/en/innovatie-impact/ontwikkeling-innovatie/innovation-projects/' in a_tag.get('href'):
                            project_links.append('https://www.tudelft.nl' + a_tag.get('href'))

            except Exception as e:
                print(f'[TU Delft Web Scraper] Error while extracting project links from page <{url}>: {e}.')
                logging.exception(f'[TU Delft Web Scraper] Error while extracting project links from page <{url}>: {e}.')

        # Iterating through links from list
        for link in project_links:
            try:
                r = requests.get(link)
            except requests.exceptions.ConnectionError:
                print(f'[TU Delft Web Scraper] Error for page <{link}>: connection refused!')
                logging.exception(f'[TU Delft Web Scraper] Error for page <{link}>: connection refused!')
                continue
            except Exception as e:
                print(f'[TU Delft Web Scraper] Error for page {link}: {e}.')
                logging.exception(f'[TU Delft Web Scraper] Error for page {link}: {e}.')
                continue

            try:
                soup = BeautifulSoup(r.content, 'html.parser')

                # Getting project title
                title = soup.find('h2').text.replace('/', '').replace('\n', '')

                # Getting project content
                content = soup.find_all('div', attrs={'class': 'sm-12 md-6'})[1]

                with open(self.path_to_results + f'{title}.txt', 'wt') as f:
                    f.write(f'Title: {title} \n')

                    # If project content is not empty
                    if content:
                        f.write(content.get_text(' '))
                with open(self.path_to_results + 'Projects.txt', 'a+') as f1:
                    f1.write(title + '\n')

            except Exception as e:
                print(f'[TU Delft Web Scraper] Error while scraping page <{link}>: {e}.')
                logging.exception(f'[TU Delft Web Scraper] Error while scraping page <{link}>: {e}.')

        print(f'[TU Delft Web Scraper] {len(project_links)} projects were scraped.')
        logging.info(f'[TU Delft Web Scraper] {len(project_links)} projects were scraped.')


class FontysWebScraper:
    """
    Web scraper for university "Fontys"
    """

    __projects_url = 'https://fontys.nl/Onderzoek/High-Tech-Systems-and-Materials/SmartMan/Student-Projects.htm'

    def __init__(self, path_to_results):
        """
        Creates the instance of web scraper for university "Fontys"
        :param path_to_results: Path to the folder where the results should be
        """
        self.path_to_results = path_to_results + '/Fontys_projects/'

    def export_projects(self):
        """
        Exports web scraped projects to .txt files
        :return: None
        """
        project_links = []

        if not os.path.exists(self.path_to_results):
            os.makedirs(self.path_to_results)

        try:
            r = requests.get(self.__projects_url)
        except requests.exceptions.ConnectionError:
            print(f'[Fontys Web Scraper] Error for page <{self.__projects_url}>: connection refused!')
            logging.exception(f'[Fontys Web Scraperr] Error for page <{self.__projects_url}>: connection refused!')
            return
        except Exception as e:
            print(f'[Fontys Web Scraper] Error for page {self.__projects_url}: {e}.')
            logging.exception(f'[Fontys Web Scraper] Error for page {self.__projects_url}: {e}.')
            return

        try:
            soup = BeautifulSoup(r.content, 'html.parser')
            a_tags = soup.find_all('a')

            # Adding links with projects
            for a_tag in a_tags:

                # Checking if link refers to project
                if '/SmartMan/Student-Projects/' in a_tag.get('href'):
                    project_links.append('https://fontys.nl/' + a_tag.get('href'))

        except Exception as e:
            print(f'[Fontys Web Scraper] Error while extracting projects\' links: {e}.')
            logging.exception(f'[Fontys Web Scraper] Error while extracting projects\' links: {e}.')

        # Iterating through links from list
        for link in project_links:
            try:
                r = requests.get(link)
            except requests.exceptions.ConnectionError:
                print(f'[Fontys Web Scraper] Error for page <{link}>: connection refused!')
                logging.exception(f'[Fontys Web Scraperr] Error for page <{link}>: connection refused!')
                continue
            except Exception as e:
                print(f'[Fontys Web Scraper] Error for page {link}: {e}.')
                logging.exception(f'[Fontys Web Scraper] Error for page {link}: {e}.')
                continue

            try:
                soup = BeautifulSoup(r.content, 'html.parser')

                # Getting project title
                title = soup.find('h1').text.replace('/', '').replace('\n', '')

                # Getting project content
                content = soup.find('div', attrs={'class': 'columns small-12 medium-6 large-6 frd_column'})

                # Getting project additional info
                additional_info = soup.find_all('div', attrs={'class': 'columns small-12 large-4 frd_column'})

                with open(self.path_to_results + f'{title}.txt', 'wt') as f:
                    f.write(f'Title: {title} \n')

                    # If project content is not empty
                    if content:
                        f.write(content.get_text(' '))

                    # If project additional info is not empty
                    if additional_info:
                        for elem in additional_info:
                            f.write(elem.get_text(' '))
                with open(self.path_to_results + 'Projects.txt', 'a+') as f1:
                    f1.write(title + '\n')

            except Exception as e:
                print(f'[Fontys Web Scraper] Error while scraping page <{link}>: {e}.')
                logging.exception(f'[Fontys Web Scraper] Error while scraping page <{link}>: {e}.')

        print(f'[Fontys Web Scraper] {len(project_links)} projects were scraped.')
        logging.info(f'[Fontys Web Scraper] {len(project_links)} projects were scraped.')


class BuasWebScraper:
    """
    Web scraper for university "Breda University of Applied Sciences"
    """

    __projects_url = 'https://pure.buas.nl/en/projects/'

    def __init__(self, years, path_to_results):
        """
        Creates the instance of web scraper for university "BUAS"
        :param years: List of years from which projects should be web scraped
        :param path_to_results: Path to the folder where the results should be
        """
        self.years = years
        self.path_to_results = path_to_results + '/BUAS_projects/'

        if not isinstance(years, list):
            print('[BUAS Web Scraper] Years should be provided as a list!')

    def export_projects(self):
        """
        Exports web scraped projects to .txt files
        :return: None
        """

        project_links = []

        if not os.path.exists(self.path_to_results):
            os.makedirs(self.path_to_results)

        # The format of url for page with projects depends on number of years given
        if len(self.years) > 1:
            url = self.__projects_url
            url += '?format='

            # Url is expanding
            for year in self.years:
                url += f'&projectStartYear={year}'
        else:
            url = f'{self.__projects_url}?format=&projectStartYear={self.years[0]}'

        try:
            driver = webdriver.Safari()
            driver.get(f'{url}')
            html = driver.page_source
        except Exception as e:
            print(f'[BUAS Web Scraper] Error for page {url}: {e}.')
            logging.exception(f'[BUAS Web Scraper] Error for page {url}: {e}.')
            return

        try:
            soup = BeautifulSoup(html, 'html.parser')
            li_tags = soup.find_all('li', attrs={'class': 'next'})

            # If page contains pagination
            if len(li_tags) != 0:
                i = 0
                while True:
                    driver.get(f'{url}&page={i}')
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    li_tags = soup.find_all('li', attrs={'class': 'next'})
                    a_tags = soup.find_all('a', attrs={'class': 'link', 'rel': 'UPMProject'})

                    # Adding links with projects
                    for a_tag in a_tags:

                        # Checking if link refers to project
                        if '/en/projects/' in a_tag.get('href'):
                            project_links.append(a_tag.get('href'))

                    # If all links were extracted (no button 'Next page')
                    if len(li_tags) == 0:
                        break
                    i += 1

            # If page doesn't contain pagination
            else:
                a_tags = soup.find_all('a', attrs={'class': 'link', 'rel': 'UPMProject'})

                # Adding links with projects
                for a_tag in a_tags:

                    # Checking if link refers to project
                    if '/en/projects/' in a_tag.get('href'):
                        project_links.append(a_tag.get('href'))
        except Exception as e:
            print(f'[BUAS Web Scraper] Error while extracting project links from page <{url}>: {e}.')
            logging.exception(f'[BUAS Web Scraper] Error while extracting project links from page <{url}>: {e}.')

        # Iterating through links from list
        for link in project_links:
            try:
                r = requests.get(link)
            except requests.exceptions.ConnectionError:
                print(f'[BUAS Web Scraper] Error for page <{link}>: connection refused!')
                logging.exception(f'[BUAS Web Scraper] Error for page <{link}>: connection refused!')
                continue
            except Exception as e:
                print(f'[BUAS Web Scraper] Error for page {link}: {e}.')
                logging.exception(f'[BUAS Web Scraper] Error for page {link}: {e}.')
                continue

            try:
                soup = BeautifulSoup(r.content, 'html.parser')

                # Getting project title
                title = soup.find('h1').text.replace('/', '').replace('\n', '')

                # Getting project content
                content = soup.find('div', attrs={'class': 'projectdescription'})

                # Getting project authors
                persons = '\n'.join([e.text.replace('(PI)', '').replace('(CoI)', '') for e in soup.find_all('ul', attrs={'class': 'relations persons'})])

                # Getting project keywords
                keywords = ', '.join([e.text for e in soup.find_all('li', attrs={'class': 'userdefined-keyword'})])

                with open(self.path_to_results + f'{title}.txt', 'wt') as f:
                    f.write(f'Title: {title} \n')

                    # If project content is not empty
                    if content:
                        f.write(content.get_text(' ') + '\n')

                    # If project persons is not empty
                    if persons:
                        f.write(f'Persons: {persons} \n')

                    # If project keywords is not empty
                    if keywords:
                        f.write(f'Keywords: {keywords} \n')
                with open(self.path_to_results + 'Projects.txt', 'a+') as f1:
                    f1.write(title + '\n')

            except Exception as e:
                print(f'[BUAS Web Scraper] Error while scraping page <{link}>: {e}.')
                logging.exception(f'[BUAS Web Scraper] Error while scraping page <{link}>: {e}.')

        driver.close()
        print(f'[BUAS Web Scraper] {len(project_links)} projects were scraped.')
        logging.info(f'[BUAS Web Scraper] {len(project_links)} projects were scraped.')



