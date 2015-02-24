'''
Created on Jan 21, 2015

@author: esmail
'''


from __future__ import absolute_import

from .. import constants
from .. import aliases
from ..question import Question
from ..question import MultipleChoiceQuestion
from ..question import Option
from ..survey import Survey
from ..section import Section


# TODO: Factor out a general 'get_body_elements' function and use it for getting questions/groups/repeats (/sections?)
def get_questions(survey, desired_python_type=None, desired_xform_type=None):
    # Force 'desired_xform_type' to be a list.
    if isinstance(desired_xform_type, basestring):
        desired_xform_type= set(desired_xform_type)

    questions= list()

    def get_questions_0(survey_element):
        if isinstance(survey_element, Question):
            if desired_python_type and not isinstance(survey_element, desired_python_type):
                pass
            elif desired_xform_type and not (aliases.get_xform_question_type(survey_element.get(constants.TYPE)) in desired_xform_type):
                pass
            else:
                questions.append(survey_element)

        elif isinstance(survey_element, (Survey, Section)):
            for child_element in survey_element[constants.CHILDREN]:
                get_questions_0(child_element)
        else:
            raise Exception('Unexpected element type "{}".'.format(type(survey_element)))

    get_questions_0(survey)

    return questions


def get_multiselect_questions(survey):
    multiselect_questions= get_questions(survey, desired_python_type=MultipleChoiceQuestion, 
      desired_xform_type=constants.SELECT_ALL_THAT_APPLY_XFORM)

    return multiselect_questions


def get_select_one_questions(survey):
    select_one_questions=  get_questions(survey, desired_python_type=MultipleChoiceQuestion, 
      desired_xform_type=constants.SELECT_ONE_XFORM)

    return select_one_questions


def get_multiple_choice_question_options(multiple_choice_question):
    options= list()
    for child in multiple_choice_question.get(constants.CHILDREN):
        if isinstance(child, Option):
            options.append(child)

    return options
