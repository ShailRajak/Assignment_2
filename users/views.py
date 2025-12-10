from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_user(request):

    # Check if data is a list (multiple users)
    if isinstance(request.data, list):
        many = True
    else:
        many = False

    serializer = UserSerializer(data=request.data, many=many)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "User(s) created successfully",
            "data": serializer.data
        }, status=201)

    return Response(serializer.errors, status=400)

@api_view(['PATCH'])
def update_user_partial(request, id):

    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    
    serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)

    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_users(request):

    ids = request.data.get("ids")

    # Step 1: Check if ids provided
    if ids is None:
        return Response({"error": "Please provide 'ids' field"}, status=400)

    # Step 2: If single integer is given → convert to list
    if isinstance(ids, int):
        ids = [ids]

    # Step 3: If still not a list → error
    if not isinstance(ids, list):
        return Response({"error": "'ids' must be a list or a single integer"}, status=400)

    # Step 4: Query and delete existing users
    users_to_delete = User.objects.filter(id__in=ids)
    count = users_to_delete.count()

    if count == 0:
        return Response({"message": "No matching users found"}, status=404)

    users_to_delete.delete()

    # Step 5: Final response
    return Response({
        "message": f"{count} user(s) deleted successfully",
        "deleted_ids": ids
    }, status=200)
