from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from .models import *
from .forms import ImageForm
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
#from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from pgeocode import GeoDistance


def index(request):
    return render(request, 'index.html')


def client_HomePage(request):
    return render(request, 'client_HomePage.html')


def client_login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            trainers = Trainer_Register.objects.all()
            parameter = {
                "Trainers": trainers,
                "user": user
            }
            return render(request, 'client_HomePage.html', parameter)
        else:
            messages.success(request, "Username and Password doesn't match")
            return render(request, 'client.html')
    else:
        # Return an 'invalid login' error message.
        return render(request, 'client.html')


def ChangeProfile_Client(request):
    name = request.user.username
    if request.method == 'POST':
        change = Client_Register.objects.get(email=name)
        base = User.objects.get(username=name)
        base.first_name = request.POST['name']
        change.name = request.POST['name']
        change.age = request.POST['age']
        change.Address = request.POST['address']
        change.postcode = request.POST['postcode']
        change.telephone = request.POST['phone']
        change.aval_days = request.POST['days']
        change.aval_time = request.POST['time']
        change.save()
        base.save()
        messages.success(request, "Profile Updated Successfully")
        trainers = Trainer_Register.objects.all()
        return render(request, "client_HomePage.html", {"Trainers": trainers})
    else:
        cli_change = Client_Register.objects.filter(name=request.user.first_name)
        base_c = User.objects.filter(username=request.user.username)
        context = {"det": cli_change,
                   "det_c": base_c
                   }
        return render(request, "ChangeProfile_Client.html", context)


def client_createAccount(request):
    if request.method == "POST":
        create_username = request.POST['username']
        global client_name, create_email, create_password
        client_name = create_username
        create_email = request.POST['email']
        create_password = request.POST['password']
        create_password_confirm = request.POST['password_confirm']

        if create_password == create_password_confirm:
            try:
                user = User.objects.get(username=create_email)
                messages.info(request, "Email already taken")
                return render(request, "Client.html")
            except User.DoesNotExist:
                user = User.objects.create_user(username=create_email, email=create_email,
                                                first_name=create_username,
                                                password=create_password
                                                )
                user.save()
                return render(request, "Client_CreateAccount.html")
        else:
            messages.info(request, "Password and Confirm Password must match")
            return render(request, "Client.html")

    else:
        return render(request, "Client.html")


def Client_CreateAccount(request):
    if request.method == "POST":
        Client = Client_Register()
        global client_name, create_email, create_password
        Client.name = client_name
        Client.email = create_email
        Client.age = request.POST['age']
        Client.Address = request.POST['address']
        Client.postcode = request.POST['postcode']
        Client.telephone = request.POST['phone']
        Client.aval_days = request.POST['days']
        Client.aval_time = request.POST['time']
        Client.save()
        user = auth.authenticate(username=create_email, password=create_password)
        auth.login(request, user)
        train = Trainer_Register.objects.all()
        return render(request, "client_HomePage.html", {"staff": train, "user": user})
    else:
        # print("not saved")
        return render(request, "Client_CreateAccount.html")


def Client_Logout(request):
    logout(request)
    return render(request, 'index.html')


def Trainer(request):
    if request.method == "POST":
        global create_username1
        create_username = request.POST['username']
        create_username1 = create_username
        global create_email1
        create_email1 = request.POST['email']
        create_password = request.POST['password']
        global trainer_password
        trainer_password = create_password
        create_password_confirm = request.POST['password_confirm']

        if create_password == create_password_confirm:
            try:
                user = User.objects.get(username=create_email1)
                messages.info(request, "Email already taken")
                return render(request, "trainer.html")
            except User.DoesNotExist:
                user = User.objects.create_user(username=create_email1, email=create_email1,
                                                first_name=create_username,
                                                password=create_password,
                                                is_staff=True
                                                )
                user.save()
                return render(request, "Trainer_CreateAccount.html")

        else:
            messages.success(request, "Password and Confirm Password must match")
            return render(request, "trainer.html")
        # print("User Created")
    else:
        return render(request, "trainer.html")


