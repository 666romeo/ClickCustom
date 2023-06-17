from django import forms
from django.forms.widgets import ClearableFileInput
from products.models import Product
from django.forms.widgets import ClearableFileInput, CheckboxInput
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class MultipleFileInput(ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        attrs['multiple'] = 'multiple'
        return super().render(name, value, attrs, renderer)

    def render_checkbox(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        checkbox_name = self.clear_checkbox_name(name)
        checkbox_id = self.clear_checkbox_id(checkbox_name)
        checkbox = CheckboxInput(attrs, check_test=lambda value: False)
        option_label = mark_safe('Удалить все загруженные фотографии')
        return format_html(
            '<label for="{0}" class="clearable-file-input">'
            '<span class="checkbox">{1}</span> {2}'
            '</label>',
            checkbox_id,
            checkbox.render(checkbox_name, False),
            option_label,
        )


class ProductImagesForm(forms.ModelForm):
    images = forms.ImageField(widget=MultipleFileInput(attrs={'class': 'your-css-class', 'required': 'True'}))

    class Meta:
        model = Product
        fields = ['images']