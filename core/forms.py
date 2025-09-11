

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'initial_balance']
