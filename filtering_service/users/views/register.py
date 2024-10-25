from rest_framework.response import Response
from rest_framework import status, permissions, parsers, generics

from filtering_service.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema
from users.serializers.register_serializer import RegisterSerializer


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
    parser_classes = [parsers.JSONParser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


RegisterAPI = apply_swagger_auto_schema(
    tags=['auth / register'], excluded_methods=[]
)(RegisterAPI)
