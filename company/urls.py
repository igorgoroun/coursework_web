from django.urls import path, include
from .views import company, employee, partner, representative

urlpatterns = [
    # Company
    path('create/', company.CompanyCreateView.as_view(), name="create_company"),
    path('<int:pk>/modify/', company.CompanyUpdateView.as_view(), name="modify_company"),
    # Employee self modify
    path('employee/modify/', employee.EmployeeSelfUpdateView.as_view(), name="modify_employee"),
    # Partner
    path('partner/list/', partner.PartnerListView.as_view(), name="partner_list"),
    path('partner/create/', partner.PartnerCreateView.as_view(), name="partner_create"),
    path('partner/<int:pk>/modify/', partner.PartnerUpdateView.as_view(), name="partner_modify"),
    path('partner/<int:pk>/', partner.PartnerDetailsView.as_view(), name="partner_details"),
    # Partner's representative
    path('representative/create/<int:partner_id>/', representative.PartnerRepresentativeCreateView.as_view(), name="representative_create"),
    path('representative/<int:pk>/modify/', representative.PartnerRepresentativeUpdateView.as_view(), name="representative_modify"),
    path('representative/list/<int:partner_id>/', representative.PartnerRepresentativeListView.as_view(), name="representative_list"),

]
