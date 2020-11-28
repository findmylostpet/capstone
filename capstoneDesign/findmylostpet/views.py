from django.shortcuts import render, get_object_or_404, redirect
from .models import Dog, LostNotice, FindNotice, Member, Photo, FindLocation
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import Profile
from django.contrib import auth
from .forms import ProfileForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
from django.core.paginator import Paginator
import requests
import geocoder
import pandas as pd
from django.shortcuts import render
from .predict_model.kau import *
import json


# Create your views here.
def main(request):
    '''
    file_path = "capstone/static/json/mapPoint.json"
    json_data = {}
    with open(file_path, "r") as json_file:
        json_data = json.load(json_file)
    json_data['positions'].append({
        "lat" : 37.599579,
        "lng" : 126.865186
    })
    with open(file_path, 'w') as outfile:
        json.dump(json_data, outfile, indent=4)
        '''
    lostPosts = LostNotice.objects.prefetch_related('dog_set').all().order_by('-PubDate')  # 모든 글들을 대상으로
    lpaginator = Paginator(lostPosts, 4)  # 객체 네 개를 한 페이지로 자르기
    lpage = request.GET.get('lpage')  # request된 페이지가 뭔지를 알아내고 ( request페이지를 변수에 담아냄 )
    lposts = lpaginator.get_page(lpage)  # request된 페이지를 얻어온 뒤 return 해 준다

    findPosts = FindNotice.objects.prefetch_related('dog_set').all().order_by('-PubDate')  # 모든 글들을 대상으로
    fpaginator = Paginator(findPosts, 4)  # 객체 네 개를 한 페이지로 자르기
    fpage = request.GET.get('fpage')  # request된 페이지가 뭔지를 알아내고 ( request페이지를 변수에 담아냄 )
    fposts = fpaginator.get_page(fpage)  # request된 페이지를 얻어온 뒤 return 해 준다

    ##findPosts=FindNotice.objects.prefetch_related('dog_set').all()
    return render(request, 'findmylostpet/main.html',
                  {'lostPosts': lostPosts, 'lposts': lposts, 'findPosts': findPosts, 'fposts': fposts})


def about(request):
    return render(request, 'findmylostpet/about.html')


@csrf_exempt
def findList(request):
    si = request.GET.get('sido')
    sigugun = request.GET.get('sigugun')
    dong = request.GET.get('dong')
    if (si):
        findPosts = FindNotice.objects.prefetch_related('dog_set__photo_set').filter(Si=si).filter(Gu=sigugun).all()
    else:
        findPosts = FindNotice.objects.prefetch_related('dog_set__photo_set').all().order_by('-PubDate')  # sort 안정함
    paginator = Paginator(findPosts, 4)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'findmylostpet/findList.html',
                  {'findPosts': findPosts, 'posts': posts, 'si': si, 'gugun': sigugun, 'dong': dong})


def findListDetail(request):
    return render(request, 'findmylostpet/findListDetail.html')


def findListDetail2(request, find_id, dog_id):
    notice = get_object_or_404(FindNotice, pk=find_id)
    dog = get_object_or_404(Dog, pk=dog_id)
    dog = get_object_or_404(Dog, FindNoticeNum=find_id)
    photo = Photo.objects.filter(DogNumber=dog_id)
    location = notice.Si + " " + notice.Gu + " " + notice.Dong

    findPosts = FindNotice.objects.prefetch_related('dog_set__photo_set').all().order_by('-PubDate')
    paginator = Paginator(findPosts, 4)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'findmylostpet/FindListDetail.html',
                  {'location': location, 'notice': notice, 'dog': dog, 'photo': photo, 'posts': posts})