def Trainer_CreateAccount(request):
    if request.method == "POST":
        global age_t, speciality_t, qualification_t, address_t, postcode_t, number_t, aval_days_t, aval_time_t, services_t
        global gender_t
        age_t = request.POST['age']
        gender_t = request.POST['gender']
        speciality_t = request.POST['speciality']
        qualification_t = request.POST['qualification']
        address_t = request.POST['address']
        postcode_t = request.POST['postcode']
        number_t = request.POST['number']
        aval_days_t = request.POST['aval_days']
        aval_time_t = request.POST['aval_time']
        services_t = request.POST['services']
        # trainer_reg = Trainer_Register()
        return render(request, "Extra_trainer_data.html")

    else:
        return render(request, "Trainer_CreateAccount.html")


def Extra_trainer_data(request):
    if request.method == "POST":
        global age_t, speciality_t, qualification_t, address_t, postcode_t, number_t, aval_days_t, aval_time_t, services_t
        global create_email1
        global gender_t
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

        profile_pic = request.FILES['docfile']
        personal_more = request.POST['personal']
        additional_pic = request.FILES['additional']
        trainer_reg = Trainer_Register()
        global create_username1
        trainer_reg.name = create_username1
        trainer_reg.email = create_email1
        trainer_reg.age = age_t
        trainer_reg.gender = gender_t.lower()
        trainer_reg.speciality = speciality_t.lower()
        trainer_reg.qualification = qualification_t.lower()
        trainer_reg.Address_of = address_t.lower()
        trainer_reg.postcode = postcode_t
        trainer_reg.telephone = number_t
        trainer_reg.aval_days = aval_days_t
        trainer_reg.aval_time = aval_time_t
        trainer_reg.ser_offered = services_t.lower()
        trainer_reg.profile_picture = profile_pic
        trainer_reg.personal_profile = personal_more
        trainer_reg.additional_pic = additional_pic
        trainer_reg.save()
        global trainer_password
        user = auth.authenticate(username=create_email1, password=trainer_password)
        auth.login(request, user)
        return render(request, "base_trai.html", {"user": user})

    else:
        form = ImageForm()

        return render(request, "Extra_trainer_data.html", {'form': form})


def Trainer_Login(request):
    if request.method == 'POST':
        create_email = request.POST['email']
        create_password = request.POST['password']
        user = auth.authenticate(username=create_email, password=create_password)
        auth.login(request, user)
        if user is not None:
            auth.login(request, user)
            return render(request, "base_trai.html", {"user": user})
        else:
            messages.success(request, "Username and Password doesn't match or not exist")
            return render(request, "trainer.html")
    else:
        return render(request, "trainer.html")


def ChangeProfile_Trainer(request):
    username = request.user.username
    if request.method == 'POST':
        change = Trainer_Register.objects.get(email=username)
        base = User.objects.get(username=username)
        base.first_name = request.POST['name']
        change.name = request.POST['name']
        change.age = request.POST['age']
        change.speciality = request.POST['speciality']
        change.qualification = request.POST['qualification']
        change.Address_of = request.POST['Address_of']
        change.postcode = request.POST['postcode']
        change.telephone = request.POST['telephone']
        change.aval_days = request.POST['days']
        change.aval_time = request.POST['time']
        change.ser_offered = request.POST['ser_offered']
        change.save()
        base.save()
        messages.success(request, "Profile Updated Successfully")
        #trainers = Trainer_Register.objects.all()
        return render(request, "Trainer_HomePage.html")
    else:
        tri_change = Trainer_Register.objects.filter(name=request.user.first_name)
        base_t = User.objects.filter(username=request.user.username)
        context = {"det_t": tri_change,
                   "det_c1": base_t
                   }
        return render(request, "ChangeProfile_Trainer.html", context)


