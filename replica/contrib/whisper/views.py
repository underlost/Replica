from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

from coreExtend.models import Account
from .models import Post, Thread, Known_IPs
from .forms import PostModelForm

def index(request):
    posts = Post.objects.order_by('pub_date').filter(is_public=True)
    ctx = {'posts': posts}
	return render(request, 'replica/contrib/whisper/index.html', ctx)

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    threads = Thread.objects.order_by('pub_date').filter(parent=post_id)
    f = ThreadModelForm(request.POST or None, instance=instance)
    if f.is_valid():
		f.save()
		messages.add_message(
			request, messages.INFO, 'New post saved!')
		return redirect('Whisper:PostDetail' post_id=post_id)

    ctx = {'post': post, 'threads': threads}
	return render(request, 'replica/contrib/whisper/post.html', ctx)

def post_add(request):
	#add a timeline.
	f = PostModelForm(request.POST or None, instance=instance)
	if f.is_valid():
		f.save()
		messages.add_message(
			request, messages.INFO, 'New post saved!')
		return redirect('Whisper:PostDetail' post_id=instance.guid)
	ctx = {'form': f, 'adding': True}
	return render(request, 'replica/contrib/whisper/edit-post.html', ctx)
