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


class DeleteImageMemberTest(ImagesFixture):

    @classmethod
    def setUpClass(cls):
        super(DeleteImageMemberTest, cls).setUpClass()

        cls.name = rand_name('image')
        cls.tag = rand_name('tag')
        resp = cls.images_client.create_image(
            name=cls.name, container_format=ImageContainerFormat.BARE,
            disk_format=ImageDiskFormat.QCOW2, tags=[cls.tag], protected=False)
        cls.image = resp.entity
        cls.resources.add(cls.image.id_, cls.images_client.delete_image)
        with open(cls.images_config.test_image_name, 'rb') as image_file:
            cls.images_client.store_image_file(image_id=cls.image.id_, file_data=image_file)
        cls.first_image = cls.images_client.get_image(cls.image.id_).entity
        cls.images_client.add_member(cls.first_image.id_, cls.alt_tenant_id)
        cls.images_client.delete_member(cls.first_image.id_, cls.alt_tenant_id)

    def test_revoked_image_member_cannot_get_shared_image(self):
        resp = self.alt_images_client.get_image(self.image.id_)
        self.assertEqual(resp.status_code, 404)

    def test_revoked_image_member_cannot_list_shared_image(self):
        images = self.alt_images_client.list_images().entity
        image_ids = [image.id_ for image in images]
        self.assertNotIn(self.image.id_, image_ids)

    def test_revoked_member_not_shown_in_list_of_members(self):
        members = self.images_client.list_members(self.image.id_).entity
        member_ids = [member.member_id for member in members]
        self.assertNotIn(self.alt_tenant_id, member_ids)
