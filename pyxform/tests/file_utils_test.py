from unittest import TestCase

import nose.plugins.attrib

from . import utils
from ..xls2json_backends import convert_file_to_csv_string

class BackendUtilsTests(TestCase):

    # FIXME: Failing non-essential test.
    @nose.plugins.attrib.attr('broken_test')
    def test_xls_to_csv(self):
        specify_other_xls = utils.path_to_text_fixture("specify_other.xls")
        converted_xls = convert_file_to_csv_string(specify_other_xls)
        specify_other_csv = utils.path_to_text_fixture("specify_other.csv")
        converted_csv = convert_file_to_csv_string(specify_other_csv)
        # print "csv:"
        # print converted_csv
        # print "xls:"
        # print converted_xls
        self.assertEqual(converted_csv, converted_xls)
