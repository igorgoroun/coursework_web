from django.urls import path
from .views import (
    CompanyBankAccountCreateView,
    CompanyBankAccountUpdateView,
    PartnerBankAccountCreateView,
    PartnerBankAccountUpdateView,
)

urlpatterns = [
    path(
        "create/company/",
        CompanyBankAccountCreateView.as_view(),
        name="create_company_bank_account",
    ),
    path(
        "create/partner/<int:partner_id>/",
        PartnerBankAccountCreateView.as_view(),
        name="create_partner_bank_account",
    ),
    path(
        "modify/<int:pk>/company/",
        CompanyBankAccountUpdateView.as_view(),
        name="company_bank_account_modify",
    ),
    path(
        "modify/<int:pk>/partner/",
        PartnerBankAccountUpdateView.as_view(),
        name="partner_bank_account_modify",
    ),
]
