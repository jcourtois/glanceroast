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


class ListImageFiltersTest(ImagesFixture):

    @classmethod
    def setUpClass(cls):
        super(ListImageFiltersTest, cls).setUpClass()

        # First image
        cls.first_image_name = rand_name('image')
        resp = cls.images_client.create_image(
            name=cls.first_image_name, container_format=ImageContainerFormat.BARE,
            disk_format=ImageDiskFormat.QCOW2, protected=False, min_disk=20, min_ram=512)
        cls.image = resp.entity
        cls.resources.add(cls.image.id_, cls.images_client.delete_image)
        cls.first_image = cls.images_client.get_image(cls.image.id_).entity

        # Second image
        cls.second_image_name = rand_name('test')
        resp = cls.images_client.create_image(
            name=cls.second_image_name, container_format=ImageContainerFormat.AMI,
            disk_format=ImageDiskFormat.VDI, protected=False, min_disk=60, min_ram=1024)
        cls.image = resp.entity
        cls.resources.add(cls.image.id_, cls.images_client.delete_image)
        cls.second_image = cls.images_client.get_image(cls.image.id_).entity

    def test_filter_images_by_name(self):
        """Verify that a list of images can be filtered by the image name."""
        images = self.images_client.list_images(name=self.first_image_name).entity
        self.assertIn(self.first_image, images)
        self.assertNotIn(self.second_image, images)

    def test_filter_images_by_container_format(self):
        """Verify that a list of images can be filtered by the container format."""
        images = self.images_client.list_images(
            container_format=ImageContainerFormat.AMI).entity
        self.assertIn(self.second_image, images)
        self.assertNotIn(self.first_image, images)

    def test_filter_images_by_disk_format(self):
        """Verify that a list of images can be filtered by the disk format."""
        images = self.images_client.list_images(
            disk_format=ImageDiskFormat.QCOW2).entity
        self.assertIn(self.first_image, images)
        self.assertNotIn(self.second_image, images)

    def test_filter_images_by_status(self):
        """Verify that a list of images can be filtered by the image status."""
        images = self.images_client.list_images(
            status=ImageStatus.QUEUED).entity
        self.assertIn(self.first_image, images)
        self.assertIn(self.second_image, images)

    def test_filter_images_by_min_disk(self):
        """Verify that a list of images can be filtered by the image min disk."""
        images = self.images_client.list_images(
            min_disk=20).entity
        self.assertIn(self.first_image, images)
        self.assertNotIn(self.second_image, images)

    def test_filter_images_by_min_ram(self):
        """Verify that a list of images can be filtered by the image min RAM."""
        images = self.images_client.list_images(
            min_ram=1024).entity
        self.assertNotIn(self.first_image, images)
        self.assertIn(self.second_image, images)
