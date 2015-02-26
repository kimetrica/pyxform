from pyxform import constants as C
from pyxform.question_type_dictionary import QUESTION_TYPE_DICT
from pyxform.errors import PyXFormError

# Aliases:
# Ideally aliases should resolve to elements in the json form schema

# select, control and settings alias keys used for parsing,
# which is why self mapped keys are necessary.

control = {
    C.GROUP: C.GROUP,
    u"lgroup": C.REPEAT,
    C.REPEAT: C.REPEAT,
    C.LOOP: C.LOOP,
    u"looped group": C.REPEAT
}

select1= {
    C.SELECT_ONE:                               C.SELECT_ONE,
    C.SELECT_ONE_XLSFORM:                       C.SELECT_ONE,
    C.SELECT_ONE_XFORM:                         C.SELECT_ONE, # KoBoForm.
    C.SELECT_ONE + u" from":                    C.SELECT_ONE,
    u"add " + C.SELECT_ONE + u" prompt using":  C.SELECT_ONE,
}

select= {
  C.SELECT_ALL_THAT_APPLY:            C.SELECT_ALL_THAT_APPLY,
  C.SELECT_ALL_THAT_APPLY_XLSFORM:    C.SELECT_ALL_THAT_APPLY,
  C.SELECT_ALL_THAT_APPLY_XFORM:      C.SELECT_ALL_THAT_APPLY,
  C.SELECT_ALL_THAT_APPLY + u" from": C.SELECT_ALL_THAT_APPLY,
  u"add select multiple prompt using":        C.SELECT_ALL_THAT_APPLY,
}

multiple_choice = {u"select_one_external": u"select one external"}
multiple_choice.update(select1)
multiple_choice.update(select)

cascading = {
    u'cascading select': C.CASCADING_SELECT,
    C.CASCADING_SELECT: C.CASCADING_SELECT,
}

settings_header = {
    u"form_title": C.TITLE,
    u"set form title": C.TITLE,
    u"form_id": C.ID_STRING,
    C.SMS_KEYWORD: C.SMS_KEYWORD,
    C.SMS_SEPARATOR: C.SMS_SEPARATOR,
    C.SMS_ALLOW_MEDIA: C.SMS_ALLOW_MEDIA,
    C.SMS_DATE_FORMAT: C.SMS_DATE_FORMAT,
    C.SMS_DATETIME_FORMAT: C.SMS_DATETIME_FORMAT,
    u"set form id": C.ID_STRING,
    C.PUBLIC_KEY: C.PUBLIC_KEY,
    C.SUBMISSION_URL: C.SUBMISSION_URL
}


# TODO: Check on bind prefix approach in json.
# Conversion dictionary from user friendly column names to meaningful values
survey_header = {
    u"Label": C.LABEL,
    u"Name": C.NAME,
    u"SMS Field": C.SMS_FIELD,
    u"SMS Option": C.SMS_OPTION,
    u"SMS Sepatator": C.SMS_SEPARATOR,
    u"SMS Allow Media": C.SMS_ALLOW_MEDIA,
    u"SMS Date Format": C.SMS_DATE_FORMAT,
    u"SMS DateTime Format": C.SMS_DATETIME_FORMAT,
    u"SMS Response": C.SMS_RESPONSE,
    u"Type": C.TYPE,
    u"List_name": u"list_name",
    u"repeat_count": u"jr:count",
    u"read_only": C.BIND + u"::readonly",
    u"readonly": C.BIND + u"::readonly",
    u"relevant": C.BIND + u"::relevant",
    u"caption": C.LABEL,
    C.APPEARANCE: C.CONTROL + u"::" + C.APPEARANCE,  # TODO: this is also an issue
    u"relevance": C.BIND + u"nd::relevant",
    u"required": C.BIND + u"::required",
    u"constraint": C.BIND + u"::constraint",
    u"constraining message": C.BIND + u"::jr:constraintMsg",
    u"constraint message": C.BIND + u"::jr:constraintMsg",
    u"constraint_message": C.BIND + u"::jr:constraintMsg",
    u"calculation": C.BIND + u"::" + C.CALCULATE_XFORM,
    u"command": C.TYPE,
    u"tag": C.NAME,
    u"value": C.NAME,
    C.IMAGE_XLSFORM: C.MEDIA + u"::" + C.IMAGE_XLSFORM,
    C.AUDIO_XLSFORM: C.MEDIA + u"::" + C.AUDIO_XLSFORM,
    C.VIDEO_XLSFORM: C.MEDIA + u"::" + C.VIDEO_XLSFORM,
    u"count": C.CONTROL + u"::jr:count",
    u"repeat_count": C.CONTROL + u"::jr:count",
    u"jr:count": C.CONTROL + u"::jr:count",
    u"autoplay": C.CONTROL + u"::autoplay",
    u"rows": C.CONTROL + u"::rows",
    # New elements that have to go into itext elements:
    u"noAppErrorString": C.BIND + u"::jr:noAppErrorString",
    u"no_app_error_string": C.BIND + u"::jr:noAppErrorString",
    u"requiredMsg": C.BIND + u"::jr:requiredMsg",
    u"required_message": C.BIND + u"::jr:requiredMsg",
    C.BODY_XFORM: C.CONTROL,
}

