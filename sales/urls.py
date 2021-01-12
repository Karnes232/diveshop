from django.urls import path
from django.contrib.auth import views as auth_views
from .views import PasswordsChangeView

from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("office", views.office, name="office"),
    path("new_employee", views.new_employee, name="new_employee"),
    path("management", views.management, name="management"),
    path("hotel", views.hotel, name="hotel"),
    path("activity", views.activity, name="activity"),
    path("tickets", views.tickets, name="tickets"),
    path("ticket/<int:sale_id>", views.ticket, name="ticket"),
    path("fired", views.fired, name="fired"),
    path("daily_reports", views.daily_reports, name="daily_reports"),
    path("monthly_reports", views.monthly_reports, name="monthly_reports"),
    path("employee_sales", views.employee_sales, name="employee_sales"),
    path("staff_list", views.staff_list, name="staff_list"),
    path("refund/<int:ticket_id>", views.refund, name="refund"),
    path("my_report", views.my_report, name="my_report"),
    path("daily_money_report", views.daily_money_report, name="daily_money_report"),
    path("cash_flow", views.cash_flow, name="cash_flow"),
    path("edit_ticket/<int:ticket_id>", views.edit_ticket, name="edit_ticket"),
    
    

    #Change Passwords
    path('password/', PasswordsChangeView.as_view(template_name='sales/change-password.html'), name="password"),
    path("password_success", views.password_success, name="password_success"),

    #Reset Password Setup
    path('reset_password', auth_views.PasswordResetView.as_view(template_name="sales/password_reset.html"), name="reset_password"),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name="sales/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="sales/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="sales/password_reset_done.html"), name="password_reset_complete"),

    #Downloads Excel file
    path(r'^export/xls/$', views.export_users_xls, name='export_users_xls'),
    path(r'^export/xls2/$', views.export_users_xls2, name='export_users_xls2'),
]