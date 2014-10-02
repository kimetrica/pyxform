'''
.. module:: test_import_xform
    :Date: 2014/09/15
    
.. codeauthor:: Esmail Fadae <esmail.fadae@kobotoolbox.org>
'''


import unittest
import os.path

from pyxform import xform2json


class Test_ImportXForm(unittest.TestCase):
    test_directory_path= os.path.dirname(__file__)

    def test_single_select_one_survey(self):
        '''
        Test that an XForm with a single "Select One" question is imported \
        correctly.
        '''
        
        xml_in_path= os.path.join(self.test_directory_path,\
                                  'example_xforms/single_select_one_survey.xml')
        
        survey= xform2json.XFormToDictBuilder(xml_in_path).survey()
        self.assertEqual(survey['title'], 'Single "select one" survey')
        self.assertEqual(survey['name'], 'single_select_one_survey')
        
        questions= survey['children']
        self.assertEqual(len(questions), 1)
                
        question_1= questions[0]
        self.assertEqual(question_1['label'], '"Select one" question')
        self.assertEqual(question_1['name'], 'Select_one_question')
        self.assertEqual(question_1['type'], 'select one')
        
        options= question_1['children']
        self.assertEqual(len(options), 2)
        
        for o_num, o in enumerate(options, 1):
            self.assertEqual(o['label'], 'Option {}'.format(o_num))
            self.assertEqual(o['name'], 'option_{}'.format(o_num))


    def test_single_select_many_survey(self):
        '''
        Test that an XForm with a single "Select Many" question is imported \
        correctly.
        '''
        
        xml_in_path= os.path.join(self.test_directory_path,\
                                  'example_xforms/single_select_many_survey.xml')
        
        survey= xform2json.XFormToDictBuilder(xml_in_path).survey()
        self.assertEqual(survey['title'], 'Single "Select Many" Survey')
        self.assertEqual(survey['name'], 'single_select_many_survey')
        
        questions= survey['children']
        self.assertEqual(len(questions), 1)
                
        question_1= questions[0]
        self.assertEqual(question_1['label'], '"Select Many" question.')
        self.assertEqual(question_1['name'], 'Select_Many_question')
        self.assertEqual(question_1['type'], 'select all that apply')
        
        options= question_1['children']
        self.assertEqual(len(options), 2)
        
        for o_num, o in enumerate(options, 1):
            self.assertEqual(o['label'], 'Option {}'.format(o_num))
            self.assertEqual(o['name'], 'option_{}'.format(o_num))


    def test_multiple_select_question_survey(self):
        '''
        Test that an XForm with a "Select One" and a "Select Many" question is \
        imported correctly.
        '''
        
        xml_in_path= os.path.join(self.test_directory_path,\
                            'example_xforms/multiple_select_question_survey.xml')
        
        survey= xform2json.XFormToDictBuilder(xml_in_path).survey()
        self.assertEqual(survey['title'], 'Multiple "Select" Question Survey.')
        self.assertEqual(survey['name'], 'multiple_select_question_survey')
        
        questions= survey['children']
        self.assertEqual(len(questions), 2)
        
        question_1= questions[0]
        self.assertEqual(question_1['label'], '"Select One" question.')
        self.assertEqual(question_1['name'], 'Select_One_question')
        self.assertEqual(question_1['type'], 'select one')
        
        options= question_1['children']
        self.assertEqual(len(options), 2)
        
        for o_num, o in enumerate(options, 1):
            self.assertEqual(o['label'], 'Option {}'.format(o_num))
            self.assertEqual(o['name'], 'option_{}'.format(o_num))

        question_2= questions[1]
        self.assertEqual(question_2['label'], '"Select Many" question.')
        self.assertEqual(question_2['name'], 'Select_Many_question')
        self.assertEqual(question_2['type'], 'select all that apply')
        
        options= question_2['children']
        self.assertEqual(len(options), 2)
        
        for o_num, o in enumerate(options, 1):
            self.assertEqual(o['label'], 'Option {}'.format(o_num))
            self.assertEqual(o['name'], 'option_{}'.format(o_num))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()