import os
from torchvision import datasets
import torchvision.transforms as transforms
import torch
import numpy as np
from PIL import ImageFile
import torch.nn as nn
import torchvision.models as models
import torch.nn.functional as F
import pandas as pd
import dlib, cv2, os
from imutils import face_utils
import numpy as np
import matplotlib.pyplot as plt

detector = dlib.cnn_face_detection_model_v1('findmylostpet/similarity/dogHeadDetector.dat')
predictor = dlib.shape_predictor('findmylostpet/similarity/landmarkDetector.dat')

criterion = nn.CrossEntropyLoss()

model = models.densenet161(pretrained=True)
# model.fc = nn.Linear(2048, 82, bias=True)
model.classifier = nn.Sequential(
    nn.Linear(2208, 1024, bias=True),
    nn.ReLU(),
    nn.BatchNorm1d(1024),
    nn.Linear(1024, 512, bias=True),
    nn.ReLU(),
    nn.BatchNorm1d(512),
    nn.Linear(512, 256, bias=True),
    nn.ReLU(),
    nn.BatchNorm1d(256),
    nn.Linear(256, 81, bias=True)
)
model.load_state_dict(
    torch.load('findmylostpet/predict_model/201028_dense161_40_92%.pt', map_location=torch.device('cpu')))
model.eval()

import cv2
from PIL import Image

obj = {
    "AfghanHound": "아프간하운드",
    "AlaskanMalamute": "알래스카맬러뮤트",
    "AmericanStaffordshireTerrier": "아메리칸스태퍼드셔테리어",
    "AustralianShepherd": "오스트레일리언셰퍼드",
    "BassetHound": "바셋하운드",
    "Beagle": "비글",
    "BeardedCollie": "비어디드콜리",
    "BedlingtonTerrier": "베들링턴테리어",
    "BelgianMalinois": "말리노이즈",
    "BerneseMountainDog": "버니즈마운틴도그",
    "BichonFrise": "비숑프리제",
    "Bloodhound": "블러드하운드",
    "BorderCollie": "보더콜리",
    "Borzoi": "보르조이",
    "BostonBull": "보스턴테리어",
    "Boxer": "복서",
    "BoykinSpaniel": "보이킨스패니얼",
    "Brittany": "브리트니",
    "BullTerrier": "불테리어",
    "Bulldog": "불독",
    "Bullmastiff": "불마스티프",
    "CardiganWelshCorgi": "카디건웰시코기",
    "CavalierKingCharlesSpaniel": "카발리에킹찰스스패니얼",
    "ChesapeakeBayRetriever": "체서피크베이리트리버",
    "Chihuahua": "치와와",
    "ChineseShar-Pei": "샤페이",
    "ChowChow": "차우차우",
    "CockerSpaniel": "코커스패니얼",
    "Collie": "콜리",
    "Dachshund": "닥스훈트",
    "Dalmatian": "달마티안",
    "DobermanPinscher": "도베르만핀셔",
    "EnglishCockerSpaniel": "잉글리시코커스패니얼",
    "EnglishSpringerSpaniel": "잉글리시스프링어스패니얼",
    "EnglishToySpaniel": "잉글리시토이스패니얼",
    "FrenchBulldog": "프렌치불독",
    "GermanPinscher": "저먼핀셔",
    "GermanShepherd": "저먼셰퍼드",
    "GlenOfImaalTerrier": "글렌오브이말테리어",
    "GoldenRetriever": "골든리트리버",
    "GordonSetter": "고든세터",
    "GreatPyrenees": "그레이트피레니즈",
    "Greyhound": "그레이하운드",
    "IbizanHound": "이비전하운드",
    "IrishSetter": "아이리시세터",
    "IrishTerrier": "아이리시테리어",
    "ItalianGreyhound": "이탈리안그레이하운드",
    "JapaneseChin": "제페니스친",
    "Komondor": "코몬돌",
    "LabradorRetriever": "래브라도리트리버",
    "LhasaApso": "라사압소",
    "Maltese": "말티즈",
    "ManchesterTerrier": "맨체스터테리어",
    "Mastiff": "잉글리쉬마스티프",
    "MiniatureSchnauzer": "미니어처슈나우저",
    "NeapolitanMastiff": "나폴리탄마스티프",
    "NorwegianBuhund": "노르웨이안부훈트",
    "OldEnglishSheepdog": "올드잉글리시쉽독",
    "Papillon": "빠삐용",
    "ParsonRussellTerrier": "파슨러셀테리어",
    "Pekingese": "페키니즈",
    "PembrokeWelshCorgi": "웰시코기",
    "Pomeranian": "포메라니안",
    "Poodle": "푸들",
    "SaintBernard": "세인트버나드",
    "SilkyTerrier": "실키테리어",
    "TibetanMastiff": "티베탄마스티프",
    "WelshSpringerSpaniel": "웰시스프링어스패니얼",
    "YorkshireTerrier": "요크셔테리어",
    "Sapsaree": "삽살개",
    "Spitz": "재패니즈스피츠",
    "ShibaInu": "시바견",
    "ShihTzu": "시츄",
    "SiberianHusky": "시베리안허스키",
    "KoreaJindo": "진돗개",

    "ToyPoodle": "토이푸들",
    "MiniaturePincher": "미니어쳐핀셔",
    "Rottweiler": "로트와일러",
    "Pug": "퍼그",
    "Samoyed": "사모예드",
    "ShetlandSheepdog": "셔틀랜드쉽독",
}

