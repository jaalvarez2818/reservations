"""reservations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.urls import path

from misc.views.reservation import ReservationListView, ReservationApproveView, ReservationRejectView, \
    ReservationExecuteView, ReservationNotExecuteView, ReservationDetailView, ReservationPDFView, LocatorView, \
    StatisticsView, ReservationCreateView, CheckAvailabilityView, CheckPersonView
from misc.views.room_typology import RoomTypologyListView
from misc.views.unpleasant_customer import UnpleasantCustomerListView, UnpleasantCustomerActiveView, \
    UnpleasantCustomerUpdateView, UnpleasantCustomerCreateView

urlpatterns = i18n_patterns(
    path('', ReservationListView.as_view(), name='reservation_list'),
    path('room_typologies', RoomTypologyListView.as_view(), name='room_typology_list'),
    path('unpleasant_customers', UnpleasantCustomerListView.as_view(), name='unpleasant_customer_list'),
    path('unpleasant_customers/create', UnpleasantCustomerCreateView.as_view(), name='unpleasant_customer_create'),
    path('unpleasant_customers/active/<int:pk>', UnpleasantCustomerActiveView.as_view(),
         name='unpleasant_customer_active'),
    path('unpleasant_customers/update/<int:pk>', UnpleasantCustomerUpdateView.as_view(),
         name='unpleasant_customer_update'),
    path('locator', LocatorView.as_view(), name='locator'),
    path('create', ReservationCreateView.as_view(), name='reservation_create'),
    path('statistics', StatisticsView.as_view(), name='statistics'),
    path('approve/<str:pk>', ReservationApproveView.as_view(), name='reservation_approve'),
    path('reject/<str:pk>', ReservationRejectView.as_view(), name='reservation_reject'),
    path('execute/<str:pk>', ReservationExecuteView.as_view(), name='reservation_execute'),
    path('not_execute/<str:pk>', ReservationNotExecuteView.as_view(), name='reservation_not_execute'),
    path('details/<str:locator>', ReservationDetailView.as_view(), name='reservation_details'),
    path('pdf/<str:locator>', ReservationPDFView.as_view(), name='reservation_pdf'),
    path('availability', CheckAvailabilityView.as_view(), name='check_availability'),
    path('check_person', CheckPersonView.as_view(), name='check_person'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
               + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
