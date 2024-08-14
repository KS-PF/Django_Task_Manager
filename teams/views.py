from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import TeamModels
from accounts.models import CustomUser
from .forms import TeamForm
from django.views.generic import (
    TemplateView, ListView, UpdateView, DeleteView, DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import HttpResponseForbidden


class TeamListView(LoginRequiredMixin, TemplateView):
    template_name = 'teams/team_list.html'

    def __init__(self):
        self.param = {
            'error':'',
            'teams_with_members':None,
            'created_teams':None,
        }
    
    def get(self, request):
        user = request.user

        member_teams = TeamModels.objects.filter(members=user, is_delete=False)
        created_teams = TeamModels.objects.filter(creator=user)

        
        # 各チームのメンバー情報を取得
        teams_with_members = []
        for team in member_teams:
            members = team.members.all()
            teams_with_members.append({
                'team': team,
                'members': members
            })


        created_teams_with_members = []
        for created_team in created_teams:
            created_members = created_team.members.all()
            created_teams_with_members.append({
                'team': created_team,
                'members': created_members
            })

        #print(created_teams_with_members)
        self.param['teams_with_members'] = teams_with_members
        self.param['created_teams_with_members'] = created_teams_with_members
        return self.render_to_response(self.param)




class CreateTeam(LoginRequiredMixin, TemplateView):
    template_name='teams/_forms.html'

    def __init__(self):
        self.param = {
            'error':'',
            'title':'新規作成',
            'label':'作成する',
            'urlName':'teams:team_create',
            'forms':TeamForm,
        }
    
    def get(self, request):
        return self.render_to_response(self.param)
    
    def post(self, request):
        form = TeamForm(request.POST)

        if form.is_valid():
            new_team = form.save(commit=False)
            new_team.creator = request.user
            new_team.save()
            form.save_m2m()  # ManyToManyFieldの保存

            url = reverse('teams:message', kwargs={'type': 'create'})
            return redirect(url)

        self.param['forms'] = TeamForm(request.POST)#前のポスト内容を残す
        return self.render_to_response(self.param)
    


@login_required
def team_edit(request, pk):
    team = get_object_or_404(TeamModels, pk=pk)

    if team.creator != request.user:
        url = reverse('teams:message', kwargs={'type': 'permission_error'})
        return redirect(url)
    
    else:
        if request.method == 'POST':
            form = TeamForm(request.POST, instance=team)
            if form.is_valid():
                form.save()
                return redirect('teams:team_list')
        else:
            form = TeamForm(instance=team)

        delete_url = reverse('teams:delete_team', kwargs={'id':  team.team_id})

        return render(request, 'teams/edit_form.html', {'form': form, 'delete_url': delete_url, })



"""
データ削除
"""
@login_required
def delete_team(request, id):
    team = get_object_or_404(TeamModels, team_id=id)

    if team.creator == request.user:
        team.delete() 
        
        url = reverse('teams:message', kwargs={'type': 'delete_team'})
        return redirect(url)
    else:
        return HttpResponseForbidden("あなたはこのチームを削除する権限がありません。")
"""
データ削除
(＊＊終わり＊＊)
"""

"""
メッセージの表示
"""
@login_required
def message(request, type):
    title = 'もう一度やり直してください'
    text = ''
    label = '戻る'
    name = 'teams:team_list'

    if type == 'create':
        title = '登録が完了しました'
        text = 'チームの新規登録が完了しました。以下のボタンから戻ってください。'
    elif type == 'updata':
        title = '更新が完了しました'
        text = '更新が完了しました。以下のボタンから戻ってください。'
    elif type == 'permission_error':
        title = '権限がありません'
        text = 'もう一度やり直してください'
        label = 'ホームに戻る'
        name = 'tasks:index'
    elif type == 'delete_team':
        title = '削除完了'
        text = 'チームを削除しました'
        label = '戻る'

    view_url = reverse(name)
    context ={
        "title":title,
        "text":text,
        "label":label,
        "url": view_url,
        }
    return render(request, 'tasks/message.html', context )
"""
メッセージの表示
(＊＊終わり＊＊)
"""