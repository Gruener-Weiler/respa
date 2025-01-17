import logging
import json
import random
from respa_o365.o365_calendar import MicrosoftApi
from django.conf import settings
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.http import HttpResponseRedirect
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission, IsAuthenticated
from requests_oauthlib import OAuth2Session
from urllib.parse import urlparse, parse_qs
from resources.models import Resource, Period
from users.models import User
from .calendar_sync import add_to_queue, perform_sync_to_exchange, ensure_notification
from .models import OutlookCalendarLink, OutlookTokenRequestData

logger = logging.getLogger(__name__)

class CanCreateCalendarLink(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Resource):
            return obj.unit.is_manager(request.user)
        return False

class LoginStartView(APIView):
    permission_classes = [IsAuthenticated, CanCreateCalendarLink]
    def get(self, request):
        resource_id = request.query_params.get('resource_id')
        return_to = request.query_params.get('return_to')

        resource = generics.get_object_or_404(Resource.objects.all(), pk=resource_id)
        self.check_object_permissions(request, resource)

        if request.user.is_superuser:
            try:
                user_id = request.query_params.get('user_id')
                user = User.objects.get(pk=user_id)
            except:
                user = request.user
        else:
            user = request.user


        authorization_url, state = LoginStartView.generate_msgraph_auth()
        o = OutlookTokenRequestData.objects.create(
            state=state,
            return_to=return_to,
            resource_id=resource_id,
            created_at=timezone.now(),
            user=user
        )
        return Response({
                'redirect_link': authorization_url,
                'state': state
            })

    @staticmethod
    def generate_msgraph_auth():
        msgraph = OAuth2Session(settings.O365_CLIENT_ID,
            scope=['offline_access', 'User.Read', 'Calendars.ReadWrite'],
            redirect_uri=settings.O365_CALLBACK_URL)

        return msgraph.authorization_url(settings.O365_AUTH_URL)

class LoginCallBackView(APIView):
    def get(self, request):
        state = request.query_params.get('state')

        try:
            stored_data = OutlookTokenRequestData.objects.get(state=state)
        except OutlookTokenRequestData.DoesNotExist:
            logger.error("Stored data does not exist for state.")
            return Response(data="Invalid state.", status=status.HTTP_400_BAD_REQUEST)

        if OutlookCalendarLink.objects.filter(resource=stored_data.resource).exists():
            # Link already exists
            logger.warn("Already linked resource {}.".format(stored_data.resource))
            return HttpResponseRedirect(redirect_to=stored_data.return_to)

        url = request.build_absolute_uri(request.get_full_path())

        msgraph = OAuth2Session(settings.O365_CLIENT_ID, state=state,
            redirect_uri=settings.O365_CALLBACK_URL)
        token = msgraph.fetch_token(settings.O365_TOKEN_URL,
                    client_secret=settings.O365_CLIENT_SECRET,
                    authorization_response=url)
        token = json.dumps(token)

        res = stored_data.resource

        api = MicrosoftApi(token=token)
        me_json = api.get('me')
        microsoft_user = me_json.get('id')

        # Delete existing periods because they will not sync to Outlook, and the format may be incompatible.
        existing_periods = Period.objects.filter(resource=res)
        existing_periods.delete()
        res.update_opening_hours()

        link = OutlookCalendarLink.objects.create(
            resource=stored_data.resource,
            user=stored_data.user,
            token=token,
            microsoft_user_id=microsoft_user
        )

        add_to_queue(link)
        ensure_notification(link)
        stored_data.delete()

        return HttpResponseRedirect(redirect_to=stored_data.return_to)
