from psistats2.reporter import PsistatsOutputPlugin
import json
import urllib.request
import urllib.error


class HttpOutput(PsistatsOutputPlugin):

    PLUGIN_ID = 'http'

    def send(self, report):
        url = self.config['url']
        data = json.dumps(dict(report)).encode('utf-8')

        user_agent = 'psistats2'

        headers = {'User-Agent': user_agent,
                   'Content-type': 'application/json'}

        try:
            req = urllib.request.Request(url, data=data, headers=headers)
            res = urllib.request.urlopen(req)
            return res
        except urllib.error.URLError as e:
            self.logger.error(str(e))

