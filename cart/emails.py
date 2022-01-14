from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def notify_vendor(order_item):
    vendor = order_item.vendor 
    
    from_email = settings.DEFAULT_EMAIL_FROM
    to_email = order_item.vendor.created_by.email
    subject = 'New order'
    text_content = 'You have a new order!'
    html_content = render_to_string('cart/email_notify_vendor.html', {'order': order_item, 'vendor': vendor})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def notify_customer(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    to_email = order.user.email
    subject = 'Order confirmation'
    text_content = 'Thank you for the order!'
    html_content = render_to_string('cart/email_notify_customer.html', {'order': order})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()