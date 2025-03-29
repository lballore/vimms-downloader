from bs4 import BeautifulSoup
import os
from prettytable import PrettyTable
import py7zr
import re
from requests.models import Response
import requests
import sys
from typing import List
import urllib3
import zipfile

from src import models, helpers
from src.helpers import CONSOLES

urllib3.disable_warnings()

HOME_DIR = f'{os.path.dirname(os.path.abspath(__file__))}/..'


def get_rom_download_url(page_url: str) -> str:
    """Gets the Download ID for the a specific ROM from the ROMs page url"""
    download_id: str = ''
    try:
        page: Response = requests.get(page_url, verify=False)
        soup: BeautifulSoup = BeautifulSoup(page.content, 'html.parser')
        result = soup.find(id='dl_form')
        result = result.find(attrs={'name': 'mediaId'})
        download_id: str = result['value']
    except:
        e = sys.exc_info()[0]
        print('Failed on getting ROM ID')
        print(e)
    return f'{vimmslair_helper.VIMMS_LAIR_DL_BASE_URL}/?mediaId={download_id}'


def get_sub_section_letter_from_str(subsection: str) -> str:
    """Returns the subsection letter to get the downloaded ROM to the correct alphanumeric directory"""
    if '&section=number' in subsection.lower():
        return 'number'
    else:
        return subsection[-1]


def get_section_of_roms(section: str) -> List[models.ROM]:
    """Gets a section of ROM home page URIs from a system category"""
    roms: List[models.ROM] = []
    section_url: str = f'{vimmslair_helper.VIMMS_LAIR_BASE_URL}/vault/{section}'
    try:
        print('Getting a list of roms for the section: ' + section)
        page: Response = requests.get(section_url, verify=False)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find(
            'table',
            {'class': 'rounded centered cellpadding1 hovertable striped'})
        rows = table.find_all('tr')

        # For each row, find the first td and then find any <a> elements inside it
        for row in rows:
            # Get the first td in this row
            first_td = row.find('td')
            # If there is a first td (some rows might be header rows with th instead)
            if first_td:
                # Find all <a> elements in this td
                rom_a = first_td.find('a')
                name = rom_a.text
                page_url = vimmslair_helper.VIMMS_LAIR_BASE_URL + rom_a.get('href')
                download_url = get_rom_download_url(page_url)
                rom = models.ROM(name, page_url, download_url)
                roms.append(rom)
    except Exception as e:
        print(f'Failed on getting section of roms: {section}. The page may not contain any roms. Error: {str(e)}')
    return roms


def get_every_system_roms() -> List[models.BulkSystemROMS]:
    """Used in bulk mode to get the home page URI for every rom on all systems available"""
    all_roms: List[models.BulkSystemROMS] = []
    for i in range(0, len(CONSOLES)):
        selection: str = vimmslair_helper.get_selection_from_num(i)
        system_uri: str = vimmslair_helper.selection_to_uri(selection)
        system_roms: models.BulkSystemROMS = get_all_system_roms(system_uri, selection)
        all_roms.append(system_roms)
    return all_roms


def get_selected_system_bulk_roms(config: models.Config) -> List[models.BulkSystemROMS]:
    """Used in bulk mode to get the home page URI for every rom on a selected system"""
    selected_bulk: List[models.BulkSystemROMS] = []
    for i in config.selections:
        selection: str = vimmslair_helper.get_selection_from_num(i)
        system_uri: str = vimmslair_helper.selection_to_uri(selection)
        system_roms: models.BulkSystemROMS = get_all_system_roms(system_uri, selection)
        selected_bulk.append(system_roms)
    return selected_bulk


