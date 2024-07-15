from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .functions import get_names, save_attendence, add_name, create_worksheet, get_worksheets_names
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
    names = get_names(None)
    sheets = get_worksheets_names()
    success = request.session.get("success", "")
    if success:
        del request.session['success']

    error = request.session.get("error", "")
    if error: 
        del request.session['error']

    return render(request, "index.html", {
        "names" : names,
        "sheets" : sheets,
        "success" : success,
        "error" : error
    })

def submit_attendance(request):
    names = request.POST.getlist("name")
    sheet_name = request.POST.get("sheet")
    date = request.POST.get("date")
    try :
        msg = save_attendence(names, date, sheet_name)
        request.session['success'] = msg
    except Exception as e:
        request.session['error'] =  str(e) 
    return HttpResponseRedirect(reverse("index"))

def retrieve_names(request, sheet_name):
    sheets = get_worksheets_names()
    if sheet_name not in sheets:
        return JsonResponse({"message":"Route is not avaliable!"}, status=404)
    return JsonResponse({"message" : "Success", "names" : get_names(sheet_name)}, status=200)

@csrf_exempt
def submit_name(request):
    body = loads(request.body.decode('utf-8'))
    name = body['name'].strip()
    sheet_name = body['sheet'].strip()
    msg = None
    status = 200
    try :
        msg = add_name(name, sheet_name)
    except Exception as e:
        msg =  str(e) 
        status = 401

    return JsonResponse({"message":msg}, status=status)

@csrf_exempt
def submit_class(request):
    body = loads(request.body.decode('utf-8'))
    sheet_name = body['sheet']
    msg = None
    status = 200
    try :
        msg = create_worksheet(sheet_name)
    except Exception as e:
        msg =  str(e) 
        status = 401

    return JsonResponse({"message":msg}, status=status)