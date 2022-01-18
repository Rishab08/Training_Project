import json
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from Test import functions
from Test.models import Test
from Test.serializers import TestSerializer
from tablib import Dataset

from accounts.models import CustomUser


class TestAPI(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = []
    serilizer_class = TestSerializer

    def post(self, request):
        serializer = self.serilizer_class(data=request.data)
        if serializer.is_valid():
            test_excel_file = request.FILES['myfile']
            print(test_excel_file)
            tested_file = functions.run_tests(test_excel_file)
            tested_file.reset_index(drop=True, inplace=True)
            data = tested_file.to_json(orients="records")
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def HomeView(request):
    if request.method == "POST":
        value = {}
        all = ' '

        if request.FILES:
            print("hello")

            test_excel_file = request.FILES['myfile']
            print(test_excel_file)
            # test_result_data = TestAPI.as_view()(request=request).data
            dataset = Dataset()
            imported_data = dataset.load(test_excel_file.read(), format='xlsx')
            for data in imported_data:
                value = CustomUser.objects.create_user(email=data[0],
                                                       username=data[1],
                                                       phone=data[3],
                                                       date_of_birth=data[4],
                                                       test_res=True)
                value.set_password(data[2])


            value.save()
            all = CustomUser.objects.all()

        return render(request, 'admin/Test/rchange.html', {"value": all}, )

    return render(request, 'admin/Test/change.html')
