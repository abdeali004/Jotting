# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from MainApp.models import note, userInfo, verifyUser
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings
from itertools import chain
import random


# Create your views here.
def error_404(request , exception, template_name="404.html"):
        data = {}
        return render(request, template_name)

def error_500(request, *args, **argv):
        data = {}
        return render(request, "500.html")

def home(request):
    msg = "Jotting is absolutely free to use. So create, save, share your notes now. "
    if request.user.is_anonymous:
        return redirect("/login")

    userdata = note.objects.filter(
        username=request.user).order_by("-datetime_created")
    userdata2 = userInfo.objects.get(
        username=request.user)

    if userdata2.newUser:
        new = True
        userdata2.newUser = False
    else:
        new = False

    userdata2.save()

    context = {
        "data": userdata,
        "searchCheck": False,
        "new": new,
        "mesg": msg,
    }

    return render(request, "home.html", context)


def about(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, "about.html")


@csrf_exempt
def registerUser(request):
    if request.method == "POST":
        userName = request.POST.get(
            "username")
        userMail = request.POST.get(
            "email")
        userPass = request.POST.get("password")
        userFullName = request.POST.get("fullname")
        user1 = User.objects.filter(username=userName)
        user2 = User.objects.filter(email=userMail)
        if len(user1) == 0 and len(user2) == 0:
            userData = verifyUser.objects.filter(email=userMail)
            if userData:
                verifyUser.objects.get(email=userMail).delete()
            verifyCode = random.choice(
                ["j", "o", "t", "t", "i", "n", "g"]) + str(random.randint(100000, 1000000))
            verifyUser.objects.create(
                username=userName, full_name=userFullName, email=userMail, verificationCode=verifyCode)
            heading = "Jotting account request."
            messageContent = "Your Jotting account's secret verification code : " + verifyCode
            msg = EmailMessage(heading, messageContent, settings.EMAIL_HOST_USER,
                               [userMail, ])
            msg.send()
            context = {
                "username": userName,
                "password": userPass,
                "email": userMail,
                "fullname": userFullName,

            }
            return render(request, "verify.html", context)

        elif user1:
            messages.warning(
                request, 'Username already taken. Please Sign Up using another username.')
            return redirect("/login")
        else:
            messages.warning(
                request, 'E-mail already taken. Please Sign Up using another E-mail.')
            return redirect("/login")
    elif not request.user.is_anonymous:
        return redirect("/home")

    return render(request, "login.html")


def userVerify(request):
    if request.method == "POST":
        userName = request.POST.get("username")
        userPass = request.POST.get("password")
        userMail = request.POST.get("email")
        userFullName = request.POST.get("fullname")
        code = request.POST.get("code")
        userData = verifyUser.objects.get(email=userMail)
        orgCode = userData.verificationCode
        if code == orgCode:
            verifyUser.objects.get(email=userMail).delete()
            user = User.objects.create_user(
                username=userName, password=userPass)
            user.first_name = userFullName
            user.email = userMail
            user.is_superuser = False
            user.save()
            # creating user info
            checkCodeValue = userName[:4] + "-" + \
                str(random.randint(11111, 100000))
            userInfo.objects.create(
                username=userName, email=userMail, checkCode=checkCodeValue)
            messages.info(
                request, 'You are registered successfully. Please Login to continue.')
            return redirect("/login")
        else:
            messages.warning(
                request, 'Verification failed!! Your verification code doesn\'t match, try again.')
            return redirect("/login")
    return render(request, "login.html")


def loginUser(request):
    if request.method == "POST":
        name = request.POST.get(
            "username")
        userPass = request.POST.get("password")
        if name.__contains__("@"):
            exist = User.objects.filter(email=name.lower())
            if exist:
                name = User.objects.get(email=name.lower()).username
            else:
                # No backend authenticated the credentials
                messages.warning(
                    request, 'Wrong Username or Password.')
                return render(request, "login.html")

        user = User.objects.filter(username=name)
        if user:
            user = authenticate(
                username=name, password=userPass)
            if user is not None:
                login(request, user)
                return redirect("/home")
            else:
                # No backend authenticated the credentials
                messages.warning(
                    request, 'Wrong Username or Password.')
                return render(request, "login.html")
        else:
            # No backend authenticated the credentials
            messages.warning(
                request, 'Username not registered! Please SignUp for a new account.')
            return render(request, "login.html")

    elif not request.user.is_anonymous:
        return redirect("/home")

    return render(request, "login.html")