def Trainer_Logout(request):
    logout(request)
    return render(request, 'index.html')


def send_to_trainer(name_of_tra, name_of_cli, message):
    Mess = Message()
    Mess.name_of_cli = name_of_cli
    Mess.name_of_tra = name_of_tra
    Mess.message = message
    Mess.save()


def TrainerMessages(request):
    if request.method == 'POST':
        global Trai
        name_of_trainer = None
        for tr in Trai:
            name_of_trainer = tr.name
        username = request.user.first_name
        message = request.POST['message']
        send_to_trainer(name_of_tra=name_of_trainer, name_of_cli=username, message=message)
        messages.success(request, 'Message Sent successfully')
        return render(request, 'TrainerDetails.html', {"trainers": Trai})


def TrainerDetails(request, trid):
    global Trai
    Trai = Trainer_Register.objects.filter(id=trid)
    return render(request, "TrainerDetails.html", {"trainers": Trai})


def ClientMessage_fetch(request):
    mess = Message.objects.filter(name_of_cli=request.user.first_name)
    return render(request, 'ClientMessages.html', {"messages1": mess})


def mapview(request):
    trainers = Trainer_Register.objects.all()
    return render(request, "map.html", {"trainer": trainers})


def is_valid_query(parameter):
    return parameter != '' and parameter is not None


def get_loc(km, post):
    kmeter = int(km)
    dis = GeoDistance('us')
    list = []
    tr = Trainer_Register.objects.all()
    for i in tr:
        postcode_tra = i.postcode
        postcode_str = str(postcode_tra)
        post_str = str(post)
        distance = int(dis.query_postal_code(post_str, postcode_str))
        if distance <= kmeter:
            list.append(i.id)
    return list


def filter(request):
    trainer = Trainer_Register.objects.all()
    eighteen_twentyfive = request.GET.get('eighteen_twentyfive')
    twentyfive_thirtyfive = request.GET.get('twentyfive_thirtyfive')
    thirtyfive_fourtyfive = request.GET.get('thirtyfive_fourtyfive')
    fourtyfive_over = request.GET.get('fourtyfive_over')
    male = request.GET.get('male')
    female = request.GET.get('female')
    group_session = request.GET.get('group_session')
    one_to_one = request.GET.get('one_to_one')
    diet_plan = request.GET.get('diet_plan')
    online_coaching = request.GET.get('online_coaching')
    km = request.GET.get('km')

    if is_valid_query(eighteen_twentyfive):
        trainer = trainer.filter(age__gte=18)
        trainer = trainer.filter(age__lt=25)

    if is_valid_query(twentyfive_thirtyfive):
        trainer = trainer.filter(age__gte=25)
        trainer = trainer.filter(age__lt=35)

    if is_valid_query(thirtyfive_fourtyfive):
        trainer = trainer.filter(age__gte=35)
        trainer = trainer.filter(age__lt=45)

    if is_valid_query(fourtyfive_over):
        trainer = trainer.filter(age__gte=45)

    if is_valid_query(male):
        trainer = trainer.filter(gender='male')

    if is_valid_query(female):
        trainer = trainer.filter(gender='female')

    if is_valid_query(group_session):
        trainer = trainer.filter(ser_offered__icontains="group")

    if is_valid_query(one_to_one):
        trainer = trainer.filter(ser_offered__icontains="one")

    if is_valid_query(diet_plan):
        trainer = trainer.filter(ser_offered__icontains="diet")

    if is_valid_query(online_coaching):
        trainer = trainer.filter(ser_offered__icontains="online")

    if is_valid_query(km):
        name = request.user.username
        use = Client_Register.objects.filter(email=name)

        for i in use:
            post = i.postcode

        trainer = trainer.filter(pk__in=get_loc(km, post))

    context = {
        'Trainers': trainer
    }

    return render(request, 'client_HomePage.html', context)

