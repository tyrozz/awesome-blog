from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator


class StaffMemberRequiredMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffMemberRequiredMixin, self).dispatch(request, *args, **kwargs)