def findWrite(request):
    g = geocoder.ip('me')
    # print("~~~~~~~~~~~~", g.latlng[0],g.latlng[1] )
    url = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={}&y={}".format(g.latlng[1], g.latlng[0])
    # print(url)
    headers = {"Authorization": "KakaoAK 5333c82c317f5870de95a45e5220b988"}
    api_test = requests.get(url, headers=headers)
    # result = json.loads(str(requests.get(url,headers=headers).text))
    print(str(api_test.text))
    url_text = json.loads(str(api_test.text))
    # print("@@@@@@@@@@@@@@@@@@@", url_text['documents'][0]['region_1depth_name'])
    findLocation = FindLocation()
    findLocation.Si = url_text['documents'][0]['region_1depth_name']
    findLocation.Gu = url_text['documents'][0]['region_2depth_name']
    findLocation.Dong = url_text['documents'][0]['region_3depth_name']
    findLocation.save()
    # 이어서 시구동 넘겨서 현재위치에 출력 + 시구동 저장
    return render(request, 'findmylostpet/findWrite.html', {'findLocation': findLocation})


@csrf_exempt
def lostList(request):
    # sido=request.POST.get('sido')

    si = request.GET.get('sido')
    sigugun = request.GET.get('sigugun')
    dong = request.GET.get('dong')
    breed = request.GET.get('selected_breed')
    print(breed)
    lostPosts=LostNotice.objects.prefetch_related('dog_set__photo_set').all().order_by('-PubDate')
    if (si):
        lostPosts = lostPosts.filter(Si=si).filter(Gu=sigugun).all()

    if(breed):
        lostPosts = lostPosts.filter(dog__Breed=breed)
    paginator = Paginator(lostPosts, 4)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'findmylostpet/lostList.html',
                  {'lostPosts': lostPosts, 'posts': posts, 'si': si, 'gugun': sigugun, 'dong': dong,'b':breed})


'''def lostListDetail(request, lost_id):
    notice = get_object_or_404(LostNotice, pk=lost_id)
    dog = get_object_or_404(Dog, LostNoticeNum=lost_id, pk=dog_id)
    photo = Photo.objects.filter(DogNumber=dog_id)

    lostPosts = LostNotice.objects.prefetch_related('dog_set__photo_set').all()
    paginator = Paginator(lostPosts, 4)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'findmylostpet/lostListDetail.html',
                  {'location': location, 'notice': notice, 'dog': dog, 'photo': photo, 'posts': posts})
'''

def lostListDetail2(request, lost_id, dog_id):
    notice = get_object_or_404(LostNotice, pk=lost_id)
    dog = get_object_or_404(Dog, pk=dog_id)
    dog = get_object_or_404(Dog, LostNoticeNum=lost_id)
    photo = Photo.objects.filter(DogNumber=dog_id)
    location = notice.Si + " " + notice.Gu + " " + notice.Dong

    lostPosts = LostNotice.objects.prefetch_related('dog_set__photo_set').all().order_by('-PubDate')
    paginator = Paginator(lostPosts, 4)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'findmylostpet/lostListDetail.html',
                  {'location': location, 'notice': notice, 'dog': dog, 'photo': photo, 'posts': posts})


def lostWrite(request):
    return render(request, 'findmylostpet/lostWrite.html')



