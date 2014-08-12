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


from cafe.drivers.unittest.fixtures import BaseTestFixture
from cloudcafe.common.resources import ResourcePool
from cloudcafe.auth.config import UserAuthConfig, UserConfig
from cloudcafe.auth.provider import AuthProvider
from cloudcafe.images.config import ImagesConfig, MarshallingConfig, AltUserConfig
from cloudcafe.images.v2.client import ImagesClient

from cloudcafe.compute.config import ComputeEndpointConfig
from cloudcafe.compute.common.exception_handler import ExceptionHandler
from cloudcafe.compute.flavors_api.client import FlavorsClient
from cloudcafe.compute.servers_api.client import ServersClient
from cloudcafe.compute.images_api.client import ImagesClient as ComputeImagesClient
from cloudcafe.compute.extensions.keypairs_api.client import KeypairsClient
from cloudcafe.compute.extensions.config_drive.behaviors import \
    ConfigDriveBehaviors
from cloudcafe.compute.servers_api.behaviors import ServerBehaviors
from cloudcafe.compute.images_api.behaviors import ImageBehaviors
from cloudcafe.compute.flavors_api.config import FlavorsConfig
from cloudcafe.compute.servers_api.config import ServersConfig


class ImagesFixture(BaseTestFixture):
    """
    @summary: Base fixture for Images tests
    """

    @classmethod
    def setUpClass(cls):
        super(ImagesFixture, cls).setUpClass()
        cls.marshalling = MarshallingConfig()
        cls.images_config = ImagesConfig()
        cls.primary_image = cls.images_config.primary_image

        cls.endpoint_config = UserAuthConfig()
        cls.user_config = UserConfig()
        cls.access_data = AuthProvider.get_access_data(cls.endpoint_config,
                                                       cls.user_config)
        # If authentication fails, halt
        if cls.access_data is None:
            cls.assertClassSetupFailure('Authentication failed.')

        image_service = cls.access_data.get_service(
            cls.images_config.endpoint_name)
        url = image_service.get_endpoint(
            cls.images_config.region).public_url + '/v2'
        client_args = {'base_url': url, 'auth_token': cls.access_data.token.id_,
                       'serialize_format': cls.marshalling.serializer,
                       'deserialize_format': cls.marshalling.deserializer}
        cls.images_client = ImagesClient(**client_args)

        cls.alt_user_config = AltUserConfig()
        cls.alt_access_data = AuthProvider.get_access_data(
            cls.endpoint_config, cls.alt_user_config)

        # If authentication fails, halt
        if cls.alt_access_data is None:
            cls.assertClassSetupFailure('Authentication failed.')
        image_service = cls.alt_access_data.get_service(
            cls.images_config.endpoint_name)
        url = image_service.get_endpoint(
            cls.images_config.region).public_url + '/v2'
        client_args = {'base_url': url, 'auth_token': cls.alt_access_data.token.id_,
                       'serialize_format': cls.marshalling.serializer,
                       'deserialize_format': cls.marshalling.deserializer}
        cls.alt_images_client = ImagesClient(**client_args)
        cls.alt_tenant_id = cls.alt_access_data.token.tenant.id_
        cls.resources = ResourcePool()
        cls.addClassCleanup(cls.resources.release)


class ComputeIntegrationFixture(ImagesFixture):
    """
    @summary: Integration fixture for compute tests
    """

    @classmethod
    def setUpClass(cls):
        super(ComputeIntegrationFixture, cls).setUpClass()
        cls.flavors_config = FlavorsConfig()
        cls.images_config = ImagesConfig()
        cls.servers_config = ServersConfig()
        cls.compute_endpoint = ComputeEndpointConfig()
        cls.marshalling = MarshallingConfig()

        cls.flavor_ref = cls.flavors_config.primary_flavor

        cls.endpoint_config = UserAuthConfig()
        cls.user_config = UserConfig()
        cls.access_data = AuthProvider.get_access_data(cls.endpoint_config,
                                                       cls.user_config)
        # If authentication fails, halt
        if cls.access_data is None:
            cls.assertClassSetupFailure('Authentication failed.')

        compute_service = cls.access_data.get_service(
            cls.compute_endpoint.compute_endpoint_name)
        url = compute_service.get_endpoint(
            cls.compute_endpoint.region).public_url
        # If a url override was provided, use that value instead
        if cls.compute_endpoint.compute_endpoint_url:
            url = '{0}/{1}'.format(cls.compute_endpoint.compute_endpoint_url,
                                   cls.user_config.tenant_id)

        client_args = {'url': url, 'auth_token': cls.access_data.token.id_,
                       'serialize_format': cls.marshalling.serializer,
                       'deserialize_format': cls.marshalling.deserializer}

        cls.flavors_client = FlavorsClient(**client_args)
        cls.servers_client = ServersClient(**client_args)
        cls.compute_images_client = ComputeImagesClient(**client_args)
        cls.keypairs_client = KeypairsClient(**client_args)
        cls.server_behaviors = ServerBehaviors(cls.servers_client,
                                               cls.servers_config,
                                               cls.images_config,
                                               cls.flavors_config)
        cls.image_behaviors = ImageBehaviors(cls.compute_images_client,
                                             cls.servers_client,
                                             cls.images_config)
        cls.config_drive_behaviors = ConfigDriveBehaviors(cls.servers_client,
                                                          cls.servers_config,
                                                          cls.server_behaviors)
        cls.resources = ResourcePool()
        cls.addClassCleanup(cls.resources.release)
