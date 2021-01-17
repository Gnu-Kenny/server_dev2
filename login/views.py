from rest_framework.views import APIView
# json response가 일반적이지만 우선 rest_framework에서 제공하는 respose 사용
from rest_framework.response import Response
from .models import LoginUser   # '.' 현재 폴더 / 안 models 파일에서 LoginUser 사용하겠다.
# 암호화   make => 어떤 문장을 pw로 사용하기 위해 hash값으로 암호화 단반향
from django.contrib.auth.hashers import make_password, check_password
from .serialize import LoginUserSerializer  # serializer
# Create your views here.

# 로그인


class AppLogin(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        user_pw = request.data.get('user_pw')

        user = LoginUser.objects.filter(user_id=user_id).first()

        # 해당 유저 존재 확인
        if user is None:
            return Response(dict(msg="해당 사용자가 없습니다."))

        # user_pw => 클라이언트에서 올라온 pw, user.user_pw => DB에 있는 pw 비교 같으면 true
        if check_password(user_pw, user.user_pw):
            return Response(dict(msg="로그인 성공", birth_day=user.birth_day, gender=user.gender, email=user.email, name=user.name, age=user.age))
        else:
            return Response(dict(msg="로그인 실패, 비밀번호 틀림!"))

# 회원가입


class RegistUser(APIView):
    def post(self, request):
        # 데이터가 request로 다 넘어오기때문에 request.data 지정시 LoginUserSerializer로 필드들이 한번에 옮겨진다.
        serializer = LoginUserSerializer(request.data)

        # serializer.date['user_id'] 이런식으로 데이터를 꺼내 쓸수있음.
        ##포함된 필드##
        # user_id = request.data.get('user_id')
        # user_pw = request.data.get('user_pw')
        # birth_day = request.data.get('birth_day', None)
        # gender = request.data.get('gender', "male")
        # email = request.data.get('email', "")
        # name = request.data.get('name', "")
        # age = request.data.get('age', 20)
        # 암호화
        #user_pw_encryted = make_password(user_pw)

        # if user_id 가 특수 문자인지 , 숫자인지, 한글인지 ...

        # 클라이언트에서 올린 user_id가  이미 DB에 있는 유저인지 확인
        if LoginUser.objects.filter(user_id=serializer.data['user_id']).exists():

            user = LoginUser.objects.filter(
                user_id=serializer.data['user_id']).first()
            data = dict(
                msg="동일한 아이디가 있습니다.",
                user_id=user.user_id,
                user_pw=user.user_pw
            )
            return Response(data)

        # LoginUser.objects.create(
        #     user_id=user_id, user_pw=user_pw_encryted, birth_day=birth_day, gender=gender, email=email, name=name, age=age)  # DB에 저장

        # data = dict(  # response는 딕셔너리로 반환 됨.
        #     user_id=user_id,
        #     user_pw=user_pw_encryted,
        #     birth_day=birth_day,
        #     gender=gender,
        #     email=email,
        #     name=name,
        #     age=age
        # )
        user = serializer.create(request.data)
        return Response(data=LoginUserSerializer(user).data)
        # data=LoginUserSerializer(user).data => 장고 model에는 data를 Json 형태로 뽑아내는 기능이 없다.
        # 따라서 이를 임의적으로 처리해줘야하는데 model -> json형태로 만드는 것이 LoginUserSerializer(user).data이다.
