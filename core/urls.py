from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'opportunities', OpportunityViewSet)
router.register(r'interactions', InteractionViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'customfields', CustomFieldViewSet)
router.register(r'emailtemplates', EmailTemplateViewSet)
router.register(r'workflowtriggers', WorkflowTriggerViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # ✅ Signup and Email Verification
    path('signup/', signup, name='signup'),
    path('verify-email/<str:token>/', verify_email, name='verify_email'),

    # ✅ JWT token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]