@csrf_exempt
def lost_create(request):
    dog = Dog()
    notice = LostNotice()
    photo = Photo()
    user_pk = request.user.id
    user = User.objects.get(pk=user_pk)
    notice.State = 1

    notice.PubDate = timezone.datetime.now()
    # 미싱 날짜 디폴트값 : 공고작성 날짜
    if request.POST.get('lost_date') == '':
        notice.MissingDate = timezone.datetime.now()
    else :
        notice.MissingDate = request.POST.get('lost_date')

    #notice.MissingDate = request.POST.get('lost_date')

    notice.Text = request.POST.get('note')
    notice.Si = request.POST.get('sido')
    notice.Gu = request.POST.get('sigugun')
    notice.Dong = request.POST.get('dong')
   

   # notice.Gratuity = request.POST.get('gratuity')
   # 사례금 디폴드값 : 0
    if request.POST.get('gratuity') == '':
        notice.Gratuity = 0
    else :
        notice.Gratuity  = request.POST.get('gratuity')
    notice.user = User.objects.get(id=request.user.id)
    notice.Phone = user.profile.phone
    notice.Author = User.objects.get(username=request.user.get_username())
    notice.save()

    notice_num = str(notice)[19:-1]
    print(notice_num)

    '''
        file_path = "json/mapPoint.json"
        json_data = {}
        with open(file_path, "r") as json_file:
            json_data = json.load(json_file)
        json_data['positions'].append({
            "lat" : 37.599579,
            "lng" : 126.865186
        })
        with open(file_path, 'w') as outfile:
            json.dump(json_data, outfile, indent=4)
    '''

    dog.LostNoticeNum = notice
    dog.Name = request.POST.get('name')
    dog.Sex = request.POST.get('sex')
    dog.save()

    dog_num = str(dog)[12:-1]

    request.method = "POST"
    if request.method == "POST":
        image_list = request.FILES.getlist('photo')
        
        if len(image_list) != 0:
            rep_item = image_list[0]
            rep_item = str(rep_item)
            rep_item = rep_item.replace(' ', '_')
            dog.rep_image_url = rep_item
            print(rep_item)
            for item in image_list:
                print("phpppppppppppp")
                print(item)
                photo = Photo.objects.create(DogNumber=dog, Photo=item)
                photo.save()

    if notice.Si != '선택' and notice.Gu !='선택' and notice.Dong != '선택' and notice.Si != '' and notice.Gu !='' and notice.Dong != '' :
        location = notice.Si + " " + notice.Gu + " " + notice.Dong
        url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + location
        headers = {"Authorization": "KakaoAK 5333c82c317f5870de95a45e5220b988"}
        result = json.loads(str(requests.get(url, headers=headers).text))
        match_first = result['documents'][0]['address']
    else :
        match_first = ''

    breeds, kor, score, dog.Eye2Nose,dog.Eye2Ears = lost_predict(image_list)
   
    
    print(dog.Eye2Nose,dog.Eye2Ears)
    dog.save()
    pro_url=[]
    for i in range(3):
        for img_file in os.listdir('media/Profile_img'):
            img_path = os.path.join('/media/Profile_img/', img_file)
            x=img_path.split('.')
            if(x[1]==breeds[i]):
                print(img_path)
                pro_url.append(str(img_path))
            
    dog.save()

    if dog.Name == '' : 
        notice_num = int(notice_num)
        dog_num = int(dog_num)
        LostNotice.objects.filter(id=notice_num).delete()
        Dog.objects.filter(id=dog_num).delete()
        return render(request, 'findmylostpet/lostWrite.html',{ 'error_name': '이름을 입력해주세요.','si' : notice.Si,'gu' : notice.Gu, 'dong' : notice.Dong ,'name':dog.Name, 'sex' : dog.Sex,'pubdate' : notice.MissingDate , 'gratuity' :notice.Gratuity, 'note' : notice.Text})
    if dog.Sex == '' : 
        notice_num = int(notice_num)
        dog_num = int(dog_num)
        LostNotice.objects.filter(id=notice_num).delete()
        Dog.objects.filter(id=dog_num).delete()
        return render(request, 'findmylostpet/lostWrite.html',{ 'error_sex': '성별을 선택해주세요.','si' : notice.Si,'gu' : notice.Gu, 'dong' : notice.Dong ,'name':dog.Name, 'sex' : dog.Sex,'pubdate' : notice.MissingDate , 'gratuity' :notice.Gratuity, 'note' : notice.Text})
    if notice.Si == '선택' or notice.Si == '': 
        notice_num = int(notice_num)
        dog_num = int(dog_num)
        LostNotice.objects.filter(id=notice_num).delete()
        Dog.objects.filter(id=dog_num).delete()
        return render(request, 'findmylostpet/lostWrite.html',{ 'error_si': '정확한 위치 주소를 선택해주세요.'  ,'name':dog.Name, 'sex' : dog.Sex,'pubdate' : notice.MissingDate , 'gratuity' :notice.Gratuity, 'note' : notice.Text})
    if notice.Gu == '선택' or notice.Gu == '' : 
        notice_num = int(notice_num)
        dog_num = int(dog_num)
        LostNotice.objects.filter(id=notice_num).delete()
        Dog.objects.filter(id=dog_num).delete()
        return render(request, 'findmylostpet/lostWrite.html',{ 'error_si': '정확한 위치 주소를 선택해주세요.'  ,'name':dog.Name, 'sex' : dog.Sex,'pubdate' : notice.MissingDate , 'gratuity' :notice.Gratuity, 'note' : notice.Text})
    if notice.Dong == '선택' or notice.Dong == '' : 
        notice_num = int(notice_num)
        dog_num = int(dog_num)
        LostNotice.objects.filter(id=notice_num).delete()
        Dog.objects.filter(id=dog_num).delete()
        return render(request, 'findmylostpet/lostWrite.html',{ 'error_si': '정확한 위치 주소를 선택해주세요.'  ,'name':dog.Name, 'sex' : dog.Sex,'pubdate' : notice.MissingDate , 'gratuity' :notice.Gratuity, 'note' : notice.Text})

    #if notice.MissingDate == '0000-00-00' : 
      #  print("!!!!!!!!!!!!!!!!!!!")
      #  return render(request, 'findmylostpet/lostWrite.html',{ 'error_date': '날짜를 선택해주세요.','si' : notice.Si,'gu' : notice.Gu, 'dong' : notice.Dong ,'name':dog.Name, 'sex' : dog.Sex,'pubdate' : notice.MissingDate , 'gratuity' :notice.Gratuity, 'note' : notice.Text})


    if len(image_list) == 0 :
        notice_num = int(notice_num)
        dog_num = int(dog_num)
        LostNotice.objects.filter(id=notice_num).delete()
        Dog.objects.filter(id=dog_num).delete()
        
        return render(request, 'findmylostpet/lostWrite.html',{'si' : notice.Si,'gu' : notice.Gu, 'dong' : notice.Dong ,'name':dog.Name, 'sex' : dog.Sex,'pubdate' : notice.MissingDate , 'gratuity' :notice.Gratuity, 'note' : notice.Text, 'error': '사진을 업로드해주세요.'})
    else:
        return render(request, "findmylostpet/ex.html",
                  {'location': location, 'dog': dog, 'notice': notice, 'photo': photo,'pred':kor,'pro_url':pro_url,'score':score})



