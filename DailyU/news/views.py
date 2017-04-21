from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import Category, User
from el_pagination.views import AjaxListView
from el_pagination.decorators import page_template
from .webhoseUtil import WebhoseUtil
from .twi_util import *
from . import word_util
from textblob import TextBlob as tb
import os
import sys
from lib2to3.fixes.fix_input import context
from reportlab.pdfgen import canvas
from easy_pdf.rendering import *
import datetime
import re


# Create your views here.

# The index page is not allow to any view without authentication
def getCurrentUser(request):
    username = request.session.get('current_user',None)
    if username is not None:
        user = User.objects.get(username =username )
    else:
        user = None
    return user

def check_login(orig_func):
    def temp_func(request):
        if getCurrentUser(request) == None:
            return HttpResponseRedirect("/login")
        else:
            return orig_func(request)
    return temp_func


@check_login
def index(request):
    username = request.session.get('current_user',None)
    user = User.objects.get(username=username)
    print(username)
    u = User.objects.get(username="yaling")
    u.addCateToUser('sports')
    print('***************test dbutils***************\n'+','.join(u.getUserCates()))
    u.rmCateFromUser('sports')
    output = ','.join(u.getUserCates())
    return render(request,"home.html",{'user':user,'categories':user.getUserCates()})

def login(request):
    username = request.POST.get('username',False)
    password = request.POST.get('password',False)
    try:
        user = User.objects.get(username=username)
        if(str(user.password) == str(password)):
            request.session['current_user'] = user.username
            return HttpResponseRedirect("/")
        else:
            return render(request,"login.html",{'err':'login error','user':None})
    except:
        e = sys.exc_info()[0]
        print(e)
    return render(request, "login.html")

def logout(request):
    del request.session['current_user']
    return HttpResponseRedirect("/login")


def editCategory(request):
    username = request.session.get('current_user',None)
    user = User.objects.get(username=username)
    if 'add_cat' in request.POST:
        new_category_name = request.POST.get('new_cat',False)
        if len(Category.objects.filter(cate_name=new_category_name)) != 0:
            #new_category = Category.objects.create(cate_name=new_category_name)
            if not new_category_name in user.getUserCates():
                user.addCateToUser(new_category_name)
        return HttpResponseRedirect("/")
        
    elif 'delete_cat' in request.POST:
        delete_cat_name = request.POST.get('current_cate',False)
        print("Deleted cate: "+delete_cat_name)
        user.rmCateFromUser(delete_cat_name)
        return HttpResponseRedirect("/")



    return render(request, "home.html")

def html_to_pdf_directly(request): 
    cur_user = getCurrentUser(request)
    sections = cur_user.getUserCates()
    wh = WebhoseUtil()
    posts = {}
    for section_name in sections:
        '''For development purpose, load existing json'''
        #wh.request(section_name)
        file_path = os.path.join(os.path.dirname(__file__), 'test_jsons/'+section_name+'.json')
        wh.loadJson(file_path)
        posts[section_name] = []
        titles = []
        texts = []
        for i in range(min(wh.numOfPosts(),10)):
            title = wh.getTitle(i)
            post_url = wh.getUrl(i)
            img = wh.getImg(i)
            text = wh.getText(i)
            author = wh.getAuthor(i)
            pub_time = wh.getPubTime(i)
            titles.append(title)
            texts.append(tb(text))
            posts[section_name].append({"title": title,
                          "post_url": post_url,
                          "text": text,
                          "author": author,
                          "pub_time": pub_time,
                          "img" : img})
     
#         tweets = ""#getTweets(texts[:10],titles[:10])
#         for i in range(min(10,wh.numOfPosts())):
#             posts[section_name][i]["tweets"] = tweets
         
    context = {
        'posts': posts,
        'sections' : sections,
    }
    template_name = "news2pdf.html"
    pdf_response = render_to_pdf_response(request,template_name,context)
    pdf_content = render_to_pdf(template_name, context)
    fname = datetime.datetime.now().strftime("%y-%m-%d")+'.pdf'
    folder_path = 'static/pdfs/'+cur_user.username+'/'#os.path.join(os.path.dirname(__file__),'pdfs/'+cur_user.username+'/')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    f = open(folder_path+fname, "wb")
    f.write(pdf_content)
    f.close()
    response = HttpResponse(pdf_response,content_type='application/pdf')
    response['Content-Disposition'] = 'filename="'+fname+'"'
    return response

