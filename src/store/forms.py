from django import forms
from .models import Product

CSS_CLASS = "w-full px-4 py-2 rounded-xl text-lg md:text-xl outline-none focus:ring-1 focus:ring-indigo-600 mb-6 block"


class ProductForm(forms.ModelForm):

    # slug , vendor
    class Meta:
        model = Product
        fields = ["category", "name", "price", "description", "image",]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add label here
        self.fields["name"].widget.attrs["placeholder"] = "Enter Product Name Here...."
        self.fields["price"].widget.attrs["placeholder"] = "Enter Product Price Here...."
        self.fields["description"].widget.attrs["placeholder"] = "Enter Product Description Here...."
        
        # add empty label here
        self.fields['category'].empty_label = "---Select Category---"
       
        # customize description rows and cols here
        self.fields["description"].widget.attrs["rows"] = 8
        self.fields["description"].widget.attrs["cols"] = 10

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = CSS_CLASS
