from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
import xlwt
from datetime import date


from .util import SuperUser, Manager, OfficeStaff, ActivityReport
from .models import User, Employee, Hotel, Management, Office, Activity, Sale, EmailList
from .forms import PasswordChangingForm
#Email to Clients
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.

#Allows users to change password
class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')

def password_success(request):
    #Checks current user (Prinipal, Teacher, or Student)
    current_user = request.user.get_username()
    is_super = SuperUser(current_user)
    is_management = Manager(current_user)
    is_office = OfficeStaff(current_user)
    return render(request, "sales/password_success.html", {
            "is_super": is_super,
            "is_management": is_management,
            "is_office": is_office
        })

#Login
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "sales/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "sales/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


#Sales
@login_required(login_url='login')
def index(request):
    if request.method == "POST":
        user = request.user.get_username()
        current = User.objects.get(username=user)
        current_user = Office.objects.get(user_id=current)
        quantity1 = float(request.POST["quantity1"])
        act1 = request.POST["activity1"]
        activity1 = Activity.objects.get(id=act1)
        price1 = float(request.POST["price1"])
        quantity2 = request.POST["quantity2"]
        quantity2 = float(quantity2)
        act2 = request.POST["activity2"]
        if quantity2 > 0:
            activity2 = Activity.objects.get(id=act2)
        price2 = request.POST["price2"]
        price2 = float(price2)
        quantity3 = request.POST["quantity3"]
        quantity3 = float(quantity3)
        act3 = request.POST["activity3"]
        if quantity3 > 0:
            activity3 = Activity.objects.get(id=act3)
        price3 = request.POST["price3"]
        price3 = float(price3)
        employee = request.POST["employee"]
        seller = Employee.objects.get(id=employee)
        payment = request.POST["payment"]
        pick_up = request.POST["pick_up"]
        comment = request.POST["comment"]
        client_email = request.POST["email"]
        room_number = request.POST["room"]
        client_name = request.POST["client_name"]
        hotel_id = request.POST["hotel"]
        hotel = Hotel.objects.get(id=hotel_id)
        activity_date = request.POST["activity_date"]
        activity_time = request.POST["activity_time"]
        total_cost = (quantity1*price1)+(quantity2*price2)+(quantity3*price3)
        concessionaire = request.POST["Radios"]
        
        #Adds to Database if 3 items are sold
        if quantity3 > 0:
            sale = Sale(seller=seller, hotel=hotel, activity_date=activity_date, activity_time=activity_time, payment=payment, client_name=client_name, room_number=room_number, client_email=client_email, quantity1=quantity1, activity1=activity1, price1=price1, quantity2=quantity2, activity2=activity2, price2=price2, quantity3=quantity3, activity3=activity3, price3=price3, total_cost=total_cost, office=current_user, pickup_location=pick_up, comments=comment)
            sale.save()
 
        #Adds to Database if 2 items are sold
        if quantity3 == 0 and quantity2 > 0:
            sale = Sale(seller=seller, hotel=hotel, activity_date=activity_date, activity_time=activity_time, payment=payment, client_name=client_name,  room_number=room_number, client_email=client_email, quantity1=quantity1, activity1=activity1, price1=price1, quantity2=quantity2, activity2=activity2, price2=price2, total_cost=total_cost, office=current_user, pickup_location=pick_up, comments=comment)
            sale.save()

            

        #Adds to Database if 1 items are sold
        if quantity3 == 0 and quantity2 == 0:
            sale = Sale(seller=seller, hotel=hotel, activity_date=activity_date, activity_time=activity_time, payment=payment, client_name=client_name,  room_number=room_number, client_email=client_email, quantity1=quantity1, activity1=activity1, price1=price1, total_cost=total_cost, office=current_user, pickup_location=pick_up, comments=comment)
            sale.save()

        try:
            match = EmailList.objects.get(client_email=client_email)
        except:
            email = EmailList(client_email=client_email, client_name=client_name)
            email.save()

        #Sends a email to client with receipt, if concessionaire sends second email to company
        tickets = Sale.objects.filter(client_name=client_name).filter(total_cost=total_cost).filter(activity_time=activity_time)
        for ticket in tickets:
            subject = 'Mariana Caribbean Sports Sales Receipt'
            html_message = render_to_string('sales/email.html', {'ticket': ticket})
            plain_message = strip_tags(html_message)
            from_email = 'From Mariana Caribbean Sports'
            if concessionaire == "Concessionaire":
                to_emails = [client_email, 'karnes.james@gmail.com']
            else:
                to_emails = [client_email]

            mail.send_mail(subject, plain_message, from_email, to_emails, html_message=html_message)


        return HttpResponseRedirect(reverse("index"))

    else:
        activities = Activity.objects.all()
        employees = Employee.objects.all().order_by("last_name").exclude(last_name__in=['Ex-Employee'])
        hotels = Hotel.objects.all().order_by("hotel_name")

        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_management = Manager(current_user)
        is_office = OfficeStaff(current_user)
        return render(request, "sales/index.html", {
                "is_super": is_super,
                "is_management": is_management,
                "is_office": is_office,
                "activities": activities,
                "employees": employees,
                "hotels": hotels
            })

