import json
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.models import Event, EventImage, Template, TemplateCategory
from api.remakerapi import remakerswapfaceapi

from django.core.files.base import ContentFile
import requests
import os


# Create your views here.
def home(request):
    return render(request,'home.html')



# @csrf_exempt
# def swapface(request):
#     if request.method == 'POST':
#         # Fetch the image files from the request
#         faceimage = request.FILES.get('face_image')
#         targetimage = request.FILES.get('target_image')
#         swapimageurl = remakerswapfaceapi(targetimage,faceimage)
#         if not faceimage or not targetimage:
#             return HttpResponse("Both images are required.", status=400)

#         # For now, return the target image directly as a placeholder
#         return JsonResponse({"image_url": swapimageurl})



@csrf_exempt
def swapface(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        faceimage = data.get('capturedimage').split(',')[1]
        templateid = data.get('templateid')
        
        targestimage = Template.objects.get(id=templateid).image
        if not faceimage or not targestimage:
            return HttpResponse("Both images are required.", status=400)
            
        swapimageurl = remakerswapfaceapi(targestimage, faceimage)
        
        try:
            response = requests.get(swapimageurl)
            response.raise_for_status()
            
            current_event = Event.objects.get(current=True)
            
            # Replace spaces with underscores in directory name
            event_name_clean = current_event.name.replace(" ", "_")
            base_dir = os.path.join(settings.MEDIA_ROOT, f"gallery/{event_name_clean}")
            
            # Create the directory if it doesn't exist
            os.makedirs(base_dir, exist_ok=True)
            
            # Get the count of existing images with same event and template
            base_name = f"swapped_face_{current_event.id}_{templateid}"
            existing_images = EventImage.objects.filter(
                event=current_event,
                image__startswith=f'gallery/{event_name_clean}/{base_name}'
            )
            
            # Find the next available number
            used_numbers = []
            for img in existing_images:
                filename = os.path.splitext(os.path.basename(img.image.name))[0]
                try:
                    num = int(filename.split('_')[-1])
                    used_numbers.append(num)
                except (ValueError, IndexError):
                    continue
            
            next_number = 1
            if used_numbers:
                next_number = max(used_numbers) + 1
            
            # Create the new image name with the next available number
            image_name = f"{base_name}_{next_number}.jpg"
            full_path = os.path.join(base_dir, image_name)
            
            # Save the file to the directory
            event_image = EventImage()
            event_image.event = current_event
            event_image.image.save(
                os.path.relpath(full_path, settings.MEDIA_ROOT),
                ContentFile(response.content),
                save=True
            )
            return JsonResponse({"image_url": event_image.image.url})
            
        except requests.RequestException as e:
            print(e)
            return JsonResponse({"error": str(e), "image_url": swapimageurl}, status=500)


def choose_template(request):
    cateogries = TemplateCategory.objects.all()
    return render(request,'choose_template.html',{'categories':cateogries})

def take_photo(request,id):
    templateimage = Template.objects.get(id = id).image.url
    return render(request,'take_photo.html',{'templateimage':templateimage,"templateid":id})

@csrf_exempt
def final_output(request):
    image = request.POST.get("image_url")
    # return render(request,'final_output.html',{'imageURL':"https://cdn.morfran.com/ApiMorfranCore/FaceSwap/MorfranFaceswap_2024_12_23_10_12_06_1163543.jpg"})
    return render(request,'final_output.html',{'imageURL':image})

def gettemplates(request):
    data = json.loads(request.body)
    categoryname = data.get('category')  
    category = TemplateCategory.objects.get(name = categoryname)
    templates = Template.objects.filter(category=category)
    templateslist = [[template.id, template.image.url] for template in templates]
    return JsonResponse({"templates": templateslist})


def manage_events(request):
    events = Event.objects.all()
    currentevent = Event.objects.filter(current=True).first()
    return render(request,'manage_events.html',{'events':events,'currentevent':currentevent})

@csrf_exempt
def change_current_event(request):
    event = Event.objects.get(name = json.loads(request.body).get('event'))
    Event.objects.all().update(current = False)
    event.current = True
    event.save()
    return JsonResponse({"status": "success"})
@csrf_exempt
def fetch_event_images(request):
    event = Event.objects.get(name = json.loads(request.body).get('event'))
    EventImages = EventImage.objects.filter(event = event)
    images = [image.image.url for image in EventImages]
    return JsonResponse({"status": "success","images": images})
