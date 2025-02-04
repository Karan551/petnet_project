from django import forms
from .models import Product, Order

CSS_CLASS = "w-full px-4 py-2 rounded-xl text-lg md:text-xl outline-none focus:ring-1 focus:ring-indigo-600 mb-6 block"


class ProductForm(forms.ModelForm):

    # slug , vendor
    class Meta:
        model = Product
        fields = ["category", "name", "price", "description", "image",]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

       
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


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ["first_name", "last_name", "contact_number",
                  "email_address", "city", "zipcode", "address", ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # customize placeholder
        self.fields["first_name"].widget.attrs["placeholder"] = "Enter First Name Here...."
        
        self.fields["last_name"].widget.attrs["placeholder"] = "Enter Last Name Here...."
        
        self.fields["contact_number"].widget.attrs["placeholder"] = "Enter Contact Number Here...."
        
        self.fields["email_address"].widget.attrs["placeholder"] = "Enter Email Address Here...."
        
        self.fields["city"].widget.attrs["placeholder"] = "Enter Your City Here...."
        
        self.fields["zipcode"].widget.attrs["placeholder"] = "Enter Zipcode Here...."
        self.fields["address"].widget.attrs["placeholder"] = "Enter Full Address Here...."
        

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = CSS_CLASS
