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
    
    def setUp(self):
        test_directory_path= os.path.dirname(__file__)
        xml_directory_path= os.path.join(test_directory_path, 'example_xml')
        self.surveys= dict()
        
        # Record the path to all files in the 'example_xml' directory.    
        xform_in_paths= [ os.path.join(xml_directory_path, filename) \
                        for filename in os.listdir(xml_directory_path)]
        
        for xform_in_p in xform_in_paths:
            self.surveys[xform_in_p]= dict()
            
            # Import and store the XForm.
            xform_survey= pyxform.survey_from.xform(xform_in_p)
            self.surveys[xform_in_p]['xform'] = xform_survey
            
            with tempfile.NamedTemporaryFile() as xls_tempfile:
                # Export the XForm survey to an XLS-formatted XLSForm file.
                xform_survey.to_xls(xls_tempfile.name)
                # Import the XLSForm back in.
                xls_survey= pyxform.survey_from.xls(xls_tempfile)
                self.surveys[xform_in_p]['xls']= xls_survey

            with tempfile.NamedTemporaryFile() as csv_tempfile:
                # Export the XForm survey to a CSV-formatted XLSForm file.
                xform_survey.to_csv(csv_tempfile.name)
                # Import the XLSForm back in.
                csv_survey= pyxform.survey_from.csv(csv_tempfile)
                self.surveys[xform_in_p]['csv']= csv_survey
        

    def consistent_export_test(self):
        '''
        Test that exporting a form to CSV and XLS result in the same data.
        '''

        for srvys in self.surveys.itervalues():
            self.assertEqual(srvys['xls'], srvys['csv'])


    def unicode_test(self):
        '''
        Test that Unicode text is correctly exported and re-importable.
        '''
        
        EXPECTED_QUESTION_LABEL= u"Don't you just \u2764 Unicode\u203d"
        XML_SURVEY_FILENAME= 'unicode_survey.xml'
        
        # Locate 'unicode_survey.xml'
        unicode_survey_path= [xform_in_p for xform_in_p in self.surveys.iterkeys() \
                             if os.path.split(xform_in_p)[1] == XML_SURVEY_FILENAME ][0]
        xls_srvy= self.surveys[unicode_survey_path]['xls']
        
        xls_question_label= xls_srvy['children'][0]['label']
        self.assertEqual(xls_question_label, EXPECTED_QUESTION_LABEL)
        
        csv_srvy= self.surveys[unicode_survey_path]['csv']
        
        csv_question_label= csv_srvy['children'][0]['label']
        self.assertEqual(csv_question_label, EXPECTED_QUESTION_LABEL)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()