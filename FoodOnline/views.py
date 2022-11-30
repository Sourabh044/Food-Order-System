from django.shortcuts import render
from vendor.models import Vendor
from django.contrib.gis.geos import GEOSGeometry
# ``D`` is a shortcut for ``Distance``
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance


def HomeView(request):
    if 'lat' in request.GET:
        lat = request.GET['lat']
        lng = request.GET['lng']
        request.session['lat'] = lat
        request.session['lng'] = lng
        pnt = GEOSGeometry('POINT(%s %s)' % (lng, lat))
        vendors = Vendor.objects.filter(user_profile__latlng__distance_lte=(pnt, D(km=5))
                                        ).annotate(distance=Distance('user_profile__latlng', pnt)).order_by('distance')[:8]

        # print(vendors)
        for v in vendors:
            v.kms = round(v.distance.km, 1)

        vendor_count = vendors.count()
        context = {
            'vendors': vendors,
            'vendors_count': vendor_count,
        }
        return render(request, "home.html", context)

    elif 'lat' in request.session:
        lat = request.session['lat']
        lng = request.session['lng']
        pnt = GEOSGeometry('POINT(%s %s)' % (lng, lat))
        vendors = Vendor.objects.filter(user_profile__latlng__distance_lte=(pnt, D(km=5))
                                        ).annotate(distance=Distance('user_profile__latlng', pnt)).order_by('distance')[:8]
        for v in vendors:
            v.kms = round(v.distance.km, 1)

        vendor_count = vendors.count()
        context = {
            'vendors': vendors,
            'vendors_count': vendor_count,
        }

        return render(request, "home.html", context)
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    context = {
        'vendors': vendors,
    }
    return render(request, "home.html",context)
