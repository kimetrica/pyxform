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


XFORM_IMPORT_WARNING= 'XForm imports are not fully supported. Please check the correctness of the resulting survey.'


def xform(path=None, filelike_obj=None, warnings=None):
    '''
    Construct a 'Survey' object from an XML XForm.
    
    :param str path: Optional path to the input file.
    :param filelike_obj: Optional file-like object from which to import the survey.
    :type filelike_obj: file or StringIO.StringIO or other type supported by lxml.etree.parse().
    :param list warnings: Optional list into which any warnings generated during import will be appended.
    :rtype: pyxform.survey.Survey
    '''

    if isinstance(warnings, list):
        warnings.append(XFORM_IMPORT_WARNING)
    
    # TODO: Implement warnings in 'XFormToDictBuilder' for un/partially-supported form elements.
    survey= pyxform.xform2json.XFormToDictBuilder(path=path, filelike_obj=filelike_obj).survey()
    return survey


def xls(path=None, filelike_obj=None, warnings=None):
    '''
    Construct a 'Survey' object from an XLS-formatted XLSForm.
    
    :param str path: Path to the input file.
    :param filelike_obj: Optional file-like object from which to import the survey.
    :type filelike_obj: file or StringIO.StringIO or other type supported by lxml.etree.parse().
    :param list warnings: Optional list into which any warnings generated during import will be appended.
    :rtype: pyxform.survey.Survey
    '''
    
    # TODO: Import XLSForms directly to 'Survey' objects.
    # Convert the XLS to JSON then import the JSON ...such a kludge.
    workbook_dict= pyxform.xls2json_backends.xls_to_dict(path)
    json_temp= pyxform.xls2json.workbook_to_json(workbook_dict, warnings=warnings)
    survey= pyxform.builder.create_survey_element_from_dict(json_temp)
    
    return survey


def csv(path=None, filey_obj=None, warnings=None):
    '''
    Construct a 'Survey' object from an CSV-formatted XLSForm.
    
    :param str xls_in_path: Path to the input file.
    :param list warnings: Optional list into which any warnings generated during import will be appended.
    :rtype: pyxform.survey.Survey
    '''

    # TODO: Import XLSForms directly to 'Survey' objects.
    # Convert the CSV to JSON then import the JSON ...such a kludge.
    workbook_dict= pyxform.xls2json_backends.csv_to_dict(path)
    json_temp= pyxform.xls2json.workbook_to_json(workbook_dict, warnings=warnings)
    survey= pyxform.builder.create_survey_element_from_dict(json_temp)

    return survey
