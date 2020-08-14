#
# Copyright (c) 2023 Felix Huettner.
#
# This file is part of Essensliste 
# (see https://github.com/huettner94/essensliste).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from django.views.generic import TemplateView
from essen.forms.dayaddform import DayAddForm
from essen.models.day import Day
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect


class HomeView(TemplateView):
    template_name = "essen/home.html"

    dayaddform = None

    def post(self, request, *args, **kwargs):
        self.dayaddform = DayAddForm(request.POST)
        if self.dayaddform.is_valid():
            try:
                day = Day(date=self.dayaddform.cleaned_data["day"])
                day.save()
                return HttpResponseRedirect("/day/%s/" % day.id)
            except IntegrityError:
                self.dayaddform.add_error("day", "Day already exists")
        return self.get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dayaddform"] = self.dayaddform or DayAddForm()
        days = Day.objects.order_by("-date")
        context["days"] = days
        context["foods"] = sorted(set([item.strip() for sublist in days for item in sublist.food.split('\n') if item]))
        context["illnesses"] = sorted(set([item.strip() for sublist in days for item in sublist.illness.split('\n') if item]))
        return context
    