def get_all_system_roms(system: str, system_name: str) -> models.BulkSystemROMS:
    """Used in bulk mode to get the home page URI for every rom on a system"""
    print('Getting a list of roms for the ' + system)
    section_roms: List[models.SectionofROMs] = []
    section_urls: List[str] = [
        f'?p=list&system={system}&section=number', f'{system}/a',
        f'{system}/b', f'{system}/c', f'{system}/d', f'{system}/e',
        f'{system}/f', f'{system}/g', f'{system}/h', f'{system}/i',
        f'{system}/j', f'{system}/k', f'{system}/l', f'{system}/m',
        f'{system}/n', f'{system}/o', f'{system}/p', f'{system}/q',
        f'{system}/r', f'{system}/s', f'{system}/t', f'{system}/u',
        f'{system}/v', f'{system}/w', f'{system}/x', f'{system}/y',
        f'{system}/z'
    ]
    for x in section_urls:
        roms: List[models.ROM] = get_section_of_roms(x)
        section: models.SectionofROMs = models.SectionofROMs(x, roms)
        section_roms.append(section)
    system_roms: models.BulkSystemROMS = models.BulkSystemROMS(section_roms, system, system_name)
    return system_roms


def download_file(download_url: str, path: str) -> str:
    """Downloads one rom from the uri, stores it in the path and returns the filename"""
    x: int = 0
    filename: str = ''
    rom_id = download_url.split('/')[-1]
    while True:
        headers: dict[str, str] = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'User-Agent': vimmslair_helper.get_random_ua(),
            'Referer': f'{vimmslair_helper.VIMMS_LAIR_BASE_URL}/vault/{rom_id}',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate'
        }
        file: Response = requests.get(
            download_url,
            headers=headers,
            verify=False,
            allow_redirects=True
        )

        if file.status_code == 200:
            filename = file.headers['Content-Disposition']
            filenames: List[str] = re.findall(r'"([^"]*)"', filename)
            filename = filenames[0]
            full_path = os.path.join(path, filename)
            open(full_path, 'wb').write(file.content)
            print('Downloaded ' + filename + '!')
            break
        if x == 4:
            print(f'5 Requests made to {download_url} and failed')
            break
        if file.status_code != 200:
            x += 1
            continue
    return filename


def get_search_selection(config: models.Config) -> models.Config:
    """Gets search criteria for search mode"""
    search_selection: models.SearchSelection = models.SearchSelection()
    print('\nPlease select what system you want to search, or press Enter to do a general site wide search\n')
    helpers.print_console_list()
    while True:
        user_input: str = sys.stdin.readline()
        try:
            if user_input == '\n':
                search_selection.system = 'general'
                config.query.search_selections = search_selection
                break
            if not (int(user_input) > 17 or int(user_input) < 0):
                search_selection.system = \
                    helpers.get_selection_from_num(int(user_input))
                config.query.search_selections = search_selection
                break
            else:
                print('Not a selection')
                print('Please select a value from the list')
        except ValueError:
            print('Please select a value from the list')
            continue
    print('\nInput what rom you want to search for:')
    search_selection.query = sys.stdin.readline()
    return config


def get_search_section(search_selection: models.SearchSelection) -> List[models.ROM]:
    """Gets a section of roms using system search from the search selection"""
    roms: List[models.ROM] = []
    try:
        page = requests.get(vimmslair_helper.get_search_url(search_selection), verify=False)
        soup: BeautifulSoup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find(
            'table',
            {'class': 'rounded centered cellpadding1 hovertable striped'})
        rows = table.find_all('tr')
        # For each row, find the first td and then find any <a> elements inside it
        for row in rows:
            # Get the first td in this row
            first_td = row.find('td')
            # If there is a first td (some rows might be header rows with th instead)
            if first_td:
                # Find all <a> elements in this td
                rom_a = first_td.find('a')
                name = rom_a.text
                page_url = vimmslair_helper.VIMMS_LAIR_BASE_URL + rom_a.get('href')
                download_url = get_rom_download_url(page_url)
                rom = models.ROM(name, page_url, download_url)
                roms.append(rom)
    except BaseException as e:
        print(f'Failed on system search section: {str(e)}')
    return roms


