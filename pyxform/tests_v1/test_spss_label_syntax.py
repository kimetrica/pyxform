'''
Created on May 8, 2015

@author: esmail
'''


import unittest
import zipfile

from .pyxform_test_case import PyxformTestCase
from ..constants import ACTUAL_DEFAULT_LANGUAGE
from ..spss import (
                    survey_to_spss_label_syntaxes,
                    survey_to_spss_label_zip,
)

class TestSpssLabelSyntax(PyxformTestCase):

    def setUp(self):
        md= \
        '''
        | survey  |                    |       |                    |                            |
        |         | type               | name  | label              | label:English              |
        |         | text               | q1    | Q1                 | Q1 English                 |
        |         | integer            | q2    | Q2                 |                            |
        |         | decimal            | q3    |                    | Q3 English                 |
        |         | select_one so      | q4    | Q4                 | Q4 English                 |
        |         | select_multiple sm | q5    | Q5                 | Q5 English                 |
        |         |                    |       |                    |                            |
        | choices |                    |       |                    |                            |
        |         | list name          | name  | label              | label:English              |
        |         | so                 | so_o1 | Select one O1      | Select one O1 English      |
        |         | so                 | so_o2 | Select one O2      |                            |
        |         | so                 | so_o3 |                    | Select one O3 English      |
        |         | sm                 | sm_o1 | Select multiple O1 |                            |
        |         | sm                 | sm_o2 |                    | Select multiple O2 English |
        '''

        self.survey = self.md_to_pyxform_survey(md)

    def test_spss_label_syntaxes_generation(self, spss_label_syntaxes=None):
        if not spss_label_syntaxes:
            spss_label_syntaxes= survey_to_spss_label_syntaxes(self.survey)

        languages= spss_label_syntaxes.keys()
        self.assertSetEqual(set(languages), {'English', ACTUAL_DEFAULT_LANGUAGE})

        english_label_syntax= spss_label_syntaxes['English']
        self.assertRegexpMatches(english_label_syntax, 'q1\s+"Q1 English"')
        self.assertNotIn('Q2', english_label_syntax)
        self.assertRegexpMatches(english_label_syntax, 'q3\s+"Q3 English"')
        self.assertRegexpMatches(english_label_syntax, ''''so_o1'\s+"Select one O1 English"''')

        default_label_syntax= spss_label_syntaxes[ACTUAL_DEFAULT_LANGUAGE]
        self.assertRegexpMatches(default_label_syntax, 'q1\s+"Q1"')
        self.assertRegexpMatches(default_label_syntax, 'q2\s+"Q2"')
        self.assertNotIn('Q3', default_label_syntax)
        self.assertRegexpMatches(default_label_syntax, ''''so_o1'\s+"Select one O1"''')

    def test_spss_label_zip_generation(self):
        spss_label_syntaxes= dict()
        base_name= 'some_base_name'
        zip_io= survey_to_spss_label_zip(self.survey, base_name)
        with zipfile.ZipFile(zip_io) as label_zipfile:
            languages= [ACTUAL_DEFAULT_LANGUAGE, 'English']
            for lang in languages:
                syntax_filename= '{}_{}_labels.sps'.format(base_name, lang)
                with label_zipfile.open(syntax_filename) as syntax_file:
                    spss_label_syntaxes[lang]= syntax_file.read()

        self.test_spss_label_syntaxes_generation(spss_label_syntaxes)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
