'''
.. module:: test_survey_to_xlsform
    :Date: 2014/09/16
    
.. codeauthor:: Esmail Fadae <esmail.fadae@kobotoolbox.org>
'''


import unittest
import os.path
import tempfile

import pyxform.survey_from
from pyxform import constants


class Test_SurveyToXlsForm(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        
        # Record the path to all files in the 'example_xml' directory.    
        test_directory_path= os.path.dirname(__file__)
        xform_directory_path= os.path.join(test_directory_path, 'example_xforms')
        
        self.xform_in_paths= [ os.path.join(xform_directory_path, filename) \
                        for filename in os.listdir(xform_directory_path)]


    def test_consistent_export(self):
        '''
        Test that exporting a form to CSV and XLS result in the same data.
        '''
                
        for xform_in_p in self.xform_in_paths:            
            # Import and store the XForm.
            xform_survey= pyxform.survey_from.xform(xform_in_p)
            
            with tempfile.NamedTemporaryFile(suffix='-pyxform.xls') as xls_tempfile:
                # Export the XForm survey to an XLS-formatted XLSForm file.
                xform_survey.to_xls(xls_tempfile.name)
                # Import the XLSForm back in.
                xls_survey= pyxform.survey_from.xls(xls_tempfile)

            with tempfile.NamedTemporaryFile(suffix='-pyxform.csv') as csv_tempfile:
                # Export the XForm survey to a CSV-formatted XLSForm file.
                xform_survey.to_csv(csv_tempfile.name)
                # Import the XLSForm back in.
                csv_survey= pyxform.survey_from.csv(csv_tempfile)

            self.assertEqual(xls_survey, csv_survey, 'XLS and CSV XLSForm mismatch for "{}".'.format(xform_in_p))


    def test_unicode(self):
        '''
        Test that Unicode text is correctly exported and re-importable.
        '''
        
        EXPECTED_QUESTION_LABEL= u"Don't you just \u2764 Unicode\u203d"
        XML_SURVEY_FILENAME= 'unicode_survey.xml'
        
        # Locate 'unicode_survey.xml'
        unicode_survey_path= [xform_in_p for xform_in_p in self.xform_in_paths \
                             if os.path.split(xform_in_p)[1] == XML_SURVEY_FILENAME ][0]
        
        xform_survey= pyxform.survey_from.xform(unicode_survey_path)
        
        # Test XLS re-import.
        with tempfile.NamedTemporaryFile(suffix='-pyxform.xls') as xls_tempfile:
            xform_survey.to_xls(xls_tempfile.name)
            xls_survey= pyxform.survey_from.xls(xls_tempfile)
        
            xls_question_label= xls_survey[constants.CHILDREN][0][constants.LABEL]
            self.assertEqual(xls_question_label, EXPECTED_QUESTION_LABEL)
        
        # Test CSV re-import.
        with tempfile.NamedTemporaryFile(suffix='-pyxform.csv') as csv_tempfile:
            xform_survey.to_csv(csv_tempfile.name)
            csv_survey= pyxform.survey_from.csv(csv_tempfile)

            csv_question_label= csv_survey[constants.CHILDREN][0][constants.LABEL]
            self.assertEqual(csv_question_label, EXPECTED_QUESTION_LABEL)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()