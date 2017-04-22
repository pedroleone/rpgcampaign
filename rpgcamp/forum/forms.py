from django import forms 

class AddTopicForm(forms.Form):
    title = forms.CharField(label='Título', max_length=250) 
    message = forms.CharField(label='Mensagem', widget=forms.Textarea(attrs={'data-provide': 'markdown', 'rows': '20'}))

class AddMessageForm(forms.Form):
    message = forms.CharField(label='Mensagem', widget=forms.Textarea(attrs={'data-provide': 'markdown', 'rows': '6'}))

class AddMessageSmallForm(forms.Form):
    message = forms.CharField(label='Mensagem', widget=forms.Textarea(attrs={'data-provide': 'markdown', 'rows': '4'}))
