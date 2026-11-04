from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Project, Atelier
from main.permissions import IsPortfolioOwnerOrReadOnly, IsPortfolioOwnerOrEditorOrReadOnly
from main.serializers import ProjectSerializer, AtelierSerializer


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_list(request):
    if request.method in ("GET", "HEAD"):
        projects = (
            Project.objects.prefetch_related("starred_by").order_by("title", "id")
        )
        title = request.query_params.get("title", "").strip()
        if title:
            projects = projects.filter(title__icontains=title)
        serializer = ProjectSerializer(
            projects, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = ProjectSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related("starred_by"), pk=project_id,
    )
    if request.method in ("GET", "HEAD"):
        serializer = ProjectSerializer(project, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ProjectSerializer(
        project, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)
    serializer = ProjectSerializer(project, context={"request": request})
    return Response(serializer.data)


# --- ATELIER API VIEWS (Assignment Section with Editor Role) ---
@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def atelier_list(request):
    if request.method in ("GET", "HEAD"):
        ateliers = (
            Atelier.objects.prefetch_related("starred_by").order_by("title", "id")
        )
        title = request.query_params.get("title", "").strip()
        if title:
            ateliers = ateliers.filter(title__icontains=title)
        serializer = AtelierSerializer(
            ateliers, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = AtelierSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def atelier_detail(request, atelier_id):
    atelier = get_object_or_404(
        Atelier.objects.prefetch_related("starred_by"), pk=atelier_id,
    )
    if request.method in ("GET", "HEAD"):
        serializer = AtelierSerializer(atelier, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        if not request.user.is_superuser:
            return Response(
                {"detail": "Only the portfolio owner can delete projects."},
                status=status.HTTP_403_FORBIDDEN,
            )
        atelier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = AtelierSerializer(
        atelier, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def atelier_star(request, atelier_id):
    atelier = get_object_or_404(Atelier, pk=atelier_id)
    if atelier.starred_by.filter(pk=request.user.pk).exists():
        atelier.starred_by.remove(request.user)
    else:
        atelier.starred_by.add(request.user)
    serializer = AtelierSerializer(atelier, context={"request": request})
    return Response(serializer.data)
