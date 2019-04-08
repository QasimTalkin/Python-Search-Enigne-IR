from .PreprocessingBase import PreprocessingBase
from bs4 import BeautifulSoup
import requests
import json
import re
from utilities import tokenize_sentence

# Module 1 - Preprocessing


class UOPreprocessing(PreprocessingBase):
    """Preprocesses the UO course collection by making an HTTP request, and then scraping it using beautiful soup

    The webscraping code was modfied from https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
    """

    def __init__(self):
        super().__init__()
        self.url = 'https://catalogue.uottawa.ca/en/courses/csi/'

    def preprocess_collections(self):
        """Preprocessing the UO collection

            Process goes as follows:
            - Makes a request to the UO Course site
            - Initialize Beautfiul Soup
            - Use beautiful Scrape the "course block" sections that make up each course
            - Save all scraped information in a NamedTuple described in PreprocessingBase.py
            - Transform list of tuples into list of dicts
            - Write list into a json file
        """
        try:
            results = requests.get(self.url)
            results.raise_for_status()
        except requests.exceptions.RequestException as r:
            print(r)
            print(f"Can't make get request with this URL: {self.url}")
            raise

        soup = BeautifulSoup(results.text, 'html.parser')
        courseblocks = soup.find_all('div', attrs={'class': 'courseblock'})

        for index, courseblock in enumerate(courseblocks, 1):
            course_title = courseblock.find(
                'p', attrs={'class': 'courseblocktitle'}).text
            course_description = courseblock.find(
                'p', attrs={'class': 'courseblockdesc'})
            course_excerpt = tokenize_sentence(course_description.text.strip())[
                0] if course_description is not None else ''
            new_document = self.Document(
                f'CSI-{index}', re.sub('\(.*?\)', '', course_title), course_description.text.strip() if course_description is not None else '', course_excerpt, "UO Courses")
            self.uniform_collections.append(new_document)

        # Since an error will be raised when I try to write the Document NamedTuples to the json file
        # we use the _asdict() method to transform each tuple into a dict
        # Modified from https://stackoverflow.com/questions/5906831/serializing-a-python-namedtuple-to-json, from benselme's answer
        uniform_dicts = [uniform_collection._asdict()
                         for uniform_collection in self.uniform_collections]

        with open('corpus.json', 'w') as outfile:
            json.dump(uniform_dicts, outfile, ensure_ascii=False, indent=4)
