import init
import wp

from pywikibot.data.api import *

_logger = "data.api"

def _submit(self):
    """Submit a query and parse the response.

    @return:  The data retrieved from api.php (a dict)

    """
    paramstring = self.http_params()
    while True:
        action = self.params.get("action", "")
        simulate = self._simulate(action)
        if simulate:
            return simulate
        self.site.throttle(write=self.write)
        uri = self.site.scriptpath() + "/api.php"
        ssl = False
        if self.site.family.name in config.available_ssl_project:
            if action == "login" and config.use_SSL_onlogin:
                ssl = True
            elif config.use_SSL_always:
                ssl = True
        try:
            if self.mime:
                # construct a MIME message containing all API key/values
                container = MIMEMultipart(_subtype='form-data')
                for key in self.params:
                    # key "file" requires special treatment in a multipart
                    # message
                    if key == "file":
                        local_filename = self.params[key]
                        filetype = mimetypes.guess_type(local_filename)[0] \
                                   or 'application/octet-stream'
                        file_content = file(local_filename, "rb").read()
                        submsg = MIMENonMultipart(*filetype.split("/"))
                        submsg.add_header("Content-disposition",
                                          "form-data", name=key,
                                          filename=local_filename)
                        submsg.set_payload(file_content)
                    else:
                        try:
                            self.params[key].encode("ascii")
                            keytype = ("text", "plain")
                        except UnicodeError:
                            keytype = ("application", "octet-stream")
                        submsg = MIMENonMultipart(*keytype)
                        submsg.add_header("Content-disposition", "form-data",
                                          name=key)
                        submsg.set_payload(self.params[key])
                    container.attach(submsg)
                # strip the headers to get the HTTP message body
                body = container.as_string()
                marker = "\n\n" # separates headers from body
                eoh = body.find(marker)
                body = body[ eoh + len(marker): ]
                # retrieve the headers from the MIME object
                mimehead = dict(container.items())
                rawdata = http.request(self.site, uri, ssl, method="POST",
                                       headers=mimehead, body=body)
            else:
                rawdata = http.request(self.site, uri, ssl, method="POST",
                            headers={'Content-Type':
                                     'application/x-www-form-urlencoded'},
                            body=paramstring)
##                import traceback
##                traceback.print_stack()
##                print rawdata
        except Server504Error:
            pywikibot.log(u"Caught HTTP 504 error; retrying")
            self.wait()
            continue
        #TODO: what other exceptions can occur here?
        except Exception, e:
            # for any other error on the http request, wait and retry
            pywikibot.error(traceback.format_exc())
            pywikibot.log(u"%s, %s" % (uri, paramstring))
            self.wait()
            continue
        if not isinstance(rawdata, unicode):
            rawdata = rawdata.decode(self.site.encoding())
        pywikibot.debug(u"API response received:\n" + rawdata, _logger)
        if rawdata.startswith(u"unknown_action"):
            raise APIError(rawdata[:14], rawdata[16:])
        try:
            result = json.loads(rawdata)
        except ValueError:
            # if the result isn't valid JSON, there must be a server
            # problem.  Wait a few seconds and try again
            pywikibot.warning(
"Non-JSON response received from server %s; the server may be down."
                             % self.site)
            pywikibot.debug(rawdata, _logger)
            # there might also be an overflow, so try a smaller limit
            for param in self.params:
                if param.endswith("limit"):
                    value = self.params[param]
                    try:
                        self.params[param] = str(int(value) // 2)
                        pywikibot.output(u"Set %s = %s"
                                         % (param, self.params[param]))
                    except:
                        pass
            self.wait()
            continue
        if not result:
            result = {}
        if type(result) is not dict:
            raise APIError("Unknown",
                           "Unable to process query response of type %s."
                               % type(result),
                           {'data': result})
        if self['action'] == 'query':
            if 'userinfo' in result.get('query', ()):
                if hasattr(self.site, '_userinfo'):
                    self.site._userinfo.update(result['query']['userinfo'])
                else:
                    self.site._userinfo = result['query']['userinfo']
            status = self.site._loginstatus  # save previous login status
            if ( ("error" in result
                        and result["error"]["code"].endswith("limit"))
                  or (status >= 0
                        and self.site._userinfo['name']
                            != self.site._username[status])):
                # user is no longer logged in (session expired?)
                # reset userinfo, then make user log in again
                del self.site._userinfo
                self.site._loginstatus = -1
                if status < 0:
                    status = 0  # default to non-sysop login
                self.site.login(status)
                # retry the previous query
                continue
        if "warnings" in result:
            modules = [k for k in result["warnings"] if k != "info"]
            for mod in modules:
                if "*" in result["warnings"][mod]:
                    pywikibot.warning(
                        u"API warning (%s): %s"
                         % (mod, result["warnings"][mod]["*"]))
                else:
                    pywikibot.warning(
                        u"API warning (%s): %s"
                         % (mod, result["warnings"][mod]))
        if "error" not in result:
            return result
        if "*" in result["error"]:
            # help text returned
            result['error']['help'] = result['error'].pop("*")
        code = result["error"].pop("code", "Unknown")
        info = result["error"].pop("info", None)
        if code == "maxlag":
            lag = lagpattern.search(info)
            if lag:
                pywikibot.log(
                    u"Pausing due to database lag: " + info)
                self.site.throttle.lag(int(lag.group("lag")))
                continue
        if code in (u'internal_api_error_DBConnectionError', ):
            self.wait()
            continue
        # raise error
        try:
            pywikibot.log(u"API Error: query=\n%s"
                           % pprint.pformat(self.params))
            pywikibot.log(u"           response=\n%s"
                           % result)
            raise APIError(code, info, **result["error"])
        except TypeError:
            raise RuntimeError(result)

Request.submit = _submit
