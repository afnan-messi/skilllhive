from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserSkillForm
from .models import UserSkill
from users.models import Activity

@login_required
def skills_page(request):
    skills = UserSkill.objects.all().select_related('user')
    return render(request, 'skills/skills.html', {'skills': skills})

@login_required
def add_skill_view(request):
    if request.method == 'POST':
        form = UserSkillForm(request.POST, request.FILES)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            
            # Update user points
            profile = request.user.profile
            profile.points += 10
            profile.save()
            
            # Log activity
            Activity.objects.create(
                user=request.user,
                action=f"Added {skill.skill_name} as a {skill.skill_type} skill"
            )
            
            return redirect('profile')
    else:
        form = UserSkillForm()
    
    return render(request, 'add_skill.html', {'form': form})
