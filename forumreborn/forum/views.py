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
        indno = max(int(self.kwargs['indno']),1)
        context['previous'] = indno-1
        context['next'] = indno+1
        perpage = 10
        tree = []
        for node in ForumMessageTestModel.get_root_nodes().order_by('-timestamp')[indno*perpage-perpage:indno*perpage]: 
            tree.extend(ForumMessageTestModel.get_annotated_list(node))
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
