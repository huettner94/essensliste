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
from essen.forms.dayeditform import DayEditForm
from essen.models.day import Day
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from essen.views.homeview import HomeView


class DayView(HomeView):
    template_name = "essen/day.html"

    dayeditform = None

    def post(self, request, *args, **kwargs):
        self.dayeditform = DayEditForm(request.POST)
        day = Day.objects.get(id=kwargs["day"])
        if request.GET.get("delete") == "true":
            day.delete()
            return HttpResponseRedirect("/")
        if self.dayeditform.is_valid():
            try:
                day.food = self.dayeditform.cleaned_data["food"]
                day.illness = self.dayeditform.cleaned_data["illness"]
                day.note = self.dayeditform.cleaned_data["note"]
                day.save()
            except IntegrityError:
                self.dayeditform.edit_error("day", "Day has issues")
        return HttpResponseRedirect(request.path_info)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        day = Day.objects.get(id=kwargs["day"])
        context["dayeditform"] = self.dayeditform
        if context["dayeditform"] is None:
            context["dayeditform"] = DayEditForm(initial={
                "food": day.food,
                "illness": day.illness,
                "note": day.note
            })
        context["day"] = day
        return context
