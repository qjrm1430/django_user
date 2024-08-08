from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .constant import USER_ROLE
from .models import Custom


# Create your views here.
# 로그인
# -> 이미 로그인한 사람 -> todolist 화면
# -> 로그인 요청한 사람 -> 아이디/비번 맞는지 확인 하고
# -> 로그인 화면 접속하는 사람 -> 로그인 화면으로 안내
def login_user(req):
    # -> 이미 로그인한 사람 -> todolist 화면
    if req.user.is_authenticated:
        return redirect("todolist-index")
    # -> 로그인 요청한 사람 -> 아이디/비번 맞는지 확인 하고
    elif req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password")
        print(f"{username}/ {password}")
        valid_user = authenticate(username=username, password=password)
        print(f"valid_user: {valid_user}")
        if valid_user:
            login(req, valid_user)
            return redirect("todolist-index")

        messages.error(req, "아이디 또는 비번이 틀립니다. 다시 입력해주세요.")

    # -> 로그인 화면 접속하는 사람 -> 로그인 화면으로 안내
    return render(req, "user/login.html")


# 가입
# -> 이미 로그인한 사람 -> todolist 화면
# -> 가입을 요청하는 사람 -> 검증
# -> 가입화면으로 이동하는 사람


def __is_vaild_user_info(req, **user_info) -> bool:
    is_vaild = True
    if not user_info["username"].strip():
        is_vaild = False
        messages.error("username 입력해주세요")
    elif not user_info["password"].strip():
        is_vaild = False
        messages.error("password 입력해주세요")
    elif not user_info["email"].strip():
        is_vaild = False
        messages.error("email 입력해주세요")

    return is_vaild


def join_user(req):
    # 이미 로그인한 사람 -> todolist 화면
    if req.user.is_authenticated:
        return redirect("todolist-index")
    # -> 가입을 요청하는 사람 -> 검증
    elif req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password")
        email = req.POST.get("email")
        # 요청한 데이터가 정상인지 확인
        is_vaild = __is_vaild_user_info(
            req=req, username=username, password=password, email=email
        )
        # DB에 요청한 데이터가 있는지 확인
        custom = Custom.objects.filter(username=username)

        if is_vaild and not custom:
            role = (
                USER_ROLE.ADMIN.name
                if "admin" in username.lower()
                else USER_ROLE.CUST.name
            )
            print(f"join: {username}/ {password}")
            new_custom = Custom.objects.create_user(
                username=username, password=password, email=email, role=role
            )

            new_custom.save()
            return redirect("login-user")
        elif custom:
            messages.error(req, "이미 등록한 사용자가 있습니다.")

    # -> 가입화면으로 이동하는 사람
    return render(req, "user/join.html")


# 로그아웃
def logout_user(req):
    if req.user.is_authenticated:
        logout(req)

    return redirect("login-user")
