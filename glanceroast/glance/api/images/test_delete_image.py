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
from cloudcafe.images.common.types import (
    ImageContainerFormat, ImageDiskFormat, ImageStatus)
from glanceroast.glance.fixtures import ImagesFixture
from cloudcafe.common.tools.datagen import rand_name


class DeleteImageTest(ImagesFixture):

    @classmethod
    def setUpClass(cls):
        super(DeleteImageTest, cls).setUpClass()
        cls.name = rand_name('image')
        cls.tag = rand_name('tag')
        resp = cls.images_client.create_image(name=cls.name, container_format=ImageContainerFormat.BARE,
                                              disk_format=ImageDiskFormat.QCOW2, tags=[cls.tag])
        cls.image = resp.entity
        with open(cls.images_config.test_image_name, 'rb') as image_file:
            cls.images_client.store_image_file(image_id=cls.image.id_, file_data=image_file)
        cls.image = cls.images_client.get_image(cls.image.id_).entity
        cls.images_client.delete_image(cls.image.id_)

    def test_get_deleted_image_fails(self):
        """Verify that a GET request for a deleted image fails."""
        resp = self.images_client.get_image(self.image.id_)
        self.assertEqual(resp.status_code, 404)

    def test_get_deleted_image_not_listed(self):
        """Verify that a deleted image does not appear in the list of all images."""
        images = self.images_client.list_images().entity
        self.assertNotIn(self.image, images)