list_header = {
    u"caption": C.LABEL,
    u"list_name": C.LIST_NAME,
    u"value": C.NAME,
    C.IMAGE_XLSFORM: C.MEDIA + u"::" + C.IMAGE_XLSFORM,
    C.AUDIO_XLSFORM: C.MEDIA + u"::" + C.AUDIO_XLSFORM,
    C.VIDEO_XLSFORM: C.MEDIA + u"::" + C.VIDEO_XLSFORM,
}
# Note that most of the type aliasing happens in all.xls
type = {
    u"imei": C.DEVICEID_XLSFORM,
    C.IMAGE_XLSFORM: u"photo",
    u"add " + C.IMAGE_XLSFORM + u" prompt": u"photo",
    u"add photo prompt": u"photo",
    u"add " + C.AUDIO_XLSFORM + u" prompt": C.AUDIO_XLSFORM,
    u"add " + C.VIDEO_XLSFORM + u" prompt": C.VIDEO_XLSFORM,
}

yes_no = {
    "yes": True,
    "Yes": True,
    "YES": True,
    "true": True,
    "True": True,
    "TRUE": True,
    "true()": True,
    "no": False,
    "No": False,
    "NO": False,
    "false": False,
    "False": False,
    "FALSE": False,
    "false()": False,
}

label_optional_types = [
    C.DEVICEID_XLSFORM,
    C.PHONENUMBER_XLSFORM,
    C.SIMSERIAL_XLSFORM,
    C.CALCULATE_XFORM, # Not 'C.CALCULATE_XLSFORM'?
    C.START_XLSFORM,
    C.END_XLSFORM,
    C.TODAY_XLSFORM,
]


def get_xform_question_type(original_question_type_str):
    '''
    Determine the XForm-compatible question type that corresponds to the given type.

    :param str original_question_type_str:
    :return: An XForm-compatible question type.
    :rtype: str
    '''

    xform_question_type_str= None

    # Strip off the "xsd:" prefix, if present.
    if original_question_type_str.startswith('xsd:'):
        question_type_str= original_question_type_str.split('xsd:')[-1]
    else:
        question_type_str= original_question_type_str

    if question_type_str in select1:
        xform_question_type_str= C.SELECT_ONE_XFORM
    elif question_type_str in select:
        xform_question_type_str= C.SELECT_ALL_THAT_APPLY_XFORM
    elif question_type_str in C.XFORM_TYPES:
        # The question type is already valid for use in an XForm.
        xform_question_type_str= question_type_str

    elif question_type_str in C.XLSFORM_TO_XFORM_TYPES:
        # The question type is an XLSForm type with a known XForm equivalent.
        xform_question_type_str= C.XLSFORM_TO_XFORM_TYPES[question_type_str]

    elif question_type_str in QUESTION_TYPE_DICT:
        # The question type is a known type possibly with an XForm equivalent.
        possible_xform_question_type= \
          QUESTION_TYPE_DICT[question_type_str][C.BIND][C.TYPE]
        if possible_xform_question_type in C.XFORM_TYPES:
            xform_question_type_str= possible_xform_question_type
    elif question_type_str == C.GROUP:
        xform_question_type_str= question_type_str

    if not xform_question_type_str:
        raise PyXFormError('Could not find XForm equivalent of type "{}".'.format(question_type_str))

    return xform_question_type_str


def get_xlsform_question_type(original_question_type_str):
    '''
    Determine the XLSForm-compatible question type that corresponds to the given type.

    :param str original_question_type_str:
    :return: An XLSForm-compatible question type.
    :rtype: str
    '''


    xlsform_question_type_str= None

    if original_question_type_str in set(C.XLSFORM_TYPES).union(C.XLSFORM_METADATA_TYPES):
        # The question type is already valid for use in an XLSForm.
        xlsform_question_type_str= original_question_type_str


    elif original_question_type_str in C.XFORM_TO_XLSFORM_TYPES:
        # The question type is an XForm type with a known XLSForm equivalent.
        xlsform_question_type_str= C.XFORM_TO_XLSFORM_TYPES[original_question_type_str]

    elif original_question_type_str == C.GROUP:
        xlsform_question_type_str= original_question_type_str
    else:
        # FIXME: This wouldn't be necessary if 'Question' internally standardized \
        #   to use types from the XForm (or alternatively XLSForm) spec.
        xform_question_type= get_xform_question_type(original_question_type_str)
        if xform_question_type in C.XFORM_TO_XLSFORM_TYPES:
            xlsform_question_type_str= C.XFORM_TO_XLSFORM_TYPES[xform_question_type]

    if not xlsform_question_type_str:
        raise PyXFormError('Could not find XLSForm equivalent of type "{}".'.format(original_question_type_str))
    else:
        return xlsform_question_type_str
