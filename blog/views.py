from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Post, Category, Comment, Like, Profile, Follow, Bookmark, Reaction, Tag, Message
from .forms import PostForm, CommentForm, RegisterForm, ProfileForm


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)  # 5 postări pe pagină
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    return render(request, 'blog/home.html', {'page_obj': page_obj, 'categories': categories})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comment_form': comment_form,
        'comments': comments
    })


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Postarea a fost creată!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Postare Nouă'})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, 'Nu ai permisiunea să editezi această postare!')
        return redirect('post_detail', pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Postarea a fost actualizată!')
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Editare Postare'})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, 'Nu ai permisiunea să ștergi această postare!')
        return redirect('post_detail', pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Postarea a fost ștearsă!')
        return redirect('home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect('post_detail', pk=pk)

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comentariul a fost adăugat!')
            return redirect('post_detail', pk=pk)
    return redirect('post_detail', pk=pk)

def search_posts(request):
    query = request.GET.get('q')
    posts = Post.objects.all()
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/search_results.html', {'page_obj': page_obj, 'query': query})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # Creează automat un profil pentru utilizator
            messages.success(request, 'Contul a fost creat! Te poți autentifica acum.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    posts = Post.objects.filter(author=user)
    return render(request, 'blog/profile_view.html', {
        'profile': profile,
        'posts': posts
    })

@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilul a fost actualizat!')
            return redirect('profile_view', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'blog/profile_edit.html', {'form': form})


@login_required
def follow_toggle_view(request, username):
    target_user = get_object_or_404(User, username=username)
    follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)
    if not created:
        follow.delete()
    return redirect('profile_view', username=username)

@login_required
def bookmark_toggle_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
    if not created:
        bookmark.delete()
    return redirect('post_detail', pk=pk)

@login_required
def react_view(request, pk, reaction_type):
    post = get_object_or_404(Post, pk=pk)
    reaction, created = Reaction.objects.get_or_create(user=request.user, post=post)
    reaction.type = reaction_type
    reaction.save()
    return redirect('post_detail', pk=pk)

def posts_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(tags=tag)
    return render(request, 'blog/posts_by_tag.html', {'tag': tag, 'posts': posts})

def hero_preview(request):
    return render(request, 'hero_preview.html')


from django.shortcuts import redirect
from django.contrib.auth import logout

def custom_logout_view(request):
    logout(request)
    return redirect('login')  # redirecționează spre pagina de login


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Message

@login_required
def chat_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/chat_list.html', {'users': users})

@login_required
def chat_detail(request, username):
    receiver = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        sender__in=[request.user, receiver],
        receiver__in=[request.user, receiver]
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            return redirect('chat_detail', username=receiver.username)

    return render(request, 'chat/chat_detail.html', {'receiver': receiver, 'messages': messages})

from django.db.models import Q
@login_required
# views.py
def chat_view(request, username): 
    recipient = get_object_or_404(User, username=username)

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=recipient) |
        Q(sender=recipient, receiver=request.user)
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=recipient, content=content)
            return redirect('chat_with_user', username=recipient.username)

    return render(request, 'personal_blog/chat_detail.html', {
        'recipient': recipient,
        'messages': messages
    })


def chat_users_view(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'personal_blog/chat_users.html', {'users': users})

@login_required
def chat_users(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'personal_blog/chat_users.html', {'users': users})

@login_required
def chat_with_user(request, username):
    return render(request, 'personal_blog/chat_room.html', {'username': username})