def logoutUser(request):
    if request.user.is_anonymous:
        return redirect("/login")
    logout(request)
    messages.info(
        request, 'You Logout Successfully. Come back soon.')
    return redirect("/login")


def getdata(request):
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method == "POST":
        head = request.POST.get("head")
        base = request.POST.get("base")
        note.objects.create(
            username=request.user, heading=head, main_note=base)
        return redirect("/home")


@csrf_exempt
def deleteNote(request):
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method == "POST":
        note_id = request.POST.get("noteID")
        note.objects.get(id=note_id).delete()
        return redirect("/home")


@csrf_exempt
def editNote(request, note_id):
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method == "POST":
        edit = note.objects.get(id=note_id)
        if(edit):
            edit.heading = request.POST.get("headEdit")
            if (request.POST.get("baseEdit")):
                edit.main_note = request.POST.get("baseEdit")
        edit.save()

    return redirect("/home")


@csrf_exempt
def shareNote(request, note_id):
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method == "POST" and request.POST.get("submit") == "Submit":
        emailin = request.POST.get("mail")
        subjectin = request.POST.get("headShare")
        messagein = request.POST.get("baseShare")

        ctx = {
            'subject': subjectin,
            'userMsg': messagein,
        }
        name = User.objects.get(username=request.user).get_short_name()
        heading = name + "'s note shared from Jotting."

        messageContent = get_template('mailTemplate.html').render(ctx)
        msg = EmailMessage(heading, messageContent, settings.EMAIL_HOST_USER,
                           [emailin, ])
        msg.content_subtype = 'html'
        msg.send()
        messages.success(request, 'Note shared. Please check the mail inbox.')
        return redirect("/home")


@csrf_exempt
def search(request):
    if request.user.is_anonymous:
        return redirect("/login")
    msg = "No results found. I think rather you forgot the keyword or you have not created note for the same."

    searchValue = False
    searchValue = request.POST.get("search").lower()
    userdata = []
    userFilter = note.objects.filter(
        username=request.user).order_by("-datetime_created")
    for obj in userFilter:
        if obj.heading.lower().__contains__(searchValue) or obj.main_note.lower().__contains__(searchValue):
            userdata.append(obj)
    none_data = note.objects.none()
    mainData = list(chain(none_data, userdata))

    msg = ""
    context = {
        "data": mainData,
        "searchCheck": True,
        "note_msg": 'Do not refresh this page just click on "view all notes" button to see all notes.',
        "mesg": msg,
    }

    return render(request, "home.html", context)


@csrf_exempt
def forgotPage(request, page):
    if page == 1:
        return render(request, "forgotPage.html")
    elif page == 2:
        if request.method == "POST":
            emailin = request.POST.get("mail")
            userdata = userInfo.objects.filter(email=emailin)
            if userdata:
                code = userdata[0].checkCode
                heading = "Jotting Password Change request."
                messageContent = "Your unique code : " + code
                msg = EmailMessage(heading, messageContent, settings.EMAIL_HOST_USER,
                                   [emailin, ])
                msg.send()
                context = {
                    "mail": emailin,

                }
                return render(request, "confirmPage.html", context)
            else:
                messages.warning(
                    request, 'Email not found. Please check and try again.')
                return redirect("/login")
        return redirect("/login")

    elif page == 3:
        if request.method == "POST":
            emailin = request.POST.get("mail")
            codeGet = request.POST.get("coded")
            userdata = userInfo.objects.filter(email=emailin)
            if userdata:
                code = userdata[0].checkCode
                if code == codeGet:
                    context = {
                        "mail": emailin,
                    }
                    return render(request, "passPage.html", context)
                else:
                    messages.warning(
                        request, 'Code is incorrect. Please try again and enter the new provided code.')
                    return redirect("/login")
            else:
                messages.warning(
                    request, 'No user found with the email. Please check and try again.')
                return redirect("/login")
            return redirect("/login")
        return redirect("/login")
    elif page == 4:
        if request.method == "POST":
            emailin = request.POST.get("mail")
            password = request.POST.get("newpass")
            userdata = userInfo.objects.get(email=emailin)
            userName = userdata.username
            checkCodeValue = userName[:4] + "-" + \
                str(random.randint(11111, 100000))
            userdata.checkCode = checkCodeValue
            userdata.save()
            u = User.objects.get(email=emailin)
            u.set_password(password)
            u.save()
            messages.success(
                request, 'Congratulations! Password changed successfully. LogIn to continue')
            return redirect("/login")
        return redirect("/login")
    else:
        return redirect("/login")
