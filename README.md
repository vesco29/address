# Development task

Given a list of people and their addresses, create a script in python3 that
groups people who live at the same address.

### Input

1) A path to a utf-8 encoded .csv file with two columns Name,Address.
2) A path to a directory where output file should be saved.
***
### Output

A text document saved at the specified location. Each line is a commaseparated list of names of the people living at the same address. The
names in a line should be sorted alphabetically. The lines of the file should
also be sorted alphabetically.
***
#### Example input file data
```
Example input file data*
Name,Address
Ivan Draganov,”ul. Shipka 34, 1000 Sofia, Bulgaria”
Leon Wu,”1 Guanghua Road, Beijing, China 100020”
Ilona Ilieva,”ул. Шипка 34, София, България”
Dragan Doichinov,”Shipka Street 34, Sofia, Bulgaria”
Li Deng,”1 Guanghua Road, Chaoyang District, Beijing, P.R.C 100020”
Frieda Müller,”Konrad-Adenauer-Straße 7, 60313 Frankfurt am Main,
Germany”
```
#### Expected output
```
Dragan Doichinov, Ilona Ilieva, Ivan Draganov
Frieda Müller
Leon Wu, Li Deng
```
### Additional requirements
1) Observe good coding practices
2) Include a short readme file documenting the solution.
3) There are no library usage restrictions.
 
# Solution 

Create a python executable using the python 3
```
python people.py -h
usage: people.py [-h] -i INPUT [-o OUTPUT] [-f OUTPUT_FILE_NAME]

Given a csv file contained people and their addresses and create output file that groups people who live at the same address.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input path to csv file containing people and their addresses
  -o OUTPUT, --output OUTPUT
                        output path to write file (default: /home/vnikolov/address)
  -f OUTPUT_FILE_NAME, --output-file-name OUTPUT_FILE_NAME
                        output file name (default: sorted.csv)
```

### Solution 

- create Selector class in src/app.py to solve the problem
- load the csv  file containing people and their addresses to list with name and addresses  
```
 [{'Name': 'Ivan Draganov', 'Address': 'ul. Shipka 34, 1000 Sofia, Bulgaria'}, 
  {'Name': 'Leon Wu', 'Address': '1 Guanghua Road, Beijing, China 100020'}, 
  {'Name': 'Ilona Ilieva', 'Address': 'ул. Шипка 34, София, България'}, 
  {'Name': 'Dragan Doichinov', 'Address': 'Shipka Street 34, Sofia, Bulgaria'}, 
  {'Name': 'Li Deng', 'Address': '1 Guanghua Road, Chaoyang District, Beijing, P.R.C 100020'}, 
  {'Name': 'Frieda Müller', 'Address': 'Konrad-Adenauer-Straße 7, 60313 Frankfurt am Main, Germany'}]
``` 
- Group people by address

process all the people data and group them by address, creating a address key for each person   
```
{'Bulgaria_Sofia_34_Shipka_Street': ['Ivan Draganov', 'Ilona Ilieva', 'Dragan Doichinov'], 'China_100020_Beijing_1_Guanghua_Road': ['Leon Wu', 'Li Deng'], 'Germany_60313_Frankfurt_am_Main_7_Konrad-Adenauer-Straße': ['Frieda Müller']}
```

- Sort people by name and create output file

# Selector Class

The `Selector` class is used for selecting people from CSV files based on their addresses and grouping them together.

## Attributes

- `BG_LETTER`: A dictionary mapping Bulgarian letters to their corresponding Latin letters.
- `_input_file`: The path to the input CSV file containing names and addresses.
- `_output_file`: The path to the output file where the sorted names grouped by address will be written.

## Methods

### Constructor

The constructor method `__init__(self, input_file: str, output_file: str)` initializes a new instance of the `Selector` class.

- `input_file` (str): The path to the input CSV file.
- `output_file` (str): The path to the output file.

### Private Methods

- `_load_file_csv(self, input_file: str) -> dict`: Reads a CSV file using the CSV library and returns a dictionary with names and addresses.
- `_load_file(self, input_file: str) -> dict`: Loads a CSV file into a dictionary with names and addresses.
- `_get_address_key(self, address: str) -> str`: Creates an address key based on a raw address string.
- `_get_address_country(self, country: str) -> str`: Returns a unified country name based on a raw country string.
- `_get_address_street(self, address: str, country: str) -> str`: Converts a street address to a unified address based on the country.
- `_unified_bg_address(self, address: str) -> str`: Converts a Bulgarian address to a unified address format.
- `_get_address_city(self, city_in: str, country: str) -> str`: Returns the city name based on a raw city string and the country.
- `_bg_to_english_transcript(self, bg: str) -> str`: Transcribes a Bulgarian character to its corresponding Latin character.
- `_select_people(self, address: list) -> list`: Selects people based on their address and returns a list of people living at the same address.

### Public Methods

- `create_out_file(self)`: Writes a CSV file with the sorted names grouped by address.

---

This Markdown document describes the `Selector` class and its attributes, constructor, private methods, and public methods.
