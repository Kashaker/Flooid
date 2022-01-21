import pandas as pd
import requests
import logging
from bs4 import BeautifulSoup
import os
from selenium import webdriver


class GeneralWebScraper:
    """
    General web scraper for partners' websites.
    """
    # Configuring file for logs
    logging.basicConfig(filename='app.log',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        datefmt='%d.%m.%Y %H:%M:%S')

    # Some of websites may not allow web scraping via BS4
    problemed_organizations = ['Van Oord', 'Chronosphere']

    def __init__(self, source, path_to_results):
        """
        Creates the instance of general web scraper
        :param source: File with list of websites. The format should be xlsx or csv
        :param path_to_results: Path to the folder where the results should be
        """

        self.source = source
        self.path_to_results = path_to_results

        if not any(map(lambda x: x in source, ['xlsx', 'csv'])):
            print('[General Web Scraper] Wrong input file format: should be .xlsx or .csv!')
            logging.error('[General Web Scraper] Wrong input file format: should be .xlsx or .csv!')

    def export(self):
        """
        Exports web scraped content to .txt files
        :return: None
        """

        if not os.path.exists(self.path_to_results):
            os.makedirs(self.path_to_results)

        # Reading data from excel file
        try:
            partners = pd.read_excel(self.source)
        except Exception as e:
            print(f'[General Web Scraper] Error while reading source file: {e}.')
            logging.exception(f'[General Web Scraper] Error while reading source file: {e}.')
            return

        # Setting conditions for language of websites
        condition_en = partners["Language"] == "EN"

        websites_result = partners[["Organization", "Page", "Language"]]
        websites_result = websites_result[condition_en]

        # Print out number of filtered websites
        print(f'[General Web Scraper] {len(websites_result)} websites were filtered.')
        logging.info(f'[General Web Scraper] {len(websites_result)} websites were filtered.')

        # Iterating through filtered websites
        for organization, page, language in websites_result.itertuples(index=False):
            # Getting the whole html page
            try:
                r = requests.get(page)
            except requests.exceptions.ConnectionError:
                print(f'[General Web Scraper] Error for page <{page}>: connection refused!')
                logging.exception(f'[General Web Scraper] Error for page <{page}>: connection refused!')
                continue
            except Exception as e:
                print(f'[General Web Scraper] Error for page {page}: {e}.')
                logging.exception(f'[General Web Scraper] Error for page {page}: {e}.')
                continue

            path_to_save = self.path_to_results + language + '/' + organization + '/'

            # If it's first page from current organization
            if not os.path.exists(path_to_save):
                i = 1
                os.makedirs(path_to_save)

            # If response is 200
            if r.status_code == 200 and organization not in self.problemed_organizations:
                soup = BeautifulSoup(r.content, "html.parser")
                try:
                    i = 1
                    # Creating .txt file and appending the result
                    if language == 'EN':
                        with open(path_to_save + organization + '_' + str(i) + '.txt', 'wt') as f:
                            f.write(soup.get_text(" "))

                    print(f'[General Web Scraper] <{organization}>: {page} was scraped successfully.')
                    logging.info(f'[General Web Scraper] <{organization}>: {page} was scraped successfully.')
                    i += 1

                except Exception as e:
                    print(f'[General Web Scraper] <{organization}>: {page} wasn\'t scraped: {e}.')
                    logging.exception(f'[General Web Scraper] <{organization}>: {page} wasn\'t scraped: {e}.')

            # If website doesn't allow web scraping via BS4 and requests
            elif r.status_code == 403 or organization in self.problemed_organizations:
                driver = webdriver.Safari()
                driver.get(page)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                try:
                    # Creating .txt file and appending the result
                    if language == 'EN':
                        with open(path_to_save + organization + '_' + str(i) + '.txt', 'wt') as f:
                            f.write(soup.get_text(' '))

                    print(f'[General Web Scraper] <{organization}>: {page} was scraped successfully')
                    logging.info(f'[General Web Scraper] <{organization}>: {page} was scraped successfully')
                    i += 1
                    driver.close()

                except Exception as e:
                    print(f'[General Web Scraper] <{organization}>: {page} wasn\'t scraped: {e}.')
                    logging.exception(f'[General Web Scraper] <{organization}>: {page} wasn\'t scraped: {e}.')

            # If something went wrong
            else:
                print(f'[General Web Scraper] <{organization}>: {page} wasn\'t scraped due Error {r.status_code}.')
                logging.error(f'[General Web Scraper] <{organization}>: {page} wasn\'t scraped due Error {r.status_code}.')

