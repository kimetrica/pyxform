'''
Created on Feb 23, 2015

@author: esmail
'''


from __future__ import unicode_literals
import re

SPSS_SYNTAX_FILE_LINE_BYTE_LIMIT= 250
SPSS_VARIABLE_NAME_BYTE_LIMIT= 64
SPSS_VARIABLE_LABEL_BYTE_LIMIT= 256
SPSS_VALUE_LABEL_BYTE_LIMIT= 120
INDENT_STRING= '\t'


def truncate_string(original_string, byte_limit):

    if len(original_string.encode('UTF-8')) <= byte_limit:
        # No truncation necessary.
        return original_string

    assert isinstance(byte_limit, int)

    # The max. number of characters we could potentially keep is the byte
    #  limit, in the case where each character can be encoded as a single byte.
    string_cutoff= byte_limit

    # Truncate the string one character at a time until we're within the limit.
    truncated_string= original_string[:string_cutoff]
    while len(truncated_string.encode('UTF-8')) > byte_limit:
        truncated_string= truncated_string[:-1]

    return truncated_string


def get_spss_variable_name(variable_name):
    '''
    A helper function to convert the provided variable name into an SPSS-compatible one.
    For details, see http://www-01.ibm.com/support/knowledgecenter/SSLVMB_22.0.0/com.ibm.spss.statistics.help/spss/base/dataedit_variable_names.htm.

    :param str variable_name: The variable name to be converted.
    :return: An SPSS-compatible version of the variable name.
    :rtype: str
    '''

    # Remove any slash or space characters.
    spss_variable_name= variable_name.replace('/', '')
    spss_variable_name= spss_variable_name.replace(' ', '')

    # Prepend a "@" character to the variable name if its first character is not legal.
    first_character= spss_variable_name[0]
    if (not first_character.decode('UTF-8').isalpha()) and (first_character != '@'):
        spss_variable_name= '@' + spss_variable_name

    # Remove any trailing underscore characters.
    spss_variable_name= spss_variable_name.rstrip('_')

    # Truncate the name to 64 bytes. Assuming will be used with SPSS in Unicode mode (dangerous?).
    spss_variable_name= truncate_string(spss_variable_name, SPSS_VARIABLE_NAME_BYTE_LIMIT)

    return spss_variable_name


def get_spss_label(label, max_byte_length):
    # Replace characters that result in a new line with a space character.
    result= re.compile(r'[\n\r\f\v]').sub(' ', label)

    # Pre-emptively truncate.
    result= truncate_string(result, max_byte_length)

    # Account for and execute the necessary doubling of double quotes.
    double_quote_count= result.count('"')
    pre_doubling_byte_limit= max_byte_length - (double_quote_count * len('"'.encode('UTF-8')))
    result= truncate_string(result, pre_doubling_byte_limit).replace('"', '""')

    return result
