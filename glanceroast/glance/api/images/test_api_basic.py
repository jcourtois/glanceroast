"""
Copyright 2013 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from cafe.drivers.unittest.decorators import tags
from cloudroast.glance.fixtures import ImagesFixture


class ImagesAPIBasicTest(ImagesFixture):

    def test_get_image_response_code(self):
        """Validate that the response code for Get Image is correct."""
        resp = self.images_client.get_image(self.primary_image)
        self.assertEqual(resp.status_code, 200)

    def test_get_images_schema_response_code(self):
        """Validate that the response code for Get Images Schema is correct."""
        resp = self.images_client.get_images_schema()
        self.assertEqual(resp.status_code, 200)

    def test_get_image_schema_response_code(self):
        """Validate that the response code for Get Image Schema is correct."""
        resp = self.images_client.get_image_schema()
        self.assertEqual(resp.status_code, 200)

    def list_images_response_code(self):
        """Validate that the response code for List Images is correct."""
        resp = self.images_client.list_images()
        self.assertEqual(resp.status_code, 200)

    def test_get_image_file_response_code(self):
        """Validate that the response code for Get Image File is correct."""
        resp = self.images_client.get_image_file(self.primary_image)
        self.assertEqual(resp.status_code, 200)

    def test_get_image_members_schema_response_code(self):
        """Validate that the response code for Get Image Members Schema is correct."""
        resp = self.images_client.get_image_members_schema()
        self.assertEqual(resp.status_code, 200)

    def test_get_image_member_schema_response_code(self):
        """Validate that the response code for Get Image Member Schema is correct."""
        resp = self.images_client.get_image_member_schema()
        self.assertEqual(resp.status_code, 200)
