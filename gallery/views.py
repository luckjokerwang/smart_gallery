from django.shortcuts import render, redirect, get_object_or_404  # <--- 1. 记得引入 get_object_or_404
from .models import Photo
from ultralytics import YOLO
from django.conf import settings
import os

# 预加载模型
print("正在加载 AI 模型...")
model_path = os.path.join(settings.BASE_DIR, 'yolov8n.pt')
model = YOLO(model_path)

def gallery_view(request):
    if request.method == 'POST':
        # =========== 🔴 删除逻辑开始 ===========
        # 如果请求里包含 'delete_id'，说明用户点了删除按钮
        if 'delete_id' in request.POST:
            photo_id = request.POST.get('delete_id')
            # 找到照片，找不到会报 404 (比较安全)
            photo = get_object_or_404(Photo, id=photo_id)
            
            # 1. 先删硬盘上的文件
            photo.image.delete(save=False)
            # 2. 再删数据库里的记录
            photo.delete()
            
            # 删完刷新页面
            return redirect('gallery:photo_list')
        # =========== 🔴 删除逻辑结束 ===========

        # =========== 🟢 上传逻辑开始 (原来的代码) ===========
        tag = request.POST.get('tags', '')
        image = request.FILES.get('image')
        
        if image:
            photo = Photo.objects.create(image=image)
            
            if tag == "":
                try:
                    results = model(photo.image.path)
                    if len(results) > 0 and len(results[0].boxes) > 0:
                        class_id = int(results[0].boxes.cls[0])
                        detected_name = results[0].names[class_id]
                        photo.tag = detected_name
                    else:
                        photo.tag = "未识别"
                except Exception as e:
                    print(f'AI识别失败: {e}')
                    photo.tag = "识别失败"
            else:
                photo.tag = tag
                
            photo.save()
        return redirect('gallery:photo_list')
        # =========== 🟢 上传逻辑结束 ===========

    # GET 请求：展示图片
    tag_filter = request.GET.get('tag')
    if tag_filter:
        photos = Photo.objects.filter(tag=tag_filter).order_by('-upload_time')
    else:
        photos = Photo.objects.all().order_by('-upload_time')

    return render(request, 'gallery/gallery.html', {'photos': photos})