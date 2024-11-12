from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView,DetailView
from . models import Result
import plotly
import plotly.graph_objs as go
import plotly.express as px
import plotly.offline as pyo
from django.db.models import Count
from collections import Counter




# Create your views here.
class ResultDetailView(DetailView):
    template_name = "voter_analytics/result_detail.html"
    model = Result
    context_object_name = 'r'
class ResultsListView(ListView):
    template_name = 'voter_analytics/results.html'
    model = Result
    context_object_name = 'results'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Generate a list of years from 2023 to 1900
        context['year_range'] = range(2023, 1899, -1)  # descending from 2023 to 1900
        context['score_range'] = range(0, 6)  # Score range from 0 to 5

        return context
    
    def get_queryset(self):
        qs = super().get_queryset()

         
    
       # Filter by party affiliation if provided
        affiliation = self.request.GET.get('affiliation')
        if affiliation:
            qs = qs.filter(Affiliation=affiliation)

        # Filter by minimum date of birth year if provided
        min_dob = self.request.GET.get('min_dob')
        if min_dob:
            try:
                min_dob_year = int(min_dob)
                qs = qs.filter(DOB__year__gte=min_dob_year)
            except ValueError:
                pass  # Ignore if conversion to int fails

        # Filter by maximum date of birth year if provided
        max_dob = self.request.GET.get('max_dob')
        if max_dob:
            try:
                max_dob_year = int(max_dob)
                qs = qs.filter(DOB__year__lte=max_dob_year)
            except ValueError:
                pass  # Ignore if conversion to int fails

        # Filter by voter score if provided
        voter_score = self.request.GET.get('voter_score')
        if voter_score:
            try:
                voter_score = int(voter_score)
                qs = qs.filter(VoterS=voter_score)
            except ValueError:
                pass  # Ignore if conversion to int fails

        # Filter by specific election participation if provided
        if self.request.GET.get('v20state') == 'true':
            qs = qs.filter(v20state=True)
        if self.request.GET.get('v21town') == 'true':
            qs = qs.filter(v21town=True)
        if self.request.GET.get('v21primary') == 'true':
            qs = qs.filter(v21primary=True)
        if self.request.GET.get('v22general') == 'true':
            qs = qs.filter(v22general=True)
        if self.request.GET.get('v23town') == 'true':
            qs = qs.filter(v23town=True)

        return qs
class GraphsView(ListView):
    model = Result
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Histogram: Distribution by Year of Birth
        dob_data = self.model.objects.values_list('DOB', flat=True)
        birth_years = [dob.year for dob in dob_data if dob]
        birth_year_hist = go.Figure(data=[go.Histogram(
            x=birth_years,
            nbinsx=30  # Set number of bins
        )])
        birth_year_hist.update_layout(
            title="Distribution of Voters by Year of Birth",
            xaxis_title="Year of Birth",
            yaxis_title="Count"
        )
        context['birth_year_hist'] = pyo.plot(birth_year_hist, auto_open=False, output_type="div")

        # Pie Chart: Distribution by Party Affiliation
        party_data = self.model.objects.values_list('Affiliation', flat=True)
        party_counts = Counter(party_data)
        party_aff_pie = go.Figure(data=[go.Pie(
            labels=list(party_counts.keys()),
            values=list(party_counts.values())
        )])
        party_aff_pie.update_layout(title="Distribution of Voters by Party Affiliation")
        context['party_aff_pie'] = pyo.plot(party_aff_pie, auto_open=False, output_type="div")

        # Histogram: Participation in Elections
        election_data = {
            '2020 State': self.model.objects.filter(v20state=True).count(),
            '2021 Town': self.model.objects.filter(v21town=True).count(),
            '2021 Primary': self.model.objects.filter(v21primary=True).count(),
            '2022 General': self.model.objects.filter(v22general=True).count(),
            '2023 Town': self.model.objects.filter(v23town=True).count(),
        }

        election_hist = go.Figure(data=[go.Bar(
            x=list(election_data.keys()),
            y=list(election_data.values())
        )])
        election_hist.update_layout(
            title="Voter Participation by Election",
            xaxis_title="Election",
            yaxis_title="Count"
        )
        context['election_hist'] = pyo.plot(election_hist, auto_open=False, output_type="div")

        return context
