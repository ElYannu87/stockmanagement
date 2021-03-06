from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from django.contrib import messages
from .models import Stock
from .form import StockCreateForm, StockSearchForm, StockUpdateForm, IssueForm, ReceiveForm

# Create your views here.


def home(request):
    title = 'Welcome to the placeholder'
    context = {
        "title": title,
    }
    return render(request, "home.html", context)


def list_item(request):
    header = 'Stocks'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        "header": header,
        "queryset": queryset,
        "form": form,
    }
    if request.method == 'POST':
        queryset = Stock.objects.filter(#category__icontains=form['category'].value(),
                                        item_name__icontains=form['item_name'].value()
                                        )
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachelent; filename="Liste des stocks.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORIE', 'NOM', 'QUANTITE'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
                return response
        context = {
            "form": form,
            "header": header,
            "queryset": queryset,
        }
    return render(request, "list_item.html", context)


def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Sauvegarde réussie')
        return redirect('/list_item')
    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, "add_items.html", context)


def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            return redirect('/list_item')

    context = {
        "form": form
    }
    return render(request, 'add_items.html', context)


def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Supression réussie')
        return redirect('/list_item')
    return render(request, 'delete_items.html')


def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "queryset": queryset,
    }
    return render(request, "stock_detail.html", context)


def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity -= instance.issue_quantity
        messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) 
                         + " " + str(instance.item_name) + "s now left in Store")
        instance.save()

        return redirect('/stock_detail/' + str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": 'Issue' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": 'Issue By: ' +str(request.user)
    }
    return render(request, "add_items.html", context)

def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity += instance.receive_quantity
        instance.save()
        messages.success(request, "Received SUCCESSFULLY" + str(instance.quantity) 
                         + " " + str(instance.item_name) +"s now in Store")
        return redirect('/stock_detail/' + str(instance.id))

    context = {
        "title": 'Receive ' + str(queryset.item_name),
        "instance" : queryset,
        "form" : form,
        "username" : 'Receive By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)
