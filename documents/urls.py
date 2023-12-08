from django.urls import path, include
from documents.views.contract import ContractListView, ContractDetailView, ContractUpdateView, ContractCreateForPartnerView
from documents.views.sequence import SequenceListView, SequenceCreateView, SequenceUpdateView
from documents.views.completition import CompletitionListView, CompletitionUpdateView, CompletitionCreateForPartnerView, CompletitionCreateForContractView, CompletitionPrintView, CompletitionCreateForInvoiceView
from documents.views.invoice import InvoiceListView, InvoicePrintView, InvoiceUpdateView, InvoiceRemoveView, InvoiceCreateForContractFormView, InvoiceCreateForPartnerFormView

urlpatterns = [
    # Sequences
    path('seq/list/', SequenceListView.as_view(), name="sequence_list"),
    path('seq/create/', SequenceCreateView.as_view(), name="sequence_create"),
    path('seq/<int:pk>/modify/', SequenceUpdateView.as_view(), name="sequence_modify"),

    # Contracts
    path('contract/list/', ContractListView.as_view(), name="contract_list"),
    path('contract/create/partner/<int:partner_id>/',  ContractCreateForPartnerView.as_view(), name="contract_create_for_partner"),
    path('contract/<int:pk>/modify/', ContractUpdateView.as_view(), name="contract_modify", ),
    path('contract/<int:pk>/', ContractDetailView.as_view(), name="contract_detail", ),

    # Invoices
    path('invoice/list', InvoiceListView.as_view(), name='invoice_list'),
    path('invoice/create/partner/<int:partner_id>', InvoiceCreateForPartnerFormView.as_view(), name='invoice_create_for_partner'),
    path('invoice/create/contract/<int:contract_id>', InvoiceCreateForContractFormView.as_view(), name='invoice_create_for_contract'),
    path('invoice/<int:pk>/print/', InvoicePrintView.as_view(), name="invoice_print", ),
    path('invoice/<int:pk>/modify/', InvoiceUpdateView.as_view(), name="invoice_modify", ),
    path('invoice/<int:pk>/rm/', InvoiceRemoveView.as_view(), name="invoice_remove", ),

    # Completition certificates (Akts)
    path('completition/list/', CompletitionListView.as_view(), name="completition_list"),
    path('completition/create/partner/<int:partner_id>/', CompletitionCreateForPartnerView.as_view(),
         name="completition_create_for_partner"),
    path('completition/create/contract/<int:contract_id>/', CompletitionCreateForContractView.as_view(), name="completition_create_for_contract"),
    path('completition/create/invoice/<int:invoice_id>/', CompletitionCreateForInvoiceView.as_view(), name="completition_create_for_invoice"),
    path('completition/<int:pk>/modify/', CompletitionUpdateView.as_view(), name="completition_modify", ),
    path('completition/<int:pk>/print/', CompletitionPrintView.as_view(), name="completition_print", ),
]
