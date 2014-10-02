'''
Convenience functions for constructing 'Survey' objects.

.. module:: survey_from
    :Date: 2014/09/17

.. codeauthor: Esmail Fadae <esmail.fadae@kobotoolbox.org>
'''


import pyxform.xform2json
import pyxform.xls2json_backends
import pyxform.xls2json
import pyxform.builder


def xform(xform_in_path):
    '''
    Construct a 'Survey' object from an XML XForm.
    
    :param str xform_in_path: Path to the input file.
    '''
    survey= pyxform.xform2json.XFormToDictBuilder(xform_in_path).survey()
    return survey


def xls(xls_in_path):
    '''
    Construct a 'Survey' object from an XLS-formatted XLSForm.
    
    :param str xls_in_path: Path to the input file.
    '''
    
    # TODO: Import XLSForms directly to 'Survey' objects.
    # Convert the XLS to JSON then import the JSON ...such a kludge.
    workbook_dict= pyxform.xls2json_backends.xls_to_dict(xls_in_path)
    json_temp= pyxform.xls2json.workbook_to_json(workbook_dict)
    survey= pyxform.builder.create_survey_element_from_dict(json_temp)
    
    return survey


def csv(csv_in_path):
    '''
    Construct a 'Survey' object from an CSV-formatted XLSForm.
    
    :param str xls_in_path: Path to the input file.
    '''

    # TODO: Import XLSForms directly to 'Survey' objects.
    # Convert the CSV to JSON then import the JSON ...such a kludge.
    workbook_dict= pyxform.xls2json_backends.csv_to_dict(csv_in_path)
    json_temp= pyxform.xls2json.workbook_to_json(workbook_dict)
    survey= pyxform.builder.create_survey_element_from_dict(json_temp)

    return survey
