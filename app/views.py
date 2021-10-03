"""
Definition of views.
"""
from .forms import AnketaForm
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models import Sum
from django.contrib.auth.forms import UserCreationForm
from django import template
from django.db import models
from .models import Blog
from .models import Comment
from .models import Catalog
from .models import Orders
from .models import Requisites
from .forms import CommentForm
from .forms import BlogForm
from .forms import ProductForm
from .forms import OrderForm
from .forms import EmailForm
from .forms import RequisitesForm
from django.core.mail import send_mail

def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

def home(request):
    posts = Catalog.objects.all() 
 
    assert isinstance(request, HttpRequest) 
    return render( 
        request, 
             'app/index.html', 
                { 
                    'posts': posts, 
                    'year': datetime.now().year, 
                } 
        ) 

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Связаться с нами',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Информация о магазине',
            'year':datetime.now().year,
        }
    )

def pool(request):
    """Опросник"""
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1':'Вопрос о товаре', '2':'У меня проблема'}
    internet = {'1':'Физ. лицо','2':'Юр. лицо'}
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['gender'] = gender[form.cleaned_data['gender'] ]
            data['internet'] = internet[form.cleaned_data['internet'] ]
            data['message'] = form.cleaned_data['message']
            toemail = form.cleaned_data['email']
            mesage = 'Что случилось: ' + data['gender'] + '\nКем Вы являетесь: ' + data['internet'] + '\nСуть вопроса: ' + data['message'] + '\nE-mail: ' + toemail
            send_mail('Лучик: ' + data['name'], mesage, 'mishhard99@mail.ru', ['mishhard@yandex.ru'], fail_silently=False)
            if(form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
                send_mail('Лучик: ' + data['name'], mesage, 'mishhard99@mail.ru', [toemail], fail_silently=False)
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            form = None
    else:
        form = AnketaForm()
    return render(
        request,
        'app/pool.html',
        {
            'title':'Обратная связь',
            'message':'Напишите нам, и мы обязательно ответим!',
            'form':form,
            'data':data,
            'year':datetime.now().year
        }
    )
def links(request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы',
            'message':'Вам может пригодиться',
            'year':datetime.now().year,
        }
    )
def blog(request):
    """Renders the contact page."""
    posts = Blog.objects.all()
    price_sum = posts.count
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'price_sum': price_sum,                
            'posts' : posts,
            'year':datetime.now().year,
        }
    )

def registration(request):
    assert isinstance(request, HttpRequest)
    if request.method == "POST": # после отправки формы
       regform = UserCreationForm (request.POST)
       if regform.is_valid(): #валидация полей 
         reg_f = regform.save(commit=False) # не сохраняем автоматически данные 
         reg_f.is_staff = False # запрещен вход в административный 
         reg_f.is_active = True # активный 
         reg_f.is_provider = False
         reg_f.is_superuser = False # не является 
         reg_f.date_joined = datetime.now() # дата 
         reg_f.last_login = datetime.now() # дата последней 
         reg_f.save() # сохраняем изменения после добавления 
         return redirect('home') # переадресация на главную страницу после 
    else:
       regform = UserCreationForm() # создание объекта формы для ввода данных нового 
    return render(
       request,
       'app/registration.html',
       {
         'title':'Регистрация',
         'regform': regform, # передача формы в шаблон веб-страницы
         'year':datetime.now().year,
       }
    )

def registration_provider(request):
    assert isinstance(request, HttpRequest)
    if request.method == "POST": # после отправки формы
       regform = UserCreationForm (request.POST)
       if regform.is_valid(): #валидация полей 
         reg_f = regform.save(commit=False) # не сохраняем автоматически данные 
         reg_f.is_staff = False # запрещен вход в административный 
         reg_f.is_active = True # активный 
         reg_f.is_provider = True
         reg_f.is_superuser = False # не является 
         reg_f.date_joined = datetime.now() # дата 
         reg_f.last_login = datetime.now() # дата последней 
         reg_f.save() # сохраняем изменения после добавления 
         return redirect('home') # переадресация на главную страницу после 
    else:
       regform = UserCreationForm() # создание объекта формы для ввода данных нового 
    return render(
       request,
       'app/registration_provider.html',
       {
         'title':'Регистрация поставщика',
         'regform': regform, # передача формы в шаблон веб-страницы
         'year':datetime.now().year,
       }
    )

