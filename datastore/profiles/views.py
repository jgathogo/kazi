from django.shortcuts import render, get_object_or_404
from .models import Firm

# Create your views here.

def firm_detail(request, firm_id):
    """
    Displays the details for a single firm.
    """
    firm = get_object_or_404(Firm, pk=firm_id)
    context = {'firm': firm}
    return render(request, 'profiles/firm_detail.html', context)
