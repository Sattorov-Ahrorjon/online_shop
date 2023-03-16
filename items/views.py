from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Product, Status, Comment, Color, Size, Filter, AveragePrice, Cart, Purchased, Activated
from account.models import Customer
from django.contrib import messages
from django.http import HttpRequest


def get_home(request):
    try:
        query = Product.objects
        categories = query.filter(status=Status.Published).order_by('category__name').distinct('category__name')
        # product_list = query.filter(status=Status.Published)
        # comment_list = Comment.objects.filter(active=True)
        # star_dict = dict()
        # for product in product_list:
        #     star_dict[product.name] = 1
        #     for com in comment_list:
        #         if product.name == com.product.name:
        #             star_dict[product.name] = star_dict[product.name] + com.star
        #
        # # hhh
        # print("Star  -  ", star_dict)

        featured = Comment.objects.filter(active=True).order_by('-star')[:8]
        recent = query.filter(status=Status.Published).order_by('-created_time')[:8]
    except:
        categories = []
        featured = []
        recent = []
    context = {
        'home': 'active',
        'categories': categories,
        'featured': featured,
        'recent': recent,
    }
    return render(request, 'index.html', context)


def get_shop(request):
    try:
        Filter.objects.create(customer=request.user.username)
    except:
        pass

    if request.GET.get('q'):
        query = request.GET.get('q')
        objects = Product.objects.filter(Q(status=Status.Published) & Q(name__icontains=query))
    else:
        objects = Product.objects.filter(status=Status.Published)

    objects_price = AveragePrice.objects.values_list('price', flat=True).order_by('price')
    objects_color = Color.objects.values_list('color', flat=True)[:5]
    objects_size = Size.objects.values_list('symbol', flat=True)[:5]
    # paginator
    paginator = Paginator(objects, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'shop': 'active',
        'objects_price': objects_price,
        'objects_color': objects_color,
        'objects_size': objects_size,
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, 'shop.html', context)


