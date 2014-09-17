'''
.. module:: export_spreadsheet_tests
    :Date: 2014/09/16
    
.. codeauthor:: Esmail Fadae <esmail.fadae@kobotoolbox.org>
'''


import unittest
import os.path
import tempfile

import pyxform.survey_from


class ExportSpreadsheetTests(unittest.TestCase):
    test_directory_path= os.path.dirname(__file__)
    xform_in_path= os.path.join(test_directory_path,\
                            'example_xml/multiple_select_question_survey.xml')

    def xls_creation_test(self):
        '''
        Test converting an XForm to an XLS-formatted XLSForm.
        '''
        
        # Convert an XForm to an XLS-formatted XLSForm.
        survey_xform= pyxform.survey_from.xform(self.xform_in_path)
        temp_xls_file= tempfile.NamedTemporaryFile()
        survey_xform.to_xls(temp_xls_file.name)
        
        # Attempt to re-import the converted XLSForm.
        # Comparison to the original ('survey_xform') will be difficult due to
        #   currently (2014/09/17) incomplete exporting, timestamp changes, etc.
        pyxform.survey_from.xls(temp_xls_file.name)
        

    def csv_creation_test(self):
        '''
        Test converting an XForm to an CSV-formatted XLSForm.
        '''
        
        # Convert an XForm to an CSV-formatted XLSForm.
        survey_xform= pyxform.survey_from.xform(self.xform_in_path)
        temp_csv_file= tempfile.NamedTemporaryFile()
        survey_xform.to_xls(temp_csv_file.name)
        
        # Attempt to re-import the converted XLSForm.
        # Comparison to the original ('survey_xform') will be difficult due to
        #   currently (2014/09/17) incomplete exporting, timestamp changes, etc.
        pyxform.survey_from.xls(temp_csv_file.name)


    def consistent_export_test(self):
        '''
        Test that exporting a form to CSV and XLS result in the same data.
        '''
        survey_xform= pyxform.survey_from.xform(self.xform_in_path)
        
        temp_xls_file= tempfile.NamedTemporaryFile()
        survey_xform.to_xls(temp_xls_file.name)
        survey_xls= pyxform.survey_from.xls(temp_xls_file.name)
        
        temp_csv_file= tempfile.NamedTemporaryFile()
        survey_xform.to_xls(temp_csv_file.name)
        survey_csv= pyxform.survey_from.xls(temp_csv_file.name)
        
        self.assertEqual(survey_xls, survey_csv)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()