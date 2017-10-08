from django import forms


class MultiSelectWidget(forms.widgets.CheckboxSelectMultiple):
    template_name = 'widgets/multiple_select.html'
