from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from mysite.core.tokens import account_activation_token

from django.core.mail import EmailMessage

from mysite.core.forms import SignUpForm
from mysite.core.models import Profile, Languages


@login_required
def home(request):
    context = {}
    user_profile = Profile.objects.filter(user=request.user)
    user_language = Languages.objects.filter(user=request.user)
    if user_profile:
        context['profile'] = user_profile.get()
    if user_language:
        context['language'] = user_language.get()
    return render(request, 'home.html', context=context)


def signup(request):
    print("inside signup")
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            first_name=form.cleaned_data.get('first_name')
            last_name=form.cleaned_data.get('last_name')
            email=form.cleaned_data.get('email')
            home_city=form.cleaned_data.get('home_city')
            country=form.cleaned_data.get('country')
            language_To_Learn=form.cleaned_data.get('language_To_Learn')
            gender=form.cleaned_data.get('gender')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            user_profile = Profile.objects.create(
                user=user, bio='bio', mode='Mode', country=country,
                city=home_city, gender=gender
            )
            user_profile.save()
            user_language = Languages.objects.create(
                user=user, language=language_To_Learn, language_type='Programming'
            )
            user_language.save()

            current_site = get_current_site(request)
            print("current_site :: ")
            print(current_site)

            mail_subject = 'Activate your account.'
            message = render_to_string('act_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()

            return redirect('logout')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})   

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

