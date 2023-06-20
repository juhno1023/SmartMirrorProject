# 스마트 미러 기반 카메라를 활용한 사용자 맞춤형 화면 조정 시스템

### 1. 시스템 소개 :
 유니버설 디자인 원칙을 바탕으로 스마트 미러 환경의 UI / UX를 설계하여, 신체적 한계를 겪는 장애인 사용자가 스마트 미러를 편리하게 사용할 수 있도록 하기 위해, 
카메라를 활용하여 사용자 맞춤형으로 UI 높이를 조정해주는 시스템을 설계하고, 최종적으로 해당 시스템을 적용한 일정 관리 프로그램을 구현해보았다.

---

### 2. 시스템 설계 방법 :
&nbsp;
휠체어 탑승자, 허리가 굽어 시야가 낮은 노인, 키가 작은 일반 사용자, 키가 큰 일반 사용자와 같이 여러 상황에서 각 사용자에게 스마트 미러가 적절한 UI를 제공하도록 설계하기 위해, 사용자의 얼굴 높이를 인식하고 알고리즘을 설계해야한다. 또한 해당 상황에서 각 사용자들이 스마트 미러의 화면을 터치할 수 있는 범위를 구함으로써, 각 상황마다 적절한 높이 조정을 하는 시스템을 구현할 수 있다. <br/><br/>
&nbsp;
이를 위해 구글에서 제공해주는 Media Pipe와 OpenCV를 활용하여 UI 조정 시스템 구현을 진행한다.
시스템 구현 방법으로는 스마트 미러에 연결할 수 있는 카메라를 사용하여, 입력되는 영상에서 대상의 얼굴에 Landmark를 이용해 키 포인트를 설정한다. 그리고 이 키 포인트를 이용하여, 카메라의 아래부터 높이를 계산한다. 높이 정보 계산 및 알고리즘 구현 방법은 다음과 같은 단계를 거친다.

<img width="897" alt="스크린샷 2023-06-20 오후 8 10 07" src="https://github.com/juhno1023/SmartMirrorProject/assets/114224596/76047d97-de09-4838-9181-d00b12fd80c1">

<br/>
&nbsp;
위 다섯 단계를 거쳐, 각 사용자의 상황에서의 얼굴 높이, 터치 가능한 범위를 계산하여 데이터를 얻고, 이를 일반화하는 공식을 구하면 이후에 다양한 상황에서 적절한 UI 를 제공하는 시스템을 구현 할 수 있다. 이때 단계 1에서 카메라를 스마트 미러 위가 아닌, 중간 위치에 설치를 한 이유는 인식에 오류를 방지하기 위함이다.

---

### 3. 결과물 :
**해당 시스템을 적용할 일정 관리 프로그램:**
<br/>
<img width="180" alt="image" src="https://github.com/juhno1023/SmartMirrorProject/assets/114224596/2b78758d-5a9c-4c11-af16-62cbb9d6186b">
<img width="180" alt="image" src="https://github.com/juhno1023/SmartMirrorProject/assets/114224596/b5b2b7ba-1db0-46fe-b724-1d9bfa2f019e">
<img width="180" alt="image" src="https://github.com/juhno1023/SmartMirrorProject/assets/114224596/39d8a240-136b-4352-a159-6657d44a63a4">
<img width="180" alt="image" src="https://github.com/juhno1023/SmartMirrorProject/assets/114224596/07d9295b-0d34-40ee-8244-8d0c468c91ba">
<br/>
<br/>
**프로그램이 카메라로 사용자의 얼굴 높이를 판단하여 화면 높이를 조정해주는 모습:**
<br/>
<img width="200" alt="image" src="https://github.com/juhno1023/SmartMirrorProject/assets/114224596/b741a42a-152f-4f46-a344-bc076bb7b553">
<img width="205" alt="image" src="https://github.com/juhno1023/SmartMirrorProject/assets/114224596/c2855eb4-3d34-4600-beee-804a83f55679">

---

### 4. 사용 방법:
1. 파일을 다운로드 받은 후, 파일을 실행하기 전, 이미지 폴더에 있는 이미지 파일들을 "SmartMirrorHeightSystem.py"파일과 동일한 디렉토리에 같이 있도록 파일들을 꺼내준다.
2. Visual Studio Code에서 "SmartMirrorHeightSystem.py" 파일을 실행한다. 이때 스마트 미러 환경에서는 카메락 설치되어 있어야 한다.
3. 프로그램이 실행 되면, "일정 관리 시작하기" 버튼을 눌렀을 때, 화면 조정이 잘 되는 것을 확인 할 수 있다.
   
---
