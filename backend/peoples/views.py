from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend


from peoples.models import Member
from peoples.serializers import MemberCreateSerializer, MemberDetailSerializer
from peoples.permissions import IsSameBranch


class MemberListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["team", "branch", "is_active", "gender"]
    search_fields = ["=nid_number", "=mobile_number"]

    def get_queryset(self):
        return Member.objects.filter(branch=self.request.user.staff.branch)

    def perform_create(self, serializer):
        serializer.save(branch=self.request.user.staff.branch)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return MemberCreateSerializer
        return MemberDetailSerializer


class MemberDetailsView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsSameBranch]
    serializer_class = MemberDetailSerializer

    def get_queryset(self):
        return Member.objects.filter(branch=self.request.user.staff.branch)
