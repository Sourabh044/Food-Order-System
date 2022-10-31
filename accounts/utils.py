
from django.shortcuts import redirect


def detectUser(user):
    if user.role == 1:
        redirecturl = 'Vendor-Dashboard'
        return redirecturl
    elif user.role == 2 :
        redirecturl = 'Customer-Dashboard'
        return redirecturl
    elif user.role == None and user.is_superadmin:
        redirecturl = '/admin'
        return redirecturl