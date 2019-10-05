from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from .forms import EmailPostForm, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from taggit.models import Tag

# Create your views here.
def post_list(request,tag_slug=None):
    #posts=Post.published.all()
    #return render(request,'blog/post/list.html',{'posts':posts})
    object_list=Post.published.all()
    tag = None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        object_list=object_list.filter(tag__in=[tag])
    paginator=Paginator(object_list,3) #3 post in each page
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        #If page is not an Integer deliver the first page
        posts=paginator.page(1)
    except EmptyPage:
        #If page is out of range deliver last page of results 
        posts=paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{'page':page,
                                                'posts':posts,
                                                'tag':tag})


def post_detail(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,
                                status='published',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    #List of active comments for this post
    comments=post.comments.filter(active=True)
    new_comment=None

    if request.method == 'POST':
        # A comment was posted
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            #create Comment Object but do not save in database yet
            new_comment=comment_form.save(commit=False)
            #Assign current post to the comment
            new_comment.post=post
            #save the comment to database
            new_comment.save()
    else:
        comment_form=CommentForm()

    return render(request,'blog/post/detail.html',{'post':post,
                                                    'comments':comments,
                                                    'new_comment':new_comment,
                                                    'comment_form':comment_form})

def post_share(request,post_id):
    post=get_object_or_404(Post,id=post_id,status='published')
    sent=False
    if request.method=='POST':
        #Form was submitted
        form=EmailPostForm(request.POST)
        if form.is_valid():
            #form fields passed verification
            cd=form.cleaned_data
            #send an email
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{} ({}) recommends your reading "{}" '.format(cd['name'],cd['email'],post.title)
            message='Read "{}" at {} \n\n {}\'s comments: '.format(post.title,post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'admin@blog.com',[cd['to']])
            sent=True
    else:
        form=EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,
                                                    'form':form,
                                                    'sent':sent})

