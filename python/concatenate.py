# This is a sample module that concatenates strings
# it expects an array in params['strings']
# for it to work correctly
# once it does its work
# it packages the response in a dict
# with the signature:
# { 'status' : 'success', 'params' : { 'concatenated_string' : the_computed_value } }
# if there is an error it returns
# a payload with the signature:
# { 'status' : 'error', 'error' : 'the error message' }
#
def concat(params):
    if 'strings' in params.keys():
        strings = params['strings']
        concatenated_string = ''
        for string in strings:
            concatenated_string += string
        return { 'status' : 'success', 'params' : { 'concatenated_string' : concatenated_string } }
    else:
        return { 'status' : 'error', 'error' : 'expected a strings param key'}
