'''
Export 'Survey' objects to CSV-or-XLS-formatted XLSForms.

.. module:: survey_to_spreadsheet
    :Date: 2014/09/24

.. codeauthor: Esmail Fadae <esmail.fadae@kobotoolbox.org>
'''


import base64
import re
import os

import pandas

import pyxform.question
from pyxform import constants
from pyxform.errors import PyXFormError


def _to_sheet_dfs(survey):
    '''
    Prepare a representation of the survey ready to be easily exported as a 
    XLSForm spreadsheet.
    
    :return: Spreadsheet data (in rows) keyed by sheet name.
    :rtype: {str: DataFrame}
    '''
    
    # TODO: Groups/repeats, 'or_other', hints, constraints, ...
    
    # Record the survey's settings if present.
    settings_row= dict()
    if constants.NAME in survey:
        settings_row['form_id']= survey[constants.NAME]
    if constants.TITLE in survey:
        settings_row['form_title']= survey[constants.TITLE]
    # TODO: More potential settings listed at xlsform.org.
    settings_sheet_df= pandas.DataFrame.from_dict([settings_row])
    
    survey_sheet_df= pandas.DataFrame()
    choices_sheet_df= pandas.DataFrame()
    
    # Keep track of 'label' columns.
    survey_label_columns= set()
    choices_label_columns= set()
    
    questions= survey['children']
    for q in questions:
        # Directly extract the fields from 'survey_sheet_columns' for this \
        #   question. Each row of data is stored as an individual 'dict'.
        survey_row= dict()
        
        # Mandatory column 'type'.
        if isinstance(q, pyxform.question.MultipleChoiceQuestion) and \
          ( q[constants.TYPE] in {constants.SELECT_ONE, constants.SELECT_ALL_THAT_APPLY} ):
            # Special handling for select-type questions.
            
            # TODO: Would be nice to reuse the 'list name' when encountering reused sets of choices. 
            list_name= base64.urlsafe_b64encode(os.urandom(16))
            
            # Strip out any non-alphanumeric characters so KoBoForm can import. \
            #   Decreasing the space of possible strings, while an egregious \
            #   affront, should be safe.
            list_name= re.compile('[\W_]+').sub('', list_name)
            
            if q['type'] == constants.SELECT_ONE:
                question_type_text= constants.SELECT_ONE_XLSFORM
            elif q['type'] == constants.SELECT_ALL_THAT_APPLY:
                question_type_text= constants.SELECT_ALL_THAT_APPLY_XLSFORM
            else:
                raise PyXFormError('Unexpected multiple-choice question type "{}"'.format(q['type']))
            
            survey_row[constants.TYPE]= question_type_text + ' ' + list_name
            
            # Extract and record the choices.
            choices= q[constants.CHILDREN]
            for c in choices:
                # Mandatory column 'list name'.
                choices_row= {constants.LIST_NAME: list_name}
                # Mandatory column 'name'.
                choices_row[constants.NAME]= c[constants.NAME]
                # Mandatory 'label' column(s).
                choice_labels= _get_question_or_choice_labels(c)
                choices_row.update(choice_labels)
                choices_label_columns.update(choice_labels.keys()) # Track any new label columns encountered.
                
                # Add the row into the 'choices' sheet.
                choices_sheet_df= pandas.concat([choices_sheet_df, pandas.DataFrame.from_dict([choices_row])])
                
                
        # Non-select questions
        elif q[constants.TYPE] in set(constants.XLSFORM_TYPES).union(constants.XLSFORM_METADATA_TYPES):
            survey_row[constants.TYPE]= q[constants.TYPE]
        elif q[constants.TYPE] in constants.XFORM_TO_XLSFORM_TYPES:
            survey_row[constants.TYPE]= constants.XFORM_TO_XLSFORM_TYPES[q[constants.TYPE]]
        else:
            raise PyXFormError('Unexpected XLSForm type "{}".'.format(q[constants.TYPE]))
        
        # Mandatory column 'name'.
        survey_row[constants.NAME]= q[constants.NAME]
        
        # Mandatory 'label' column(s).
        question_labels= _get_question_or_choice_labels(q)
        survey_row.update(question_labels)
        survey_label_columns.update(question_labels.keys()) # Track any new label columns encountered.
        
        # Add the row into the 'survey' sheet.
        survey_sheet_df= pandas.concat([survey_sheet_df, pandas.DataFrame.from_dict([survey_row])])
    
    # If only one translation, rename translated label column (e.g. \
    #   'label::English') to 'label'.
    if len(survey_label_columns) == 1:
        survey_sheet_df.rename( \
          columns={survey_label_columns.pop(): constants.LABEL}, inplace=True)
    if len(choices_label_columns) == 1:
        choices_sheet_df.rename( \
          columns={choices_label_columns.pop(): constants.LABEL}, inplace=True)
    
    sheet_dfs= dict()
    if len(settings_sheet_df):
        sheet_dfs[constants.SETTINGS]= settings_sheet_df
    if len(survey_sheet_df):
        sheet_dfs[constants.SURVEY]= survey_sheet_df
    if len(choices_sheet_df):
        sheet_dfs[constants.CHOICES]= choices_sheet_df
    
    return sheet_dfs


