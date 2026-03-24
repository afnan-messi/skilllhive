from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ResearchPaper, PaperReview, Discussion
from .forms import ResearchPaperForm, PaperReviewForm, DiscussionForm
from django.contrib import messages
from django.db.models import Avg, Count
from django.db import models

@login_required
def research_hub(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    papers = ResearchPaper.objects.all().annotate(avg_rating=Avg('reviews__rating'), review_count=Count('reviews'))
    
    if query:
        papers = papers.filter(models.Q(title__icontains=query) | models.Q(abstract__icontains=query))
    if category:
        papers = papers.filter(category=category)
        
    categories = ResearchPaper.CATEGORIES
    return render(request, 'research_hub.html', {'papers': papers, 'categories': categories, 'query': query, 'selected_category': category})

@login_required
def upload_paper(request):
    if request.method == 'POST':
        form = ResearchPaperForm(request.POST, request.FILES)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.author = request.user
            paper.save()
            
            # Gamification: +20 points
            profile = request.user.profile
            profile.points += 20
            profile.save()
            
            messages.success(request, "Research paper uploaded successfully! +20 points earned.")
            return redirect('research_hub')
    else:
        form = ResearchPaperForm()
    return render(request, 'upload_paper.html', {'form': form})

@login_required
def paper_detail(request, paper_id):
    paper = get_object_or_404(ResearchPaper, id=paper_id)
    reviews = paper.reviews.all()
    discussions = paper.discussions.all()
    
    review_form = PaperReviewForm()
    discussion_form = DiscussionForm()
    
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    if request.method == 'POST':
        if 'submit_review' in request.POST:
            r_form = PaperReviewForm(request.POST)
            if r_form.is_valid():
                review = r_form.save(commit=False)
                review.paper = paper
                review.reviewer = request.user
                review.save()
                
                # Gamification: +10 points for reviewing
                profile = request.user.profile
                profile.points += 10
                profile.save()
                
                # Points to author for good ratings (rating >= 4)
                if review.rating >= 4:
                    author_profile = paper.author.profile
                    author_profile.points += 15
                    author_profile.save()
                
                messages.success(request, "Review submitted! Points rewarded.")
                return redirect('paper_detail', paper_id=paper_id)
        
        elif 'submit_discussion' in request.POST:
            d_form = DiscussionForm(request.POST)
            if d_form.is_valid():
                comment = d_form.save(commit=False)
                comment.paper = paper
                comment.user = request.user
                comment.save()
                return redirect('paper_detail', paper_id=paper_id)

    return render(request, 'paper_detail.html', {
        'paper': paper,
        'reviews': reviews,
        'discussions': discussions,
        'review_form': review_form,
        'discussion_form': discussion_form,
        'avg_rating': avg_rating
    })

@login_required
def research_leaderboard(request):
    from django.contrib.auth.models import User
    # Calculating research specific points for the leaderboard
    contributors = User.objects.filter(papers__isnull=False).distinct().annotate(
        paper_count=Count('papers', distinct=True),
        review_count=Count('paperreview', distinct=True)
    )
    
    # We'll calculate the score manually in a list if annotation is complex, 
    # but let's try a simple estimate for display.
    # Actually, let's just use their profile points for now but order by research activity.
    contributors = contributors.order_by('-paper_count')[:10]
    
    return render(request, 'research_leaderboard.html', {'contributors': contributors})
