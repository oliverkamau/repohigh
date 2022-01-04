from django.db import models

from setups.academics.classes.models import SchoolClasses
from setups.academics.termdates.models import TermDates
from setups.accounts.bankbranches.models import BankBranches
from setups.accounts.paymentmodes.models import PaymentModes
from studentmanager.student.models import Students
from useradmin.users.models import User


class FeePayment(models.Model):
    payment_code = models.AutoField(primary_key=True)
    payment_date = models.DateTimeField()
    payment_docno = models.CharField(max_length=200, null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=13,decimal_places=2,default=0)
    payment_receiptno = models.CharField(max_length=200)
    payment_class = models.ForeignKey(SchoolClasses, on_delete=models.CASCADE)
    payment_student = models.ForeignKey(Students, on_delete=models.CASCADE)
    payment_capturedby = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_term = models.ForeignKey(TermDates, on_delete=models.CASCADE)
    payment_mode = models.ForeignKey(PaymentModes, on_delete=models.CASCADE)
    payment_bank = models.ForeignKey(BankBranches, on_delete=models.CASCADE)

