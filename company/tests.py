from django.test import TestCase
from .models.bank_account import BankAccount
from .models.partner import Partner
from .models.company import Company


# Create your tests here.
class CompanyTestCase(TestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_bank_company_partner_created(self):
        company = Company.objects.create(
            name_last='Горун',
            name_first='Игорь',
            name_middle='Петрович',
            address_line_1='18 Vesnyaniy lane',
            itn='2944013075'
        )
        self.assertIsInstance(company, Company)
        self.assertEqual(str(company), "ФОП Горун И. П.")
        self.assertEqual(company.fop_name_full(), 'Фізична особа-підприємець Горун Игорь Петрович')
        self.assertEqual(company.single_tax_value, 5.0)

        company = Company.objects.get(itn='2944013075')
        bnk = BankAccount.objects.create(
            account_number='26006555262001',
            iban='UA03 326610 00000 266555262001',
            company=company
        )
        self.assertIsInstance(bnk, BankAccount)
        self.assertLessEqual(len(bnk.iban), 29)
        bnk2 = BankAccount.objects.create(
            account_number='260051555262001',
            iban='UA03 326610 00000 260051555262001',
            company=company
        )
        self.assertLessEqual(len(bnk2.iban), 29)
        for acc in company.bank_accounts.iterator():
            self.assertIsInstance(acc, BankAccount)

        feofania = Partner.objects.create(
            company=company,
            name='Феофания',
            address_line_1='Україна, 03143, м. Київ',
            address_line_2='вул. Академіка Заболотного, 21',
            representative_name_first='Андрей',
            representative_name_middle='Владимирович',
            representative_name_last='Крылов',
            representative_position='ITMan',
            itn='333221123'
        )
        self.assertIsInstance(feofania, Partner)
        feo_bnk_1 = BankAccount.objects.create(
            iban='ua 3 8820 1720 343140001000009636',
            bank_name='ДКСУ, м. Київ',
            partner=feofania
        )
        feo_bnk_2 = BankAccount.objects.create(
            iban='UA5 4820172 0343131001200009636',
            bank_name='ДКСУ, м. Київ',
            partner=feofania
        )
        for pacc in feofania.bank_accounts.iterator() :
            print("{} : {} : {}".format(pacc.iban, pacc.iban_readable(), pacc.account_number))
            self.assertIsInstance(pacc, BankAccount)
        for pacc in company.bank_accounts.iterator():
            print("{} : {} : {}".format(pacc.iban, pacc.iban_readable(), pacc.account_number))
            self.assertIsInstance(pacc, BankAccount)
