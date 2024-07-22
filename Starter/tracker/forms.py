from django import forms
from tracker.models import Transaction, Category
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Field, Field

class TransactionForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.RadioSelect(),
    )

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("El monto debe ser un número positivo")
        return amount
    
    class Meta:
        model = Transaction
        fields = (
            'category',
            'type',
            'amount',
            'description',
            'date'
        )
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class ContactForm(forms.Form):
    REASON_CHOICES = [
        ('', 'Selecciona un motivo'),
        ('general', 'General'),
        ('support', 'Soporte técnico'),
        ('feedback', 'Feedback'),
        ('other', 'Otro'),
    ]
    name = forms.CharField(label='Nombre', max_length=100, required=True)
    email = forms.EmailField(label='Email', required=True)
    reason = forms.ChoiceField(label='Motivo de contacto', choices=REASON_CHOICES, required=True)
    subject = forms.CharField(label='Asunto', max_length=200, required=False)
    message = forms.CharField(label='Mensaje', widget=forms.Textarea(attrs={'rows': 4}), required=True)
    subscribe = forms.BooleanField(label='Suscribirse para anuncios y promociones', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'border p-8'
        self.helper.label_class = 'text-white-400'
        self.helper.layout = Layout(
            Div(
                Div('name', css_class="md:w-[50%] text-white-200"),
                Div('reason', css_class="md:w-[50%] text-white-200"),
                css_class="md:flex md:justify-between"
            ),
            'subject',
            'message',
            'subscribe',
            Submit('submit', 'Submit', css_class='btn btn-outline btn-primary mt-4'),
        )