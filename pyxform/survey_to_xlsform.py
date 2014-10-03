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
import pyxform.aliases
from pyxform import constants
from pyxform.errors import PyXFormError


class XlsFormExporter():
    
    def __init__(self, survey):
        '''
        Prepare a representation of the survey ready to be easily exported as a 
        XLSForm spreadsheet.

        :param pyxform.survey.Survey survey: The survey to be exported.
        '''
        
        # TODO: Repeats, 'or_other', hints, constraints, ...
        
        self.survey_sheet_df= pandas.DataFrame()
        self.choices_sheet_df= pandas.DataFrame()
        self.settings_sheet_df= pandas.DataFrame()

        # Keep track of 'label' columns.
        self.survey_label_columns= set()
        self.choices_label_columns= set()
        
        self.record_settings(survey)
        
        for survey_child in survey['children']:
            if isinstance(survey_child, pyxform.question.Question):
                self.record_question_data(survey_child)
            elif isinstance(survey_child, pyxform.section.GroupedSection):
                self.record_grouped_section(survey_child)
            else:
                raise PyXFormError('Unexpected survey child type "{}".'.format(type(survey_child)))
        
        self.sheet_dfs= {
          constants.SURVEY:     self.survey_sheet_df,
          constants.CHOICES:    self.choices_sheet_df,
          constants.SETTINGS:   self.settings_sheet_df,
        }


    def record_question_data(self, question):
        '''
        Record the given question and any associated data such as the options 
        for multiple-choice questions.
        
        :param pyxform.question.Question question:
        '''
        
        # Buffer the question's eventual additions to the 'survey' sheet.
        survey_row= dict()
        
        question_name= question[constants.NAME]
        xlsform_question_type= pyxform.aliases.get_xlsform_question_type(question[constants.TYPE])
        
        if isinstance(question, pyxform.question.MultipleChoiceQuestion):
            # Special handling for select-type questions.
            
            # Check that the reported 'type' matches the object type.
            if xlsform_question_type not in \
              [constants.SELECT_ONE_XLSFORM, constants.SELECT_ALL_THAT_APPLY_XLSFORM]:
                raise PyXFormError('Unexpected multiple-choice question type "{}"'.format(question['type']))
            
            
            # TODO: Would be nice to reuse the 'list name' when encountering reused sets of choices.
            # Generate a 'list name' comprised of the question name followed by 8 random bytes cast to string.
            list_name= question_name + '_' + base64.urlsafe_b64encode(os.urandom(8))
            
            # Strip out any non-alphanumeric characters so KoBoForm can import. \
            #   Decreasing the space of possible strings, while an egregious \
            #   affront, should be safe.
            list_name= re.compile('[\W_]+').sub('_', list_name)
            
            survey_row[constants.TYPE]= xlsform_question_type + ' ' + list_name
            
            # TODO: Handle cascading-select questions (http://opendatakit.github.io/odk-xform-spec/#secondary-instances).
            # If the question appears to be a cascading-select, report in the \
            #   output that the question choices could not be gathered.
            if question.get(constants.ITEMSET_XFORM):
                manual_sad_choice_row= \
                  {constants.LIST_NAME: list_name,
                   constants.NAME: 'question_choices_not_imported',
                   constants.LABEL: 'Apologies, your choices for this (cascading-select) question could not be automatically imported.'
                   }
                self.choices_sheet_df= pandas.concat([self.choices_sheet_df, pandas.DataFrame.from_dict([manual_sad_choice_row])])
                
            else:
                # Extract and record the choices.
                for question_choice in question[constants.CHILDREN]:
                    self.record_question_choice(question_choice, list_name)
            
        # Non-select questions
        else:
            survey_row[constants.TYPE]= xlsform_question_type

        # Mandatory column 'name'.
        survey_row[constants.NAME]= question_name
        
        # Mandatory 'label' column(s).
        question_labels= self._get_question_or_choice_labels(question)
        survey_row.update(question_labels)
        self.survey_label_columns.update(question_labels.keys()) # Track any new label columns encountered.

        if xlsform_question_type == constants.CALCULATE_XLSFORM:
            survey_row['calculation']= question[constants.BIND][constants.CALCULATE_XLSFORM]

        # Add the row into the 'survey' sheet.
        self.survey_sheet_df= pandas.concat([self.survey_sheet_df, pandas.DataFrame.from_dict([survey_row])])


    def record_question_choice(self, question_choice, list_name):
        '''
        Record the 
        '''
        # Mandatory column 'list name'.
        choices_row= {constants.LIST_NAME: list_name}
        # Mandatory column 'name'.
        choices_row[constants.NAME]= question_choice[constants.NAME]
        # Mandatory 'label' column(s).
        choice_labels= self._get_question_or_choice_labels(question_choice)
        choices_row.update(choice_labels)
        
        # Track any new label columns (translations like 'label::English') encountered.
        self.choices_label_columns.update(choice_labels.keys())
        
        # Add the row into the 'choices' sheet.
        self.choices_sheet_df= pandas.concat([self.choices_sheet_df, pandas.DataFrame.from_dict([choices_row])])
        

    def record_grouped_section(self, grouped_section):
        '''
        Record the data associated with a group of questions.
        
        :param 
        '''
        
        # Record the question group and return.
        
        if grouped_section[constants.NAME] == constants.META_XFORM:
            # Do not export the 'meta' group.
            return
        
        # Generate and insert the group's header.
        group_header= {constants.TYPE: u'begin group'}
        if constants.NAME in grouped_section:
            group_header[constants.NAME]= grouped_section[constants.NAME]
        if constants.LABEL in grouped_section:
            question_labels= self._get_question_or_choice_labels(grouped_section)
            group_header.update(question_labels)
        self.survey_sheet_df= pandas.concat([self.survey_sheet_df, pandas.DataFrame.from_dict([group_header])])
        
        # Insert the grouped questions.
        for question in grouped_section['children']:
            self.record_question_data(question)
        
        # Insert the group's footer.
        group_footer= {constants.TYPE: u'end group'}
        self.survey_sheet_df= pandas.concat([self.survey_sheet_df, pandas.DataFrame.from_dict([group_footer])])


    def record_settings(self, survey):
        # Record the survey's settings if present.
        # TODO: More potential settings listed at xlsform.org.
        if constants.NAME in survey:
            self.settings_sheet_df['form_id']= [survey[constants.NAME]]
        if constants.TITLE in survey:
            self.settings_sheet_df['form_title']= [survey[constants.TITLE]]


    @staticmethod
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
    sheet_dfs= XlsFormExporter(survey).sheet_dfs
    
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
    sheet_dfs= XlsFormExporter(survey).sheet_dfs
    
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
        
