import datetime
import pytest
from django.conf import settings
from django.test.utils import override_settings
from resources.models.utils import get_payment_requested_waiting_time

from resources.models import Reservation, Resource, Unit
from payments.models import Product, Order
from payments.factories import OrderFactory


@pytest.fixture
def unit_payment_time_defined():
    return Unit.objects.create(
        name="unit_payment",
        time_zone='Europe/Helsinki',
        payment_requested_waiting_time=98
    )

@pytest.fixture
def unit_payment_time_env():
    return Unit.objects.create(
        name="unit_payment",
        time_zone='Europe/Helsinki',
        payment_requested_waiting_time=0
    )

@pytest.fixture
def get_resource_data(space_resource_type):
    return {
        'type': space_resource_type,
        'authentication': 'weak',
        'need_manual_confirmation': True,
        'max_reservations_per_user': 1,
        'max_period': datetime.timedelta(hours=2),
        'reservable': True,
    }

@pytest.fixture
def resource_resource_waiting_time(unit_payment_time_defined, get_resource_data):
    return Resource.objects.create(
        name="resource with waiting_time value.",
        unit=unit_payment_time_defined,
        payment_requested_waiting_time=48,
        **get_resource_data
    )

@pytest.fixture
def resource_unit_waiting_time(unit_payment_time_defined, get_resource_data):
    return Resource.objects.create(
        name="resource with no waiting_time value.",
        unit=unit_payment_time_defined,
        payment_requested_waiting_time=0,
        **get_resource_data
    )
@pytest.fixture
def resource_env_waiting_time(unit_payment_time_env, get_resource_data):
    return Resource.objects.create(
        name="resource with no waiting_time value.",
        unit=unit_payment_time_env,
        payment_requested_waiting_time=0,
        **get_resource_data
    )


@pytest.fixture
def get_reservation_data(user):
    '''
    Dict containing reservation data for the other reservation fixtures.
    '''
    return {
        'begin': '2022-02-02T12:00:00+02:00',
        'end': '2022-02-02T14:00:00+02:00',
        'user': user,
        'state': Reservation.WAITING_FOR_PAYMENT
    }

@pytest.fixture
def reservation_resource_waiting_time(resource_resource_waiting_time, get_reservation_data):
    '''
    Reservation for test where the resource waiting_time is used.
    '''
    return Reservation.objects.create(
        resource=resource_resource_waiting_time,
        reserver_name='name_time_from_resource',
        **get_reservation_data
    )

@pytest.fixture
def reservation_unit_waiting_time(resource_unit_waiting_time, get_reservation_data):
    '''
    Reservation for test where the unit waiting_time is used.
    '''
    return Reservation.objects.create(
        resource=resource_unit_waiting_time,
        reserver_name='name_time_from_unit',
        **get_reservation_data
    )


@pytest.fixture
def reservation_env_waiting_time(resource_env_waiting_time, get_reservation_data):
    '''
    Reservation for test where the env waiting_time is used.
    '''
    return Reservation.objects.create(
        resource=resource_env_waiting_time,
        reserver_name='name_time_from_env',
        **get_reservation_data
    )

@pytest.fixture
def get_order_data():
    '''
    Dict containing order data for other fixtures.
    '''
    return {'state': Order.WAITING, 'confirmed_by_staff_at':'2022-01-10T12:00:00+02:00'}

@pytest.fixture
def order_resource_waiting_time(reservation_resource_waiting_time, get_order_data):
    '''
    Order for test where the resource waiting_time is used.
    '''
    return OrderFactory(
        reservation=reservation_resource_waiting_time,
        **get_order_data
    )

@pytest.fixture
def order_unit_waiting_time(reservation_unit_waiting_time, get_order_data):
    '''
    Order for test where the unit waiting_time is used.
    '''
    return OrderFactory(
        reservation=reservation_unit_waiting_time,
        **get_order_data
    )

@pytest.fixture
def order_env_waiting_time(reservation_env_waiting_time, get_order_data):
    '''
    Order for test where the env waiting_time is used.
    '''
    return OrderFactory(
        reservation=reservation_env_waiting_time,
        **get_order_data
    )


def calculate_times(reservation, waiting_time):
    '''
    Used to calculate the expected waiting_time.
    '''
    exact_value = reservation.order.confirmed_by_staff_at + datetime.timedelta(hours=waiting_time)
    rounded_value = exact_value.replace(microsecond=0, second=0, minute=0)
    return rounded_value.astimezone(reservation.resource.unit.get_tz()).strftime('%d.%m.%Y %H:%M')


@pytest.mark.django_db
def test_returns_waiting_time_from_resource(reservation_resource_waiting_time, order_resource_waiting_time):
    '''
    Resource's waiting_time is used if defined.
    '''
    reservation = Reservation.objects.get(reserver_name='name_time_from_resource')
    return_value = get_payment_requested_waiting_time(reservation)
    
    expected_value = calculate_times(reservation=reservation, waiting_time=reservation.resource.payment_requested_waiting_time)
    assert return_value == expected_value


@pytest.mark.django_db
def test_return_waiting_time_from_unit(reservation_unit_waiting_time, order_unit_waiting_time):
    '''
    Unit waiting_time is used when the resource does not have a waiting_time.
    '''
    reservation = Reservation.objects.get(reserver_name='name_time_from_unit')
    return_value = get_payment_requested_waiting_time(reservation)
    
    expected_value = calculate_times(reservation=reservation, waiting_time=reservation.resource.unit.payment_requested_waiting_time)
    assert return_value == expected_value


@pytest.mark.django_db
@override_settings(RESPA_PAYMENTS_PAYMENT_REQUESTED_WAITING_TIME=6)
def test_return_waiting_time_from_env(reservation_env_waiting_time, order_env_waiting_time):
    '''
    Environment variable is used when neither the resource or the unit have a waiting_time. 
    '''
    reservation = Reservation.objects.get(reserver_name='name_time_from_env')
    return_value = get_payment_requested_waiting_time(reservation)
    
    expected_value = calculate_times(reservation=reservation, waiting_time=settings.RESPA_PAYMENTS_PAYMENT_REQUESTED_WAITING_TIME)
    assert return_value == expected_value