def newspaper_archive(request):
    cur_user = getCurrentUser(request)
    folder_path = 'static/pdfs/'+cur_user.username+'/'
    pdfs_com = os.listdir(folder_path)
    pdfs = []
    for p in pdfs_com:
        pdfs.append(p.split('.')[0])
    #print(pdfs)
    context = {
        'user': cur_user,
        "pdfs":pdfs,
    }
    return render(request, "archive.html",context)

def view_pdf(request,pdf_name):
    cur_user = getCurrentUser(request)
    folder_path = 'static/pdfs/'+cur_user.username+'/'
    fs = FileSystemStorage()
    filename = folder_path+pdf_name+'.pdf'
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'filename="'+filename+'"'
            return response
    else:
        return HttpResponseNotFound('The requested pdf was not found in our server.')

def newspaperIndex(request):
    cur_user = getCurrentUser(request)
    sections = cur_user.getUserCates()
    sup_sections = []
    wh = WebhoseUtil()
    for s in sections:
        '''For development purpose, load existing json'''
        wh.request(s)
        file_path = os.path.join(os.path.dirname(__file__), 'test_jsons/'+s+'.json')
        wh.saveToFile(file_path)
        wh.loadJson(file_path)
        text = ""
        for i in range(min(10,wh.numOfPosts())):
            title = wh.getTitle(i)
            text = text+str(i+1)+". "+title+"\n"
        text = text+"More to be explored..."
        sup_sections.append({"name":s,"text":text})
    return render(request, "sections.html", {'sections':sup_sections})

@page_template('post_list_page.html')
def generateNewspaper(request,section_name,extra_context=None):
    cur_user = getCurrentUser(request)
    sections = cur_user.getUserCates()
    wh = WebhoseUtil()
    '''For development purpose, load existing json'''
    #wh.request(section_name)
    file_path = os.path.join(os.path.dirname(__file__), 'test_jsons/'+section_name+'.json')
    wh.loadJson(file_path)
    posts = []
    titles = []
    texts = []
    for i in range(min(wh.numOfPosts(),50)):
        title = wh.getTitle(i)
        post_url = wh.getUrl(i)
        img = wh.getImg(i)
        text = wh.getText(i)
        author = wh.getAuthor(i)
        pub_time = wh.getPubTime(i)
        titles.append(title)
        texts.append(tb(text))
        posts.append({"title": title,
                      "post_url": post_url,
                      "text": text,
                      "author": author,
                      "pub_time": pub_time,
                      "img" : img})


    current_time = datetime.datetime.now().strftime("%y-%m-%d_%H:%M")
    tw_file_path = os.path.join(os.path.dirname(__file__), 'saved_tweets/')
    r = re.compile(r"^"+section_name+".*")
    f = os.listdir(tw_file_path)
    get_file = list(filter(r.match,f))
    if get_file != [] and saved_tw_not_expired(current_time,get_file[0]):
        file_path = os.path.join(os.path.dirname(__file__), 'saved_tweets/')
        filename = get_file[0]
        with open(filename,'r') as f:
            for line in f:
                posts[i]["tweets"] = line
        f.close()

    else:
        
        filename = section_name+"&"+current_time
        tweets = getTweets(texts,titles,3)
        with open(filename,'w') as f:
            for i in range(len(posts)):
                f.write(tweets[i]+'\n')
                posts[i]["tweets"] = tweets[i]
        f.close()


    
    context = {
        'posts': posts,
        'sections' : sections,
        'section_name':section_name,
        'page_template': page_template,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, "post_list.html", context)

def getTweets(text_list,title_list,return_num):
    sorted_title_list= word_util._sort_words(text_list,title_list)
    tw = twi_util()
    tw.appAuth_api()
    tw_for_section = []
    for title in sorted_title_list:
        raw_tw =tw.get_all_related_tweets(title,5)
        filtered = list(tw.most_relevant(raw_tw,return_num))
        tw_for_section.append(filtered)
    return tw_for_section



def saved_tw_not_expired(c_time,filename):

    archive_time = filename.split('&')[1]
    t_dif = datetime.datetime.strptime(c_time,"%y-%m-%d_%H:%M") - datetime.datetime.strptime(archive_time,"%y-%m-%d_%H:%M")
    t_in_hours = t_dif.seconds/3600
    if(t_in_hours > 2):
        return False
    return True

