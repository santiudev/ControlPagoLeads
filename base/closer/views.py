from django.contrib.auth.views import LoginView, LogoutView

class CloserLoginView(LoginView):
    template_name = 'login.html'
    success_url = '/leads/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_navbar'] = True
        return context
    


class CloserLogoutView(LogoutView):
    next_page = 'login'



def closer_context(request):
    closer_name = None
    if request.user.is_authenticated and hasattr(request.user, 'closer'):
        closer_name = request.user.closer.name
    return {'closer_name': closer_name}