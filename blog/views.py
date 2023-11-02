from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import Post, Comment
from .form import CommentForm

# Create your views here.


def get_date(post):
    return post['date']


def starting_page(request):

    latest_post = Post.objects.all().order_by("-date")[:3]

    return render(request, "blog/home.html", {
        "posts": latest_post
    })


def posts(request):
    all_posts = Post.objects.all()
    return render(request, "blog/all-post.html", {
        "posts": all_posts
    })


def post_detail(request, slug):

    if request.method == "POST":
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            form_data = Comment(user_name=comment_form.cleaned_data["user_name"],
                                email=comment_form.cleaned_data["user_email"],
                                text=comment_form.cleaned_data["text"])

            comment = form_data
            comment.post = Post.objects.get(slug=slug)
            comment.save()

            return HttpResponseRedirect("/posts/"+slug)

        identified_post = Post.objects.get(slug=slug)
        return render(request, "blog/post-detail.html", {
            "form": comment_form,
            "post": identified_post,
            "tags": identified_post.tags.all()
        })

    comments = Comment.objects.all().order_by("-id")

    
    form = CommentForm()
    identified_post = Post.objects.get(slug=slug)
    stored_post = request.session.get("stored_posts")
    
    if stored_post is not None:
          save_for_later = identified_post.id in stored_post
    else:
        save_for_later = False


    return render(request, "blog/post-detail.html", {
        "post": identified_post,
        "tags": identified_post.tags.all(),
        "form": form,
        "comments": comments,
        "is_saved":save_for_later
    })




def read_later(request):
    if request.method == "POST":
        stored_posts = request.session.get("stored_posts", [])

        try:
            post_id_str = request.POST.get("post_id", "")
            if post_id_str:
                post_id = int(post_id_str)

                if post_id not in stored_posts:
                    stored_posts.append(post_id)

                else:
                    stored_posts.remove(post_id)    

                request.session["stored_posts"] = stored_posts
                print("Saved post_id:", post_id)

        except ValueError:
            # Handle the case where post_id is not a valid integer
            pass

        return HttpResponseRedirect("/")

    stored_posts = request.session.get("stored_posts", [])
    has_posts = bool(stored_posts)
    
    if has_posts:
        posts = Post.objects.filter(id__in=stored_posts)
    else:
        posts = []

    print("Stored posts:", posts)

    return render(request, "blog/stored-posts.html", {
        "hasPosts": has_posts,
        "posts": posts
    })

