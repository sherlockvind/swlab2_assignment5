from django import forms
import re

class FileForm(forms.Form):
	#_csv_file_name_regex = ".+\.csv"
	file = forms.FileField(required=True)
