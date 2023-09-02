from django.urls import path
from .views import *


urlpatterns = [
        path("", index, name='index'),
        path('ocr', ocr, name='ocr'),
        path('upload_img', upload_img),
        path('search_name', search_name, name='search_name'),
        path('get_document/<int:roll>', get_document_id, name='get_document'),
        path('save_document', save_document, name='save_document'),
        path('reset_camera', index, name='reset_camera'),
        path('save_image', save_image, name='save_image')

]
