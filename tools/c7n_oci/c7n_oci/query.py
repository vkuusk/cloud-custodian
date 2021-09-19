# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0

import jmespath
import json
import itertools
import logging

from googleapiclient.errors import HttpError

from c7n.actions import ActionRegistry
from c7n.filters import FilterRegistry
from c7n.manager import ResourceManager
from c7n.query import sources, MaxResourceLimit
from c7n.utils import local_session, chunks


log = logging.getLogger('c7n_oci.query')


class ResourceQuery:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def filter(self, resource_manager, **params):
        m = resource_manager.resource_type
        session = local_session(self.session_factory)
        client = session.client(
            m.service, m.version, m.component)

        # depends on resource scope
        if m.scope in ('project', 'zone'):
            project = session.get_default_project()
            if m.scope_template:
                project = m.scope_template.format(project)
            if m.scope_key:
                params[m.scope_key] = project
            else:
                params['project'] = project

        if m.scope == 'zone':
            if session.get_default_zone():
                params['zone'] = session.get_default_zone()

        enum_op, path, extra_args = m.enum_spec
        if extra_args:
            params.update(extra_args)
        return self._invoke_client_enum(
            client, enum_op, params, path)

    def _invoke_client_enum(self, client, enum_op, params, path):
        if client.supports_pagination(enum_op):
            results = []
            for page in client.execute_paged_query(enum_op, params):
                page_items = jmespath.search(path, page)
                if page_items:
                    results.extend(page_items)
            return results
        else:
            return jmespath.search(path,
                client.execute_query(enum_op, verb_arguments=params))


@sources.register('describe-oci')
class DescribeSource:


    def __init__(self, manager):
        self.manager = manager
        self.query = ResourceQuery(manager.session_factory)

    def get_resources(self, query):
        if query is None:
            query = {}
        return self.query.filter(self.manager, **query)

    def get_permissions(self):
        m = self.manager.resource_type
        if m.permissions:
            return m.permissions
        method = m.enum_spec[0]
        if method == 'aggregatedList':
            method = 'list'
        component = m.component
        if '.' in component:
            component = component.split('.')[-1]
        return ("%s.%s.%s" % (
            m.perm_service or m.service, component, method),)

    def augment(self, resources):
        return resources
