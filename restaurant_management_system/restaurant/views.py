from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Table, Order, Reservation

def restaurant_home(request):
    menu_items = MenuItem.objects.all()
    tables = Table.objects.all()
    return render(request, 'restaurant/home.html', {
        'menu_items': menu_items,
        'tables': tables
    })

def place_order(request):
    if request.method == 'POST':
        table_id = request.POST.get('table_id')
        item_ids = request.POST.getlist('items')

        table = get_object_or_404(Table, id=table_id)
        order = Order.objects.create(table=table)

        total = 0
        for item_id in item_ids:
            item = MenuItem.objects.get(id=item_id)
            if item.stock_quantity > 0:
                order.items.add(item)
                item.stock_quantity -= 1 # Inventory Logic
                item.save()
                total += item.price

        order.total_price = total
        order.save()
        return render(request, 'restaurant/order_success.html', {'order': order})
    return redirect('restaurant_home')
