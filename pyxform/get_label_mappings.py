'''
Created on Dec 9, 2014

@author: esmail
'''


from __future__ import absolute_import 

from . import constants
from . import survey
from . import section
from . import question


# Use 'constants.DEFAULT_LANGUAGE' prohibited presumably by "ball of mud" design method.
ACTUAL_DEFAULT_LANGUAGE= u'default'

def get_label_mappings(survey_in, variable_paths=False):
    question_label_mappings= dict()
    option_label_mappings= dict()
    label_languages= set()

    def get_label_mappings_0(survey_element, variable_name_prefix=''):

        # If a name prefix was passed in, append a trailing slash before adding to it.
        if variable_name_prefix != '':
            variable_name_prefix= variable_name_prefix + '/'

        # Recur into sections.
        if isinstance(survey_element, (survey.Survey, section.Section) ):
            group_path= variable_name_prefix + survey_element[constants.NAME]
            for child_element in survey_element.get('children', []):
                get_label_mappings_0(child_element, variable_name_prefix=group_path)

        # Get label(s) associated with a question.
        elif isinstance(survey_element, question.Question):
            # Construct the question name including "path" prefix, if necessary.
            question_name= variable_name_prefix if variable_paths else ''
            question_name+= survey_element[constants.NAME]
            question_name.encode('UTF-8')
            question_labels= survey_element.get(constants.LABEL)

            # Record the question's label(s) and associated language(s), if any.
            if question_labels:
                if isinstance(question_labels, basestring):
                    label_string= question_labels
                    question_label_mappings[question_name]= {ACTUAL_DEFAULT_LANGUAGE: label_string}
                    label_languages.update([ACTUAL_DEFAULT_LANGUAGE])
                elif isinstance(question_labels, dict):
                    question_label_mappings[question_name]= question_labels
                    label_languages.update(question_labels.keys())
                else:
                    raise Exception('Unexpected question label type "{}".'.format(type(question_labels)))

            # Get labels associated with multiple-choice questions.
            if isinstance(survey_element, question.MultipleChoiceQuestion):
                question_options_map= dict()
                for option in survey_element.get('children', []):
                    option_name= option[constants.NAME].encode('UTF-8')
                    option_labels= option.get(constants.LABEL)
                    
                    # Record the option's label(s) and associated language(s), if any.
                    if option_labels:
                        if isinstance(option_labels, basestring):
                            label_string= option_labels
                            question_options_map[option_name]= {ACTUAL_DEFAULT_LANGUAGE: label_string}
                            label_languages.update([ACTUAL_DEFAULT_LANGUAGE])
                        elif isinstance(option_labels, dict):
                            question_options_map[option_name]= option_labels
                            label_languages.update(option_labels.keys())
                        else:
                            raise Exception('Unexpected option label type "{}".'.format(type(option_labels)))

                if question_options_map:
                    option_label_mappings[question_name]= question_options_map

        else:
            raise Exception('Unexpected survey element type "{}"'.format(type(survey_element)))

        return


    for survey_element in survey_in['children']:
        get_label_mappings_0(survey_element)

    return question_label_mappings, option_label_mappings, label_languages
