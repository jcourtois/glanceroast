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

from cloudcafe.images.common.types import (
    ImageContainerFormat, ImageDiskFormat, ImageStatus)
from cloudroast.glance.fixtures import ComputeIntegrationFixture
from cloudcafe.common.tools.datagen import rand_name


class CreateServerFromNewImageTest(ComputeIntegrationFixture):

    @classmethod
    def setUpClass(cls):
        super(CreateServerFromNewImageTest, cls).setUpClass()
        cls.name = rand_name('image')
        cls.tag = rand_name('tag')
        resp = cls.images_client.create_image(name=cls.name, container_format=ImageContainerFormat.BARE,
                                              disk_format=ImageDiskFormat.QCOW2, tags=[cls.tag])
        cls.image = resp.entity
        cls.resources.add(cls.image.id_, cls.images_client.delete_image)
        with open(cls.images_config.test_image_name, 'rb') as image_file:
            cls.images_client.store_image_file(image_id=cls.image.id_, file_data=image_file)
        cls.image = cls.images_client.get_image(cls.image.id_).entity

    def test_create_server_from_new_image(self):
        self.server_behaviors.create_active_server(flavor_ref=self.flavor_ref, image_ref=self.image.id_)