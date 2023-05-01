from django.utils import timezone

from rest_framework import serializers

from experiences.serializers import ExperienceDetailSerializer

from .models import Booking


class CreateRoomBookingSerializer(serializers.ModelSerializer):

    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = [
            "check_in",
            "check_out",
            "guests",
        ]

    def validate(self, attrs):
        check_in = attrs.get("check_in")
        check_out = attrs.get("check_out")
        now = timezone.localtime(timezone.now()).date()
        if check_in >= check_out:
            raise serializers.ValidationError("Check-Out should be later than Check-In")
        if now > check_in or now > check_out:
            raise serializers.ValidationError("Can't book in the past.")

        if Booking.objects.filter(
            check_in__lte=check_out,
            check_out__gte=check_in,
        ).exists():
            print(Booking.objects.filter(check_in__lte=check_out, check_out__gte=check_in))
            raise serializers.ValidationError("This room is already reserved..")
        return attrs


class CreateExperienceBookingSerializer(serializers.ModelSerializer):
    experience_time = serializers.DateTimeField()

    class Meta:
        model = Booking
        fields = [
            "kind",
            "experience_time",
            "guests",
        ]

    def validate(self, attrs):
        experience_time = attrs.get('experience_time')
        now = timezone.localtime(timezone.now())

        if now > experience_time:
            raise serializers.ValidationError("Can't book in the past..")
        if Booking.objects.filter(
            experience_time__date=experience_time.date()
        ).exists():
            print(Booking.objects.filter(experience_time__date=experience_time).exists())
            raise serializers.ValidationError("This experience is already reserved..")
        return attrs


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        ]


class PublicExperienceBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "experience_time",
            "guests",
        ]

class PrivateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"