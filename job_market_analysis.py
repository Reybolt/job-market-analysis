"""
    Job Market Analysis

    I want to investigate what the current job market looks like
    for a software developer across different cities in order
    to help determine whether my current skill set matches
    the market.

    Note: We are retrieving all keywords but just select ones.

    Author: Reynaldo Arteaga 2020
"""

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd


def fetch_data_from_url(url):
    """
    Given a URL fetch the html.

    Args:
        url (str): Link to page we want to scrape.

    Returns:
        soup (BeautifulSoup): BeautifulSoup object of a website page.
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup


def fetch_element_by_id(soup, element_id):
    """
    Given the html of page, select a specific element.
    Args:
        soup (BeautifulSoup): BeautifulSoup object of a website page.
        element_id (str): The element ID of the html we want to investigate.

    Returns:
        results (BeautifulSoup.element.Tag): Html tag data for specific
                                             element.
    """
    results = soup.find(id=element_id)
    return results


def get_number_of_jobs(url, element_id):
    """
    Retrieve number of jobs from website.

    Args:
        url (str): Link to page we want to scrape.
        element_id (str): The element ID of the html we want to investigate.

    Returns:
        number_of_pages (int): Number of pages this job search has.
    """

    if url is None or element_id is None:
        return 0

    soup = fetch_data_from_url(url)
    html = fetch_element_by_id(soup, element_id)

    if not html:
        return 0

    # Remove empty spaces.
    html = html.text.strip()

    # Extract number of pages from html
    number_of_pages = html.split("of ", 1)[1].split(" jobs", 1)[0]
    number_of_pages = int(number_of_pages)

    return number_of_pages


def create_url(website, data, filter):
    """
    Create the URL we will search on.

    Args:
        website (str, enum): The company website we are searching on.
            - indeed
        data (dict): Data we require to seach
            {
                'city': 'fake_city',
                'province': 'fake_province',
                'filters': list of dicts.
                    For each dict, each key is the search filter and the value
                    corresponds to whether it is included or not.
            }
        filter (dict): The specific filters for this search.

    Returns:
        url, element_id, all_filters (tuple):
            url (str) The full URL we are requesting.
            element_id (str): The element ID we require for this particular
                              website.
            all_filters (str): Formatted filters used when presenting the
                               results.
    """
    if website == 'indeed':
        url, all_filters = create_indeed_url(website, data, filter)
        element_id = 'searchCountPages'
    else:
        # We don't handle this website yet.
        url = None
        element_id = None
        all_filters = None

    return url, element_id, all_filters


def create_indeed_url(website, data, filter):
    """
    Create URL for indeed website.

    Assumption: Job type is not configurable.

    Args:
        website (str, enum): The company website we are searching on.
            - indeed
        data (dict): Data we require to seach
            {
                'city': 'fake_city',
                'province': 'fake_province',
                'filters': list of dicts.
                    For each dict, each key is the search filter and the value
                    corresponds to whether it is included or not.
            }
        filter (dict): The specific filters for this search.

    Returns:
        format_url, all_filters (tuple):
            format_url (str) The full URL we are requesting.
            all_filters (str): Formatted filters used when presenting the
                               results.
    """
    base_url = 'https://ca.indeed.com/jobs?q=software+developer{}'

    all_filters = ''
    for filter_name, value in filter.items():
        if value:
            all_filters += '+' + filter_name
        else:
            all_filters += '+-' + filter_name

    format_url = base_url.format(all_filters)

    # Insert location data if requested
    city = data.get('city', '')
    province = data.get('province', '')
    if city != '' and province != '':
        location_base = '&l={}%2C+{}'
        format_url += location_base.format(city, province)
    return format_url, all_filters


def get_job_market_breakdown(data):
    """
    Get job market breakdown for Software Developers

    Args:
        data (list of dict): Job search data. Each item consists of:
            {
                'city': 'fake_city',
                'province': 'fake_province',
                'filters': list of dicts.
                    For each dict, each key is the search filter and the value
                    corresponds to whether it is included or not.
            }
    """
    # Data
    website = 'indeed'

    result = {}
    for d in data:
        # Get site details
        for filter in d.get('filters', {}):
            URL, element_id, all_filters = create_url(website, d, filter)
            if (
                URL is None or
                element_id is None
                or all_filters is None
            ):
                continue
            number_of_jobs = get_number_of_jobs(URL, element_id)
            if result.get(d['city']):
                result[d['city']][all_filters] = number_of_jobs
            else:
                result[d['city']] = {all_filters: number_of_jobs}

    return result


def plot_results(data):
    """Plot results for visual ease."""
    df = pd.DataFrame.from_dict(data)
    df.plot(kind='bar')

    # Keep plot open for viewing.
    plt.show(block=True)


if __name__ == '__main__':

    filters = [
        {'Django': True},
        {'Golang': True},
        {'Machine Learning': True},
        {'Jenkins': True},
        {'API': True},
        {'C++': True},
        {'C': True},
        {'C++': True, 'C': True},
        {'Python': True},
        {'Javascript': True},
        {'Python': True, 'Javascript': True},
        {'SQL': True},
        {'Postgresql': True},
        {'SQL': True, 'Postgresql': True},
        {'AWS': True},
        {'Azure': True},
        {'AWS': True, 'Azure': True},
        {'Agile': True},
        {'React': True},
        {'Angular': True},
        {'Vue': True},
        {'Node': True},
    ]

    data = [
        {
            'city': 'Ottawa',
            'province': 'ON',
            'filters': filters,
        },
        {
            'city': 'Vancouver',
            'province': 'BC',
            'filters': filters,
        },
        {
            'city': 'Halifax',
            'province': 'NS',
            'filters': filters,
        },
    ]

    result = get_job_market_breakdown(data)
    print(result)

    plot_results(result)
