from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet

from .models import Category, Lead
from .permissions import IsAdminOrOrganizer, IsAgent, IsOrganizer
from .serializers import (CategorySerializer, LeadAdminSerializer,
                          LeadSerializer)


# @api_view(["GET"])
# def api_root(request, format=None):
#     """
#     Leads nad Categories endpoints for browsable api
#     """
#     return Response(
#         {
#             "leads": reverse("leads", request=request, format=format),
#             "categories": reverse("categories", request=request, format=format),
#         }
#     )


class LeadsListApiView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrOrganizer]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "agent", "organizer"]
    search_fields = ["description"]
    ordering_fields = ["category", "date_added"]

    def get_serializer_class(self):
        user = self.request.user

        if user.is_staff:
            return LeadAdminSerializer
        else:
            return LeadSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Lead.objects.all()
        elif user.is_organizer:
            return Lead.objects.filter(organizer=user.organizeruser)
        elif user.is_agent:
            return Lead.objects.filter(agent=user.agent)
        else:
            raise ValidationError({"error": "Your are not an agent or an organizer "})

    def get_serializer_context(self):
        return {"user": self.request.user}
        # to access the authenticated user in the serializer


class LeadDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOrganizer]
    queryset = Lead.objects.all()

    def get_permissions(self):

        if self.request.method in ["PUT", "DELETE"]:
            return [IsAuthenticated(), IsOrganizer()]
        else:
            return [IsAuthenticated(), IsAgent()]


# class CategoryListView(generics.ListCreateAPIView):
#     serializer_class = CategorySerializer
#     permission_classes = [IsAuthenticated, IsAdminOrOrganizer]
#     queryset = Category.objects.all()
#
#
# class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = CategorySerializer
#     permission_classes = [IsAuthenticated, IsAdminOrOrganizer]
#     queryset = Category.objects.all()


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminOrOrganizer]
    queryset = Category.objects.all()
