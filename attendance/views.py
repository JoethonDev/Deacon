from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .functions import get_names, save_attendence, add_name
from json import loads



# Task 1 : Get Names Done
# Task 2 : Write Attendance.. Post method.. Body = {
#   names : []
#   date : dateTime
# } => Check if date exists Done - Rearrange and Insert by Date
# Task 3 : Add Name to tables Done
# Task 4 : Add Sheet Class
# Task 5 : Get Sheet Class


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

@csrf_exempt
def submit_name(request):
    body = request.body.decode('utf-8')
    name = loads(body)['name']
    msg = None
    status = 200
    try :
        msg = add_name(name)
    except Exception as e:
        msg =  str(e) 
        status = 401

    return JsonResponse({"message":msg}, status=status)