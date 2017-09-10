from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from django.http import HttpResponse
from forum.models import ForumMessageTestModel

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class IndexView(TemplateView):
    
    template_name = 'forumindex.html'
    title = "De Prinsen! reborn"
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['title'] = self.title
        tree = ForumMessageTestModel.get_annotated_list()
        for item, info in tree:
            info['depthrange']=range(info['level'])
        context['tree'] = tree
        return context

    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return super(TemplateView, self).render_to_response(context)

class MessageView(TemplateView):
    
    template_name = 'forummessage.html'
    title = "De Prinsen! reborn: post"
    
    def get_context_data(self, **kwargs):
        context = super(MessageView, self).get_context_data(**kwargs)
        context['title'] = self.title
        post = ForumMessageTestModel.objects.get(n54ID=self.kwargs['id'])
        context['post'] = post
        tree = ForumMessageTestModel.get_annotated_list(parent=post)[1:]
        for item, info in tree:
            info['depthrange']=range(info['level']-1)
        context['tree'] = tree
        return context
    
    def get(self,request,*args,**kwargs):
        context = self.get_context_data()
        return super(TemplateView, self).render_to_response(context)