#Add New Office Staff to list and as user and employee
@login_required(login_url='login')
def office(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        telephone = request.POST["telephone"]
        id_number = request.POST["id_number"]
        

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "sales/new_office.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "sales/new_office.html", {
                "message": "Username already taken."
            })
        #login(request, user)
        try:
            user_id = User.objects.get(username=username)
            office = Office(user=user_id, first_name=first_name, last_name=last_name)
            office.save()
            user_id.is_office = True
            user_id.save()
        except:
            pass
        try:
            employee = Employee(first_name=first_name, last_name=last_name, telephone=telephone, id_number=id_number, email=email)
            employee.save()

        except:
            pass
        return HttpResponseRedirect(reverse("index"))
    else:
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_management = Manager(current_user)
        is_office = OfficeStaff(current_user)
        return render(request, "sales/new_office.html", {
            "is_super": is_super,
            "is_management": is_management,
            "is_office": is_office
        })

#Creates new employee for sales team
@login_required(login_url='login')
def new_employee(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        telephone = request.POST["telephone"]
        id_number = request.POST["id_number"]
        email = request.POST["email"]

        employee = Employee(first_name=first_name, last_name=last_name, telephone=telephone, id_number=id_number, email=email)
        employee.save()
        return HttpResponseRedirect(reverse("index"))


    else:
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_management = Manager(current_user)
        is_office = OfficeStaff(current_user)
        return render(request, "sales/new_employee.html", {
            "is_super": is_super,
            "is_management": is_management,
            "is_office": is_office
        })

#Deletes employee from sales, and if Office user deletes User
@login_required(login_url='login')
def fired(request):
    if request.method == "POST":
        employee = request.POST["employee"]
        office = request.POST["office"]
        if employee != "":
            Employee.objects.filter(id=employee).delete()
        if office != "":
            fired = Office.objects.get(id=office)
            User.objects.get(id=fired.user_id).delete()
            Office.objects.filter(id=office).delete()
        
        return HttpResponseRedirect(reverse("index"))

    else:
        employees = Employee.objects.all().order_by("last_name")
        offices = Office.objects.all()

        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_management = Manager(current_user)
        is_office = OfficeStaff(current_user)
        return render(request, "sales/fired.html", {
            "is_super": is_super,
            "is_management": is_management,
            "is_office": is_office,
            "employees": employees,
            "offices": offices
        })

#Add New Manager to list and as user
@login_required(login_url='login')
def management(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        telephone = request.POST["telephone"]
        id_number = request.POST["id_number"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "sales/new_management.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "sales/new_management.html", {
                "message": "Username already taken."
            })
        #login(request, user)
        try:
            user_id = User.objects.get(username=username)
            management = Management(user=user_id, first_name=first_name, last_name=last_name, telephone=telephone, id_number=id_number, email=email)
            management.save()          
            user_id.is_management = True
            user_id.save()
            office = Office(user=user_id, first_name=first_name, last_name=last_name)
            office.save()
            
        except:
            pass
        return HttpResponseRedirect(reverse("index"))
    else:
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_management = Manager(current_user)
        is_office = OfficeStaff(current_user)
        return render(request, "sales/new_management.html", {
            "is_super": is_super,
            "is_management": is_management,
            "is_office": is_office
        })

#Adds New hotel to list
@login_required(login_url='login')
def hotel(request):
    if request.method == "POST":
        hotel_name = request.POST["hotel_name"]
        hotel = Hotel(hotel_name=hotel_name)
        hotel.save()
        return HttpResponseRedirect(reverse("hotel"))

    else:
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_management = Manager(current_user)
        is_office = OfficeStaff(current_user)
        return render(request, "sales/new_hotel.html", {
            "is_super": is_super,
            "is_management": is_management,
            "is_office": is_office
        })

#Adds new activity to the list
@login_required(login_url='login')
def activity(request):
    if request.method == "POST":
        activity = request.POST["activity"]
        activity = Activity(activity=activity)
        activity.save()

        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_management = Manager(current_user)
        is_office = OfficeStaff(current_user)
        return render(request, "sales/new_activity.html", {
            "is_super": is_super,
            "is_management": is_management,
            "is_office": is_office,
            "message": "Activity Added"
        })

    else:
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_management = Manager(current_user)
        is_office = OfficeStaff(current_user)
        return render(request, "sales/new_activity.html", {
            "is_super": is_super,
            "is_management": is_management,
            "is_office": is_office,
        })

#Searches ticekts by Hotel with either Room Number or Email
@login_required(login_url='login')
def tickets(request):
    if request.method == "POST":
        room_number = request.POST["room_number"]
        client_email = request.POST["client_email"]
        hotel_id = request.POST["hotel"]
        hotel = Hotel.objects.get(id=hotel_id)
        tickets=[]
        try:
            tickets = Sale.objects.filter(room_number=room_number).filter(hotel=hotel).order_by("-date_sold")
        except:
            pass
        
        try:
            tickets2 = Sale.objects.filter(client_email=client_email).filter(hotel=hotel).order_by("-date_sold")        

        except:
            pass
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_management = Manager(current_user)
        is_office = OfficeStaff(current_user)
        return render(request, "sales/ticket-list.html", {
                "is_super": is_super,
                "is_management": is_management,
                "is_office": is_office,
                "tickets": tickets,
                "tickets2": tickets2
            })

    else:
        hotels = Hotel.objects.all()
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_management = Manager(current_user)
        is_office = OfficeStaff(current_user)
        return render(request, "sales/ticket-search.html", {
            "is_super": is_super,
            "is_management": is_management,
            "is_office": is_office,
            "hotels": hotels
        })


@login_required(login_url='login')
def ticket(request, sale_id):
    #Resends receipt to client 
    if request.method == "POST":
        ticket = Sale.objects.get(id=sale_id)
        client_email = ticket.client_email
        subject = 'Mariana Caribbean Sports Sales Receipt'
        html_message = render_to_string('sales/email.html', {'ticket': ticket})
        plain_message = strip_tags(html_message)
        from_email = 'From Mariana Caribbean Sports'
        to = client_email

        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        
        return HttpResponseRedirect(reverse("index"))
    
    else:
        #Gets a single ticket of a client
        ticket = Sale.objects.get(id=sale_id)
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_management = Manager(current_user)
        is_office = OfficeStaff(current_user)
        return render(request, "sales/ticket.html", {
            "is_super": is_super,
            "is_management": is_management,
            "is_office": is_office,
            "ticket": ticket
        })

#Shows a daily report of sales
@login_required(login_url='login')
def daily_reports(request):
    if request.method == "POST":
        hotel_id = request.POST["hotel"]
        hotel = Hotel.objects.get(id=hotel_id)
        date = request.POST["date"]
        tickets = Sale.objects.filter(date_sold=date).filter(hotel=hotel).order_by("-id")        
        
        #Finds Payment Types and totals it
        usds = tickets.filter(payment="US Dollar")
        usd_total = 0
        for usd in usds:
            usd_total += usd.total_cost

        cdns = tickets.filter(payment="Canadian Dollar")
        cdn_total = 0
        for cdn in cdns:
            cdn_total += cdn.total_cost

        rds = tickets.filter(payment="Dominican Peso")
        rd_total = 0
        for rd in rds:
            rd_total += rd.total_cost

        euros = tickets.filter(payment="Euro")
        euro_total = 0
        for euro in euros:
            euro_total += euro.total_cost

        visas = tickets.filter(payment="Visa")
        visa_total = 0
        for visa in visas:
            visa_total += visa.total_cost

        mcs = tickets.filter(payment="Master Card")
        mc_total = 0
        for mc in mcs:
            mc_total += mc.total_cost

        amexs = tickets.filter(payment="Amex")
        amex_total = 0
        for amex in amexs:
            amex_total += amex.total_cost

        #Gets All Activity Names
        activities = Activity.objects.all()
        act_list = []
        for a in activities:
            act_list.append(a.activity)

        #Gets all Activity Sales
        sales_numbers = []
        for a in activities:
            x = ActivityReport(a, tickets) 
            sales_numbers.append(x)

        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_management = Manager(current_user)
        is_office = OfficeStaff(current_user)
        return render(request, "sales/daily-report.html", {
            "is_super": is_super,
            "is_management": is_management,
            "is_office": is_office,
            "tickets": tickets,
            "date": date,
            "hotel": hotel,
            "usd_total": usd_total,
            "cdn_total": cdn_total,
            "rd_total": rd_total,
            "euro_total": euro_total,
            "visa_total":  visa_total,
            "mc_total": mc_total,
            "amex_total": amex_total,
            "act_list": act_list,
            "sales_numbers": sales_numbers,
        })

    else:
        hotels = Hotel.objects.all()
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_management = Manager(current_user)
        is_office = OfficeStaff(current_user)
        return render(request, "sales/daily-report-search.html", {
            "is_super": is_super,
            "is_management": is_management,
            "is_office": is_office,
            "hotels": hotels
        })

#Shows a Monthly report of sales
@login_required(login_url='login')
def monthly_reports(request):
    if request.method == "POST":
        hotel_id = request.POST["hotel"]
        year = request.POST["year"]
        month = request.POST["month"]
        date = ""
        if month == "0":
            if hotel_id == "All Hotels":
                tickets = Sale.objects.filter(date_sold__year=year)
                hotel = "All Hotels"
            else:
                hotel = Hotel.objects.get(id=hotel_id)        
                tickets = Sale.objects.filter(date_sold__year=year).filter(hotel=hotel)
        else:
            if hotel_id == "All Hotels":
                tickets = Sale.objects.filter(date_sold__year=year).filter(date_sold__month=month)
                hotel = "All Hotels"
            else:
                hotel = Hotel.objects.get(id=hotel_id)        
                tickets = Sale.objects.filter(date_sold__year=year).filter(date_sold__month=month).filter(hotel=hotel)
        
        #Gets All Activity Names
        activities = Activity.objects.all()
        act_list = []
        for a in activities:
            act_list.append(a.activity)

        #Gets all Activity Sales
        sales_numbers = []
        for a in activities:
            x = ActivityReport(a, tickets) 
            sales_numbers.append(x)

        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_management = Manager(current_user)
        is_office = OfficeStaff(current_user)
        return render(request, "sales/monthly-report.html", {
            "is_super": is_super,
            "is_management": is_management,
            "is_office": is_office,
            "hotel": hotel,
            "date": date,
            "year": year,
            "month": month,
            "act_list": act_list,
            "sales_numbers": sales_numbers,
        })

    else:
        hotels = Hotel.objects.all()
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_management = Manager(current_user)
        is_office = OfficeStaff(current_user)
        return render(request, "sales/monthly-report-search.html", {
            "is_super": is_super,
            "is_management": is_management,
            "is_office": is_office,
            "hotels": hotels
        })


#Shows a report of sales by Employee
@login_required(login_url='login')
def employee_sales(request):
    if request.method == "POST":
        employee_id = request.POST["employee"]
        year = request.POST["year"]
        month = request.POST["month"]
        date = request.POST["date"]
        if date == "":
            if month == "0":
                employee = Employee.objects.get(id=employee_id)        
                tickets = Sale.objects.filter(date_sold__year=year).filter(seller=employee)
            else:
                employee = Employee.objects.get(id=employee_id)        
                tickets = Sale.objects.filter(date_sold__year=year).filter(date_sold__month=month).filter(seller=employee)
        else:
            if month == "0":
                employee = Employee.objects.get(id=employee_id)        
                tickets = Sale.objects.filter(date_sold=date).filter(seller=employee)
            else:
                employee = Employee.objects.get(id=employee_id)        
                tickets = Sale.objects.filter(date_sold=date).filter(seller=employee)
        
        #Gets All Activity Names
        activities = Activity.objects.all()
        act_list = []
        for a in activities:
            act_list.append(a.activity)

        #Gets all Activity Sales
        sales_numbers = []
        for a in activities:
            x = ActivityReport(a, tickets) 
            sales_numbers.append(x)
    
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_management = Manager(current_user)
        is_office = OfficeStaff(current_user)
        return render(request, "sales/monthly-report.html", {
            "is_super": is_super,
            "is_management": is_management,
            "is_office": is_office,
            "employee": employee,
            "date": date,
            "year": year,
            "tickets": tickets,
            "month": month,
            "act_list": act_list,
            "sales_numbers": sales_numbers,
        })

    else:
        employees = Employee.objects.all().order_by("last_name")
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_management = Manager(current_user)
        is_office = OfficeStaff(current_user)
        return render(request, "sales/employee-report-search.html", {
            "is_super": is_super,
            "is_management": is_management,
            "is_office": is_office,
            "employees": employees
        })

@login_required(login_url='login')
def staff_list(request):
    if request.method == "POST":
        pass
    
    else:
        employees = Employee.objects.all().order_by("last_name")
        current_user = request.user.get_username()
        is_super = SuperUser(current_user)
        is_management = Manager(current_user)
        is_office = OfficeStaff(current_user)
        return render(request, "sales/employee-list.html", {
            "is_super": is_super,
            "is_management": is_management,
            "is_office": is_office,
            "employees": employees
        })

#SuperUser or Management are able to delete sales
@login_required(login_url='login')
def refund(request, ticket_id):
    if request.method == "POST":
        Sale.objects.filter(id=ticket_id).delete()

        return HttpResponseRedirect(reverse("daily_reports"))
    
    else:
        pass

def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="emails.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Client Name', 'Email address']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = EmailList.objects.all().values_list('client_name', 'client_email')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


    #Shows a daily report of sales
@login_required(login_url='login')
def my_report(request):
    user = request.user.get_username()
    current = User.objects.get(username=user)
    current_user = Office.objects.get(user_id=current)
    today = date.today()
    tickets = Sale.objects.filter(date_sold=today).filter(office=current_user).order_by("-id")
   
    #Finds Payment Types and totals it
    usds = tickets.filter(payment="US Dollar")
    usd_total = 0
    for usd in usds:
        usd_total += usd.total_cost

    cdns = tickets.filter(payment="Canadian Dollar")
    cdn_total = 0
    for cdn in cdns:
        cdn_total += cdn.total_cost

    rds = tickets.filter(payment="Dominican Peso")
    rd_total = 0
    for rd in rds:
        rd_total += rd.total_cost

    euros = tickets.filter(payment="Euro")
    euro_total = 0
    for euro in euros:
        euro_total += euro.total_cost

    visas = tickets.filter(payment="Visa")
    visa_total = 0
    for visa in visas:
        visa_total += visa.total_cost

    mcs = tickets.filter(payment="Master Card")
    mc_total = 0
    for mc in mcs:
        mc_total += mc.total_cost

    amexs = tickets.filter(payment="Amex")
    amex_total = 0
    for amex in amexs:
        amex_total += amex.total_cost

    #Gets All Activity Names
    activities = Activity.objects.all()
    act_list = []
    for a in activities:
        act_list.append(a.activity)

    #Gets all Activity Sales
    sales_numbers = []
    for a in activities:
        x = ActivityReport(a, tickets) 
        sales_numbers.append(x)


    current_user = request.user.get_username()
    is_super = SuperUser(current_user)
    is_management = Manager(current_user)
    is_office = OfficeStaff(current_user)
    return render(request, "sales/daily-report.html", {
        "is_super": is_super,
        "is_management": is_management,
        "is_office": is_office,
        "tickets": tickets,
        "date": today,
        "hotel": hotel,
        "usd_total": usd_total,
        "cdn_total": cdn_total,
        "rd_total": rd_total,
        "euro_total": euro_total,
        "visa_total":  visa_total,
        "mc_total": mc_total,
        "amex_total": amex_total,
        "act_list": act_list,
        "sales_numbers": sales_numbers,
    })

def export_users_xls2(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sales.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Ticket Number', 'Seller', 'Hotel', 'Date Sold', 'Activity Date', 'Activity Time', 'Payment', 'Room Number', 'Client Name', 'Client Email', 'Quantity1', 'Activity1', 'Price1', 'Quantity2', 'Activity2', 'Price2', 'Quantity3', 'Activity3', 'Price3', 'Total Cost', 'Office', 'Pickup location', 'Comments']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Sale.objects.all().values_list('id', 'seller', 'hotel', 'date_sold', 'activity_date', 'activity_time', 'payment', 'room_number', 'client_name', 'client_email', 'quantity1', 'activity1', 'price1', 'quantity2', 'activity2', 'price2', 'quantity3', 'activity3', 'price3', 'total_cost', 'office', 'pickup_location', 'comments').order_by("-id") 
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response