def get_program_mode() -> models.Config:
    """Gets input from user to go into either (Bulk/Search) mode"""
    config: models.Config = models.Config()
    print(
        '\nWould you like to bulk download roms for systems or search for specific roms? (B/s)'
    )
    print("For bulk mode use 'b' and search mode use 's'")
    print('Default is \'b\'')
    while True:
        user_input: str = sys.stdin.readline()
        if user_input == '\n':
            config.bulk_mode = True
            break
        if user_input.lower() == 'b\n':
            config.bulk_mode = True
            break
        if user_input.lower() == 's\n':
            config.search_mode = True
            break
        else:
            print('Not a selection')
            print('Please Select B/s')
            continue
    return config


def get_bulk_selections(config: models.Config) -> models.Config:
    """Gets input in bulk mode if the user wants to only download specific consoles"""
    print("Press Enter to download all of Vimm's roms or select from the following of what systems you would like to download")
    print('Enter \'d\' when finished if choosing specific consoles\n')
    vimmslair_helper.print_console_list()
    while True:
        user_input: str = sys.stdin.readline()
        if user_input == '\n' and len(config.selections) == 0:
            config.all = True
            break
        if user_input == 'd\n':
            break
        try:
            if not (int(user_input) > len(helpers.CONSOLES) - 1 or int(user_input) < 0):
                config.selections.append(int(user_input))
            else:
                print('Not a selection')
                print('Please select a value from the list')
        except ValueError:
            print('Please select a value from the list')
            continue
    return config


def get_extraction_status(config: models.Config) -> models.Config:
    """Used in Bulk and Search mode to check if user wants to extract and delete downloaded ROM archives"""
    print(
        'Would you like to automatically extract and delete archives after download? (Y/n)'
    )
    print('Default is \'y\'')
    while True:
        user_input: str = sys.stdin.readline()
        if user_input == '\n':
            config.extract = True
            break
        if user_input.lower() == 'y\n':
            config.extract = True
            break
        if user_input.lower() == 'n\n':
            config.extract = False
            break
        if (user_input.lower() != 'n\n') and (user_input.lower() != 'y\n'):
            print('Not a selection')
            print('Please Select Y/n')
            continue
    return config


def print_general_search(roms: List[models.ROM]):
    table = PrettyTable()
    table.field_names = ["Selection Number", "System", "ROM"]
    count = 0
    print(
        "\nSelect which roms you would like to download and then enter 'd'\n")
    for x in roms:
        table.add_row([count, x.console, x.name])
        count += 1
    table.align = "l"
    table.right_padding_width = 0
    print(table)


def print_system_search(roms: List[models.ROM]):
    """Prints the results from a system search"""
    table = PrettyTable()
    table.field_names = ["Selection Number", "ROM"]
    count: int = 0

    for x in roms:
        table.add_row([count, x.name])
        count += 1
    table.align = "l"
    table.right_padding_width = 0
    print('\nFound ' + str(count) + ' results:')
    print(table)


def print_search_results(roms: List[models.ROM]) -> None:
    """Prints the returned search results from the users query"""
    if roms[0].console != '':
        print_general_search(roms)
    else:
        print_system_search(roms)


def get_search_result_input(roms: List[models.ROM]) -> List[int]:
    """Used to get input in search mode for what ROMs the user wants to download"""
    download_sel_roms: List[int] = []
    print(
        '\nSelect which roms you would like to download and then enter \'d\'')
    while True:
        user_input = sys.stdin.readline()
        if user_input == '\n':
            print('Please select a rom or press \'q\' to quit program')
            continue
        if user_input == 'q\n':
            exit()
        if user_input == 'd\n':
            break
        try:
            if not (int(user_input) > len(roms) - 1 or int(user_input) < 0):
                download_sel_roms.append(int(user_input))
            else:
                print('Not a selection')
                print('Please select a value from the list')
        except ValueError:
            print('Please select a value from the list')
            continue
    return download_sel_roms


def download_search_results(downloads: List[int], roms: List[models.ROM], config: models.Config) -> None:
    """Downloads the users specified roms in search mode"""
    for x in downloads:
        download_name = download_file(roms[x].download_url, HOME_DIR)
        if config.extract:
            extract_and_delete_search_results(HOME_DIR, download_name)


