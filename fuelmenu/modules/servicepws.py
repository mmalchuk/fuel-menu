#!/usr/bin/env python
# Copyright 2013 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from fuelmenu.common.modulehelper import ModuleHelper
from fuelmenu.common import pwgen
import logging
import urwid
import urwid.raw_display
import urwid.web_display
log = logging.getLogger('fuelmenu.servicepws')
blank = urwid.Divider()


class ServicePasswords(urwid.WidgetWrap):
    def __init__(self, parent):
        self.name = "Service Passwords"
        self.visible = False
        self.parent = parent
        # UI text
        self.header_content = ["Set service passwords", ""]
        self.defaults = \
            {
                "astute/user": {"label": "Astute user",
                                "tooltip": "",
                                "value": "naily"},
                "astute/password": {"label": "Astute password",
                                    "tooltip": "",
                                    "value": pwgen.password()},
                "cobbler/user": {"label": "Cobbler user",
                                 "tooltip": "",
                                 "value": "cobbler"},
                "cobbler/password": {"label": "Cobbler password",
                                     "tooltip": "",
                                     "value": pwgen.password()},
                "keystone/admin_token": {"label": "Keystone Admin Token",
                                         "tooltip": "",
                                         "value": pwgen.password()},
                "keystone/nailgun_user": {
                    "label": "Keystone username for Nailgun",
                    "tooltip": "",
                    "value": "nailgun"},
                "keystone/nailgun_password": {
                    "label": "Keystone password for Nailgun",
                    "tooltip": "",
                    "value": pwgen.password()},
                "keystone/ostf_user": {
                    "label": "Keystone username for OSTF",
                    "tooltip": "",
                    "value": "ostf"},
                "keystone/ostf_password": {
                    "label": "Keystone password for OSTF",
                    "tooltip": "",
                    "value": pwgen.password()},
                "keystone/monitord_user": {
                    "label": "Master node monitoring user",
                    "tooltip": "",
                    "value": "monitord"
                },
                "keystone/monitord_password": {
                    "label": "Master node monitoring password",
                    "tooltip": "",
                    "value": pwgen.password(),
                },
                "keystone/service_token_off": {
                    "label": "Disable keystone service token",
                    "tooltip": "",
                    "value": "true",
                },
                "mcollective/user": {"label": "Mcollective user",
                                     "tooltip": "",
                                     "value": "mcollective"},
                "mcollective/password": {"label": "Mcollective password",
                                         "tooltip": "",
                                         "value": pwgen.password()},
                "postgres/keystone_dbname": {"label": "Keystone DB name",
                                             "tooltip": "",
                                             "value": "keystone"},
                "postgres/keystone_user": {"label": "Keystone DB user",
                                           "tooltip": "",
                                           "value": "keystone"},
                "postgres/keystone_password": {"label": "Keystone DB password",
                                               "tooltip": "",
                                               "value": pwgen.password()},
                "postgres/nailgun_dbname": {"label": "Nailgun DB name",
                                            "tooltip": "",
                                            "value": "nailgun"},
                "postgres/nailgun_user": {"label": "Nailgun DB user",
                                          "tooltip": "",
                                          "value": "nailgun"},
                "postgres/nailgun_password": {"label": "Nailgun DB password",
                                              "tooltip": "",
                                              "value": pwgen.password()},
                "postgres/ostf_dbname": {"label": "OSTF DB name",
                                         "tooltip": "",
                                         "value": "ostf"},
                "postgres/ostf_user": {"label": "OSTF DB user",
                                       "tooltip": "",
                                       "value": "ostf"},
                "postgres/ostf_password": {"label": "OSTF DB password",
                                           "tooltip": "",
                                           "value": pwgen.password()},
            }
        self.fields = self.defaults.keys()

        self.load()
        self.screen = None

    def check(self, args):
        # Get field information
        responses = dict()

        for index, fieldname in enumerate(self.fields):
            if fieldname == "blank":
                pass
            else:
                responses[fieldname] = self.edits[index].get_edit_text()
        return responses

    def apply(self, args):
        log.debug('start saving servicepws')
        responses = self.check(args)
        if responses is False:
            log.error("Check failed. Not applying")
            log.error("%s" % (responses))
            for index, fieldname in enumerate(self.fields):
                if fieldname == "PASSWORD":
                    return (self.edits[index].get_edit_text() == "")
            return False

        self.save(responses)

    def load(self):
        ModuleHelper.load_to_defaults(self.parent.settings, self.defaults)

    def save(self, responses):
        newsettings = ModuleHelper.make_settings_from_responses(responses)
        self.parent.settings.merge(newsettings)
        log.debug('done saving servicepws')

        # Update defaults
        for index, fieldname in enumerate(self.fields):
            if fieldname != "blank" and fieldname in newsettings:
                self.defaults[fieldname]['value'] = newsettings[fieldname]

    def cancel(self, button):
        ModuleHelper.cancel(self, button)

    def refresh(self):
        pass

    def screenUI(self):
        return ModuleHelper.screenUI(self, self.header_content, self.fields,
                                     self.defaults)
