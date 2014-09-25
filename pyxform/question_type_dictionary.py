from xls2json import QuestionTypesReader, print_pyobj_to_json
from pyxform import constants

def generate_new_dict():
    """
    This is just here incase there is ever any need to generate the question type dictionary from all.xls again.
    It shouldn't be called as part of any application.
    """
    path_to_question_types = "/home/nathan/aptana-workspace/pyxform/pyxform/question_types/all.xls"
    json_dict = QuestionTypesReader(path_to_question_types).to_json_dict()
    print_pyobj_to_json(json_dict, 'new_quesiton_type_dict.json')


_SELECT_1_TYPE_DICT= {
    "control": {
        "tag": constants.SELECT_ONE_XFORM
    }, 
    "bind": {
        "type": constants.SELECT_ONE_XFORM
    }
}

_SELECT_TYPE_DICT= {
    "control": {
        "tag": constants.SELECT_ALL_THAT_APPLY_XFORM
    }, 
    "bind": {
        "type": constants.SELECT_ALL_THAT_APPLY_XFORM
    }
}

_IMAGE_TYPE= {
    "control": {
        "tag": "upload",
        "mediatype": "image/*"
    }, 
    "bind": {
        "type": constants.BINARY_XFORM
    }
}

_VIDEO_TYPE= {
    "control": {
        "tag": "upload", 
        "mediatype": "video/*"
    }, 
    "bind": {
        "type": constants.BINARY_XFORM
    }
}

_AUDIO_TYPE= {
    "control": {
        "tag": "upload", 
        "mediatype": "audio/*"
    }, 
    "bind": {
        "type": constants.BINARY_XFORM
    }
}

_DATE_TYPE= {
    "control": {
        "tag": "input"
    }, 
    "bind": {
        "type": constants.DATE_XFORM
    }
}

_DATETIME_TYPE= {
    "control": {
        "tag": "input"
    }, 
    "bind": {
        "type": constants.DATETIME_XFORM
    }
}

_GEOPOINT_TYPE= {
    "control": {
        "tag": "input"
    }, 
    "bind": {
        "type": constants.GEOPOINT_XFORM
    }
}

_GEOPOINT_TYPE_W_HINT= dict(_GEOPOINT_TYPE, \
    **{"hint": "GPS coordinates can only be collected when outside."})

_GEOSHAPE_TYPE= {
    "control": {
        "tag": "input"
    }, 
    "bind": {
        "type": constants.GEOSHAPE_XFORM
    }
}

_GEOSHAPE_TYPE_W_HINT= dict(_GEOSHAPE_TYPE, \
            **{"hint": "GPS coordinates can only be collected when outside."})

_GEOTRACE_TYPE= {
    "control": {
        "tag": "input"
    }, 
    "bind": {
        "type": constants.GEOTRACE_XFORM
    }
}

_GEOTRACE_TYPE_W_HINT= dict(_GEOTRACE_TYPE, \
            **{"hint": "GPS coordinates can only be collected when outside."})

_INT_TYPE= {
    "control": {
        "tag": "input"
    }, 
    "bind": {
        "type": constants.INT_XFORM
    }
}

_DECIMAL_TYPE= {
    "control": {
        "tag": "input"
    }, 
    "bind": {
        "type": constants.DECIMAL_XFORM
    }
}

_STRING_TYPE= {
    "control": {
        "tag": "input"
    }, 
    "bind": {
        "type": constants.STRING_XFORM
    }
}

_NOTE_TYPE= {
    "control": {
        "tag": "input"
    }, 
    "bind": {
        "readonly": "true()", 
        "type": constants.STRING_XFORM
    }
}

_TRIGGER_TYPE= {
    "control": {
        "tag": constants.TRIGGER_XFORM
    }, 
    "bind": {
        "type": constants.STRING_XFORM
    }
}

_BARCODE_TYPE= {
    "control": {
        "tag": "input"
    }, 
    "bind": {
        "type": constants.BARCODE_XFORM
    }
}

_TODAY_TYPE= {
    "bind": {
        "jr:preload": constants.DATE_XFORM, 
        "type": constants.DATE_XFORM, 
        "jr:preloadParams": constants.TODAY_XLSFORM
    }
}

_NONINPUT_STING_TYPE= {
    "bind": {
        "type": constants.STRING_XFORM
    }
}

