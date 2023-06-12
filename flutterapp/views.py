# from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes
# from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
# from segno import QRCode
from .models import Cylinder, OrderItem, Order, OrderInfo, Rating, Payment, AddressInfo
from .serializers import *
# Create your views here.
# from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt


# @authentication_classes([SessionAuthentication, TokenAuthentication])
@api_view(['GET',])
@permission_classes([AllowAny])
# @csrf_exempt
def products(request, pk=None):
    print(request.data)
    if pk == None:
        queryset = Cylinder.objects.all()
        serializer = CylinderSerializer(queryset, many = True)
        return Response(serializer.data)

        # data = Cylinder.objects.all()
        # data = list(data.values())
        # print(data)
        # return Response(data)
    else:

        queryset = Cylinder.objects.get(id=pk)
        serializer = CylinderSerializer(queryset)
        return Response(serializer.data)

# @api_view(['GET'])  # Add the API view decorator to specify allowed methods
# @permission_classes([AllowAny])  # Add the permission classes to allow any user
# @csrf_exempt  # Add the CSRF exemption to disable CSRF protection
# class ProductListView(ListAPIView):
#     queryset = Cylinder.objects.all()
#     serializer_class = CylinderSerializer

# @api_view(['GET'])  # Add the API view decorator to specify allowed methods
# @permission_classes([AllowAny])  # Add the permission classes to allow any user
# @csrf_exempt  # Add the CSRF exemption to disable CSRF protection
# def products(request, pk):
#     queryset = Cylinder.objects.filter(pk=pk)
#     serializer = CylinderSerializer(queryset, many=True)
#     return Response(serializer.data)

# from django.http import JsonResponse

# def search_products(request):
#     search = request.GET['search']
    
#     size = request.GET['size']

#     price = request.GET['price']

#     print(search, size, price)

#     # Construct the initial queryset
#     queryset = Cylinder.objects.all()



#     # Filter the queryset based on the parameters
#     if search != 'null':
#         queryset = queryset.filter(name__icontains=search)
#     if size != 'null':
#         queryset = queryset.filter(size=size)
#     if price != 'null': 
#         queryset = queryset.filter(price=price)

#     # Retrieve all products if all parameters are null
#     if not search and not size and not price:
#         queryset = Cylinder.objects.all()

#     # Do something with the filtered queryset
#     # ...

#     # Return a JSON response
#     response_data = {
#         'message': 'Success',
#         'products': list(queryset.values()),
#     }
#     return JsonResponse(response_data)

# @permission_classes([IsAuthenticated])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @api_view(['GET', 'POST'])
# @csrf_exempt
# def cart(request):
#     print(request.data)
#     return Response(f"I received data as: {request.data}")

# @permission_classes([IsAuthenticated])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @api_view(['GET', 'POST'])
# @csrf_exempt
# def checkout(request):
#     print(request.data)
#     print(request.user)
#     return Response(f"You are user: {request.user}")


# @permission_classes([IsAuthenticated])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @api_view(['GET', 'POST'])
# @csrf_exempt
# def address(request):
#     print(request.data)
#     print(request.user)
#     return Response(f"You are user: {request.user} and address {request.data}")

@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@api_view(['GET', 'POST'])
@csrf_exempt
def distributor(request):
    print(request.data)
    
    queryset = Distributor.objects.all()
    serializer = DistributorSerializer(queryset, many = True)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@api_view(['GET', 'POST'])
