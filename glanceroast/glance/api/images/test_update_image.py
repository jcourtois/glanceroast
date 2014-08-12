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
from cloudroast.glance.fixtures import ImagesFixture
from cloudcafe.common.tools.datagen import rand_name


class UpdateImageTest(ImagesFixture):

    @classmethod
    def setUpClass(cls):
        super(UpdateImageTest, cls).setUpClass()
        cls.name = rand_name('image')
        cls.tag = rand_name('tag')
        resp = cls.images_client.create_image(
            name=cls.name, container_format=ImageContainerFormat.BARE,
            disk_format=ImageDiskFormat.QCOW2, tags=[cls.tag], protected=False)
        cls.image = resp.entity
        cls.resources.add(cls.image.id_, cls.images_client.delete_image)
        with open(cls.images_config.test_image_name, 'rb') as image_file:
            cls.images_client.store_image_file(image_id=cls.image.id_, file_data=image_file)
        cls.image = cls.images_client.get_image(cls.image.id_).entity

    def test_update_image_name(self):
        """When the image name is updated, verify the change is propagated."""
        updated_name = rand_name('image')
        resp = self.images_client.update_image(
            self.image.id_, replace={'name': updated_name})
        self.assertEqual(resp.status_code, 200)

        updated_image = self.images_client.get_image(self.image.id_).entity
        self.assertEqual(updated_image.name, updated_name)

    def test_update_image_protected_status(self):
        """When the protected status of an image is updated, verify the change is propagated."""
        resp = self.images_client.update_image(
            self.image.id_,
            replace={'protected': True})
        self.assertEqual(resp.status_code, 200)

        updated_image = self.images_client.get_image(self.image.id_).entity
        self.assertEqual(updated_image.protected, True)

    def test_update_image_tags(self):
        """When the tags for an image are updated, verify the change is propagated."""
        new_tag = rand_name('tag')

        resp = self.images_client.update_image(
            self.image.id_,
            replace={'tags': [new_tag]})
        self.assertEqual(resp.status_code, 200)

        updated_image = self.images_client.get_image(self.image.id_).entity
        self.assertIn(new_tag, updated_image.tags)
        self.assertNotIn(self.tag, updated_image.tags)

