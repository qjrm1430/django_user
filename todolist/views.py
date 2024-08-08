from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from user.constant import USER_ROLE

from .models import todo


# Create your views here.
@login_required(login_url="/user/login/")
def get_todolist(req):
    # 저장
    if req.method == "POST":
        title = req.POST.get("title")
        if title:
            new_todo = todo(custom=req.user, title=title)
            new_todo.save()
        else:
            messages.error(req, "no title, retry again!!")

    # 조회
    if req.user.role == USER_ROLE.ADMIN.name:
        todolist = todo.objects.all()
    else:
        todolist = todo.objects.filter(custom=req.user)
    context = {"todolist": todolist}
    return render(req, "todolist/todolist.html", context)


@login_required(login_url="/user/login/")
def update_todo(req, title):
    if req.user.role == USER_ROLE.ADMIN.name:
        update_todo = todo.objects.get(title=title)
    else:
        update_todo = todo.objects.get(custom=req.user, title=title)
    update_todo.status = True
    update_todo.save()
    return redirect("todolist-index")


@login_required(login_url="/user/login/")
def delete_todo(req, title):
    if req.user.role == USER_ROLE.ADMIN.name:
        delete_todo = todo.objects.get(title=title)
    else:
        delete_todo = todo.objects.get(custom=req.user, title=title)
    delete_todo.delete()
    return redirect("todolist-index")