def blogpost(request, parametr):
    """Renders the about page."""
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = Blog.objects.get(id=parametr)
            comment_f.save()

            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blogpost.html',
        {   'form': form,
            'comments': comments,
            'post_1': post_1,
            'year':datetime.now().year
        }
    )

def newpost(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()
    
    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью',
            'year':datetime.now().year,
        }
    )

def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'year':datetime.now().year,
        }
    )

def finances(request):
    assert isinstance(request, HttpRequest)
    data = None
    posts = Catalog.objects.filter(author = request.user) 
    price_sum = sum(post.stonks for post in posts)
    context = {
                'price_sum': price_sum,                
                }
    if Requisites.objects.filter(provider_id = request.user):
        req = Requisites.objects.get(provider_id = request.user)
        return render(
        request,
        'app/finances.html',
        {
            'title':'Финансы',
            'message':'Вы заработали ' + str(price_sum) + '₽. Мы вычтем из этой суммы ' + str(price_sum * 0.03) + '₽ в качестве комиссии и отправим в ваш банк',
            'req' :req,
            'year':datetime.now().year
        }
        )
    else:
        if request.method == 'POST':
            form = RequisitesForm(request.POST)
            if form.is_valid():
                data = dict()
                data['bank'] = form.cleaned_data['bank']
                bank = data['bank']
                data['bik'] = form.cleaned_data['bik']
                bik = data['bik']
                data['kpp'] = form.cleaned_data['kpp']
                kpp = data['kpp']
                data['account'] = form.cleaned_data['account']
                account = data['account']
                provider = request.user
                cost_obj = Requisites(provider=provider, bank=bank, bik=bik, kpp=kpp, account=account)
                cost_obj.save()
                form = None
        else:
            form = RequisitesForm()
    return render(
        request,
        'app/finances.html',
        {
            'title':'Финансы',
            'message':'Вы заработали ' + str(price_sum) + '₽. Мы вычтем из этой суммы ' + str(price_sum * 0.03) + '₽ в качестве комиссии и отправим в ваш банк',
            'form':form,
            'data':data,
            'year':datetime.now().year
        }
    )


def cart(request): 
    posts = Orders.objects.filter(author = request.user, ready=False) 
    posts_all = Catalog.objects.all() 
    price_sum = Orders.objects.filter(author = request.user, ready=False).count 
    price_summ = sum(post.qnt for post in posts)
    context = {
                'price_sum': price_sum,                
                }
    assert isinstance(request, HttpRequest) 
    return render( 
        request, 
            'app/cart.html', 
            { 
                'title': 'Корзина', 
                'posts': posts, 
                'posts_all': posts_all, 
                'year': datetime.now().year, 
                'price_sum': price_sum,
            } 
        ) 

 
def addtocart(request,id): 
    test = Catalog.objects.filter(id=id) 

    assert isinstance(request, HttpRequest) 
    if request.method == "POST": 
        orderform = OrderForm(request.POST, request.FILES) 
        if orderform.is_valid(): 
             order_f = orderform.save(commit=False) 
             order_f.post_id = id 
             order_f.posted = datetime.now() 
             order_f.quantity = +1
             order_f.author = request.user 
             order_f.save() 
             
 
             return redirect('cart') 
    else: 
        orderform = OrderForm() 
 
    return render( 
     request, 
         'app/addtocart.html', 
         { 
             'orderform': orderform, 
             'posts': test, 
             'title': 'Информация о товаре', 
             'year': datetime.now().year, 
         } 
     )

def payed(request,bid): 
    query = Orders.objects.get(id = bid)
    bob = User.objects.get(id=request.user.id)
    product = Catalog.objects.get(id = query.post_id)
    product.quantity = product.quantity - query.qnt
    if product.quantity < 0:
        return render( 
         request, 
             'app/Nope.html', 
             { 
                 'message': 'Доступное количество товара: ' + str(product.quantity), 
                   'title': 'Ошибка', 
                 'year': datetime.now().year, 
             } 
         )
    elif query.on_processing == True:
            return render( 
             request, 
                 'app/Nope.html', 
                 { 
                     'message': 'Мы уже проверяем оплату заказа', 
                       'title': 'Спасибо', 
                     'year': datetime.now().year, 
                 } 
                 )
    else:
        query.on_processing = True
        query.save()
        product.save()
    return render( 
     request, 
         'app/Nope.html', 
         { 
             'message': 'Как только средства поступят, мы отправим товар на вашу почту ' + str(bob.email), 
               'title': 'Спасибо', 
             'year': datetime.now().year, 
         } 
     )

