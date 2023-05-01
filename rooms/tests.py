from rest_framework.test import APITestCase
from . import models


class TestAmenities(APITestCase):
    NAME = "Amenity Test"
    DESC = "Amenity Description"
    URL = "/api/v1/rooms/amenities/"

    def setUp(self) -> None:
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenities(self):
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200."
        )
        self.assertIsInstance(
            data,
            list,
        )

        self.assertEqual(
            len(data),
            1
        )

        self.assertEqual(
            data[0]["name"],
            self.NAME,
        )

        self.assertEqual(
            data[0]["description"],
            self.DESC,
        )

    def test_create_amenity(self):
        response = self.client.post(self.URL, data={
            #"name": "Valid Amenity",
            "description": "My Valid Amenity"
        })

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200"
        )