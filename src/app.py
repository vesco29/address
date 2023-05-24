# The Selector class takes an input file of addresses and names, processes the data, and outputs a
# file with sorted names grouped by address.
import os
from csv import DictReader


class Selector(object):
    """Selector class for selecting people from csv files."""

    BG_LETTER = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g',	'д': 'd', 'е': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'ѝ': 'y',
                 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',	'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
                 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch',	'ш': 'sh', 'щ': 'sht', 'ъ': 'a', 'ь': 'y', 'ю': 'yu', 'я': 'ya'
                 }

    def __init__(self, input_file: str, output_file: str):
        """Selector class constructor

        Args:
            input_file (str): csv file containing names ans address
            output_file (str): new file containing people living in same address
        """
        assert os.path.exists(input_file), f" {input_file} not exists"
        out_path = os.path.abspath(os.path.dirname(output_file))
        assert os.path.exists(out_path), f" {out_path} not exists"
        self._input_file = input_file
        self._output_file = output_file

    @classmethod
    def _load_file_csv(cls, input_file: str) -> dict:
        """read csv file using csv lib

        Args:
            input_file (_type_): csv input file

        Returns:
            dictionary:  dict with name and address
        """
        with open(input_file, 'r', encoding="utf-8-sig") as f:
            dict_reader = DictReader(f)
            list_data = list(dict_reader)
            return list_data

    @classmethod
    def _load_file(cls, input_file: str) -> dict:
        """load csv file to dictionary

        Args:
            input_file (_type_): csv input file

        Returns:
            dictionary:  dict with name and address
        """
        col_name = list()
        list_data = list()
        with open(input_file, 'r', encoding="utf-8-sig") as f:
            for line in f.readlines():
                line = line.rstrip()
                if not col_name:
                    col_name = line.split(',')
                    continue
                split_line = line.split(',')
                address = ','.join(split_line[1:])
                el_dict = {col_name[0]: split_line[0],
                           col_name[1]: address.replace('"', '')
                           }
                list_data.append(el_dict)

        return list_data

    def _get_address_key(self, address: str) -> str:
        """create address key

        Args:
            address (string):  raw address string

        Returns:
            string: unified address string
        """
        address = address.split(',')
        country = self._get_address_country(address[-1])
        city = self._get_address_city(address[-2], country)
        street = self._get_address_street(address[0], country)
        return f'{country}_{city}_{street}'

    def _get_address_country(self, country: str) -> str:
        """get unified country name 

        Args:
            country (string): raw country string

        Returns:
            string: unified country string
        """
        if 'Germany' in country:
            return 'Germany'
        if 'P.R.C' in country or 'China' in country:
            for el in country.split():
                if el[0].isdigit():
                    return f'China_{el}'
            return 'China'
        if 'Bulgaria' in country or 'България' in country:
            return 'Bulgaria'

    def _get_address_street(self, address: str, country: str) -> str:
        """convert street address to unified address 

        Args:
            address (string): street address
            country (string): country name

        Returns:
            string: unified street address
        """
        street = list()
        for el in address.split():
            if el.isdigit():
                number = el
            else:
                street.append(el)
        street = ' '.join(street)
        if country in ['Bulgaria']:
            street = self._unified_bg_address(street)

        return f"{number}_{street.replace(' ', '_')}"

    def _unified_bg_address(self, address: str) -> str:
        """get unified bulgarian address
           if address is written in bulgarian letters convert to latin letters transcription    
        Args:
            address (string): raw bulgarian address(bulgarian or latin letters)

        Returns:
            string: unified bulgarian address
        """
        unified_address = list()
        for el in address.split():
            if el in ('ul.', 'ул.'):
                unified_address.append('Street')
            elif el[0].lower() in self.BG_LETTER:
                unified_address.append(
                    ''.join([self._bg_to_english_transcript(c) for c in el]))
            else:
                unified_address.append(el)
        return ' '.join(sorted(unified_address))

    def _get_address_city(self, city_in: str, country:str)->str:
        """get city name 

        Args:
            city_in (string): raw city name
            country (string): country name

        Returns:
            string: City name
        """
        bg_city = {'София': 'Sofia'}
        post = None
        city = list()
        for el in city_in.split():
            if el.isdigit():
                post = el
            else:
                city.append(el)
        city = ' '.join(city)
        if city[0].lower() in self.BG_LETTER and city in bg_city:
            city = bg_city[city]

        if country in ['Bulgaria']:
            return city

        if post is None:
            return city.replace(' ', '_')
        else:
            return f"{post}_{city.replace(' ', '_')}"

    def _bg_to_english_transcript(self, bg:str)->str:
        """ transcript bulgarian character to latin1 character

        Args:
            bg (string): bulgarian character

        Returns:
            string: latin1 character
        """
        if bg.islower():
            return self.BG_LETTER.get(bg, bg)
        else:
            return (self.BG_LETTER.get(bg.lower(), bg)).capitalize()

    def _select_people(self, address:list)->list:
        """select people by address

        Args:
            address (list): list of people and their addresses

        Returns:
            list: list of people live in same address
        """
        people = dict()
        for el in address:
            address_key = self._get_address_key(el['Address'])
            if address_key in people:
                people[address_key].append(el['Name'])
            else:
                people[address_key] = [el['Name']]

        return sorted([','.join(sorted(el)) for el in people.values()])

    def create_out_file(self):
        """write csv file with order names by address 
        """
        addresses_data = self._load_file(self._input_file)
        people = self._select_people(addresses_data)
        with open(self._output_file, 'w') as f:
            f.writelines([f"{line}\n" for line in people])
