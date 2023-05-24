import unittest
import sys
import os
import shutil
import csv

HOME = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join( HOME, '..'))

from app import Selector

class TestStringMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.testdata = os.path.join(HOME, 'testdata')
        self.output_path = os.path.join(HOME, 'output')
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path )
        os.mkdir(self.output_path)
        return super().setUp()
    
    def tearDown(self) -> None:
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path )
        return super().tearDown()

    def test_init(self):
        input_file = os.path.join(self.testdata, 'test.csv')
        obj = Selector(input_file, self.output_path)
        message = "given object is not instance of Selector."
        self.assertIsInstance(obj, Selector, message)
    
    def test_init_validate_input(self):
        self.assertRaises(AssertionError, Selector, 'not_exist_test.csv', self.output_path)
    
    def test_init_validate_output(self):
        input_file = os.path.join(self.testdata, 'test.csv')
        self.assertRaises(AssertionError, Selector, input_file, os.path.join(HOME,'not_exist_path','test.csv'))

    def test_load_file_csv(self):
        input_file = os.path.join(self.testdata, 'test.csv')
        output_file = os.path.join(self.output_path, 'selector.csv')
        objects = Selector(input_file, output_file)
        addresses_data = objects._load_file_csv(input_file)
        expected = [{'Name': 'Ivan Draganov', 'Address': 'ul. Shipka 34, 1000 Sofia, Bulgaria'}, 
                    {'Name': 'Leon Wu', 'Address': '1 Guanghua Road, Beijing, China 100020'}, 
                    {'Name': 'Ilona Ilieva', 'Address': 'ул. Шипка 34, София, България'}, 
                    {'Name': 'Dragan Doichinov', 'Address': 'Shipka Street 34, Sofia, Bulgaria'}, 
                    {'Name': 'Li Deng', 'Address': '1 Guanghua Road, Chaoyang District, Beijing, P.R.C 100020'}, 
                    {'Name': 'Frieda Müller', 'Address': 'Konrad-Adenauer-Straße 7, 60313 Frankfurt am Main, Germany'}]
        self.assertListEqual(addresses_data, expected)
    
    def test_load_file(self):
        input_file = os.path.join(self.testdata, 'test.csv')
        output_file = os.path.join(self.output_path, 'selector.csv')
        objects = Selector(input_file, output_file)
        addresses_data = objects._load_file(input_file)
        expected = [{'Name': 'Ivan Draganov', 'Address': 'ul. Shipka 34, 1000 Sofia, Bulgaria'}, 
                    {'Name': 'Leon Wu', 'Address': '1 Guanghua Road, Beijing, China 100020'}, 
                    {'Name': 'Ilona Ilieva', 'Address': 'ул. Шипка 34, София, България'}, 
                    {'Name': 'Dragan Doichinov', 'Address': 'Shipka Street 34, Sofia, Bulgaria'}, 
                    {'Name': 'Li Deng', 'Address': '1 Guanghua Road, Chaoyang District, Beijing, P.R.C 100020'}, 
                    {'Name': 'Frieda Müller', 'Address': 'Konrad-Adenauer-Straße 7, 60313 Frankfurt am Main, Germany'}]
        self.assertListEqual(addresses_data, expected)
    
    def test_address_key_Germany(self):
        input_file = os.path.join(self.testdata, 'test.csv')
        output_file = os.path.join(self.output_path, 'selector.csv')
        objects = Selector(input_file, output_file)
        addresses_key = objects._get_address_key('Konrad-Adenauer-Straße 7, 60313 Frankfurt am Main, Germany')
        addresses_key_2 = objects._get_address_key('Konrad-Adenauer-Straße 7, 60313 Frankfurt am Main, Germany')
    
        self.assertTrue(addresses_key == addresses_key_2)

    def test_address_key_China(self):
        input_file = os.path.join(self.testdata, 'test.csv')
        output_file = os.path.join(self.output_path, 'selector.csv')
        objects = Selector(input_file, output_file)
        addresses_key = objects._get_address_key('1 Guanghua Road, Beijing, China 100020')
        addresses_key_2 = objects._get_address_key('1 Guanghua Road, Chaoyang District, Beijing, P.R.C 100020')
    
        self.assertTrue(addresses_key == addresses_key_2)

    def test_address_key_Bulgaria(self):
        input_file = os.path.join(self.testdata, 'test.csv')
        output_file = os.path.join(self.output_path, 'selector.csv')
        objects = Selector(input_file, output_file)
        addresses_key = objects._get_address_key('ul. Shipka 34, 1000 Sofia, Bulgaria')
        addresses_key_2 = objects._get_address_key('ул. Шипка 34, София, България')
        addresses_key_3 = objects._get_address_key('Shipka Street 34, Sofia, Bulgaria')

        self.assertTrue(addresses_key == addresses_key_2 == addresses_key_3)

    def test_address_select(self):
        input_file = os.path.join(self.testdata, 'test.csv')
        output_file = os.path.join(self.output_path, 'selector.csv')
        objects = Selector(input_file, output_file)
        addresses_data = objects._load_file(input_file)
        people = objects._select_people(addresses_data)        
        expected = ['Dragan Doichinov,Ilona Ilieva,Ivan Draganov',      
                    'Frieda Müller',
                    'Leon Wu,Li Deng']
        self.assertListEqual(people, expected)

    def test_create_out_file(self):
        input_file = os.path.join(self.testdata, 'test.csv')
        output_file = os.path.join(self.output_path, 'selector.csv')
        objects = Selector(input_file, output_file)
        objects.create_out_file() 
        with open(output_file,'r') as data:
            people =  [line for line in csv.reader(data)]
        expected = [['Dragan Doichinov','Ilona Ilieva','Ivan Draganov'],      
                    ['Frieda Müller'],
                    ['Leon Wu','Li Deng']]
        self.assertListEqual(people, expected)

    def test_bg_to_english_transcript(self):
        input_file = os.path.join(self.testdata, 'test.csv')
        output_file = os.path.join(self.output_path, 'selector.csv')
        objects = Selector(input_file, output_file)
        self.assertEqual('a', objects._bg_to_english_transcript('а'))
        self.assertEqual('A', objects._bg_to_english_transcript('А'))



if __name__ == '__main__':
    unittest.main()