def extract_file(path: str, name: str) -> None:
    """Extracts the downloaded archives"""
    full_path: str = os.path.join(path, name)
    base_filename: List[str] = re.findall(r'(.+?)(\.[^.]*$|$)', name)
    try:
        file_name: str = str(base_filename[0][0])
        file_type = re.findall(r'(zip|7z)', full_path)
        if str(file_type[0]).lower() == 'zip':
            with (zipfile.ZipFile(full_path, 'r')) as z:
                dir_path = create_directory_for_rom(file_name, path)
                z.extractall(os.path.join(dir_path))
        if str(file_type[0]).lower() == '7z':
            with py7zr.SevenZipFile(full_path, mode='r') as z:
                dir_path = create_directory_for_rom(file_name, path)
                z.extractall(dir_path)
    except Exception as e:
        print(f'Failed to extract {name}. Error: {str(e)}')


def delete_file(path: str, name: str) -> None:
    """Deletes the archives"""
    os.remove(os.path.join(path, name))


def check_if_need_to_re_search() -> bool:
    """Gets user input to research if query didn't return wanted results"""
    search: bool = False
    print('Do you want to search again?(y/N)')
    while True:
        user_input = sys.stdin.readline()
        if user_input == '\n':
            break
        if user_input.lower() == 'y\n':
            search = True
            break
        if user_input.lower() == 'n\n':
            break
        if (user_input.lower() != 'n\n') and user_input.lower() != 'y\n':
            print('Not a selection')
            print('Please Select y/N')
            continue
    return search


def run_search(config: models.Config) -> List[models.ROM]:
    """Runs the correct search method to get a list of the search results"""
    roms: List[models.ROM] = get_search_section(config.query.search_selections)
    return roms


def create_directory_for_rom(name: str, path: str) -> str:
    """Used to create the directory for the ROMs archived files to be extracted to"""
    new_path: str = os.path.join(path, name)
    try:
        os.mkdir(new_path)
    except FileExistsError:
        print(f'Directory already exists: {new_path}')
        pass
    return new_path


def run_search_loop(config: models.Config) -> None:
    """Main loop for the search program"""
    while True:
        config = get_search_selection(config)
        roms: List[models.ROM] = run_search(config)
        print_search_results(roms)
        restart: bool = check_if_need_to_re_search()
        if restart:
            continue
        downloads: List[int] = get_search_result_input(roms)
        download_search_results(downloads, roms, config)
        print('Done!')
        restart = check_if_need_to_re_search()
        if restart:
            continue
        else:
            exit()


def extract_and_delete_search_results(path: str, download: str) -> None:
    """Used to extract and delete the archives in search mode"""
    extract_file(path, download)
    print('Finished extracting ' + download + '!')
    delete_file(path, download)


def download_bulk_roms(config: models.Config,
                       roms: List[models.BulkSystemROMS]):
    for system in roms:
        print('Starting to download all roms for the ' + system.system + '!')
        for section in system.sections:
            for rom in section.roms:
                download_name = download_file(rom.download_url, section.path)
                if download_name == '':
                    print('Failed to download ' + rom.name)
                    continue
                if config.extract:
                    extract_and_delete_search_results(section.path, download_name)


def run_selected_program(config: models.Config) -> None:
    """Runs selected program"""
    if config.bulk_mode:
        config = get_bulk_selections(config)

        if config.all:
            roms = get_every_system_roms()
        else:
            roms = get_selected_system_bulk_roms(config)
        roms = vimmslair_helper.generate_path_to_bulk_roms(roms, HOME_DIR)

        vimmslair_helper.create_directory_structure(config, HOME_DIR)
        download_bulk_roms(config, roms)
        exit()
    if config.search_mode:
        run_search_loop(config)


def main() -> None:
    """Programs main method"""
    vimmslair_helper.print_welcome()

    config: models.Config = get_program_mode()
    config: models.Config = get_extraction_status(config)
    run_selected_program(config)


if __name__ == '__main__':
    vimmslair_helper: helpers.VimmsLairHelper = helpers.VimmsLairHelper()
    main()
