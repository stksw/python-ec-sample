from django.shortcuts import redirect
from django.views.generic import View, TemplateView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from base.models import Item
import stripe

stripe.api_key = settings.STRIPE_API_SECRET_KEY

class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/success.html'

    def get(self, request, *args, **kwargs):
        # 
        # セッション変数のカートを削除
        del request.session['cart']
        return super().get(request, *args, **kwargs)

class PaymentCancelView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/cancel.html'

    # *argsはタプル型の引数, **kwargsは辞書型のキーワード引数
    def get(self, request, *args, **kwargs):
        # Orderオブジェクトを取得
        # 在庫数と販売数を戻す
        # is_confirmedがFalseであれば削除
        return super().get(request, *args, **kwargs)

class PaymentWithStripe(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not check_profile_filled(request.user.profile):
            return redirect('/profile/')
        
        cart = request.session.get('cart', None)
        if cart is not None or len(cart) == 0:
          return redirect('/')

        line_items = []
        for item_pk, quantity in cart['items'].items():
            item = Item.objects.get(pk=item_pk)
            line_item = create_line_item(item.price, item.name, quantity)
            line_items.append(line_item)

        checkout_session = stripe.checkout.Session.create(
            # customer_email = request.user.email,
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=f'{settings.BASE_URL}/payment/success/',
            cancel_url=f'{settings.BASE_URL}/payment/cancel',
        )
        return redirect(checkout_session.url)

tax_rate = stripe.TaxRate.create(
    display_name = '消費税',
    description = '消費税',
    country = 'JP',
    jurisdiction = 'JP',
    percentage = settings.TAX_RATE * 100,
    inclusive=False,
)

def check_profile_filled(profile):
    if profile.name is None or profile.name == '':
        return False
    elif profile.zipcode is None or profile.zipcode == '':
        return False
    elif profile.city is None or profile.city == '':
        return False
    elif profile.address1 is None or profile.address1 == '':
        return False
    return True


def create_line_item(price, name, quantity):
    return {
        'price_data': {
            'currency': 'JPY',
            'unit_amount': price,
            'product_data': { 'name': name },
        },
        'quantity': quantity,
        'tax_rates': [tax_rate.id],
    }
