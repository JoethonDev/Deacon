from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from .functions import get_names, save_attendence, add_name




# Task 1 : Get Names
# Task 2 : Write Attendance.. Post method.. Body = {
#   names : []
#   date : dateTime
# }
# Task 3 : Add Name to tables


# Create your views here.
def index(request):
    names = get_names()
    success = request.session.get("success", "")
    if success:
        del request.session['success']

    error = request.session.get("error", "")
    if error: 
        del request.session['error']

    return render(request, "index.html", {
        "names" : names,
        "success" : success,
        "error" : error
    })

def submit_attendance(request):
    names = request.POST.getlist("name")
    date = request.POST.get("date")
    try :
        msg = save_attendence(names, date)
        request.session['success'] = msg
    except Exception as e:
        request.session['error'] =  str(e) 
    return HttpResponseRedirect(reverse("index"))

def submit_name(request):
    name = request.POST.get("name")
    try :
        msg = add_name(name)
        request.session['success'] = msg
    except Exception as e:
        request.session['error'] =  str(e) 
    return HttpResponseRedirect(reverse("index"))