def jsonDataShow(request):
    return render(request, 'findmylostpet/json/mapPoint.json')

def jsonDataShow_find(request):
    return render(request, 'findmylostpet/json/mapPoint_find.json')


@csrf_exempt
def find_create(request):
    dog = Dog()
    notice = FindNotice()
    photo = Photo()
    user_pk = request.user.id
    user = User.objects.get(pk=user_pk)

    notice.State = request.POST.get('state')
    notice.PubDate = timezone.datetime.now()
    notice.MissingDate = request.POST.get('find_date')
    notice.Text = request.POST.get('note')
    notice.user = User.objects.get(id=request.user.id)
    notice.Phone = user.profile.phone
    notice.Author = User.objects.get(username=request.user.get_username())
    
    dog.FindNoticeNum = notice
    dog.Name = 'Unknown'
    #dog.Breed = request.POST.get('breed')
    dog.Sex = request.POST.get('sex')
    

    request.method = "POST"
    if request.method == "POST":
        notice.Si = request.POST.get('si')
        notice.Gu = request.POST.get('gu')
        notice.Dong = request.POST.get('dong')
    notice.save()

    location = notice.Si + " " + notice.Gu + " " + notice.Dong
    
    notice_num = str(notice)[19:-1]
    
    dog.save()  
    dog_num = str(dog)[12:-1] 

    '''
    if request.method == "POST":
        image_list = request.FILES.getlist('photo')
        for item in image_list: 
            photo = Photo.objects.create(DogNumber=dog, Photo=item)
            photo.save()
    '''

    if request.method == "POST":
        image_list = request.FILES.getlist('photo')
        if len(image_list) != 0:
            rep_item = image_list[0]
            rep_item = str(rep_item)
            rep_item = rep_item.replace(' ', '_')
            dog.rep_image_url = rep_item
            for item in image_list:
                photo = Photo.objects.create(DogNumber=dog, Photo=item)
                photo.save()


    

    breeds, kor, score, dog.Eye2Nose, dog.Eye2Ear = lost_predict(image_list)

    dog.save()
    pro_url=[]
    for i in range(3):
        for img_file in os.listdir('media/Profile_img'):
            img_path = os.path.join('/media/Profile_img/', img_file)
            x=img_path.split('.')
            if(x[1]==breeds[i]):
                print(img_path)
                pro_url.append(str(img_path))
            
    if dog.Sex == '' : 
        notice_num = int(notice_num)
        dog_num = int(dog_num)
        FindNotice.objects.filter(id=notice_num).delete()
        Dog.objects.filter(id=dog_num).delete()
        return render(request, 'findmylostpet/findWrite.html',{ 'error_sex': '성별을 선택해주세요.','pubdate' : notice.MissingDate , 'note' : notice.Text})
    
    if notice.State == '' : 
        notice_num = int(notice_num)
        dog_num = int(dog_num)
        FindNotice.objects.filter(id=notice_num).delete()
        Dog.objects.filter(id=dog_num).delete()
        return render(request, 'findmylostpet/findWrite.html',{ 'error_state': '상태를 선택해주세요.','sex' : dog.Sex ,'pubdate' : notice.MissingDate , 'note' : notice.Text})    
    
    if len(image_list) == 0 :
        notice_num = int(notice_num)
        dog_num = int(dog_num)
        FindNotice.objects.filter(id=notice_num).delete()
        Dog.objects.filter(id=dog_num).delete()
        return render(request, 'findmylostpet/findWrite.html',{ 'error_photo': '사진을 업로드 해주세요.','sex' : dog.Sex ,'note' : notice.Text ,'state' : notice.State ,'pubdate' : notice.MissingDate , 'note' : notice.Text})    
    
    
    return render(request, 'findmylostpet/find_predict.html',
                  {'location': location, 'dog': dog, 'notice': notice, 'photo': photo,'pred':kor,'pro_url':pro_url,'score':score})