def get_sorting_store(request, number):
    if request.user.is_authenticated:
        one = ''
        two = ''
        shop = 'active'
        query = Product.objects
        filter = Filter.objects

        try:
            dv = filter.get(customer=request.user.username)
            dv.number = number
            dv.save()
        except:
            pass

        category = filter.get(customer=request.user.username).category
        if not category:
            category = query.get(id=1).category.name

        color = filter.get(customer=request.user.username).color
        if not color:
            color = query.get(id=1).color.color

        size = filter.get(customer=request.user.username).size
        if not size:
            size = query.get(id=1).size.symbol

        price = filter.get(customer=request.user.username).price
        if not price:
            price = query.get(id=1).price

        if number == 1:
            one = 'active'
            objects = query.filter(
                Q(status=Status.Published) & Q(color__color=color) & Q(size__symbol=size) & Q(price__lte=price) & Q(
                    category__name=category)).order_by(
                '-created_time')[:9]
        elif number == 2:
            two = 'active'
            objects = Comment.objects.filter(
                Q(active=True) & Q(product__color__color=color) & Q(product__size__symbol=size) & Q(
                    product__price__lte=price) & Q(product__category__name=category)).order_by('-star')[:9]
            products = []
            for obj in objects:
                products.append(obj.product)
            objects = list(set(products))
        else:
            objects = query.filter(
                Q(status=Status.Published) & Q(color__color=color) & Q(size__symbol=size) & Q(price__lte=price) & Q(
                    category__name=category)).order_by(
                '-created_time')[:9]

        objects_price = AveragePrice.objects.values_list('price', flat=True).order_by('price')
        objects_color = Color.objects.values_list('color', flat=True)[:5]
        objects_size = Size.objects.values_list('symbol', flat=True)[:5]
        # paginator
        paginator = Paginator(objects, 9)
        page_number = request.GET.get('page')
        page_objects = paginator.get_page(page_number)
        messages.success(request,
                         f"category => {category} / price => {price} / color => {color} / size => {size} /")

        context = {
            'shop': shop,
            'one': one,
            'two': two,

            'objects_price': objects_price,
            'objects_color': objects_color,
            'objects_size': objects_size,

            'page_obj': page_objects,
            'paginator': paginator,
        }
    else:
        objects = Product.objects.filter(status=Status.Published)

        objects_price = AveragePrice.objects.values_list('price', flat=True).order_by('price')
        objects_color = Color.objects.values_list('color', flat=True)[:5]
        objects_size = Size.objects.values_list('symbol', flat=True)[:5]
        # paginator
        paginator = Paginator(objects, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        messages.success(request, "If you are not registered, the contest will not work !")

        context = {
            'shop': 'active',
            'objects_price': objects_price,
            'objects_color': objects_color,
            'objects_size': objects_size,
            'page_obj': page_obj,
            'paginator': paginator,
        }

    return render(request, 'shop.html', context)


def get_sorting_price(request, price):
    if request.user.is_authenticated:

        one = ''
        two = ''
        shop = 'active'
        query = Product.objects
        filter = Filter.objects

        try:
            dv = filter.get(customer=request.user.username)
            dv.price = price
            dv.save()
        except:
            pass
        category = filter.get(customer=request.user.username).category
        if not category:
            category = query.get(id=1).category.name

        color = filter.get(customer=request.user.username).color
        if not color:
            color = query.get(id=1).color.color

        size = filter.get(customer=request.user.username).size
        if not size:
            size = query.get(id=1).size.symbol

        number = filter.get(customer=request.user.username).number

        if number == 1:
            one = 'active'
            objects = query.filter(
                Q(status=Status.Published) & Q(color__color=color) & Q(size__symbol=size) & Q(price__lte=price) & Q(
                    category__name=category)).order_by(
                '-created_time')[:9]
        elif number == 2:
            two = 'active'
            objects = Comment.objects.filter(
                Q(active=True) & Q(product__color__color=color) & Q(product__size__symbol=size) & Q(
                    product__price__lte=price) & Q(product__category__name=category)).order_by(
                '-star')[:9]
            products = []
            for obj in objects:
                products.append(obj.product)
            objects = list(set(products))
        else:
            objects = query.filter(
                Q(status=Status.Published) & Q(color__color=color) & Q(size__symbol=size) & Q(price__lte=price) & Q(
                    category__name=category)).order_by(
                '-created_time')[:9]

        objects_price = AveragePrice.objects.values_list('price', flat=True).order_by('price')
        objects_color = Color.objects.values_list('color', flat=True)[:5]
        objects_size = Size.objects.values_list('symbol', flat=True)[:5]
        # paginator
        paginator = Paginator(objects, 9)
        page_number = request.GET.get('page')
        page_objects = paginator.get_page(page_number)
        messages.success(request,
                         f"category => {category} / price => {price} / color => {color} / size => {size} /")

        context = {
            'shop': shop,
            'one': one,
            'two': two,

            'objects_price': objects_price,
            'objects_color': objects_color,
            'objects_size': objects_size,

            'page_obj': page_objects,
            'paginator': paginator,
        }
    else:
        objects = Product.objects.filter(status=Status.Published)

        objects_price = AveragePrice.objects.values_list('price', flat=True).order_by('price')
        objects_color = Color.objects.values_list('color', flat=True)[:5]
        objects_size = Size.objects.values_list('symbol', flat=True)[:5]
        # paginator
        paginator = Paginator(objects, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        messages.success(request, "If you are not registered, the contest will not work !")

        context = {
            'shop': 'active',
            'objects_price': objects_price,
            'objects_color': objects_color,
            'objects_size': objects_size,
            'page_obj': page_obj,
            'paginator': paginator,
        }

    return render(request, 'shop.html', context)


def get_sorting_color(request, color):
    if request.user.is_authenticated:

        one = ''
        two = ''
        shop = 'active'
        query = Product.objects
        filter = Filter.objects

        try:
            dv = filter.get(customer=request.user.username)
            dv.color = color
            dv.save()
        except:
            pass

        category = filter.get(customer=request.user.username).category
        if not category:
            category = query.get(id=1).category.name

        size = filter.get(customer=request.user.username).size
        if not size:
            size = query.get(id=1).size.symbol

        price = filter.get(customer=request.user.username).price
        if not price:
            price = query.get(id=1).price

        number = filter.get(customer=request.user.username).number

        if number == 1:
            one = 'active'
            objects = query.filter(
                Q(status=Status.Published) & Q(color__color=color) & Q(size__symbol=size) & Q(price__lte=price) & Q(
                    category__name=category)).order_by('-created_time')[:9]
        elif number == 2:
            two = 'active'
            objects = Comment.objects.filter(
                Q(active=True) & Q(product__color__color=color) & Q(product__size__symbol=size) & Q(
                    product__price__lte=price) & Q(product__category__name=category)).order_by(
                '-star')[:9]
            products = []
            for obj in objects:
                products.append(obj.product)
            objects = list(set(products))
        else:
            objects = query.filter(
                Q(status=Status.Published) & Q(color__color=color) & Q(size__symbol=size) & Q(price__lte=price) & Q(
                    category__name=category)).order_by(
                '-created_time')[:9]

        objects_price = AveragePrice.objects.values_list('price', flat=True).order_by('price')
        objects_color = Color.objects.values_list('color', flat=True)[:5]
        objects_size = Size.objects.values_list('symbol', flat=True)[:5]
        # paginator
        paginator = Paginator(objects, 9)
        page_number = request.GET.get('page')
        page_objects = paginator.get_page(page_number)
        messages.success(request,
                         f"category => {category} / price => {price} / color => {color} / size => {size} /")

        context = {
            'shop': shop,
            'one': one,
            'two': two,

            'objects_price': objects_price,
            'objects_color': objects_color,
            'objects_size': objects_size,

            'page_obj': page_objects,
            'paginator': paginator,
        }
    else:
        objects = Product.objects.filter(status=Status.Published)

        objects_price = AveragePrice.objects.values_list('price', flat=True).order_by('price')
        objects_color = Color.objects.values_list('color', flat=True)[:5]
        objects_size = Size.objects.values_list('symbol', flat=True)[:5]
        # paginator
        paginator = Paginator(objects, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        messages.success(request, "If you are not registered, the contest will not work !")

        context = {
            'shop': 'active',
            'objects_price': objects_price,
            'objects_color': objects_color,
            'objects_size': objects_size,
            'page_obj': page_obj,
            'paginator': paginator,
        }

    return render(request, 'shop.html', context)


def get_sorting_size(request, size):
    if request.user.is_authenticated:

        one = ''
        two = ''
        shop = 'active'
        query = Product.objects
        filter = Filter.objects

        try:
            dv = filter.get(customer=request.user.username)
            dv.size = size
            dv.save()
        except:
            pass

        category = filter.get(customer=request.user.username).category
        if not category:
            category = query.get(id=1).category.name
        color = filter.get(customer=request.user.username).color
        if not color:
            color = query.get(id=1).color.color
        price = filter.get(customer=request.user.username).price
        if not price:
            price = query.get(id=1).price
        number = filter.get(customer=request.user.username).number

        if number == 1:
            one = 'active'
            objects = query.filter(
                Q(status=Status.Published) & Q(color__color=color) & Q(size__symbol=size) & Q(price__lte=price) & Q(
                    category__name=category)).order_by(
                '-created_time')[:9]
        elif number == 2:
            two = 'active'
            objects = Comment.objects.filter(
                Q(active=True) & Q(product__color__color=color) & Q(product__size__symbol=size) & Q(
                    product__price__lte=price) & Q(product__category__name=category)).order_by(
                '-star')[:9]
            products = []
            for obj in objects:
                products.append(obj.product)
            objects = list(set(products))
        else:
            objects = query.filter(
                Q(status=Status.Published) & Q(color__color=color) & Q(size__symbol=size) & Q(price__lte=price) & Q(
                    category__name=category)).order_by(
                '-created_time')[:9]

        objects_price = AveragePrice.objects.values_list('price', flat=True).order_by('price')
        objects_color = Color.objects.values_list('color', flat=True)[:5]
        objects_size = Size.objects.values_list('symbol', flat=True)[:5]
        # paginator
        paginator = Paginator(objects, 9)
        page_number = request.GET.get('page')
        page_objects = paginator.get_page(page_number)
        messages.success(request,
                         f"category => {category} / price => {price} / color => {color} / size => {size} /")

        context = {
            'shop': shop,
            'one': one,
            'two': two,

            'objects_price': objects_price,
            'objects_color': objects_color,
            'objects_size': objects_size,

            'page_obj': page_objects,
            'paginator': paginator,
        }
    else:
        objects = Product.objects.filter(status=Status.Published)

        objects_price = AveragePrice.objects.values_list('price', flat=True).order_by('price')
        objects_color = Color.objects.values_list('color', flat=True)[:5]
        objects_size = Size.objects.values_list('symbol', flat=True)[:5]
        # paginator
        paginator = Paginator(objects, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        messages.success(request, "If you are not registered, the contest will not work !")

        context = {
            'shop': 'active',
            'objects_price': objects_price,
            'objects_color': objects_color,
            'objects_size': objects_size,
            'page_obj': page_obj,
            'paginator': paginator,
        }

    return render(request, 'shop.html', context)


def get_sorting_category(request, category):
    if request.user.is_authenticated:

        try:
            Filter.objects.create(customer=request.user.username)
        except:
            pass

        one = ''
        two = ''
        shop = 'active'
        query = Product.objects
        filter = Filter.objects

        try:
            dv = filter.get(customer=request.user.username)
            dv.category = category
            dv.save()
        except:
            pass

        size = filter.get(customer=request.user.username).size
        if not size:
            size = query.get(id=1).size.symbol
        color = filter.get(customer=request.user.username).color
        if not color:
            color = query.get(id=1).color.color
        price = filter.get(customer=request.user.username).price
        if not price:
            price = query.get(id=1).price
        number = filter.get(customer=request.user.username).number

        if number == 1:
            one = 'active'
            objects = query.filter(
                Q(status=Status.Published) & Q(color__color=color) & Q(size__symbol=size) & Q(price__lte=price) & Q(
                    category__name=category)).order_by('-created_time')[:9]
        elif number == 2:
            two = 'active'
            objects = Comment.objects.filter(
                Q(active=True) & Q(product__color__color=color) & Q(product__size__symbol=size) & Q(
                    product__price__lte=price) & Q(product__category__name=category)).order_by('-star')[:9]
            products = []
            for obj in objects:
                products.append(obj.product)
            objects = list(set(products))
        else:
            objects = query.filter(
                Q(status=Status.Published) & Q(color__color=color) & Q(size__symbol=size) & Q(price__lte=price) & Q(
                    category__name=category)).order_by('-created_time')[:9]

        objects_price = AveragePrice.objects.values_list('price', flat=True).order_by('price')
        objects_color = Color.objects.values_list('color', flat=True)[:5]
        objects_size = Size.objects.values_list('symbol', flat=True)[:5]

        # paginator
        paginator = Paginator(objects, 9)
        page_number = request.GET.get('page')
        page_objects = paginator.get_page(page_number)
        messages.success(request,
                         f"category => {category} / price => {price} / color => {color} / size => {size} /")

        context = {
            'shop': shop,
            'one': one,
            'two': two,

            'objects_price': objects_price,
            'objects_color': objects_color,
            'objects_size': objects_size,

            'page_obj': page_objects,
            'paginator': paginator,
        }
    else:
        objects = Product.objects.filter(status=Status.Published)

        objects_price = AveragePrice.objects.values_list('price', flat=True).order_by('price')
        objects_color = Color.objects.values_list('color', flat=True)[:5]
        objects_size = Size.objects.values_list('symbol', flat=True)[:5]
        # paginator
        paginator = Paginator(objects, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        messages.success(request, "If you are not registered, the contest will not work !")

        context = {
            'shop': 'active',
            'objects_price': objects_price,
            'objects_color': objects_color,
            'objects_size': objects_size,
            'page_obj': page_obj,
            'paginator': paginator,
        }

    return render(request, 'shop.html', context)


def get_detail(request, slug, idd):
    object = Product.objects.filter(Q(status=Status.Published)).get(id=idd)
    objects = Product.objects.filter(Q(status=Status.Published) & Q(slug=slug))
    comments = Comment.objects.filter(Q(active=True) & Q(product__slug=slug))
    colors = Product.objects.filter(Q(status=Status.Published) & Q(slug=slug)).values_list('color__color', flat=True)
    sizes = Product.objects.filter(Q(status=Status.Published) & Q(slug=slug)).values_list('size__symbol', flat=True)
    com_count = comments.count()

    context = {
        'detail': 'active',
        'comments': comments,
        'com_count': com_count,
        'objects': objects,
        'object': object,
        'colors': colors,
        'sizes': sizes,
    }
    return render(request, 'detail.html', context)


def save_comment(request, slug, idd):
    object = Product.objects.filter(Q(status=Status.Published) & Q(slug=slug)).get(id=idd)
    if request.method == 'POST' and request.user.is_authenticated:
        print('POST')
        if request.POST['review']:
            comment = request.POST['review']
            star = request.POST['star']
            user = Customer.objects.get(id=request.user.id)
            Comment.objects.create(customer=user, product=object, body=comment, star=star)
    else:
        pass
    return redirect(f"/detail/{slug}/{idd}")


def save_product(request):
    slug = request.POST['slug']
    idd = request.POST['idd']
    if request.user.is_authenticated:
        if request.method == 'POST':
            price = int(request.POST['price'])
            size = request.POST['size']
            color = request.POST['color']
            number = int(request.POST['number'])
            product = request.POST['product']
            product_name = request.POST['product_name']

            summ = price * number
            messages.success(request, "Product added")

            Cart.objects.create(customer=request.user.id, customer_name=request.user.username, product=product,
                                product_name=product_name, price=price,
                                size=size, color=color, number=number, summ=summ)

    else:
        messages.success(request, "You are not registered")
    return redirect(f"/detail/{slug}/{idd}")


def remove_product(request, idd):
    delete = Cart.objects.get(id=idd)
    delete.delete()
    return redirect('cart_page')


def get_cart(request):
    context = {
        'cart': 'active'
    }
    if request.user.is_authenticated:
        context['objects'] = Cart.objects.filter(customer=request.user.id)
        context['sum_commont'] = sum(Cart.objects.values_list('summ', flat=True))

    return render(request, 'cart.html', context)


def get_checkout(request):
    context = {
        'checkout': 'active'
    }
    if request.user.is_authenticated:

        objects = Cart.objects.filter(customer=request.user.id)

        context['objects'] = objects
        context['sum_common'] = sum(Cart.objects.values_list('summ', flat=True))
        context['sum_product'] = sum(Cart.objects.values_list('price', flat=True))

        if objects:
            objectid = list()
            for obj in objects:
                objectid.append(obj.id)
            context['objects_id'] = objectid

    return render(request, 'checkout.html', context)


def get_payment(request):
    if request.method == 'POST':

        objects = Cart.objects.filter(customer=request.user.id)  # .product

        payment_method = request.POST['payment']
        country = request.POST['country']
        city = request.POST['city']
        street = request.POST['street']
        house_number = request.POST['house_number']
        for pr in objects:
            Activated.objects.create(customer=request.user.id, customer_name=pr.customer_name, product=pr.product,
                                     product_name=pr.product_name,
                                     country=country, city=city, street=street, house_number=house_number,
                                     payment_method=payment_method)
            Purchased.objects.create(customer=request.user.id, customer_name=pr.customer_name, product=pr.product,
                                     product_name=pr.product_name)
            pr.delete()
        print(payment_method)
    return redirect('home_page')
