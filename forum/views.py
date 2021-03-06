from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from .forms import UserRegistrationForm, ProfileUpdateForm, PostForm
from .models import Profile, FriendRequest, Friend, Post
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView

from datetime import date

# Create your views here.
def index(request):
    return render(
        request,
        'forum/index.html',
    )


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'forum/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context


class CreateProfilePageView(CreateView):
    model = Profile

    template_name = 'forum/create_profile.html'
    form_class = ProfileUpdateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('home')


class UpdateProfilePageView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm

    template_name = 'forum/update_profile.html'
    #fields = ['profile_pic', 'first_name', 'last_name', 'bio', 'facebook', 'twitter', 'instagram']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('home')


def send_request(request, spk, rpk):
    if request.user.id == int(spk) and spk != rpk:
        recipient = User.objects.get(pk=int(rpk))
        if (FriendRequest.objects.filter(recipient=recipient, sender=request.user)):
            print("такое уже есть")
        else:
            FriendRequest.objects.create(recipient=recipient, sender=request.user)
    return redirect('all_users')


class UserFriendRequests(LoginRequiredMixin, ListView):
    model = FriendRequest
    template_name = 'forum/user_friend_requests.html'
    paginate_by = 10

    def get_queryset(self):
        return FriendRequest.objects.filter(recipient=self.request.user)


def change_friend(request, operation, pk):
    req = FriendRequest.objects.get(pk=pk)
    friend = req.sender
    if operation == 'add':
        Friend.make_friend(friend, request.user)
    req.delete()
    return redirect('user_friend_requests')


def remove_friend(request, pk):
    friend = User.objects.get(pk=pk)
    Friend.lose_friend(friend, request.user)
    return redirect('friends')


class AllUserList(ListView):
    model = Profile
    template_name = 'forum/user_list.html'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Profile.objects.filter(Q(first_name=query) | Q(last_name=query))
        else:
            return Profile.objects.all()


class FriendList(ListView):
    model = Profile

    template_name = 'forum/friend_list.html'
    paginate_by = 5

    def get_queryset(self):
        if Friend.objects.filter(current_user=self.request.user):
            return Friend.objects.get(current_user=self.request.user).users.all()
        else:
            Friend.objects.get_or_create(current_user=self.request.user)
            return ''


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


class CreatePost(CreateView):
    model = Post

    template_name = 'forum/create_post.html'
    form_class = PostForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.current_user = self.request.user
        obj.date = date.today()
        obj.save()
        return super().form_valid(form)

    success_url = reverse_lazy('my_posts')


class UpdatePost(UpdateView):
    model = Post

    template_name = 'forum/update_post.html'
    form_class = PostForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.date = date.today()
        obj.save()
        return super().form_valid(form)

    success_url = reverse_lazy('my_posts')


class DeletePost(DeleteView):
    model = Post

    success_url = reverse_lazy('my_posts')


class MyPostsList(ListView):
    model = Post
    template_name = 'forum/my_posts.html'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(current_user=self.request.user).order_by('-date')


class UserPostsList(ListView):
    model = Post
    template_name = 'forum/user_posts.html'
    paginate_by = 3

    def get_queryset(self):
        user = User.objects.get(pk=int(self.kwargs['pk']))
        return Post.objects.filter(current_user=user).order_by('-date')


class FriendsPostList(ListView):
    model = Post
    template_name = 'forum/fiends_posts.html'
    paginate_by = 3

    def get_queryset(self):
        user = self.request.user
        try:
            return Post.objects.filter(current_user__in=Friend.objects.get(current_user=user).users.all()).order_by('-date')
        except:
            return ''