def breed(request):
    return render(request, 'findmylostpet/breedfounder.html')


def add_find_breed(request,find_id,dog_id):
   
    notice = get_object_or_404(FindNotice, pk=find_id)
    dog = get_object_or_404(Dog, pk=dog_id)
    dog = get_object_or_404(Dog, FindNoticeNum=find_id)
    dog.Breed = request.POST.get('breed')
    
    dog.save()

    photo = Photo.objects.filter(DogNumber=dog_id)
    location = notice.Si + " " + notice.Gu + " " + notice.Dong
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + location
    headers = {"Authorization": "KakaoAK 5333c82c317f5870de95a45e5220b988"}
    result = json.loads(str(requests.get(url, headers=headers).text))
    match_first = result['documents'][0]['address']
    file_path = "findmylostpet/templates/findmylostpet/json/mapPoint_find.json"
    # capstone/static/json/mapPoint.json
    json_data = {}
    notice_num = str(notice)[19:-1]
    dog_num = str(dog)[12:-1]
    with open(file_path, "r",encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    print(notice.State)


    
    json_data['positions'].append({
            "dog_breed": dog.Breed,
            "dog_sex": dog.Sex,
            "notice_num": notice_num,
            "address_name": str(match_first['address_name']),
            "lat": float(match_first['y']),
            "lng": float(match_first['x']),
            "content": '<div class="wrap">' +
                    '    <div class="info">' +
                    '        <div class="title"> ' + dog.Breed +
                    '            <div class="close" onclick="closeOverlay()" title="닫기"></div>' +
                    '        </div>' +
                    '        <div class="body">' +
                    '            <div class="img">' +
                    '                <img src=' + '"/media/lostList/images/' + dog.rep_image_url+ '" ' + 'width="90" height="90">' +
                    '           </div>' +
                    '            <div class="desc">' +
                    '                <div class="Sex"> 성별 : ' + dog.Sex + '</div>' +
                    '                <div class="State"> 상태: ' + notice.State + '</div>' +
                    '                <div><a href="../findListDetail/' + notice_num + '/' + dog_num + '"' + 'target="_blank" class="link">공고 상세보기</a></div>' +
                    '            </div>' +
                    '        </div>' +
                    '    </div>' +
                    '</div>'
        })

    with open(file_path, 'w', encoding='utf-8') as outfile:
        json.dump(json_data, outfile, indent=4, ensure_ascii=False)


    lostPosts = LostNotice.objects.prefetch_related('dog_set__photo_set').all().order_by('-PubDate')
    paginator = Paginator(lostPosts, 4)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'findmylostpet/findListDetail.html',
                  {'location': location, 'notice': notice, 'dog': dog, 'photo': photo, 'posts': posts})

