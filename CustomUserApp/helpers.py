from django.core.mail import send_mail
from django.conf import settings
from xhtml2pdf import pisa # type: ignore
from django.http import HttpResponse
from io import BytesIO
def mail(subject,message,email_from,recipient_list):
    # html_message=render_to_string(message,'verification_mail.html')
    
    send_mail(subject,message,email_from,recipient_list)
    return True 


def generate_pdf(order_id,payment_id,name,item,price,quantity,order_date,total_price,invoice_number):
    html = '<html><body>'
    html += '<h1>Invoice</h1>'
    html += '<p>Company Name: ' + 'EZ Cart '+ '</p>'
    html += '<p>Invoice Number: ' + invoice_number + '</p>'
    html += '<p>Order Date: ' + order_date + '</p>'
    html += '<p>Customer Name: ' + name + '</p>'
    html += '<p> Order Id : ' + order_id + '</p>'
    html += '<p> Payment Id : ' + payment_id + '</p>'
    html += '<h2>Product Details</h2>'
    html += '<p> Product Name :' + item + '</p>'
    html += '<p> Price : ' + price + '</p>'
    html += '<p> Quantity : ' + quantity + '</p>'
    html += '<p> Total Price :' + total_price + '</p>'
    html += '</body></html>'
    result = pisa.CreatePDF(html, dest=BytesIO())
    return result





















# def verification_mail(email,token,uid,message,subject):
#     subject='Email Verification Link'
#     message=f'Hi, Click on the link to verify your mail http://127.0.0.1:8000/CustomUserApp/activate/{uid}/{token}/ '
#     # html_message=render_to_string(message,'verification_mail.html')
#     email_from=settings.EMAIL_HOST_USER
#     recipient_list=[email]
#     send_mail(subject,message,email_from,recipient_list)
#     return True 