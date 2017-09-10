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


