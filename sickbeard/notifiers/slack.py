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

    def _sendMessage(self, title, msg, webhook_url):

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
            # FIXME: Python 2.5 hack, it wrongly reports 201 as an error
            # if hasattr(e, 'code') and e.code == 201:
            #     logger.log(u"PUSHOVER: Notification successful.", logger.MESSAGE)
            #     return True
            #
            # # if we get an error back that doesn't have an error code then who knows what's really happening
            # if not hasattr(e, 'code'):
            #     logger.log(u"PUSHOVER: Notification failed." + ex(e), logger.ERROR)
            #     return False
            # else:
            #     logger.log(u"PUSHOVER: Notification failed. Error code: " + str(e.code), logger.ERROR)
            #
            # # HTTP status 404 if the provided email address isn't a Pushover user.
            # if e.code == 404:
            #     logger.log(u"PUSHOVER: Username is wrong/not a Pushover email. Pushover will send an email to it", logger.WARNING)
            #     return False
            #
            # # For HTTP status code 401's, it is because you are passing in either an invalid token, or the user has not added your service.
            # elif e.code == 401:
            #
            #     # HTTP status 401 if the user doesn't have the service added
            #     subscribeNote = self._sendPushover(title, msg, userKey)
            #     if subscribeNote:
            #         logger.log(u"PUSHOVER: Subscription sent", logger.DEBUG)
            #         return True
            #     else:
            #         logger.log(u"PUSHOVER: Subscription could not be sent", logger.ERROR)
            #         return False
            #
            # # If you receive an HTTP status code of 400, it is because you failed to send the proper parameters
            # elif e.code == 400:
            #     logger.log(u"PUSHOVER: Wrong data sent to Pushover", logger.ERROR)
            #     return False

        logger.log(u"SLACK: Message sent successfully.", logger.MESSAGE)
        return True

    def _notify(self, title, message, webhook_url=None, force=False):
        """
        Sends a pushover notification based on the provided info or SB config
        """

        # suppress notifications if the notifier is disabled but the notify options are checked
        if not sickbeard.USE_PUSHOVER and not force:
            return False

        # fill in omitted parameters
        if not webhook_url:
            webhook_url = sickbeard.SLACK_WEBHOOK_URL

        logger.log(u"SLACK: Sending message with details: title=\"%s\", message=\"%s\", webhook_url=%s" % (title, message, webhook_url), logger.DEBUG)

        return self._sendMessage(title, message, webhook_url)

##############################################################################
# Public functions
##############################################################################

    def notify_snatch(self, ep_name):
        if sickbeard.SLACK_NOTIFY_ONSNATCH:
            self._notify(notifyStrings[NOTIFY_SNATCH], ep_name)

    def notify_download(self, ep_name):
        if sickbeard.SLACK_NOTIFY_ONDOWNLOAD:
            self._notify(notifyStrings[NOTIFY_DOWNLOAD], ep_name)

    def test_notify(self, webhook_url):
        return self._notify("Test", "This is a test message from Sick Beard.", webhook_url=webhook_url, force=True)

    def update_library(self, ep_obj=None):
        pass

notifier = SlackNotifier