def paying(request,bid): 
    posts = Orders.objects.filter(id=bid) 
    posts_all = Catalog.objects.all 
    query = Orders.objects.get(id = bid)
    bob = User.objects.get(id=request.user.id)
    product = Catalog.objects.get(id = query.post_id)
    product.quantity = product.quantity - query.qnt
    if product.quantity < 0:
        return render( 
         request, 
             'app/Nope.html', 
             { 
                 'message': 'Доступное количество товара: ' + str(product.quantity + query.qnt), 
                   'title': 'Ошибка', 
                 'year': datetime.now().year, 
             } 
         )
    else:
        query.save()
        
        assert isinstance(request, HttpRequest) 
        data = None
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            data = dict()
            data['email'] = form.cleaned_data['email']
            bob.email = data['email']
            bob.save(update_fields=["email"])
            return render( 
            request, 
            'app/nope.html', 
            { 
                     'posts': posts, 
                      'posts_all': posts_all,  
                       'title': 'Спасибо', 
                       'message' : 'После подтверждения оплаты мы отправим ваш товар на почту ' + str(bob.email),
                     'year': datetime.now().year, 
             } 
             )
 

    else:
        form = EmailForm()
        return render(
        request, 
        'app/paying.html', 
        { 
          'posts': posts, 
          'posts_all': posts_all,  
          'title': 'Оплата заказа №', 
          'form':form,
          'data':data,
          'year': datetime.now().year, 
         } 
         )
       
       
    


def buy(request,bid):
    assert isinstance(request, HttpRequest)

    query = Orders.objects.get(id = bid)
    query.ready = True
    query.date = datetime.now() 
    query.save()

    return redirect('completeorders')

def buymanage(request,bid):
    assert isinstance(request, HttpRequest)

    query = Orders.objects.get(id = bid)
    product = Catalog.objects.get(id = query.post_id)
    product.stonks = product.stonks+query.qnt*product.price
    query.ready = True
    query.on_processing = False
    query.date = datetime.now() 
    query.save()
    product.save(update_fields=["stonks"])
    return redirect('allorders')

def unbuymanage(request,bid):
    assert isinstance(request, HttpRequest)
    posts = Orders.objects.filter(id=bid) 
    posts_all = Catalog.objects.all 
    query = Orders.objects.get(id = bid)
    query.on_processing = True
    product = Catalog.objects.get(id = query.post_id)
    product.quantity = product.quantity + query.qnt
    product.save()
    query.ready = False
    query.on_processing = False
    query.date = datetime.now() 
    query.save()

    return redirect('allorders')


def onemore(request,nid):
    assert isinstance(request, HttpRequest)

    query = Orders.objects.get(id = nid)
    product = Catalog.objects.get(id = query.post_id)
    query.qnt =   query.qnt + 1
    query.save()
    product.save()
    return redirect('cart')

def onemoreproductmanage(request,pid):
    assert isinstance(request, HttpRequest)

    product = Catalog.objects.get(id = pid)
    product.quantity =   product.quantity + 1
    product.save()
    return redirect('home')

def onemoreproduct(request,pid):
    assert isinstance(request, HttpRequest)

    product = Catalog.objects.get(id = pid)
    if product.author == request.user :
        product.quantity =   product.quantity + 1
        product.save()
        return redirect('home')
    else:
        return render(
        request,
        'app/nope.html',
        {
            'title':'Ошибка',
            'message': 'У вас нет полномочий на совершение этого действия',
            'year':datetime.now().year,
        }
    )

def onelessproduct(request,pid):
    assert isinstance(request, HttpRequest)

    product = Catalog.objects.get(id = pid)
    if product.author == request.user :
        product.quantity =   product.quantity - 1
        product.save()
        return redirect('home')
    else:
        return render(
        request,
        'app/nope.html',
        {
            'title':'Ошибка',
            'message': 'У вас нет полномочий на совершение этого действия',
            'year':datetime.now().year,
        }
    )


def onelessproductmanage(request,pid):
    assert isinstance(request, HttpRequest)

    product = Catalog.objects.get(id = pid)
    product.quantity =   product.quantity - 1
    product.save()
    return redirect('home')

