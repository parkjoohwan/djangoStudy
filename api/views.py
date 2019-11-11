from django.shortcuts import *
from django.http import *
from django.views.generic import View
from django.conf import settings


from .models import Image
from .forms import ImageForm


import glob, numpy as np
from PIL import Image as pil
import tensorflow as tf
import os


modelPath = os.path.dirname(os.path.abspath(__file__)) + "/model/cat_dog_calssification.h5"
model = tf.keras.models.load_model(modelPath)

class testapi(View):
    def get(self, request):
        return HttpResponse("Class get")
    

# file upload
class upload_file(View):
    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        newimage = Image(imagefile=request.FILES['imagefile'])
        newimage.save()

        return HttpResponseRedirect('uploadimage')

    def get(self, request):
        form = ImageForm()
        images = Image.objects.all()

        return render(request, 'upload_image.html', {'images': images, 'form': form})
    
    
    
class predict(View):
    def imgToRgb(self, file):
        img = pil.open(file)
        img = img.convert("RGB")
        img = img.resize((256, 256))
        return np.asarray(img, dtype=np.float)  

    def result(self, pre_ans, filename):
        if pre_ans == 0:
            ret = "해당 " + filename.split("/")[-1] + "이미지는 고양이 사진으로 추정됩니다."
        elif pre_ans == 1:
            ret = "해당 " + filename.split("/")[-1] + "이미지는 강아지 사진으로 추정됩니다."
        return ret

    def get(self, request):
        testImagePath = settings.BASE_DIR + request.GET["image_url"]

        X = []
        filenames = []

        files = glob.glob(testImagePath)
        for i, f in enumerate(files):
            filenames.append(f)
            X.append(self.imgToRgb(f))

        X = np.array(X)

        prediction = model.predict(X)
        np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
        cnt = 0

        response = []

        for i in prediction:
            pre_ans = i.argmax() 
            response.append(self.result(pre_ans, filenames[cnt]))
            cnt += 1

        return JsonResponse(
            {
                'Api Name': 'Predict'
                , 'Result': response
                , 'DirPath': os.path.dirname(os.path.abspath(__file__))
                , 'testImagePath': testImagePath
                , 'modelPath': modelPath

                , 'prediction': prediction.tolist()
            }
            , json_dumps_params={'ensure_ascii': False, 'indent': 4})