# XForm.
_START_TYPE= {
    "bind": {
        "jr:preload": "timestamp", 
        "type": constants.DATETIME_XFORM, 
        "jr:preloadParams": constants.START_XLSFORM
    }
}

# XForm.
_END_TYPE= {
    "bind": {
        "jr:preload": "timestamp", 
        "type": constants.DATETIME_XFORM, 
        "jr:preloadParams": constants.END_XLSFORM
    }
}

# XForm.
_DEVICEID_TYPE= {
    "bind": {
        "jr:preload": "property", 
        "type": constants.STRING_XFORM, 
        "jr:preloadParams": constants.DEVICEID_XLSFORM
    }
}

# XForm.
_EMAIL_TYPE= {
    "bind": {
        "jr:preload": "property", 
        "type": constants.STRING_XFORM, 
        "jr:preloadParams": "email"
    }
}

# XForm.
_USERNAME_TYPE= {
    "bind": {
        "jr:preload": "property", 
        "type": constants.STRING_XFORM, 
        "jr:preloadParams": "username"
    }
}

# XForm.
_PHONENUMBER_TYPE= {
    "bind": {
        "jr:preload": "property", 
        "type": constants.STRING_XFORM, 
        "jr:preloadParams": constants.PHONENUMBER_XLSFORM
    }
}

# XForm.
_SIMSERIAL_TYPE= {
    "bind": {
        "jr:preload": "property", 
        "type": constants.STRING_XFORM, 
        "jr:preloadParams": constants.SIMSERIAL_XLSFORM
    }
}

# XForm.
_SUBSCRIBERID_TYPE= {
    "bind": {
        "jr:preload": "property", 
        "type": constants.STRING_XFORM, 
        "jr:preloadParams": constants.SUBSCRIBERID_XLSFORM
    }
}

