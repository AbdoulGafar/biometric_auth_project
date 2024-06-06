# decorators.py

from django.shortcuts import render
from django.http import HttpResponseForbidden
from passageidentity import Passage, PassageError
import os

PASSAGE_APP_ID = os.getenv('PASSAGE_APP_ID')
PASSAGE_API_KEY = os.getenv('PASSAGE_API_KEY')

try:
    psg = Passage(PASSAGE_APP_ID, PASSAGE_API_KEY)
except PassageError as e:
    print(e)
    exit()

def before_auth(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            request.user = psg.authenticateRequest(request)
        except PassageError as e:
            # Return 401 if authentication fails
            return render(request, 'unauthorized.html')
        return view_func(request, *args, **kwargs)
    return wrapper


def reset_passage():
    global psg
    try:
        psg = Passage(PASSAGE_APP_ID, PASSAGE_API_KEY)
    except PassageError as e:
        print(e)
        exit()