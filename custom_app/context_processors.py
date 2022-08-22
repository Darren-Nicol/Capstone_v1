import sys

global FILES_PATH

def filepath_processor(request):
    if 'runserver' in sys.argv:
        FILES_PATH = '../../static/auctions'
    else:
        FILES_PATH = ''
    return {'files_path': FILES_PATH}