def add_breed(request,lost_id,dog_id):
   
    notice = get_object_or_404(LostNotice, pk=lost_id)
    dog = get_object_or_404(Dog, pk=dog_id)
    dog = get_object_or_404(Dog, LostNoticeNum=lost_id)
    dog.Breed = request.POST.get('breed')
    dog.save()

    photo = Photo.objects.filter(DogNumber=dog_id)
    location = notice.Si + " " + notice.Gu + " " + notice.Dong
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + location
    headers = {"Authorization": "KakaoAK 5333c82c317f5870de95a45e5220b988"}
    result = json.loads(str(requests.get(url, headers=headers).text))
    match_first = result['documents'][0]['address']
    file_path = "findmylostpet/templates/findmylostpet/json/mapPoint.json"
    # capstone/static/json/mapPoint.json
    json_data = {}
    notice_num = str(notice)[19:-1]
    dog_num = str(dog)[12:-1]
    with open(file_path, "r",encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    
    json_data['positions'].append({
            "dog_name": dog.Name,
            "dog_breed": dog.Breed,
            "dog_sex": dog.Sex,
            "notice_num": notice_num,
            "address_name": str(match_first['address_name']),
            "lat": float(match_first['y']),
            "lng": float(match_first['x']),
            "content": '<div class="wrap">' +
                    '    <div class="info">' +
                    '        <div class="title"> ' + dog.Name +
                    '            <div class="close" onclick="closeOverlay()" title="닫기"></div>' +
                    '        </div>' +
                    '        <div class="body">' +
                    '            <div class="img">' +
                    '                <img src=' + '"/media/lostList/images/' + dog.rep_image_url+ '" ' + 'width="90" height="90">' +
                    '           </div>' +
                    '            <div class="desc">' +
                    '                <div class="Breed"> 종류: ' + dog.Breed + '</div>' +
                    '                <div class="Sex"> 성별 : ' + dog.Sex + '</div>' +
                    '                <div><a href="../lostListDetail/' + notice_num + '/' + dog_num + '"' + 'target="_blank" class="link">공고 상세보기</a></div>' +
                    '            </div>' +
                    '        </div>' +
                    '    </div>' +
                    '</div>'
        })

    with open(file_path, 'w', encoding='utf-8') as outfile:
        json.dump(json_data, outfile, indent=4, ensure_ascii=False)

    lostPosts = LostNotice.objects.prefetch_related('dog_set__photo_set').all().order_by('-PubDate')
    paginator = Paginator(lostPosts, 4)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    

    return render(request, 'findmylostpet/lostListDetail.html',
                  {'location': location, 'notice': notice, 'dog': dog, 'photo': photo, 'posts': posts})