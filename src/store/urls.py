from django.urls import path
from . import views

app_name = "store"
urlpatterns = [
    path("search/", views.product_search, name="search"),
    path("category/<int:category_id>/",
         views.category_detail, name="category_detail"),

    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path("product/add-product/",views.add_product,name="add_product"),
    path("product/edit-product/<int:product_id>",views.edit_product,name="edit_product"),
    path("product/delete-product/<int:product_id>",views.delete_product,name="delete_product"),

]
