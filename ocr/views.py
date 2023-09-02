
from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, HttpResponse, FileResponse
from django.views.decorators import gzip
import os
import time
from PIL import Image
from pythainlp.tokenize import word_tokenize
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
from pythainlp.tag import named_entity
from pythainlp import *
import requests
import numpy as np
import json
import base64
from django.conf import settings
from django.http import JsonResponse
from .forms import ImageUploadForm
import numpy as np
from django.core.files.storage import FileSystemStorage
import re
from pythainlp.tag import NER, NNER
from pymongo import MongoClient
from django.conf import settings
from .models import *
from fuzzywuzzy import fuzz, process
import datetime
import json
from bson import ObjectId
from .models import *
from django.contrib.auth.decorators import login_required
import difflib
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from pytesseract import *






@login_required(login_url='../project/login/')
def index(request, *args, **kwargs):


    image = ''
    

    return render(request, 'index.html', {'image': image})
    



        
                

def upload_img(request):
    media_path = os.path.join(settings.MEDIA_ROOT, 'capture.jpg')
   

    if request.method == 'POST':
        if os.path.exists(media_path):
            os.remove(media_path)
        upload_image = request.FILES.get('file_image')
    
    
        if upload_image:
            fs = FileSystemStorage()
            filename = fs.save("capture.jpg",upload_image)
            request.session['file_image'] = filename
            with open(media_path, 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            # return render(request, 'index.html', {'encoded_image': encoded_image})
            return HttpResponse(encoded_image)
            

        # return render(request, 'index.html')
        return HttpResponse()





    
   

        

def capture(request):
    media_path = os.path.join(settings.MEDIA_ROOT , 'capture.jpg')
    if os.path.exists(media_path):
        with open(media_path, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            return render(request, 'index.html', {'encoded_image': encoded_image})
        
    else:
        return render(request, 'index.html')
    




            

def save_image(request):
    if request.method == 'POST':
        print('save')
        image_data = request.POST.get('image_data')  # This should contain the data URL of the image
        if image_data:
            # Remove the "data:image/png;base64," prefix
            image_data = image_data.replace('data:image/png;base64,', '')

            # Decode base64 image data and save it
            image_data = image_data.encode()
            with open(os.path.join(settings.MEDIA_ROOT, 'capture.jpg'), 'wb') as f:
                f.write(base64.b64decode(image_data))

            return JsonResponse({'success': True})

    return JsonResponse({'success': False})
   
    




# def ocr(request):
#     media_path = os.path.join(settings.MEDIA_ROOT, 'capture.jpg')
#     ocr_path = os.path.join(settings.OCR_ROOT, 'tessdata_best-main')
#     if os.path.exists(media_path):
#         with PyTessBaseAPI(path=ocr_path,lang='tha+eng') as api:
#             api.SetImageFile(media_path)
#             text = api.GetUTF8Text()
#             conf = api.AllWordConfidences()
#             print(text)
#             name = os.path.join(settings.NER_ROOT, 'thainer-corpus-v2-base-model')
#             tokenizer = AutoTokenizer.from_pretrained(name)
#             model = AutoModelForTokenClassification.from_pretrained(name)

#             if len(text) > 512:
#                 text = text[:512]

    

#             sentence = f'{text}'
            
#             formatted_content = re.sub(r'\s+', ' ', text).strip()

#             print(formatted_content)
        
            

            

#             cut=word_tokenize(formatted_content.replace(" ", "<_>"))
#             inputs=tokenizer(cut,is_split_into_words=True,return_tensors="pt")

#             ids = inputs["input_ids"]
#             mask = inputs["attention_mask"]
#             # forward pass
#             outputs = model(ids, attention_mask=mask)
#             logits = outputs[0]

#             predictions = torch.argmax(logits, dim=2)
#             predicted_token_class = [model.config.id2label[t.item()] for t in predictions[0]]

#             def fix_span_error(words,ner):
#                 _ner = []
#                 _ner=ner
#                 _new_tag=[]
#                 for i,j in zip(words,_ner):
#                     #print(i,j)
#                     i=tokenizer.decode(i)
#                     if i.isspace() and j.startswith("B-"):
#                         j="O"
#                     if i=='' or i=='<s>' or i=='</s>':
#                         continue
#                     if i=="<_>":
#                         i=" "
#                     _new_tag.append((i,j))
#                 return _new_tag

#             ner_tag=fix_span_error(inputs['input_ids'][0],predicted_token_class)
#             print(ner_tag)

#             merged_ner=[]
#             for i in ner_tag:
#                 if i[1].startswith("B-"):
#                     merged_ner.append(i)
#                 elif i[1].startswith("I-"):
#                     merged_ner[-1]=(merged_ner[-1][0]+i[0],merged_ner[-1][1])
#                 else:
#                     merged_ner.append(i)

#             print(merged_ner)

#             #display only entity of person  name
#             person = []
#             _pharse = []
#             for i in merged_ner:
#                 if i[1].startswith("B-PERSON") and i[0] != ' ' and len(i[0]) > 5 :
#                     _pharse.append(i)
#                     person.append(i[0])

#             print(person)
#             print(_pharse)

#             if len(person) == 2:
#                 print('ผู้ส่ง :',person[0]),print('ผู้รับ :',person[1])
#                 return JsonResponse({'tag1': person[0], 'tag': person[1], 'text': formatted_content}, status=200)

#             elif len(person) > 2:
#                 # print('ผู้ส่ง :',person[0]),print('ผู้รับ :',person[1]+person[2])
#                 for i in range(2,len(person)):
#                     person[1] = person[1] + person[i]
#                 print('ผู้ส่ง :',person[0]),print('ผู้รับ :',person[1])
#                 return JsonResponse({'tag1': person[0], 'tag': person[1], 'text': formatted_content}, status=200)
#             else :
#                 return JsonResponse({'tag1': 'ไม่พบข้อมูล', 'tag': 'ไม่พบข้อมูล','tex' : formatted_content}, status=200)
            
            
#     return HttpResponse(status=200)

_engine = NER(engine="thainer-v2", corpus="thainer")

def get_person_names(text):
    formatted_content = re.sub(r'\s+', ' ', text).strip()
    ner_tag = _engine.tag(formatted_content)
    merged_ner = []
    print(ner_tag)

    for i in ner_tag:
        if i[1].startswith("B-"):
            merged_ner.append(i)
        elif i[1].startswith("I-"):
            merged_ner[-1] = (merged_ner[-1][0] + i[0], merged_ner[-1][1])
        else:
            merged_ner.append(i)

    person = []
    _pharse = []
    

    # for i in merged_ner:
    #     if i[1].startswith("B-PERSON") and i[0] != ' ' and len(i[0]) > 5:
    #         _pharse.append(i)
    #         person.append(i[0])
    #         #remove prefix in person name
    #         for j in prefix:
    #             if j in person[0]:
    #                 person[0] = person[0].replace(j,'')
    #                 person[0] = person[0].strip()


    for i in merged_ner:
        if i[1].startswith("B-PERSON") and i[0] != ' ' and len(i[0]) > 5:
            _pharse.append(i)
            person.append(i[0])

            
    



    return person



def ocr(request):
    media_path = os.path.join(settings.MEDIA_ROOT, 'capture.jpg')
    ocr_path = os.path.join(settings.OCR_ROOT, 'tessdata_best-main')
    tesseract_path = os.path.join(settings.OCR_ROOT, 'Tesseract-OCR')
    pytesseract.pytesseract.tesseract_cmd = os.path.join(tesseract_path, 'tesseract.exe')

    if os.path.exists(media_path):
            custom_oem_psm_config = r'--oem 3 --psm 6'
            tessdata_dir_config = f'--tessdata-dir {ocr_path}'
            text = image_to_string(media_path,lang='tha+eng',config=custom_oem_psm_config+''+tessdata_dir_config)
            print(text)


            person_names = get_person_names(text)

            if len(person_names) == 0:

                
                return JsonResponse({'tag1': 'ไม่พบข้อมูล', 'tag': 'ไม่พบข้อมูล', 'text': _engine.tag(text,tag=True)}, status=200)

            elif len(person_names) == 1:
                #sender, receiver = person_names[0], person_names[0]
                person = person_names[0]
                person = remove_prefix(person)
                sender, receiver = person, person

            elif len(person_names) == 2:
                #sender, receiver = person_names[0], person_names[1]
                sender = remove_prefix(person_names[0])
                receiver = remove_prefix(person_names[1])
            else:
                #sender, receiver = person_names[0], ' '.join(person_names[1:])
                sender = remove_prefix(person_names[0])
                receiver = remove_prefix(' '.join(person_names[1:]))

            print('ผู้ส่ง:', sender)
            print('ผู้รับ:', receiver)

            os.remove(media_path)

        
            return JsonResponse({'tag1': sender, 'tag': receiver, 'text': _engine.tag(text,tag=True)}, status=200)

    else:
        return JsonResponse({'tag1': 'ไม่พบข้อมูล', 'tag': 'ไม่พบข้อมูล', 'tex': _engine.tag(text,tag=True)}, status=200)
    

def remove_prefix(person):
    prefixs = ['นาย', 'นาง', 'นางสาว']
    

    best_match_position = -1
    best_match_ratio = 0 
    for i, p in enumerate(prefixs):
        match = difflib.SequenceMatcher(None, p, person).find_longest_match(0, len(p), 0, len(person))
        if match.size > best_match_ratio:
            best_match_position = match.b
            best_match_ratio = match.size  
    if best_match_position >= 0:
        person = person[:best_match_position] + person[best_match_position + best_match_ratio:]

    return person


def search_name(request):

    




    if request.method == 'POST':
        search_string = request.POST.get('tag')
        text = request.POST.get('text')
        

        search_string_parts = search_string.split(' ')
        if len(search_string_parts) >= 2:
            search_string_firstname = search_string_parts[0]
            search_string_lastname = ' '.join(search_string_parts[1:])
        else:
            search_string_firstname = search_string
            search_string_lastname = ''

        print('fname=>', search_string_firstname)
        print('lname=>', search_string_lastname)

        client = MongoClient(settings.MONGODB_URI)
        db = client[settings.MONGODB_NAME]

        data_firstname = []
        data_lastname = []

        # Use index to improve query performance
        results = db['project_users'].find({}, {'firstname': 1, 'last_name': 1})
        matching_data_firstname = []
        confidence_threshold = 60
        for document in results:
            data_firstname.append(document['firstname'])
            data_lastname.append(document['last_name'])

        for i in range(len(data_firstname)):
            
            confidence = fuzz.ratio(search_string_firstname, data_firstname[i])

            

            if confidence >= confidence_threshold:
                document = db['project_users'].find({'firstname': data_firstname[i]})
                print(document)

                for doc in document:
                    doc['confidence'] = confidence
                    matching_data_firstname.append(doc)

        matching_data_firstname.sort(key=lambda x: fuzz.ratio(search_string_firstname, x['firstname']), reverse=True)

        # Limit the number of results to improve performance
        matching_data_firstname = matching_data_firstname[:10]

        if len(matching_data_firstname) == 1:
            result = db['project_users'].find_one({'firstname': matching_data_firstname[0]['firstname']})
            print(result)

            context = {
                'result_parcels': result,
                'document': matching_data_firstname,
                'conf': confidence,
                'result': matching_data_firstname[0],
                'tag': search_string,
                'text': text
            }

            html_res = render(request, 'index.html', context)

            
            # return render(request, 'index.html', {'result_parcels': result, 'document': matching_data_firstname, 'conf': confidence, 'result': matching_data_firstname[0], 'tag': search_string})
            return html_res 
            

        elif len(matching_data_firstname) > 1:
            return render(request, 'index.html', {'result': matching_data_firstname, 'document': matching_data_firstname, 'conf': confidence, 'tag': search_string, 'text': text})
            

        else:
            return render(request, 'index.html', {'result': 'ไม่พบข้อมูล', 'document': ' ', 'conf': 'ไม่พบข้อมูล'})

        
            
        
            
        

            
            



def get_document_id(request, roll):
    if request.method == 'POST':
        client = MongoClient(settings.MONGODB_URI)
        db = client[settings.MONGODB_NAME]

        result = db['project_users'].find_one({'id': int(roll)}, {'_id': 0, 'firstname': 1, 'last_name': 1, 'room_num': 1})

        # if result:
        #     getfirstname = result['firstname']
        #     getlastname = result['last_name']
        #     getroom = result['room_num']

        #     media_path = os.path.join(settings.MEDIA_ROOT, 'capture.jpg')
        #     with open(media_path, 'rb') as f:
        #         data = f.read()
        #     encoded_string = base64.b64encode(data).decode('utf-8')

        return render(request, 'index.html', {'result_parcels': result})
    else:
        return render(request, 'index.html', {'result': 'ไม่พบข้อมูล'})






def save_document(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        last_name = request.POST.get('last_name')
        room_num = request.POST.get('room_num')
        status = request.POST.get('status')
        date = request.POST.get('dateInput')

        current_time = datetime.datetime.now()
        current_time = current_time.strftime(date+ f' {current_time.hour}:{current_time.minute}:{current_time.second}')

    
        

        d = Document(
            firstname=firstname,
            last_name=last_name,
            room_num=room_num,
            status=status,
            date=current_time
        )
        d.save()
        messages.success(request, 'บันทึกข้อมูลสำเร็จ')
        

        return render(request, 'index.html', {'result': 'บันทึกข้อมูลสำเร็จ'})

    return redirect('index')

            

    




    


    