class_name = list(obj.keys())
kor_name = list(obj.values())


def lost_predict(img_list):
    result_softmax = torch.zeros(1, 81)
    print(os.getcwd())
    flag = True
    a,b=None,None
    for img in img_list:
        img = str(img)
        img = img.replace(' ', '_')

        print("FindMyLostPet/capstoneDesign/media/lostList/images/" + str(img))
        img = "media/lostList/images/" + str(img)
        image = load_input_image(img)
        result_softmax += soft_predict(image)
        if flag == True:

            try:
                shape = point(img)
                a,b = ratio(shape)
            except:
                a,b=9999,9999

            flag == False

    result_softmax /= len(img_list)
    print("Sum soft")
    print(torch.sum(result_softmax))
    scores1, indices1 = torch.topk(result_softmax, 3)
    scores1 = scores1[0].tolist()
    indices1 = indices1[0].tolist()

    breed = []
    kor = []
    score = []
    for i in range(0, 3):
        print(i + 1, "", class_name[indices1[i]], "and", round(scores1[i] * 100, 2), "%")
        # result_dict.update({ class_name[indices1[i]] : indices1[i]})
        score.append(round(scores1[i] * 100, 2))
        breed.append(class_name[indices1[i]])
        kor.append(kor_name[indices1[i]])

    return breed, kor, score, a, b


def soft_predict(image):
    result = model(image)
    return nn.Softmax(dim=1)(result)


def load_input_image(img_path):
    image = Image.open(img_path).convert('RGB')
    prediction_transform = transforms.Compose([transforms.Resize(size=(224, 224)),
                                               transforms.ToTensor(),
                                               transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                                    std=[0.229, 0.224, 0.225])])

    # discard the transparent, alpha channel (that's the :3) and add the batch dimension
    image = prediction_transform(image)[:3, :, :].unsqueeze(0)
    return image


def predict_breed_transfer(model, img_path):
    # load the image and return the predicted breed
    if os.path.isfile(img_path):
        model = model.cpu()
        model.eval()
        img = load_input_image(img_path)
        idx = torch.argmax(model(img))
        # print("idx 들어왔다: "+str(idx))
        # print(class_name[idx])
        return class_name[idx]


def process(img_path):
    prediction = predict_breed_transfer(model, img_path)
    print(prediction)

    return (prediction)


def process2():
    # /Users/choejaeyun/Documents/git/moon/FindMyLostPet/capstoneDesign/findmylostpet/predict_model/images
    for img_file in os.listdir('findmylostpet/predict_model/images'):
        img_path = os.path.join('findmylostpet/predict_model/images', img_file)
        print(img_path)
        prediction = predict_breed_transfer(model, img_path)
        print(prediction)

        # print("image_file_name: {0}, \t predition breed: {1}\n\n".format(img_path, predition))

    return (prediction)


def point(img_path):
    # filename, ext = os.path.splitext(os.path.basename(img_path))
    print('hello')
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(img.shape)
    height = 300
    if (img.shape[1] > height):
        width = int(height * img.shape[1] / img.shape[0])
        print(height, width)
        img = cv2.resize(img, dsize=(width, height), interpolation=cv2.INTER_LINEAR)

    print(img.shape)
    print('hello')
    dets = detector(img, upsample_num_times=1)
    shape = []
    for i, d in enumerate(dets):
        shape = predictor(img, d.rect)
        shape = face_utils.shape_to_np(shape)
    '''
        for i, d in enumerate(dets):
            shape = predictor(img, d.rect)
            shape = face_utils.shape_to_np(shape)

            for i, p in enumerate(shape):
                shapes.append(shape)
                cv2.circle(img_result, center=tuple(p), radius=3, color=(0, 0, 255), thickness=-1, lineType=cv2.LINE_AA)
                cv2.putText(img_result, str(i), tuple(p), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        img_out = cv2.cvtColor(img_result, cv2.COLOR_RGB2BGR)
        cv2.imwrite('img/%s_out%s' % (img_path, img_out))
        '''
    print(shape)
    return (shape)


def ratio(shape):
    eye2eye = np.sqrt(float(shape[2][0] - shape[5][0]) ** 2 + float(shape[2][0] - shape[5][0]) ** 2)
    nose = np.sqrt((float(shape[2][0] - shape[5][0]) / 2 - shape[3][0]) ** 2 + (
                float(shape[2][1] - shape[5][1]) / 2 - shape[3][1]) ** 2)
    eye2nose = int(eye2eye / nose * 1000)

    ear2ear = np.sqrt(float(shape[1][0] - shape[4][0]) ** 2 + float(shape[1][0] - shape[4][0]) ** 2)
    eye2ear = int(eye2eye / ear2ear * 1000)
    print("dd", eye2nose, eye2ear)
    return eye2nose, eye2ear

    '''
    import os
import re
f_path="FindMyLostPet/capstoneDesign/media/Profile_img/"
i=0
for img_file in os.listdir(f_path):

    img_file = img_file.replace(' ', '_')
    src=f_path+str(img_file)

    p = re.compile("[^0-9]")

    dst=f_path+str("".join(p.findall(img_file))[1:])
    os.rename(src,dst)
    print(dst)
'''