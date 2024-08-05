from django import forms
from .models import TasksModel, SubTasksModel
from accounts.models import CustomUser
from teams.models import TeamModels


class TaskForm(forms.ModelForm):
    team_id = forms.ModelChoiceField(
        queryset=TeamModels.objects.none(),
        required=True,
        label='チームID',
        empty_label="チームIDを選択してください",  
    )

    manager = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        required=True,
        label='責任者社員ID',
        empty_label="社員IDを選択してください",  
    )

    start_date =  forms.DateTimeField(
        label='開始',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True,
        )
    
    end_date =  forms.DateTimeField(
        label='期日',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True,
        )

    class Meta:
        model = TasksModel
        fields = ['team_id', 'name', 'description', 'start_date', 'end_date', 'manager']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # ユーザーを引数として取得
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['team_id'].queryset = TeamModels.objects.filter(members=user, is_delete=False)



class TaskUpdataForm(forms.ModelForm):

    start_date =  forms.DateTimeField(
        label='開始',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True,
        )
    
    end_date =  forms.DateTimeField(
        label='期日',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True,
        )

    class Meta:
        model = TasksModel
        fields = ['name', 'description', 'start_date', 'end_date','progress_status']





class SubTaskForm(forms.ModelForm):
    manager = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        required=True,
        label='担当社員ID',
        empty_label="社員IDを選択してください", 
    )

    task_id = forms.ModelChoiceField(
        queryset=TasksModel.objects.all(),
        required=True,
        label='タスクID',
        to_field_name='task_id',
        empty_label="タスクを選択してください",
    )

    start_date =  forms.DateTimeField(
        label='開始',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True,
        )

    end_date =  forms.DateTimeField(
        label='期日',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True,
    )

    class Meta:
        model = SubTasksModel
        fields = ['task_id', 'name', 'description', 'start_date', 'end_date', 'manager']



class SubTaskUpdataForm(forms.ModelForm):

    task_id = forms.ModelChoiceField(
        queryset=TasksModel.objects.all(),
        required=True,
        label='タスクID',
        to_field_name='task_id',
        empty_label="タスクを選択してください",
    )

    start_date =  forms.DateTimeField(
        label='開始',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True,
    )

    end_date =  forms.DateTimeField(
        label='期日',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True,
    )

    class Meta:
        model = SubTasksModel
        fields = ['task_id', 'name', 'description', 'start_date', 'end_date', 'progress_status']
