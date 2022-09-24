from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
from numpy import loadtxt
from tensorflow import keras
from keras.models import load_model
from keras.preprocessing import image
import os
import time
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import numpy as np


# load and evaluate a saved model 
# load model
model = load_model('model.h5')
# summarize model.
model.summary()

#convert the predicted and actual test values back to their associated labels
def class_convert(classess):
    pred=[]
    for i in classess:
        if i ==0:
            pred.append('Cardboard')
        elif i==1:
            pred.append('Glass')
        elif i==2:
            pred.append('Metal')
        elif i==3:
            pred.append('Paper')
        elif i==4:
            pred.append('Plastic')
        elif i==5:
            pred.append('Trash')
    return pred

def classify_image(my_image):
  custom_image = keras.utils.load_img(my_image, target_size=(224, 224))
  img_array = keras.utils.img_to_array(custom_image)
  processed_img = keras.applications.xception.preprocess_input(img_array).astype(np.float32)
  swapped = np.moveaxis(processed_img, 0,1) 
  arr4d = np.expand_dims(swapped, 0)
  new_prediction= class_convert(np.argmax(model.predict(arr4d), axis = -1))
  try:
    os.remove(my_image)
  except OSError:
    pass
  return {"item":new_prediction[0], 'recyclable': 'no' if new_prediction[0] == 'Trash' else 'yes'}

# Create your views here.
def index(request):
    return render(request, 'main.html', {'message':"Done"})

@csrf_exempt
def image_classification(request):
    try:
        image = request.FILES["pictureFile"] 
        name = image.name
        path = default_storage.save(f'{time.time()}_{name}', ContentFile(image.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        if image:
            return JsonResponse(classify_image(tmp_file), status=200)  
        else:
            return JsonResponse({'status':'False','message':'No Image sent'}, status=400) 
    except Exception as e:
        return JsonResponse({"data":'error', "msg":str(e)}, status=404)