'''
Created on Dec 9, 2014

@author: esmail
'''


from __future__ import absolute_import
from collections import OrderedDict

from .. import constants
from .. import question
from .. import aliases
from ..survey import Survey
from ..section import Section


def get_label_mappings(survey, path_prefixes=False, path_delimiter='/'):
    '''
    Generate dictionaries mapping question and option names to their labels/
    label dictionaries.

    :param pyxform.survey.Survey survey: The survey from which to get the labels.
    :param bool path_prefixes: Flag indicating whether or not to use group/section
        path prefixes when storing question and option names.
    :param str path_delimiter: Delimiter to insert after path prefix elements.
    :return: Question label mappings (e.g. {question_name: question_label_dict}).
    :rtype: dict
    :return: Option label mappings.
    :rtype: dict
    :return: The set of all languages used in the labels.
    :rtype: set
    '''

    question_label_mappings= OrderedDict()
    option_label_mappings= OrderedDict()
    label_languages= set()


    def get_label_mappings_0(survey_element, current_prefix=''):
        '''
        Do the work of generating the label mappings, recurring down into groups
        and sections.

        :param pyxform.survey_element.SurveyElement survey_element: The element
            to get the labels for or recur into.
        :param str current_prefix: The path prefix, if any, of the current element.
        '''

        # If a name prefix was passed in, append a trailing delimiter before adding to it.
        if current_prefix != '':
            current_prefix= current_prefix + path_delimiter

        # Recur into sections.
        if isinstance(survey_element, (Survey, Section) ):
            group_path= current_prefix + survey_element[constants.NAME]
            for child_element in survey_element.get('children', []):
                get_label_mappings_0(child_element, current_prefix=group_path)

        # Get label(s) associated with a question.
        elif isinstance(survey_element, question.Question):
            # Construct the question name including "path" prefix, if necessary.
            question_name= current_prefix if path_prefixes else ''
            question_name+= survey_element[constants.NAME]
            question_name.encode('UTF-8')
            question_labels= survey_element.get(constants.LABEL)

            # Record the question's label(s) and associated language(s), if any.
            question_labels_dict= dict() # Must exist, even if empty, for below.
            if question_labels:
                if isinstance(question_labels, basestring):
                    question_labels_dict[constants.ACTUAL_DEFAULT_LANGUAGE]= question_labels
                elif isinstance(question_labels, dict):
                    question_labels_dict= question_labels
                else:
                    raise Exception('Unexpected question label type: {}.'.format(type(question_labels)))

                question_label_mappings[question_name]= question_labels_dict
                label_languages.update(question_labels_dict.keys())

            # Get labels associated with multiple-choice questions.
            if isinstance(survey_element, question.MultipleChoiceQuestion):
                question_options_map= OrderedDict()
                for option in survey_element.get('children', []):
                    option_name= option[constants.NAME].encode('UTF-8')
                    option_labels= option.get(constants.LABEL)

                    # Record the option's label(s) and associated language(s), if any.
                    if option_labels:
                        if isinstance(option_labels, basestring):
                            option_labels_dict= {constants.ACTUAL_DEFAULT_LANGUAGE: option_labels}
                        elif isinstance(option_labels, dict):
                            option_labels_dict= option_labels
                        else:
                            raise Exception('Unexpected option label type: {}.'.format(type(option_labels)))

                    question_options_map[option_name]= option_labels_dict
                    label_languages.update(option_labels_dict.keys())

                if aliases.get_xform_question_type(survey_element[constants.TYPE]) == constants.SELECT_ONE_XFORM:
                    if question_options_map:
                        option_label_mappings[question_name]= question_options_map
                elif aliases.get_xform_question_type(survey_element[constants.TYPE]) == constants.SELECT_ALL_THAT_APPLY_XFORM:
                    # Multi-select question. Record a separate question corresponding to each option and skip labeling the options.
                    for language in label_languages:
                        for option_name, option_labels_dict in question_options_map.iteritems():
                            if (language in question_labels_dict) or (language in option_labels_dict):
                                multi_select_question_name= question_name + path_delimiter + option_name
                                multi_select_question_label= question_labels_dict.get(language, question_name) + ' :: ' + option_labels_dict.get(language, option_name)
                                question_label_mappings.setdefault(multi_select_question_name, dict())[language]= multi_select_question_label
                else:
                    raise Exception('Unexpected multiple-choice question "type": {}.'.format(survey_element[constants.TYPE]))

        else:
            raise Exception('Unexpected survey element type "{}"'.format(type(survey_element)))

        return


    # Do the work.
    for survey_element in survey['children']:
        get_label_mappings_0(survey_element)

    return question_label_mappings, option_label_mappings, label_languages