def onemoremanage(request,nid):
    assert isinstance(request, HttpRequest)

    query = Orders.objects.get(id = nid)
    query.qnt =   query.qnt + 1
    query.save()

    return redirect('allorders')

def oneless(request,pid):
    assert isinstance(request, HttpRequest)

    query = Orders.objects.get(id = pid)
    query.qnt =   query.qnt -  1
    if query.qnt < 1:
        query.qnt = 1
   
    query.save()

    return redirect('cart')

def onelessmanage(request,pid):
    assert isinstance(request, HttpRequest)

    query = Orders.objects.get(id = pid)
    query.qnt =   query.qnt -  1
    if query.qnt < 1:
        query.qnt = 1
   
    query.save()

    return redirect('allorders')


def order(request,did):
    assert isinstance(request, HttpRequest)
    posts = Orders.objects.filter(id = did) 
    posts_all = Catalog.objects.all 
    price_sum = sum(post.qnt for post in posts)
    query = Orders.objects.get(id = did)
    product = Catalog.objects.get(id = query.post_id)
    market = query.author.id
    bob = User.objects.get(id = market)


    return render( 
        request, 
            'app/order.html', 
            { 
                'bob' : bob,
              'posts': posts, 
              'posts_all': posts_all,  
             'title': 'Заказ №', 
            'year': datetime.now().year, 
            } 
           ) 


def delcart(request,did):
    assert isinstance(request, HttpRequest)

    query = Orders.objects.get(id = did)
    product = Catalog.objects.get(id = query.post_id)
    if query.on_processing == True:
       if query.ready == False:
          product.quantity = product.quantity + query.qnt
    query.delete()
    product.save()

    return redirect('cart')

def delcartmanage(request,did):
    assert isinstance(request, HttpRequest)

    query = Orders.objects.get(id = did)
    query.delete()

    return redirect('allorders')

def completeorders(request): 
    posts = Orders.objects.filter(author = request.user, ready=True) 
    posts_all = Catalog.objects.all() 
    price_sum = Orders.objects.filter(author = request.user, ready=True).count
    context = {
                'price_sum': price_sum,                
                }
    assert isinstance(request, HttpRequest) 
    return render( 
        request, 
            'app/orders.html', 
            { 
                'title': 'Заказы', 
                'posts': posts, 
                'posts_all': posts_all, 
                'year': datetime.now().year, 
                 'price_sum': price_sum,
            } 
        ) 


def allorders(request):
    """Renders the contact page."""
    posts = Orders.objects.all()
    posts_all = Catalog.objects.all() 
    if request.user.is_provider == True:
        b = Catalog.objects.all().filter(author = request.user)
        bb = sum((count.author.id)/request.user.id for count in b)
        price_sum = 0
        i = 0
        count = 0
        countt = 0
        summm = 0
        while i < bb:
            c = b[i]
            d = c.id
            counts = Orders.objects.filter(post = d)
            summ = int(sum((count.id/count.id) for count in counts))
            i += 1
            price_sum += summ
        posts_all = Catalog.objects.filter(author = request.user.id)
    else:
        price_sum = Orders.objects.all().count
    me = request.user
    assert isinstance(request, HttpRequest)
    return render(    
     request,
     'app/allorders.html',
                 {
                'title':'Управление заказами',
                'posts' : posts,
                'me' : me,
                'posts_all' : posts_all,
                'year':datetime.now().year,
                'price_sum': price_sum,
                }
            )
        


def newproduct(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        productform = ProductForm(request.POST, request.FILES)
        if productform.is_valid():
           Catalog_f = productform.save(commit=False)
           Catalog_f.posted = datetime.now()
           Catalog_f.author = request.user
           Catalog_f.save()
           return redirect('home')
    else:
       productform = ProductForm()
    
    return render(
        request,
        'app/newproduct.html',
        {
            'productform': productform,
            'title': 'Добавить товар',
            'year':datetime.now().year,
        }
    )

def delproductmanage(request,did):
    assert isinstance(request, HttpRequest)

    query = Catalog.objects.get(id = did)
    udalitel = request.user.is_staff
    if request.user.is_staff == 1:
       query.delete()
       return redirect('home')
    elif query.author_id - request.user.id == 0:
         query.delete()
         return redirect('home')
    else:
       return redirect('nope')
      

def nope(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/nope.html',
        {
            'title':'Ошибка',
            'message': 'У вас нет полномочий на совершение этого действия',
            'year':datetime.now().year,
        }
    )
