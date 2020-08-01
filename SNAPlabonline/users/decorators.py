from functools import wraps
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse
from .models import Subject


# Decorator to ensure that subject ID is available.
# For use with function-based views
def subjid_required(orig_func_view):
    @wraps(orig_func_view)
    def _wrapper(request, *args, **kwargs):
        subjid = request.session.get('subjid', None)
        # TO DO: Check logic for logged-in users (usually experimenter)
        if subjid is None:
            # Check if PROLIFIC_PID is in GET parameters
            # but still get subject confirmation:
            subjid = request.GET.get('PROLIFIC_PID', None)
            if subjid is None:
                # Assume SUBJID_URL view accepts GET parameter called next
                return redirect(f'{reverse(settings.SUBJID_URL)}?next={request.path}')
            else:
                return redirect(
                    f'{reverse(settings.SUBJID_URL)}'
                    f'?next={request.path}&PROLIFIC_PID={subjid}')
        else:
            return orig_func_view(request, *args, **kwargs)
    return _wrapper



# Decorator to ensure that subject has consented.
# Also checks that the consent was witthin 6 months.
# For use with function-based views
# Assumes subject ID is available =>
# decorate with an outer @subjid_required
def consent_required(orig_func_view):
    @wraps(orig_func_view)
    def _wrapper(request, *args, **kwargs):
        subjid = request.session.get('subjid')
        subj = Subject.objects.get(subjid=subjid)
        if subj.consented:
            if subj.latest_consent is not None:
                delta = timezone.now() - subj.latest_consent
                if delta.days < 7:
                    return orig_func_view(request, *args, **kwargs)

        # If consent is absent (or) date unmarked (or) older than 6 months:
        # Assume CONSENT_URL view accepts <path:next> parameter 
        # return redirect(settings.CONSENT_URL, next=request.path)
        return redirect(f'{reverse(settings.CONSENT_URL)}?next={request.path}')
    return _wrapper