def _get_question_or_choice_labels(question_or_choice):
    '''
    Return a dictionary containing the question/choice's singular label or its 
    translations, if present, ready for export to an XLSForm. Labels are keyed 
    by 'label' or 'label::Language'.
    
    :return: Spreadsheet data (in rows) keyed by sheet name.
    :rtype: {str: DataFrame}
    '''
    
    labels= dict()
    if isinstance(question_or_choice.get(constants.LABEL), basestring) \
      and (question_or_choice[constants.LABEL] != ''):
        # Simple label.
        label_column= constants.LABEL
        labels[label_column]= question_or_choice[constants.LABEL]
    elif question_or_choice.get(constants.LABEL):
        # Label(s) provided in a 'dict' of translations.
        for language in question_or_choice[constants.LABEL].iterkeys():
            label_column= constants.LABEL + '::' + language
            labels[label_column]= question_or_choice[constants.LABEL][language]
    
    return labels
    

def to_xls(survey, out_file_path):
    '''
    Convert the provided survey to a XLS-encoded XForm.
    
    :param pyxform.survey.Survey survey:
    :param str out_file_path: Filesystem path to the desired output file.
    '''
    
    # Organize the data for spreadsheet output.
    sheet_dfs= _to_sheet_dfs(survey)
    
    xls_writer= pandas.ExcelWriter(out_file_path, encoding='UTF-8')
    for sheet_name, df in sheet_dfs.iteritems():
        df.to_excel(xls_writer, sheet_name, index=False)
         
    xls_writer.save()

       
def to_csv(survey, out_file_path):
    '''
    Convert the provided survey to a CSV-formatted XForm.
    
    :param pyxform.survey.Survey survey:
    :param str out_file_path: Filesystem path to the desired output file.
    '''
    
    # Organize the data for spreadsheet output.
    sheet_dfs= _to_sheet_dfs(survey)
    
    csv_buffer= str()
    for sheet_name, df in sheet_dfs.iteritems():
        # Prepend a row of the column names into the sheet.
        csv_df= pandas.concat([pandas.DataFrame(df.columns.to_series()).T, df])
        # Insert column for the sheet name into the sheet and put the name in the first row.
        csv_df= pandas.concat([pandas.DataFrame.from_dict([{'sheet': sheet_name}]), csv_df])
        # Move the 'sheet' column to the front.
        csv_df= csv_df[['sheet']+csv_df.columns.drop('sheet').tolist()]
        
        csv_buffer+= csv_df.to_csv(header=False, index=False, encoding='UTF-8')

    with open(out_file_path,'w') as f:
        f.write(csv_buffer)
        
