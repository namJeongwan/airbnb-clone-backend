from datetime import datetime

from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Perk, Experience

from bookings.serializers import *

from . import serializers



class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = serializers.PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PerkSerializer(data=request.data)
        if serializer.is_valid():
            new_perk = serializer.save()
            return Response(serializers.PerkSerializer(new_perk).data)


class PerksDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        return Response(serializers.PerkSerializer(self.get_object(pk)).data)

    def put(self, request, pk):
        serializer = serializers.PerkSerializer(
            self.get_object(pk),
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(serializers.PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExperienceList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        """
        Get All Experiences
        :param request:
        :return: All Experiences Response(QuerySet)
        """
        experiences = Experience.objects.all()
        serializer = serializers.ExperienceListSerializer(
            experiences,
            many=True
        )
        return Response(serializer.data)

    def post(self, request):
        """
        Create New Experience
        :param request:
        :return:
        """
        serializer = serializers.ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                host=request.user,
            )
            return Response({"ok": True})
        else:
            return Response(serializer.errors)


class ExperienceDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    """
    Experience Detail Class
    """
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            return NotFound()

    def get(self, request, pk):
        """
        Get Detail Experience
        :param request:
        :param pk:
        :return:
        """
        experience = self.get_object(pk)
        serializer = serializers.ExperienceDetailSerializer(experience)
        print(experience)
        print(serializer.data)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update Experience by pk
        :param request:
        :param pk:
        :return:
        """
        experience = self.get_object(pk)
        serializer = serializers.ExperienceDetailSerializer(
            experience,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            if request.data.get('perks'):
                print(request.data.get('perks'))
                updated_experience = serializer.save(
                    perks=request.data.get('perks'),
                )
            else:
                updated_experience = serializer.save()
            serializer = serializers.ExperienceDetailSerializer(updated_experience)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        """
        Delete Experience by pk
        :param request:
        :param pk:
        :return:
        """
        experience = self.get_object(pk)
        experience.delete()
        return Response(status=status.HTTP_200_OK)


class ExperiencePerks(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound()

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = serializers.PerkSerializer(
            experience.perks,
            many=True,
        )
        return Response(serializer.data)


class ExperienceBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound()

    def get(self, request, pk):
        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now())
        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            experience_time__gt=now,
        )
        serializer = PublicExperienceBookingSerializer(
            bookings,
            many=True
        )
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        try:
            experience = self.get_object(pk)
            serializer = CreateExperienceBookingSerializer(data=request.data)
            if serializer.is_valid():
                new_booking = serializer.save(
                    user=request.user,
                    experience=experience,
                    kind=Booking.BookingKindChoices.EXPERIENCE,
                )
                serializer = PublicBookingSerializer(new_booking)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except Exception as e:
            print(e)
            return Response({"errors": e})