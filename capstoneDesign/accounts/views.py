from django.shortcuts import render, redirect,get_object_or_404

from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages

from .models import Profile

from findmylostpet.views import FindNotice, LostNotice, findListDetail2, lostListDetail2
from findmylostpet.models import Dog,LostNotice,FindNotice,Member, Photo
from django.core.paginator import Paginator

def register(request):
    if request.method == "POST":
        if request.POST["password"] == request.POST["passwordCheck"]:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/register.html', {'error': '이미 있는 아이디입니다.'})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username = request.POST["username"],
                    password = request.POST["password"])
                phone = request.POST["phone"]
                nickname = request.POST["nickname"]
                profile = Profile(user=user, phone = phone, nickname = nickname)
                profile.save()
                #user.save()
                auth.login(request, user)         
                return redirect('main')
        else:
            return render(request, 'accounts/register.html', {'error': '비밀번호가 다릅니다.'})
    else:
        return render(request, 'accounts/register.html')
   
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        print("~~~~user")
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('main')   
        else:
            return render(request, 'accounts/login.html',{'error': '아이디나 비밀번호가 일치하지 않습니다.'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('main')
    return render(request, 'accounts/register.html')

def mypage(request):
    username=User.objects.get(username = request.user.get_username())

    lostPosts = LostNotice.objects.prefetch_related('dog_set__photo_set').filter(Author=username).all().order_by('-PubDate')
    lpaginator = Paginator(lostPosts,4)
    lpage=request.GET.get('lpage')
    lposts = lpaginator.get_page(lpage)
    #return render(request, 'findmylostpet/lostList.html', {'lostPosts' : lostPosts,'posts':posts})
    

    findPosts=FindNotice.objects.prefetch_related('dog_set__photo_set').filter(Author=username).all().order_by('-PubDate')
    fpaginator = Paginator(findPosts,4)
    fpage=request.GET.get('fpage')
    fposts = fpaginator.get_page(fpage)
    #return render(request, 'findmylostpet/findList.html', {'findPosts' : findPosts,'posts':posts})
    
    return render(request, 'accounts/mypage.html', {'lostPosts' : lostPosts,'lposts':lposts,'findPosts' : findPosts,'fposts':fposts})
    #return render(request, 'accounts/mypage.html', {'lostPosts' : lostPosts, 'findPosts' : findPosts})


def lost_delete(request,lost_id):
    notice=get_object_or_404(LostNotice,pk=lost_id)
    notice.delete()
    return redirect('mypage')

def lost_edit(request,lost_id):
    notice=get_object_or_404(LostNotice,pk=lost_id)
    dog=get_object_or_404(Dog,LostNoticeNum=lost_id)
    photo=Photo.objects.filter(DogNumber=dog.id)
    data={"breed":{"푸들", "말티즈","포메라니안","비숑프리제","스피츠","치와와","진돗개","시츄","웰시코기","기타"},
    "gender":{"암컷","수컷","미상"}}
    
    return render(request,'accounts/lostWrite.html',{'notice':notice,'dog':dog, 'photo':photo,'data':data})

def lost_editing(request,lost_id):
    notice=get_object_or_404(LostNotice,pk=lost_id)
    dog=get_object_or_404(Dog,LostNoticeNum=lost_id)
    photo=Photo.objects.filter(DogNumber=dog.id)

    
    notice.MissingDate= request.POST.get('lost_date')
    notice.Text=request.POST.get('note')
    notice.Si = request.POST.get('sido')
    notice.Gu = request.POST.get('sigugun')
    notice.Dong = request.POST.get('dong')
    notice.Gratuity=request.POST.get('gratuity')
    notice.Phone=request.POST.get('phone')
    
    notice.save()

    dog.Name=request.POST.get('name')
    dog.Breed=request.POST.get('breed')
    dog.Sex=request.POST.get('sex')
    dog.save()
    
    request.method = "POST"
    if request.method == "POST":
        image_list = request.FILES.getlist('photo')
        for item in image_list: 
            photo = Photo.objects.create(DogNumber=dog, Photo=item)
            photo.save()

    location=notice.Si+" "+notice.Gu+" "+notice.Dong

    return render(request, 'findmylostpet/lostListDetail.html', {'location' :location,'dog':dog,'notice':notice, 'photo':photo})


def find_delete(request,find_id):
    notice=FindNotice.objects.get(id=find_id)
    notice.delete()
    return redirect('mypage')

def find_edit(request,find_id):
    notice=get_object_or_404(FindNotice,pk=find_id)
    dog=get_object_or_404(Dog,FindNoticeNum=find_id)
    photo=Photo.objects.filter(DogNumber=dog.id)
    data={"breed":{"푸들", "말티즈","포메라니안","비숑프리제","스피츠","치와와","진돗개","시츄","웰시코기","기타"},
    "gender":{"암컷","수컷","미상"}}
    
    return render(request,'accounts/findWrite.html',{'notice':notice,'dog':dog, 'photo':photo,'data':data})

def find_editing(request,find_id):
    notice=get_object_or_404(FindNotice,pk=find_id)
    dog=get_object_or_404(Dog,FindNoticeNum=find_id)
    photo=Photo.objects.filter(DogNumber=dog.id)

    
    notice.MissingDate= request.POST.get('find_date')
    notice.Text=request.POST.get('note')
    notice.Si = request.POST.get('sido')
    notice.Gu = request.POST.get('sigugun')
    notice.Dong = request.POST.get('dong')
    notice.Phone=request.POST.get('phone')
    notice.Author=User.objects.get(username = request.user.get_username())
    notice.save()


    dog.Name='Unknown'
    dog.Breed=request.POST.get('breed')
    dog.Sex=request.POST.get('sex')
    dog.save()
    

    request.method = "POST"
    if request.method == "POST":
        image_list = request.FILES.getlist('photo')
        for item in image_list: 
            photo = Photo.objects.create(DogNumber=dog, Photo=item)
            photo.save()

    location=notice.Si+" "+notice.Gu+" "+notice.Dong

    return render(request, 'findmylostpet/findListDetail.html', {'location' :location,'dog':dog,'notice':notice, 'photo':photo})

def lost_similarity(request,lost_id):
    notice = get_object_or_404(LostNotice, pk=lost_id)
    print(notice)
    doggy = get_object_or_404(Dog, LostNoticeNum=lost_id)
    print(doggy)
    photo = Photo.objects.filter(DogNumber=doggy.id)
    print(photo)

    # lostPosts=LostNotice.objects.prefetch_related('dog_set').all()
    # lostPosts.filter(dog.Breed=doggy.Breed)
    losts = Dog.objects.filter(Breed=doggy.Breed)
    print('####')
    print(losts)
    # print(losts.LostNoticeNum)
    dogs = []
    for i in losts:
        print(i)
        dogs.append(int(str(i)[12:15]))
    # print(dogs)
    dogs.remove(int(str(doggy)[12:15]))
    # print(dogs)
    dict = {}
    dict = calc(dogs, doggy)
    print("return dict")
    print(dict)
    dog_num = []
    # dog_num = [dog_num.append(x[0]) for x in dict]
    for x in dict:
        print(x[0])
        a = int(x[0])
        dog_num.append(a)
    print('dog_num: ',dog_num)
    """result_notice_num = []
    for i in range(len(dog_num)):
        print('i: ',i)
        dog = get_object_or_404(Dog, pk=dog_num[i])
        print(str(dog.FindNoticeNum)[19:22])
        result_notice_num.append(int(str(dog.FindNoticeNum)[19:22]))

    print(result_notice_num)
    """
    # for i in range(len(result_notice_num)) :
    lostFinal = Dog.objects.filter(id__in=dog_num)
    #  print(lostFinal)
    lostPosts = FindNotice.objects.filter(dog__pk__in=dog_num)
    # print(lostPosts)
    paginator = Paginator(lostPosts, 4)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'accounts/findList.html', {'posts': posts, "lost": lostFinal})

def find_similarity(request, find_id):
    notice = get_object_or_404(FindNotice, pk=find_id)
    print(notice)
    doggy = get_object_or_404(Dog, FindNoticeNum=find_id)
    print(doggy)
    photo = Photo.objects.filter(DogNumber=doggy.id)
    print(photo)

    # lostPosts=LostNotice.objects.prefetch_related('dog_set').all()
    # lostPosts.filter(dog.Breed=doggy.Breed)
    losts = Dog.objects.filter(Breed=doggy.Breed)
    print('####')
    print(losts)
    # print(losts.LostNoticeNum)
    dogs = []
    for i in losts:
        print(i)
        dogs.append(int(str(i)[12:15]))
    # print(dogs)
    dogs.remove(int(str(doggy)[12:15]))
    # print(dogs)
    dict = {}
    dict = calc(dogs, doggy)
    print("return dict")
    print(dict)
    dog_num = []
    # dog_num = [dog_num.append(x[0]) for x in dict]
    for x in dict:
        print(x[0])
        a = int(x[0])
        dog_num.append(a)
    #  print(dog_num)
    result_notice_num = []
    for i in range(len(dog_num)):
        print('i: ',i)
        dog = get_object_or_404(Dog, pk=dog_num[i])
        print(str(dog.LostNoticeNum)[19:22])
        result_notice_num.append(int(str(dog.LostNoticeNum)[19:22]))

    print(result_notice_num)

    # for i in range(len(result_notice_num)) :
    lostFinal = Dog.objects.filter(id__in=dog_num)
    #  print(lostFinal)
    lostPosts = LostNotice.objects.filter(id__in=result_notice_num)
    # print(lostPosts)
    paginator = Paginator(lostPosts, 4)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'accounts/lostList.html', {'posts': posts, "lost": lostFinal})


def calc(dogs, target):
    dict = {}
    for i in dogs :
        dog =get_object_or_404(Dog ,pk=i)
        print(dog.Eye2Nose,dog.Eye2Ears)
        print("dd",target.Eye2Nose, target.Eye2Ears)
        if(dog.Eye2Ears == None or dog.Eye2Nose==None or target.Eye2Ears == None or target.Eye2Nose==None):
            ratio = 10000
        else :
            ratio= abs(target.Eye2Nose-dog.Eye2Nose)+abs(target.Eye2Ears-dog.Eye2Ears)
        
        print("--------rateio: ",ratio)
        dict.update({ i : ratio})
    dict = sorted(dict.items(), key=func)

    return dict


def func(x):
    return x[1]