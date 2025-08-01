from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Q
from .models import BlogPost
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .forms import BlogPostForm



def home(request):
    return render(request, 'home.html') 


def blog_list(request):
    query = request.GET.get('q')
    
    if query:
        posts = BlogPost.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).order_by('-created_at')
    else:
        posts = BlogPost.objects.all().order_by('-created_at')

    # Add pagination (5 posts per page)
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog_list.html', {
        'page_obj': page_obj,
        'query': query
    })



def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'blog_detail.html', {'post': post})





def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']
        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')
        user = User.objects.create_user(username=email, email=email, password=password)
        login(request, user)
        messages.success(request, "Welcome to myblog")
        return redirect('blog_list')
    return render(request, 'register.html')




def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            messages.success(request, "you are succesfully logged in")
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "you are succesfully logged out")
    return redirect('login')


@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.slug = slugify(blog.title)
            blog.save()
            return redirect('blog_detail', slug=blog.slug)
    else:
        form = BlogPostForm()

    return render(request, 'create_post.html', {'form': form})





@login_required
def user_blog_list(request):
    # Fetch blog posts authored by the logged-in user
    posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'user_blog_list.html', {'posts': posts})

@login_required
def edit_blog(request, pk):
    # Allow only the author to edit their post
    post = get_object_or_404(BlogPost, pk=pk, author=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('user_blog_list')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'edit_blog.html', {'form': form})

@login_required
def delete_blog(request, pk):
    # Allow only the author to delete their post
    post = get_object_or_404(BlogPost, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('user_blog_list')
    return render(request, 'delete_confirm.html', {'post': post})




