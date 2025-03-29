import os
import random
import sys
from typing import List
from src import models


USER_AGENTS: list[str] = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
]


CONSOLES = {
    'Atari 7800': 'Atari7800',
    'Nintendo NES': 'NES',
    'Super Nintendo': 'SNES',
    'Nintendo 64': 'N64',
    'Wii': 'Wii',
    'Wii Ware': 'WiiWare',
    'Gamecube': 'GameCube',
    'Master System': 'SMS',
    'Mega Drive': 'Genesis',
    'Saturn': 'Saturn',
    'Dreamcast': 'Dreamcast',
    'Playstation': 'PS1',
    'Playstation 2': 'PS2',
    'Playstation 3': 'PS3',
    'Xbox': 'Xbox',
    ### Portable consoles ###
    'Game Boy': 'GB',
    'Game Boy Color': 'GBC',
    'Game Boy Advanced': 'GBA',
    'Nintendo DS': 'DS',
    'Playstation Portable': 'PSP'
}


class VimmsLairHelper:
    """Helper class to hold the vimms lair helper methods"""

    USER_AGENTS: list[str] = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    ]
    DIRNAMES: list[str] = [
        '#', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    VIMMS_LAIR_BASE_URL: str = 'https://vimm.net'
    VIMMS_LAIR_DL_BASE_URL: str = 'https://dl2.vimm.net'

    def __init__(self, roms_directory: str = 'ROMS'):
        self.roms_directory = roms_directory

    def print_welcome(self):
        """Prints the welcome message"""
        print(r"""
        _   _ _                          _           _     ______                    _                 _
        | | | (_)                        | |         (_)    |  _  \                  | |               | |
        | | | |_ _ __ ___  _ __ ___  ___ | |     __ _ _ _ __| | | |_____      ___ __ | | ___   __ _  __| | ___ _ __
        | | | | | '_ ` _ \| '_ ` _ \/ __|| |    / _` | | '__| | | / _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
        \ \_/ / | | | | | | | | | | \__ \| |___| (_| | | |  | |/ / (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |
        \___/|_|_| |_| |_|_| |_| |_|___/\_____/\__,_|_|_|  |___/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|
            """)
        print('Welcome to the Vimm\'s Lair Download Script!')
        print('Please use responsibly, I am not liable for any damages or legal issues caused by using this script')

    def create_directory_structure(self, config: models.Config, path: str):
        """Public helper to be used in bulk mode"""
        if config.selections != None:
            if config.all:
                self.__create_all_dirs(path)
            if not config.all:
                self.__create_dirs(path, config.selections)

    def selection_to_uri(self, selection: str):
        """Public helper to return the correct uri from the prettier printed version"""
        return CONSOLES[selection]

    def print_console_list(self):
        """Public helper to print the consoles listed on Vimms"""
        console_list = list(CONSOLES.keys())
        num_consoles = len(console_list)
        # Add 1 to ensure odd numbers of consoles put the extra item in the left column
        half = (num_consoles + 1) // 2

        # Create format string with fixed width for both columns
        format_str = "{:<30} {:<30}"
        for i in range(half):
            left = f"{i:2d} ==> {console_list[i]}"
            right = f"{i + half:2d} ==> {console_list[i + half]}" if i + half < num_consoles else ""
            print(format_str.format(left, right))

    def get_selection_from_num(self, selection: int) -> str:
        """Returns the specified selection from CONSOLE"""
        return list(CONSOLES.keys())[selection]

    def get_random_ua(self) -> str:
        """Returns a random user agent for download method"""
        index: int = random.randint(0, len(USER_AGENTS) - 1)
        return USER_AGENTS[index]

    def get_search_url(self, search_selection: models.SearchSelection) -> str:
        """Returns a hydrated search_url with the correct system and query"""
        if search_selection.system != 'general':
            console_uri_name: str = self.selection_to_uri(search_selection.system)
            url: str = f'{self.VIMMS_LAIR_BASE_URL}/vault/?p=list&system={console_uri_name}&q={search_selection.query}'
            url.replace('\n', '')
            return url
        else:
            url: str = (
                f'{self.VIMMS_LAIR_BASE_URL}/vault/?p=list&q={search_selection.query}')
            return url

    def generate_path_to_bulk_roms(self, roms: List[models.BulkSystemROMS], home_dir: str) -> List[models.BulkSystemROMS]:
        """Creates the absolute path to where each rom should be downloaded"""
        for system in roms:
            for section in system.sections:
                folder = '#' if 'number' in section.section else section.section[-1].upper()
                section.path = os.path.join(home_dir, self.roms_directory, system.system_name, folder)
        return roms


    def __create_alpha_num_structure(self, path: str, system: str):
        """Used in bulk mode to create the Alphanumeric directory structure in a system's directory"""
        try:
            for x in self.DIRNAMES:
                os.mkdir(os.path.join(path, self.roms_directory, system, x))
        except:
            e = sys.exc_info()[0]
            print('Failed Creating AlphaNum Structure')
            print(e)


    def __create_rom_home_dir(self, path: str):
        """Creates the main ROMS directory in the root of the project"""
        try:
            os.mkdir(os.path.join(path, self.roms_directory))
        except:
            e = sys.exc_info()[0]
            print('Failed Creating Home Directory')
            print(e)


    def __create_rom_system_dir(self, path: str, system: str):
        """Creates a specific system's directory inside the ROMS folder"""
        try:
            os.mkdir(os.path.join(path, self.roms_directory, system))
        except:
            e = sys.exc_info()[0]
            print('Failed Creating ROM System Directory')
            print(e)


    def __is_home_dir_created(self, path: str) -> bool:
        """Checks for the existence of the ROMS directory"""
        for x in os.listdir(path):
            if x == self.roms_directory:
                return True
        return False


    def __is_system_dir_created(self, path: str, system: str) -> bool:
        """Checks for the existence of a specific system directory in the ROMS directory"""
        for x in os.listdir(os.path.join(path, self.roms_directory)):
            if x == system:
                return True


    def __create_all_dirs(self, path: str):
        """Used in bulk mode to create all the directories and sub-directories"""
        all_consoles: list[str] = CONSOLES.keys()
        self.__create_dirs(path, all_consoles)


    def __create_dirs(self, path: str, user_selections: List[str]):
        """Used in bulk mode to create directories and sub-directories for selected systems"""
        if not self.__is_home_dir_created(path):
            self.__create_rom_home_dir(path)
        for selection in user_selections:
            console_name = self.get_selection_from_num(int(selection))
            if not self.__is_system_dir_created(path, console_name):
                self.__create_rom_system_dir(path, console_name)
                self.__create_alpha_num_structure(path, console_name)
