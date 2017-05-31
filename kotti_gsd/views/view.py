# -*- coding: utf-8 -*-

"""
Created on 2017-05-11
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

import deform
import colander
from pyramid.view import view_config
from pyramid.view import view_defaults

from kotti import get_settings
from kotti_gsd import _, util
from kotti_gsd.fanstatic import css_and_js
from kotti_gsd.views import BaseView


@view_defaults(permission='view')
class GitlabServiceDeskViews(BaseView):
    """ Views for :class:`kotti_gsd.resources.CustomContent` """

    @view_config(name='service-desk', permission='view',
                 renderer='kotti_gsd:templates/service-desk.pt')
    def default_view(self):
        settings = get_settings()
        service_email = settings.get("service_desk.email", None)
        service_number = settings.get("service_desk.number", None)
        return {
            "contact_number": service_number,
            "form": self.build_form()
        }

    def build_form(self):
        if self.request.method == "POST":
            user_email = self.request.params.get("email", "")
            message = self.request.params.get("issue", "")
            subject = self.request.params.get("subject", "Reported Issue")
            settings = get_settings()
            site_title = settings['kotti.site_title']
            service_email = settings.get("service_desk.email", None)

            if not service_email:
                self.request.session.flash(
                    _(u"No service email was provided"),
                    "error"
                )
            else:
                util.send_email(
                    self.request,
                    [service_email],
                    'kotti_gsd:templates/message.pt',
                    {
                        "message": message,
                        "subject": subject,
                        "site_title": site_title
                    },
                    sender=user_email
                )
                self.request.session.flash(
                    _(u"Issue has been submitted"),
                    "success"
                )

        else:
            if self.request.user is not None:
                user_email = self.request.user.email
            else:
                user_email = ""

        class ServiceDeskSchema(colander.MappingSchema):
            email = colander.SchemaNode(
                colander.String(),
                title=_(u'Email'),
                default=user_email
            )
            issue = colander.SchemaNode(
                colander.String(),
                title=_(u'Issue'),
                widget=deform.widget.RichTextWidget(height=500)
            )

        def succeed():
            return Response('<div id="thanks">Thanks!</div>')

        form = deform.Form(ServiceDeskSchema(), buttons=('submit',), use_ajax=True)
        return form
