'''
Created on Dec 9, 2014

@author: esmail
'''


from collections import OrderedDict

from .. import constants
from .. import aliases
from ..errors   import PyXFormError
from ..question import MultipleChoiceQuestion
from ..question import Question
from ..survey   import Survey
from ..section  import Section

def _get_labels_dict(survey_element):
    label= survey_element.get(constants.LABEL)

    # Record the label(s) and associated language(s), if any.
    if label:
        if isinstance(label, basestring):
            labels_dict= {constants.ACTUAL_DEFAULT_LANGUAGE: label}
        elif isinstance(label, dict):
            labels_dict= label
        else:
            raise PyXFormError('Unexpected label type: {}.'.format(type(label)))
    else:
        labels_dict= dict()

    return labels_dict


def get_multiple_choice_option_labels(question):
    '''
    Retrieve a 'dict' of the option labels for a multiple-choice question.
    '''

    assert isinstance(question, MultipleChoiceQuestion)

    question_options_map= OrderedDict()
    option_label_languages= set()
    for option in question.get('children', []):
        option_name= option[constants.NAME].encode('UTF-8')
        option_labels_dict= _get_labels_dict(option)
        question_options_map[option_name]= option_labels_dict
        option_label_languages.update(option_labels_dict.keys())

    return question_options_map, option_label_languages


def get_label_mappings(survey, path_prefixes=False, path_delimiter='/'):
    '''
    Generate dictionaries mapping question and option names to their labels/
    label dictionaries.

    :param pyxform.survey.Survey survey: The survey from which to get the labels.
    :param bool path_prefixes: Flag indicating whether or not to use group/section
        path prefixes when storing question and option names (e.g. "A/A01").
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

        # If a name prefix was passed in (indicating this is a sub-element),
        #   append a trailing delimiter before adding to it.
        if current_prefix != '':
            current_prefix= current_prefix + path_delimiter

        # Recur into the survey root/sub-sections.
        if isinstance(survey_element, (Survey, Section) ):
            group_path= current_prefix + survey_element[constants.NAME]
            for child_element in survey_element.get('children', []):
                get_label_mappings_0(child_element, current_prefix=group_path)

        # Get label(s) associated with a question.
        elif isinstance(survey_element, Question):
            # Construct the question name including "path" prefix, if necessary.
            recorded_question_name= current_prefix if path_prefixes else ''
            recorded_question_name+= survey_element[constants.NAME].encode('UTF-8')
            question_labels_dict= _get_labels_dict(survey_element)
            question_label_mappings[recorded_question_name]= question_labels_dict
            label_languages.update(question_labels_dict.keys())

            # Get labels associated with multiple-choice questions' options.
            if isinstance(survey_element, MultipleChoiceQuestion):
                question_options_map, option_label_languages= get_multiple_choice_option_labels(survey_element)
                label_languages.update(option_label_languages)

                if aliases.get_xform_question_type(survey_element[constants.TYPE]) == constants.SELECT_ONE_XFORM:
                    if question_options_map:
                        option_label_mappings[recorded_question_name]= question_options_map
                elif aliases.get_xform_question_type(survey_element[constants.TYPE]) == constants.SELECT_ALL_THAT_APPLY_XFORM:
                    # FIXME: Make this optional and fully configurable.
                    # Multi-select question. Record a separate question corresponding to each option and skip labeling the options.
                    for language in label_languages:
                        for option_name, option_labels_dict in question_options_map.iteritems():
                            if (language in question_labels_dict) or (language in option_labels_dict):
                                multi_select_question_name= recorded_question_name + path_delimiter + option_name
                                multi_select_question_label= question_labels_dict.get(language, recorded_question_name) + ' :: ' + option_labels_dict.get(language, option_name)
                                question_label_mappings.setdefault(multi_select_question_name, dict())[language]= multi_select_question_label
                else:
                    raise PyXFormError('Unexpected multiple-choice question "type": {}.'.format(survey_element[constants.TYPE]))

        else:
            raise PyXFormError('Unexpected survey element type "{}"'.format(type(survey_element)))

        return


    # Do the work.
    for survey_element in survey['children']:
        get_label_mappings_0(survey_element)

    return question_label_mappings, option_label_mappings, label_languages
