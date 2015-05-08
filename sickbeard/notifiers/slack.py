# Author: Jonathan Jordan <jonathan@jmjordan.com>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of Sick Beard.
#
# Sick Beard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sick Beard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sick Beard.  If not, see <http://www.gnu.org/licenses/>.

import urllib2
import sickbeard
import json

from sickbeard import logger
from sickbeard.common import notifyStrings, NOTIFY_SNATCH, NOTIFY_DOWNLOAD
from sickbeard.exceptions import ex


class SlackNotifier:

    def _sendMessage(self, msg, webhook_url):

        # build up the URL and parameters
        msg = msg.strip()

        data = json.dumps({"text": msg})

        # send the request to pushover
        try:
            req = urllib2.Request(webhook_url, data)
            handle = sickbeard.helpers.getURLFileLike(req, throw_exc=True)
            handle.close()
        except urllib2.URLError, e:
            logger.log(u"SLACK: Message failed." + ex(e), logger.ERROR)
            return False

        logger.log(u"SLACK: Message sent successfully.", logger.MESSAGE)
        return True

    def _notify(self, message, webhook_url=None, force=False):
        """
        Sends a pushover notification based on the provided info or SB config
        """

        # suppress notifications if the notifier is disabled but the notify options are checked
        if not sickbeard.USE_PUSHOVER and not force:
            return False

        # fill in omitted parameters
        if not webhook_url:
            webhook_url = sickbeard.SLACK_WEBHOOK_URL

        logger.log(u"SLACK: Sending message with details: message=\"%s\", webhook_url=%s" % (message, webhook_url), logger.DEBUG)

        return self._sendMessage(message, webhook_url)

##############################################################################
# Public functions
##############################################################################

    def notify_snatch(self, ep_name):
        if sickbeard.SLACK_NOTIFY_ONSNATCH:
            self._notify(notifyStrings[NOTIFY_SNATCH] + ' - ' + ep_name)

    def notify_download(self, ep_name):
        if sickbeard.SLACK_NOTIFY_ONDOWNLOAD:
            self._notify(notifyStrings[NOTIFY_DOWNLOAD] + ' - ' + ep_name)

    def test_notify(self, webhook_url):
        return self._notify("Hi! This is a test message from SickBeard.", webhook_url=webhook_url, force=True)

    def update_library(self, ep_obj=None):
        pass

notifier = SlackNotifier
