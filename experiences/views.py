from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Perk
from .serializers import PerkSerializer


class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            new_perk = serializer.save()
            return Response(PerkSerializer(new_perk).data)


class PerksDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        return Response(PerkSerializer(self.get_object(pk)).data)

    def put(self, request, pk):
        serializer = PerkSerializer(
            self.get_object(pk),
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)