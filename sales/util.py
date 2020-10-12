from .models import User, Activity

def SuperUser(current_user):
    superusers = User.objects.filter(is_owner=True)
    current_id = User.objects.get(username=current_user)
    is_super = False
    for su in superusers:
        if current_id == su:
            is_super = True
    return is_super


def Manager(current_user):
    managers = User.objects.filter(is_management=True)
    current_id = User.objects.get(username=current_user)
    is_management = False
    for manager in managers:
        if current_id == manager:
            is_management = True
    return is_management


def OfficeStaff(current_user):
    office = User.objects.filter(is_office=True)
    current_id = User.objects.get(username=current_user)
    is_office = False
    for o in office:
        if current_id == o:
            is_office = True
    return is_office


def ActivityReport(Id, tickets):
    activity1_1 = tickets.filter(activity1=Id)
    activity1_2 = tickets.filter(activity2=Id)
    activity1_3 = tickets.filter(activity3=Id)
    activity1 = 0
    for act in activity1_1:
        activity1 += (act.quantity1*act.price1)
    for act in activity1_2:
        activity1 += (act.quantity2*act.price2)
    for act in activity1_3:
            activity1 += (act.quantity3*act.price3)
    return activity1


