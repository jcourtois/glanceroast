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
    ImageContainerFormat, ImageDiskFormat, ImageStatus, ImageMemberStatus)
from glanceroast.glance.fixtures import ImagesFixture
from cloudcafe.common.tools.datagen import rand_name


class AddImageMemberTest(ImagesFixture):

    @classmethod
    def setUpClass(cls):
        super(AddImageMemberTest, cls).setUpClass()

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
        cls.alt_images_client.update_member(
            image_id=cls.image.id_, member_id=cls.alt_tenant_id,
            status=ImageMemberStatus.REJECTED)

    def test_image_member_can_get_shared_image(self):
        resp = self.alt_images_client.get_image(self.image.id_)
        self.assertEqual(resp.status_code, 200)

    def test_new_member_shown_in_list_of_members(self):
        members = self.images_client.list_members(self.image.id_).entity
        member_ids = [member.member_id for member in members]
        self.assertIn(self.alt_tenant_id, member_ids)

    def test_image_member_cannot_add_tag(self):
        resp = self.alt_images_client.add_tag(self.image.id_, 'tag1')
        self.assertEqual(resp.status_code, 403)

    def test_image_member_cannot_delete_image(self):
        resp = self.alt_images_client.delete_image(self.image.id_)
        self.assertEqual(resp.status_code, 403)

    def test_image_member_can_list_image_members(self):
        resp = self.alt_images_client.list_members(self.image.id_)
        self.assertEqual(resp.status_code, 200)