@csrf_exempt
def order(request, pk=None):
    if request.method == "POST":
        print(request.data)
        user = request.user
        order = Order.objects.create(user=user)
        print(order)

        dist_id = request.data.get('dis_id')
        distributor = Distributor.objects.get(id = dist_id)
        cart = request.data.get('cart')
        print("CART IS", cart)
        
        address = request.data.get('address')
        address = f"{address['houseNo']} {address['area'], {address['city']}}"
        total_quantity = 0
        total_price = 0
        for item in cart:
            cylinder = Cylinder.objects.get(id=item['id'])
            quantity = item['quantity']
            price = item['price']
            total_quantity += quantity
            total_price += price

            OrderItem.objects.create(order=order, cylinder=cylinder, quantity=quantity, price = price)
        OrderInfo.objects.create(order=order, status='Pending', distributor= distributor,total_price=total_price, total_items_qty=total_quantity, address=address)

        payment_type = request.data.get('type')
        if payment_type == 'COD':
            transaction_id = None
        else:
            transaction_id=78
        amount = 20
        Payment.objects.create(order=order, transaction_id=transaction_id, payment_method = payment_type, amount = total_price)
    # Generate the QR code based on the order information
        qr_code_data = f"Order ID: {order.id}, Total Quantity: {total_quantity}, Total Amount: {total_price}"  # Customize the QR code data as per your requirement
        qr_code_image = generate_qr_code(qr_code_data)

        # Convert the QR code image to base64 string
        qr_code_base64 = qr_code_image.decode("utf-8")
        order_of_user = Order.objects.filter(user=user)
        recent_order = order_of_user.last()

        # Pass the QR code base64 string to the frontend
        return Response({'data': recent_order,'cart':cart, 'qr_code': qr_code_base64})
    if request.method == "GET":
        queryset1 = OrderInfo.objects.get(order=pk)
        serializer1 = OrderInfoSerializer(queryset1, many=True)
        queryset2 = OrderItem.objects.get(order=pk)
        serializer2 = OrderItemSerializer(queryset2, many=True)
        return Response({'order_info':serializer1.data, 'order_item':serializer2.data})
        
    # queryset = Distributor.objects.all()
    # serializer = DistributorSerializer(queryset, many = True)
    # return Response(request.data)

@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@api_view(['GET'])
@csrf_exempt
def history(request):
    user = request.user
    print(user, user.pk)
    
    history = {}
    for order in Order.objects.filter(user=user):
        order_items = []
        total_items_qty = 0
        total_price = 0
        for item in OrderItem.objects.filter(order=order):
            order_items.append({'name': item.cylinder.name, 'quantity': item.quantity})
            total_items_qty += item.quantity
            total_price += item.price
        if order.orderinfo_set.exists():
            order_info = {'id': order.id, 'date': order.orderinfo_set.first().date,
                          'status': order.orderinfo_set.first().status,
                          'total_items_qty': total_items_qty }
            # if order_info['status'] == 'Delivered':
            #     history['completed'].append(order_info)
            # else:
            #     history['pending'].append(order_info)
        # else:
        #     order_info = {'id': order.id, 'status': 'Pending',
        #                   'items': order_items,'date': order.orderinfo_set.first().date, 
        #                   'total_items_qty': total_items_qty, 'total_price': total_price}
        #     history['pending'].append(order_info)

    # # Retrieve all orders for the user
    # orders = Order.objects.filter(user=user)

    # order_history = []
    # print("ORDERS", orders)
    # for order in orders:
    #     print("ORDER", order)
    #     order_info = OrderInfo.objects.get(order=order)
    #     print("ORDERINFO", order_info)
    #     order_items = OrderItem.objects.filter(order=order.pk)
        
    #     order_data = {
    #         'order_info': order_info,
    #         'order_items': order_items
    #     }
    #     order_history.append(order_data)

    # Perform any additional processing or serialization as needed
    # ...

    return Response(history)
    # queryset = OrderInfo.objects.filter(order=Order.objects.filter(user=user.pk))
    # print(queryset)
    # serializer = OrderInfoSerializer(queryset, many = True)
    # print(serializer.data)

    
    # return Response(serializer.data)

    
    # queryset = Distributor.objects.all()
    # serializer = DistributorSerializer(queryset, many = True)
    # return Response(serializer.data)



import qr_code
from qr_code.qrcode.utils import QRCodeOptions
def generate_qr_code(data):
    my_options=QRCodeOptions(size='t', border=6, error_correction='L')  
    qr_code_image = qr_code.qrcode.maker.make_qr_code_image(data=data, qr_code_options=my_options)
    print(qr_code_image)
    return qr_code_image

