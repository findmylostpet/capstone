 찾아주개  
=======
### 모델
>모델을 git에 업로드 하기 위해선 git-lfs설치
>https://git-lfs.github.com/</br>
>*git-lfs를 설치하고도 에러가 발생하면 bfg를 통해 git 히스토리 삭제*
```
git lfs install
git lfs track "*.pt"
```

### 가상환경  

>가상환경 실행하기  
>*Django개발은 반드시 가상환경을 키고 시작*  
`source myvenv/Scripts/activate`  
</br>

>가상환경에 설치  
```
pip install django  
pip install requests  
pip install geocoder
pip install pandas  
pip install torchvision==0.7.0 -f https://download.pytorch.org/whl/torch_stable.html
pip install opencv-python
pip install cmake
pip install dlib
```
</br>

>가상환경 끄기  
`deactivate`

***

### Django  

>Django 서버 작동  
`python manage.py runserver`  
`python3 manage.py runserver`
</br>

>슈퍼유저생성  
`python manage.py createsuperuser`  
</br>

>MERGE
>*migration과 mapPoint.json확인 kau.py의 절대경로 상대경로로 수정*  
```
python manage.py makemigrations 
python manage.py migrate
```  
</br>

>마이그레이션 삭제  
```
python manage.py makemigrations  
python manage.py showmigrations  
python manage.py migrate --fake 프로젝트_앱 zero  
마이그레이션 파일 삭제  
python manage.py makemigrations  
python manage.py migrate --fake-initial  
```
</br>

>DB 모두 삭제  
```
find . -name "db.sqlite3" -delte  
python manage.py makemigrations  
python manage.py migrate  
```
</br>

### Tip  

>Visual Studio Code 코드 자동정렬  
```
Ctrl + A 로 코드를 모두 선택한 후  
Ctrl 을 누른 상태에서 K 와 F 를 차례로 눌러줍니다  
```

### pickle.UnpicklingError: invalid load key, 'v'. 에러 발생기
모델 지웠다가 다시 넣으면 됨.
###### 2020 KAU Software CapstoneDesign

