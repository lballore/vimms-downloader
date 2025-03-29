"""Data models for Vimms-DL"""

from typing import List


class ROM:
    """Used to hold a details about a single ROM"""
    def __init__(
        self,
        name: str,
        page_url: str,
        download_url: str,
        console: str = ''
    ):
        self.name = name
        self.page_url = page_url
        self.download_url = download_url
        self.console = console


class SectionofROMs:
    """
    Used to hold a details about multiple ROMs.
    Sections are either a search query or #-A-Z subsections on Vimms.
    """
    def __init__(self, section: str, roms: List[ROM], path: str = ''):
        self.section = section
        self.roms = roms
        self.path = path


class SearchSelection:
    """Used when in search mode to get the parameters for the search criteria"""
    def __init__(self, system: str = '', query: str = ''):
        self.system = system
        self.query = query


class BulkSystemROMS:
    """Used hold all of a systems ROMS"""
    def __init__(self, sections: List[SectionofROMs], system: str, system_name: str = ''):
        self.system = system  # The URI version (e.g. 'NES')
        self.system_name = system_name  # The display version (e.g. 'Nintendo NES')
        self.sections = sections


class Search:
    """Used in search mode to hold data for the type of search"""
    def __init__(self, search_selections: SearchSelection, general: bool = False):
        self.search_selections = search_selections
        self.general = general


class Config:
    """Config object created based on user input"""
    def __init__(
        self,
        all: bool = False,
        extract: bool = False,
        bulk_mode: bool = False,
        search_mode: bool = False
    ):
        self.selections: List[int] = []
        self.all = all
        self.extract = extract
        self.search_mode = search_mode
        self.bulk_mode = bulk_mode
        self.query_selection: SearchSelection = SearchSelection()
        self.query: Search = Search(self.query_selection)
