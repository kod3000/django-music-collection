from django import forms
from django.utils.html import format_html


class AlbumDataWidget(forms.Textarea):
    def render(self, name, value, attrs=None, renderer=None):
        # Ensures we have attrs and updates with specific classes
        if attrs is None:
            attrs = {}
        attrs.update({
                         'class': 'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6'})

        # Call the parent class's render method to get the textarea HTML
        textarea_html = super().render(name, value, attrs, renderer)

        # Wrap the textarea in the custom HTML structure
        html = format_html('''
            <div class="mx-auto mt-4 max-w-2xl">
                <form method="post">
                    <label for="{0}" class="block w-full text-left text-sm font-medium leading-6 text-gray-400">Add in Album Data</label>
                    <div class="mt-2">
                        {1}
                    </div>
                    <div class="flex-shrink-0 mt-2 w-full text-right">
                        <button type="submit" class="inline-flex items-center rounded-md bg-gray-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-gray-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600">Submit</button>
                    </div>
                </form>
            </div>
        ''', name, textarea_html)

        return html


class AlbumDataForm(forms.Form):
    array_data = forms.CharField(widget=AlbumDataWidget(attrs={'rows': 4, 'required': True}), label='')
