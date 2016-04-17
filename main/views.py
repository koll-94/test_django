# -*- coding: utf-8 -*-
import functools
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

from main.models import Document
from main.models import DocType
from main.models import DocField
from main.models import Profile
from main.models import DocStructure

from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic.base import View
from django.http import *
from django.views.decorators.csrf import csrf_exempt


def private(request_number=0):
    """
        Декоратор, делат метод доступным только после авторизации.
        В противном случае отсылает на форму авторизации
        :param request_number - номер параметра запроса
    """
    def _wrap(method):
        @functools.wraps(method)
        def _wrapped(*args, **kwargs):
            try:
                request = args[request_number]
                if request.user.is_authenticated():
                    return method(*args, **kwargs)
                else:
                    return redirect('/')
            except:
                raise
        return _wrapped
    return _wrap


class EAuthenticationForm (AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super (EAuthenticationForm, self).__init__ (request, *args, **kwargs)
        self.fields['username'].label = u'Логин:'
        self.fields['password'].label = u'Пароль:'


class LoginFormView (FormView):
    form_class = EAuthenticationForm

    template_name = "login.html"
    success_url = "/main"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView (View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


def main(reqwest):
    doctypes = DocType.objects.all(),
    templ_data = {
        'doctypes': doctypes[0],
    }
    return render_to_response('main.html', templ_data)


@private()
def grid_document(reqwest, doctype):
    doctype_id = int(doctype)

    doctypes = DocType.objects.all()
    doctype = DocType.objects.get(id=doctype_id)
    docstructure = DocStructure.objects.select_related().filter(doctype__id=doctype_id)

    #TODO нормальное отображение списка документов с полями
    docfields = DocField.objects.select_related().filter(
        document__user__id=reqwest.user.id,
        document__doctype__id=doctype_id).order_by('document_id')

    templ_data = {
        'doctypes': doctypes,
        'doctype': doctype,
        'docstructure': docstructure,
        'docfields': docfields,
    }
    return render_to_response('grid_document.html', templ_data)


@private()
def form_document(reqwest, doctype, document=None):
    doctype_id = int(doctype)

    doctypes = DocType.objects.all()
    doctype = DocType.objects.get(id=doctype_id)
    docstructure = DocStructure.objects.select_related().filter(doctype__id=doctype_id)

    templ_data = {
        'doctypes': doctypes,
        'doctype': doctype,
        'docstructure': docstructure,
    }
    return render_to_response('form_document.html', templ_data)


@private()
@csrf_exempt
def save_document(request, doctype, document=None):
    doctype_id = int(doctype)
    docstructure = DocStructure.objects.select_related().filter(doctype__id=doctype_id)

    if document is None or not document:
        doctype = DocType.objects.get(id=doctype_id)
        user = User.objects.get(id=request.user.id)
        cur_document = Document.objects.update_or_create(doctype=doctype, user=user)
        document = cur_document[0]
    else:
        document_id = int(document)
        document = Document.objects.get(id=document_id)

    for row in docstructure:
        value = request.POST.get(unicode(row.id), '')
        docstructure = DocStructure.objects.get(id=row.id)
        DocField.objects.update_or_create(document=document, value=value, docstructure=docstructure)

    return HttpResponseRedirect("/grid_document/{}".format(doctype_id))


def main_correct(reqwest):
    UchStep = Profile.objects.filter()
    templ_data = {
        'uch_step': UchStep,
    }
    return render_to_response('main_correct.html', templ_data)