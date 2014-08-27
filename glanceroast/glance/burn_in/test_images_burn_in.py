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

import unittest2 as unittest
from unittest2.suite import TestSuite

from cloudcafe.images.common.types import (
    ImageContainerFormat, ImageDiskFormat, ImageStatus)
from glanceroast.glance.fixtures import ImagesFixture
from cloudcafe.common.tools.datagen import rand_name


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(ImagesBurnIn("test_upload_image_file"))
    suite.addTest(ImagesBurnIn("test_get_image"))
    suite.addTest(ImagesBurnIn("test_delete_image"))
    return suite


class ImagesBurnIn(ImagesFixture):

    @classmethod
    def setUpClass(cls):
        super(ImagesBurnIn, cls).setUpClass()
        cls.name = rand_name('image')
        cls.tag = rand_name('tag')
        resp = cls.images_client.create_image(name=cls.name, container_format=ImageContainerFormat.BARE,
                                              disk_format=ImageDiskFormat.QCOW2, tags=[cls.tag])
        cls.image = resp.entity

    def test_upload_image_file(self):
        with open(self.images_config.test_image_name, 'rb') as image_file:
            self.images_client.store_image_file(image_id=self.image.id_, file_data=image_file)

    def test_get_image(self):
        self.images_client.get_image(self.image.id_)

    def test_delete_image(self):
        self.images_client.delete_image(self.image.id_)

