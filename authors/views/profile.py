from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from authors.models import Profile


class ProfileView(TemplateView):
    template_name = 'authors/pages/profile.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        profile_id = context.get('id')

        filter_ = Profile.objects.filter(
            id=profile_id).select_related('author')
        profile = get_object_or_404(filter_, id=profile_id)

        return self.render_to_response(context={
            **context,
            'profile': profile,
        })
