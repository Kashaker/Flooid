import universities as uni
import general
import boskalis
import os


if __name__ == '__main__':
    path_to_results = 'export/'
    source_partners = 'partners.xlsx'

    if not os.path.exists(path_to_results):
        os.makedirs(path_to_results)

    general = general.GeneralWebScraper(source_partners, path_to_results)
    boskalis = boskalis.BoskalisWebScraper(path_to_results)

    tudelft_scraper = uni.TUDelftWebScraper([2019, 2020], path_to_results)
    fontys_scraper = uni.FontysWebScraper(path_to_results)
    buas_scraper = uni.BuasWebScraper(['2019', '2020', '2021'], path_to_results)

    general.export()
    boskalis.export()

    tudelft_scraper.export_projects()
    fontys_scraper.export_projects()
    buas_scraper.export_projects()




