from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os

from .decorators import before_auth, reset_passage
from passageidentity import Passage, PassageError
import os


PASSAGE_APP_ID = os.getenv('PASSAGE_APP_ID')
PASSAGE_API_KEY = os.getenv('PASSAGE_API_KEY')

reset_passage()



try:
    psg = Passage(PASSAGE_APP_ID, PASSAGE_API_KEY)
except PassageError as e:
    print(e)
    exit()


def index(request):
    return render(request, 'index.html', {'psg_app_id': PASSAGE_APP_ID})

# def login(request):
#     if request.method == 'POST':
#         biometric_data = request.POST['biometric_data']  # Exemple de champ de formulaire
#         # authenticated = authenticate_user(biometric_data)
#         authenticated = True
#         if authenticated:
#             request.session['authenticated'] = True
#             return redirect('dashboard')
#         else:
#             messages.error(request, 'Authentication failed.')
#     return render(request, 'index.html')

@before_auth
def dashboard(request):
    psg_user = psg.getUser(request.user)
    email = psg_user.email
    context = {
        'email' : email,
        'psg_user' : psg_user
    }
    return render(request, 'dashboard.html',context)

# @before_auth
# def dashboard(request):
#     try:
#         psg_user = psg.getUser(request.user)
#         email = psg_user.email
#     except PassageError as e:
#         return render(request, 'unauthorized.html')

#     return render(request, 'dashboard.html', {'email': email})


def unauthorized(request):
    return render(request, 'unauthorized.html')

