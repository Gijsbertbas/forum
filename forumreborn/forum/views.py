from django.views.generic.base import TemplateView
#from django.templatetags.static import static
from django.conf import settings
from forum.models import ForumMessageModel
from random import randint
import pickle

class IndexView(TemplateView):

    template_name = 'forumindex.html'
    title = "De Prinsen!"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['title'] = self.title
        indno = max(int(self.kwargs['indno']),1)
        context['previous'] = indno-1
        context['random'] = randint(1,int(ForumMessageModel.get_root_nodes().count()/20))
        context['next'] = indno+1
        perpage = 20
        tree = []
        for node in ForumMessageModel.get_root_nodes().order_by('-timestamp')[indno*perpage-perpage:indno*perpage]:
            tree.extend(ForumMessageModel.get_annotated_list(node))
        for item, info in tree:
            info['depthrange']=range(info['level'])
        context['tree'] = tree
        return context


    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return super(TemplateView, self).render_to_response(context)

class MessageView(TemplateView):

    template_name = 'forummessage.html'
    title = "De Prinsen! post"

    def get_context_data(self, **kwargs):
        context = super(MessageView, self).get_context_data(**kwargs)
        context['title'] = self.title
        post = ForumMessageModel.objects.get(n54ID=self.kwargs['id'])
        context['post'] = post
        tree = ForumMessageModel.get_annotated_list(parent=post)[1:]
        for item, info in tree:
            info['depthrange']=range(info['level']-1)
        context['tree'] = tree
        return context

    def get(self,request,*args,**kwargs):
        context = self.get_context_data()
        return super(TemplateView, self).render_to_response(context)

class FactsView(TemplateView):

    template_name = 'forumfacts.html'
    title = "De Prinsen! facts en figures"

    def get_context_data(self, **kwargs):
        context = super(FactsView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['baarden'] = ForumMessageModel.get_root_nodes().count()
        context['posts'] = ForumMessageModel.objects.all().count()
        context['authors'] = ForumMessageModel.objects.order_by().values('author').distinct().count()
        context['prinsennamen'] = pickle.load(open(settings.STATIC_ROOT+'/forum/prinsennamen.pickle','rb'))
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['woord'] = 'Prins'
        context['woordcount'] = ForumMessageModel.objects.filter(body__contains='Prins').count()
        return super(TemplateView, self).render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['woord'] = request.POST['woord']
        context['woordcount'] = ForumMessageModel.objects.filter(body__icontains=context['woord']).count()
        return super(TemplateView, self).render_to_response(context)
