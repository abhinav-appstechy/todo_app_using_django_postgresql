from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from todoapp.models import TodoModel
from django.shortcuts import get_object_or_404
import json
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.
def home_page(request):
    all_todos = TodoModel.objects.all()
    current_datetime = timezone.now()
    modified_todos = []
    for todo in all_todos:
        todo.is_todo_expired = todo.due_date_and_time < current_datetime
        modified_todos.append(todo)

    total_todos = len(all_todos)
    # print(total_todos)
    context = {
        "all_todos": modified_todos,
        "total_todos": total_todos,
        "activeLink": "Home"
    }
    return render(request, "homepage.html",context)

def logout_view(request):
    if request.method == "POST":     
        logout(request)
        return redirect("homepage")

def about_us(request):
    context = {
        "array": [1,1,1,1],
        "activeLink": "AboutUs"
    }
    return render(request, "aboutus.html", context)

def contact_us(request):
    context = {
        "activeLink": "ContactUs"
    }
    return render(request, "contactus.html", context)

@staff_member_required
def add_todo(request):
    return render(request, "add_new_todo_page.html")

@staff_member_required
def add_new_todo_logic(request):
    if request.method == "POST":
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        file = request.FILES.get('file')
        date_and_time = request.POST.get('date_and_time')
        
        new_todo = TodoModel(title=title, desc=desc, image=file, due_date_and_time=date_and_time )
        new_todo.save()
        return JsonResponse({'message':"Successfully created!","status":200}, status=200)
    
    return JsonResponse({'message':"error!", "status": 400}, status=400)

@staff_member_required
def update_todo_page(request, id):
    todo = get_object_or_404(TodoModel, pk = id)
    context = {
        "todo":todo
    }

    return render(request, "update_todo_page.html", context)

@staff_member_required
def update_todo_logic(request):
    if request.method == "POST":
        todo_id = request.POST.get("todo_id")
        todo = get_object_or_404(TodoModel, pk=todo_id)

        title = request.POST.get("title")
        desc = request.POST.get('desc')
        image = request.FILES.get("file")
        date_and_time = request.POST.get("date_and_time")

        todo.title = title
        todo.desc = desc
        if image:
            todo.image = image

        todo.due_date_and_time = date_and_time
        todo.save()

        return JsonResponse({"message": "Succesfully updated it!", "status": 200}, status=200)
    
    return JsonResponse({"message": "error", "status": 400}, status=400)

@staff_member_required
def change_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            status = data.get('status')
            id = data.get('id') 
            print(status, id)

            
            todo = get_object_or_404(TodoModel, pk=id)
            todo.complete_status = True if status == "Incomplete" else False
            todo.save()
            
            return JsonResponse({"message":"successfully changed status!", "status":200, "todo_status":todo.complete_status}, status=200)



        except Exception as e:
            return JsonResponse({"message":"exception occured!", "status": 400}, status=400)
        
    return JsonResponse({"message":"changed successfully!", "status": 200}, status = 200)

@staff_member_required
def delete_todo(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            id = data.get('id')
            all_todos = list(TodoModel.objects.exclude(pk=id).values())
            todo = get_object_or_404(TodoModel, pk=id)
            todo.delete()


            return JsonResponse({"message":"successfully deleted!", "status":200, "all_todos":all_todos }, status = 200)

        except Exception as e:
            return JsonResponse({"message":"exception occured!", "status":400}, status = 400)

    return JsonResponse({"message":"error occured!", "status":400}, status = 400)


