'''
.. module:: import_xml_tests
    :Date: 2014/09/15
    
.. codeauthor:: Esmail Fadae <esmail.fadae@kobotoolbox.org>
'''


import unittest
import os.path

from pyxform import xform2json


class ImportXmlTests(unittest.TestCase):
    test_directory_path= os.path.dirname(__file__)

    def single_select_one_test(self):
        xml_in_path= os.path.join(self.test_directory_path,\
                                  'example_xml/single_select_one_survey.xml')
        
        survey= xform2json.XFormToDictBuilder(xml_in_path).survey()
        self.assertEqual(survey['title'], 'Single "select one" survey')
        self.assertEqual(survey['name'], 'single_select_one_survey')
        
        questions= survey['children']
        self.assertEqual(len(questions), 1,)
                
        question_1= questions[0]
        self.assertEqual(question_1['label'], '"Select one" question')
        self.assertEqual(question_1['name'], 'Select_one_question')
        self.assertEqual(question_1['type'], 'select one')
        
        options= question_1['children']
        self.assertEqual(len(options), 2)
        
        for i, o in enumerate(options, 1):
            self.assertEqual(o['label'], 'Option {}'.format(i))
            self.assertEqual(o['name'], 'option_{}'.format(i))
                

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()