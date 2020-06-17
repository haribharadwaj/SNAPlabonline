from functools import wraps
from django.conf import settings
from django.shortcuts import redirect
from .models import Subject


def subjid_required(orig_func_view):
    @wraps(orig_func_view)
    def _wrapper(request, *args, **kwargs):
        print('In SUBJID decorator!')
        subjid = request.session.get('subjid', None)
        if subjid is None:
            return redirect(settings.SUBJID_URL, next=request.path)
        else:
            return orig_func_view(request, *args, **kwargs)
    return _wrapper


def consent_required(orig_func_view):
    @wraps(orig_func_view)
    def _wrapper(request, *args, **kwargs):
        subjid = request.session.get('subjid')
        subj = Subject.objects.get(subjid=subjid)
        if subj.consented:
            return orig_func_view(request, *args, **kwargs)
        else:
            return redirect(settings.CONSENT_URL, next=request.path)
    return _wrapper