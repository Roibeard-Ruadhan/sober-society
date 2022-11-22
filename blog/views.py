from multiprocessing import context
from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post, Comment
from django.contrib import messages
from .forms import CommentForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


def handler_403(request, exception):
    '''403 error view'''
    return render(request, '403.html', status=403)


def handler_404(request, exception):
    '''
    A 404 error handling view
    '''
    return render(request, '404.html', status=404)


def handler_500(request, *args, **argv):
    '''
    A 500 error handling view
    '''
    return render(request, '500.html', status=500)


# Homepage details
def Homepage(request):
    template_name = 'index.html'
    return render(request, template_name)


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "blog.html"
    paginate_by = 6


# Add blog
@login_required
def create_post(request):
    """
    Allow an admin user to create a Blop Post
    """
    if request.user:

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                blog_post = form.save(commit=False)
                blog_post.author = request.user
                blog_post.save()
                messages.info(request, 'Blog added successfully!')
                return redirect('blog')
            else:
                messages.error(request, 'Please check the form for errors. \
                    Blog failed to add.')
        else:
            form = PostForm()
    else:
        messages.error(
            request, 'Sorry, you do not have permission to do that.')
        return redirect(reverse('home'))

    template = 'add_blog.html'

    context = {
        'form': form,
    }

    return render(request, template, context)


class PostDetail(View):
    """ Post Detail"""

    def get(self, request, blog_post_id):
        post = get_object_or_404(Post, pk=blog_post_id)
        comments = post.comments.filter(post=post).order_by("-created_on")

        queryset = Comment.objects.filter(post=post, approved=True)

        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        context = {
            "post": post,
            "comments": comments,
            "commented": False,
            'queryset': queryset,
            "liked": liked,
            "comment_form": CommentForm()
        }
        return render(request, "blog_detail.html", context)

    def post(self, request, blog_post_id):
        """ Post Method"""
        post = get_object_or_404(Post, pk=blog_post_id)
        comments = post.comments.filter(post=post).order_by("-created_on")

        queryset = Comment.objects.filter(post=post, approved=True)

        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            comment_form = CommentForm()
            messages.info(request, 'You need to be logged in to add a comment')

        context = {
                "post": post,
                "comments": comments,
                'queryset': queryset,
                "commented": False,
                "comment_form": comment_form,
                "liked": liked
                    }
        return redirect(reverse('blog_detail',  args=[blog_post_id]))


# Edit Blog Post
@login_required
def edit_blog(request, blog_post_id):
    """
    Allow all users to edit the blogs they created
    """
    if request.user:

        blog_post = get_object_or_404(Post, pk=blog_post_id)

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=blog_post)
            if form.is_valid():
                form.save()
                messages.success(request, 'Blog post updated successfully!')
                return redirect('blog')
            else:
                messages.error(request, 'Please check the form for errors. \
                    Blog post failed to update.')
        else:
            form = PostForm(instance=blog_post)
            messages.info(request, f'Editing {blog_post.title}')
    else:
        messages.error(request, 'Sorry, you do not have permission for that.')
        return redirect(reverse('home'))

    template = 'edit_blog.html'

    context = {
        'form': form,
        'blog_post': blog_post,
    }

    return render(request, template, context)


def delete_blog(request, blog_post_id):
    """User can delet their own blog post"""
    if request.method == "POST":
        blog_post = get_object_or_404(Post, pk=blog_post_id)
        blog_post.delete()
    else:
        return render(request, 'delete_blog.html')
    messages.success(request, 'The blog has been deleted successfully!')

    return redirect('blog')


def edit_comment(request, id):
    """User may edit comment method """
    comment_obj = Comment.objects.get(id=id)
    post_id = comment_obj.post.id
    form = CommentForm(instance=comment_obj)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment_obj)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'The comment has been updated successfully!')
            return redirect(reverse('blog_detail', args=[post_id]))

    context = {
        'form': form
    }

    return render(request, 'edit_comment.html', context)


def delete_comment(request, id):
    comment_obj = Comment.objects.get(id=id)
    blog_post_id = comment_obj.post.id
    if request.method == "POST":
        if request.user == comment_obj.name:
            comment_obj.delete()
            messages.info(request, 'Comment deleted successfully!')
            return redirect(reverse('blog_detail', args=[blog_post_id]))
    else:
        context = {
            'blog_post_id': blog_post_id
        }
        return render(request, 'delete_comment.html', context)


class PostLike(View):
    """Method for liking Blogs"""
    def post(self, request, blog_post_id):
        post = Post.objects.get(id=blog_post_id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        messages.success(request, 'Blog has been liked successfully!')
        return HttpResponseRedirect(
            reverse('blog_detail', args=[blog_post_id]))
