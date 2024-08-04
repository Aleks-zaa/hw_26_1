import stripe
from config.settings import STRIPE_API_KEY


stripe.api_key = STRIPE_API_KEY


def create_stripe_product(payment):
    """Создаем stripe продукт."""

    title_product = payment.paid_course if payment.paid_course else payment.paid_lesson
    stripe_product = stripe.Product.create(name=title_product)
    return stripe_product.get('id')


def create_stripe_price(product_id, payment):
    """ Создает цену в страйпе. """

    price = stripe.Price.create(
        currency="RUB",
        unit_amount=payment.payment_sum * 100,
        product=product_id,
    )
    return price.id


def create_stripe_session(price_id):
    """ Создает сессию На оплату в страйпе. """

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')
