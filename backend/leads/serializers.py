from rest_framework import serializers

from .models import Category, Lead


class LeadSerializer(serializers.ModelSerializer):
    organizer = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        """
        organizer shouldn't see the organizer field while creating a new lead. so organizer is a readonly field.
        in this create method organizer will be added automatically to the organizer field
        """
        user = self.context["user"]
        # authenticated user which is an organizer user

        return Lead.objects.create(organizer=user.organizeruser, **validated_data)

    class Meta:
        model = Lead
        fields = [
            "id",
            "first_name",
            "last_name",
            "age",
            "agent",
            "organizer",
            "category",
            "description",
            "date_added",
            "phone_number",
            "email",
            "converted_date",
        ]


class LeadAdminSerializer(serializers.ModelSerializer):
    """Admin can see the organizer field and choose the organizer user"""

    class Meta:
        model = Lead
        fields = [
            "id",
            "first_name",
            "last_name",
            "age",
            "organizer",
            "agent",
            "category",
            "description",
            "date_added",
            "phone_number",
            "email",
            "converted_date",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]
