from django.db.models import Q
from .models import Product, Status, Category, Cart, Purchased


def get_context(request):
    obj = Product.objects.filter(status=Status.Published).first()
    categs = Category.objects.all()
    count_product = Cart.objects.filter(customer=request.user.id).count()
    count_comment = Purchased.objects.filter(customer=request.user.id).count()
    context = {
        'obj': obj,
        'star': '12345',
        'categs': categs,
        'count_product': count_product,
        'count_comment': count_comment,
    }
    return context
