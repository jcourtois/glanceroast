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


class ImageTagTest(ImagesFixture):

    @classmethod
    def setUpClass(cls):
        super(ImageTagTest, cls).setUpClass()
        cls.name = rand_name('image')
        cls.tag = rand_name('tag')
        resp = cls.images_client.create_image(name=cls.name, container_format=ImageContainerFormat.BARE,
                                              disk_format=ImageDiskFormat.QCOW2, tags=[cls.tag])
        cls.image = resp.entity
        cls.resources.add(cls.image.id_, cls.images_client.delete_image)
        with open(cls.images_config.test_image_name, 'rb') as image_file:
            cls.images_client.store_image_file(image_id=cls.image.id_, file_data=image_file)
        cls.image = cls.images_client.get_image(cls.image.id_).entity

    def test_duplicate_image_tag_ignored(self):
        resp = self.images_client.add_tag(self.image.id_, self.tag)
        self.assertEqual(204, resp.status_code)

        # Get the new list of tags
        image = self.images_client.get_image(self.image.id_).entity
        filtered_tags = [tag for tag in image.tags if tag == self.tag]
        self.assertEqual(len(filtered_tags), 1)

    def test_add_new_tag(self):
        new_tag = rand_name('tag')
        resp = self.images_client.add_tag(self.image.id_, new_tag)
        self.assertEqual(204, resp.status_code)

        image = self.images_client.get_image(self.image.id_).entity
        self.assertIn(new_tag, image.tags)

    def test_delete_tag(self):
        new_tag = rand_name('tag')
        self.images_client.add_tag(self.image.id_, new_tag)

        # Delete tag
        resp = self.images_client.delete_tag(self.image.id_, new_tag)
        self.assertEqual(204, resp.status_code)

        # Verify tag removed
        image = self.images_client.get_image(self.image.id_).entity
        self.assertNotIn(new_tag, image.tags)