QUESTION_TYPE_DICT = \
{
    # FIXME: These seemingly could be condensed to one entry per question type if 'pyxform.aliases.select' were put to use.
    # Select one.
    constants.SELECT_ONE:                               _SELECT_1_TYPE_DICT,
    "add " + constants.SELECT_ONE + " prompt using":    _SELECT_1_TYPE_DICT, # Already in 'pyxform.aliases.select'.
    constants.SELECT_ONE + " using":                    _SELECT_1_TYPE_DICT,
    "q " + constants.SELECT_ONE_XFORM:                  _SELECT_1_TYPE_DICT,
    
    # Select multiple.
    constants.SELECT_ALL_THAT_APPLY:                _SELECT_TYPE_DICT,  # Already in 'pyxform.aliases.select'.
    constants.SELECT_ALL_THAT_APPLY + " from":      _SELECT_TYPE_DICT, # Already in 'pyxform.aliases.select'.
    "add select multiple prompt using":             _SELECT_TYPE_DICT, # Already in 'pyxform.aliases.select'.
    "select multiple from":                         _SELECT_TYPE_DICT,
    "q " + constants.SELECT_ALL_THAT_APPLY_XFORM:   _SELECT_TYPE_DICT,
    "select multiple using":                        _SELECT_TYPE_DICT,
    
    "q picture":                                    _IMAGE_TYPE,
    "photo":                                        _IMAGE_TYPE,
    "q " + constants.IMAGE_XLSFORM:                 _IMAGE_TYPE,
    "add " + constants.IMAGE_XLSFORM + " prompt":   _IMAGE_TYPE,
    constants.IMAGE_XLSFORM:                        _IMAGE_TYPE,
    
    "add date time prompt":     _DATETIME_TYPE,
    "q date time":              _DATETIME_TYPE,
    
    constants.VIDEO_XLSFORM:                        _VIDEO_TYPE,
    "add " + constants.VIDEO_XLSFORM + " prompt":   _VIDEO_TYPE,
    "q " + constants.VIDEO_XLSFORM:                 _VIDEO_TYPE,
    
    "add " + constants.AUDIO_XLSFORM + " prompt":   _AUDIO_TYPE,
    "q " + constants.AUDIO_XLSFORM:                 _AUDIO_TYPE,
    constants.AUDIO_XLSFORM:                        _AUDIO_TYPE,
    
    "add " + constants.DATE_XFORM + " prompt":  _DATE_TYPE,
    "q " + constants.DATE_XFORM:                _DATE_TYPE,
    constants.DATE_XFORM:                       _DATE_TYPE,
    
    "datetime":                                     _DATETIME_TYPE, 
    constants.DATETIME_XFORM:                       _DATETIME_TYPE, 
    "add " + constants.DATETIME_XFORM + " prompt":  _DATETIME_TYPE, 
    "q " + constants.DATETIME_XFORM:                _DATETIME_TYPE, 
    "date time":                                    _DATETIME_TYPE, 
    
    "q " + constants.GEOPOINT_XFORM:    _GEOPOINT_TYPE,
    "location":                         _GEOPOINT_TYPE,
    "q location":                       _GEOPOINT_TYPE,
    "add location prompt":              _GEOPOINT_TYPE,
    
    constants.GEOPOINT_XFORM:   _GEOPOINT_TYPE_W_HINT,
    "gps":                      _GEOPOINT_TYPE_W_HINT,
    
    "q " + constants.GEOTRACE_XFORM:    _GEOTRACE_TYPE,
    
    constants.GEOTRACE_XFORM:     _GEOTRACE_TYPE_W_HINT,
    
    "q " + constants.GEOSHAPE_XFORM:    _GEOSHAPE_TYPE,
    
    constants.GEOSHAPE_XFORM:   _GEOSHAPE_TYPE_W_HINT,

    constants.INT_XLSFORM:                      _INT_TYPE,
    "q " + constants.INT_XFORM:                 _INT_TYPE,
    constants.INT_XFORM:                        _INT_TYPE,
    "add " + constants.INT_XLSFORM + " prompt": _INT_TYPE,
    
    constants.DECIMAL_XFORM:                        _DECIMAL_TYPE,
    "add " + constants.DECIMAL_XFORM + " prompt":   _DECIMAL_TYPE,
    "q " + constants.DECIMAL_XFORM:                 _DECIMAL_TYPE,
    
    constants.STRING_XLSFORM:                       _STRING_TYPE,
    constants.STRING_XFORM:                         _STRING_TYPE,
    "q " + constants.STRING_XFORM:                  _STRING_TYPE,
    "select one external":                          _STRING_TYPE,
    "add " + constants.STRING_XLSFORM + " prompt":  _STRING_TYPE,
    
    "add " + constants.NOTE_XLSFORM + " prompt":    _NOTE_TYPE,
    "q " + constants.NOTE_XLSFORM:                  _NOTE_TYPE,
    constants.NOTE_XLSFORM:                         _NOTE_TYPE,

    "add " + constants.TRIGGER_XLSFORM + " prompt": _TRIGGER_TYPE,
    constants.TRIGGER_XLSFORM:                      _TRIGGER_TYPE,
    "q " + constants.TRIGGER_XLSFORM:               _TRIGGER_TYPE,
    
    "add " + constants.BARCODE_XFORM + " prompt":   _BARCODE_TYPE,
    "q " + constants.BARCODE_XFORM:                 _BARCODE_TYPE,
    constants.BARCODE_XFORM:                        _BARCODE_TYPE,

    constants.PHONENUMBER_XLSFORM:  _PHONENUMBER_TYPE,
    "get phone number":             _PHONENUMBER_TYPE,
    
    constants.START_XLSFORM:    _START_TYPE,
    "get start time":           _START_TYPE,
    
    "get end time":         _END_TYPE,
    "end time":             _END_TYPE,
    constants.END_XLSFORM:  _END_TYPE,
    
    "get sim id":                   _SIMSERIAL_TYPE,
    constants.SIMSERIAL_XLSFORM:    _SIMSERIAL_TYPE,
    "sim id":                       _SIMSERIAL_TYPE,
    
    "imei":                     _DEVICEID_TYPE,
    "device id":                _DEVICEID_TYPE,
    "get device id":            _DEVICEID_TYPE,
    constants.DEVICEID_XLSFORM: _DEVICEID_TYPE,

    "subscriber id":                _SUBSCRIBERID_TYPE,
    constants.SUBSCRIBERID_XLSFORM: _SUBSCRIBERID_TYPE,
    "get subscriber id":            _SUBSCRIBERID_TYPE,
    
    "get today":                _TODAY_TYPE,
    constants.TODAY_XLSFORM:    _TODAY_TYPE,
    
    "start time":   _START_TYPE,
    
    constants.CALCULATE_XLSFORM:                        _NONINPUT_STING_TYPE,
    "q " + constants.CALCULATE_XLSFORM:                 _NONINPUT_STING_TYPE,
    "add " + constants.CALCULATE_XLSFORM + " prompt":   _NONINPUT_STING_TYPE, 
    "hidden":                                           _NONINPUT_STING_TYPE,
    
    "username": _USERNAME_TYPE, 
    
    "email": _EMAIL_TYPE,
    
    "number of days in last month": {
        "control": {
            "tag": "input"
        }, 
        "bind": {
            "type": constants.INT_XFORM, 
            "constraint": "0 <= . and . <= 31"
        }, 
        "hint": "Enter a number 0-31."
    }, 
    constants.TRIGGER_XFORM: {
        "control": {
            "tag": constants.TRIGGER_XFORM
        }
    }, 
    "percentage": {
        "control": {
            "tag": "input"
        }, 
        "bind": {
            "type": constants.INT_XFORM, 
            "constraint": "0 <= . and . <= 100"
        }
    }, 
    "number of days in last six months": {
        "control": {
            "tag": "input"
        }, 
        "bind": {
            "type": constants.INT_XFORM, 
            "constraint": "0 <= . and . <= 183"
        }, 
        "hint": "Enter a number 0-183."
    }, 
    "phone number": {
        "control": {
            "tag": "input"
        }, 
        "bind": {
            "type": constants.STRING_XFORM, 
            "constraint": "regex(., '^\\d*$')"
        }, 
        "hint": "Enter numbers only."
    }, 
    "number of days in last year": {
        "control": {
            "tag": "input"
        }, 
        "bind": {
            "type": constants.INT_XFORM, 
            "constraint": "0 <= . and . <= 365"
        }, 
        "hint": "Enter a number 0-365."
    }, 
    constants.TIME_XFORM: {
        "control": {
            "tag": "input"
        }, 
        "bind": {
            "type": constants.TIME_XFORM
        }
    }, 
    "uri:" + constants.SUBSCRIBERID_XLSFORM: {
        "bind": {
            "jr:preload": "property", 
            "type": constants.STRING_XFORM, 
            "jr:preloadParams": "uri:" + constants.SUBSCRIBERID_XLSFORM
        }
    },
    "uri:" + constants.PHONENUMBER_XLSFORM: {
        "bind": {
            "jr:preload": "property", 
            "type": constants.STRING_XFORM, 
            "jr:preloadParams": "uri:" + constants.PHONENUMBER_XLSFORM
        }
    },
    "uri:" + constants.SIMSERIAL_XLSFORM: {
        "bind": {
            "jr:preload": "property", 
            "type": constants.STRING_XFORM, 
            "jr:preloadParams": "uri:" + constants.SIMSERIAL_XLSFORM
        }
    },
    "uri:" + constants.DEVICEID_XLSFORM: {
        "bind": {
            "jr:preload": "property", 
            "type": constants.STRING_XFORM, 
            "jr:preloadParams": "uri:" + constants.DEVICEID_XLSFORM
        }
    }, 
    "uri:username": {
        "bind": {
            "jr:preload": "property", 
            "type": constants.STRING_XFORM, 
            "jr:preloadParams": "uri:username"
        }
    }, 
    "uri:email": {
        "bind": {
            "jr:preload": "property",
            "type": constants.STRING_XFORM, 
            "jr:preloadParams": "uri:email"
        }
    },
}

#import os
#class QuestionTypeDictionary(dict):
#    """
#    A dictionary parsed from an xls file that defines question types.
#    """
#    def __init__(self, file_name="base"):
#        # Right now we're using an excel file to describe question
#        # types we will use in creating XForms, we'll switch over to
#        # json soon.
#        self._name = file_name
#        path_to_this_file = os.path.abspath(__file__)
#        path_to_this_dir = os.path.dirname(path_to_this_file)
#        path_to_question_types = os.path.join(
#            path_to_this_dir,
#            "question_types",
#            "%s.xls" % file_name
#            )
#        excel_reader = QuestionTypesReader(path_to_question_types)
#        for k, v in excel_reader.to_json_dict().iteritems():
#            self[k] = v
#
#    def get_definition(self, question_type_str):
#        return self.get(question_type_str, {})
#
#DEFAULT_QUESTION_TYPE_DICTIONARY = QuestionTypeDictionary("all")
