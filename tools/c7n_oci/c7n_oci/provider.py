# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0

from c7n.registry import PluginRegistry
from c7n.provider import Provider, clouds

from .resources.resource_map import ResourceMap
from .client import Session

import logging

log = logging.getLogger('custodian.oci')


@clouds.register('oci')
class OracleCloud(Provider):

    display_name = 'OCI'
    resource_prefix = 'oci'
    resources = PluginRegistry('%s.resources' % resource_prefix)
    resource_map = ResourceMap

    def initialize(self, options):
        return options

    def initialize_policies(self, policy_collection, options):
        return policy_collection

    def get_session_factory(self, options):
        """Get a credential/session factory for api usage."""
        return Session


resources = OracleCloud.resources
