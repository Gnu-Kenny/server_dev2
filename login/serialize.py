from rest_framework import serializers
from .models import LoginUser
from django.contrib.auth.hashers import make_password


class LoginUserSerializer(serializers.ModelSerializer):
    # serializer를 이용해 모델 만들때 어떤 식의 로직이 들어갈지 넣는 부분 validated_data:직렬화된 데이터
    def create(self, validated_data):
        validated_data['user_pw'] = make_password(validated_data['user_pw'])
        # 실제 create하는 부분 클라에서 넘어오는 (**validated_data) 데이터를 DB에 추가
        user = LoginUser.objects.create(**validated_data)
        return user

    def validate(self, attrs):
        return attrs

    class Meta:
        model = LoginUser
        fields = ('user_id', 'user_pw', 'birth_day',
                  'gender', 'email', 'name', 'age')  # 모델 전체 필드를 사용하지 않아도 된다. 한 모델당 serializer가 여러개일수있다.
