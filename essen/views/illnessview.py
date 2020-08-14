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
from essen.models.day import Day
from essen.views.homeview import HomeView
from essen import util


class IllnessView(HomeView):
    template_name = "essen/illness.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        details = "details" in kwargs
        context["details"] = details
        illness = kwargs["illness"]
        context["illness"] = illness
        days = [d for d in Day.objects.filter(illness__contains=illness) if illness in [x.strip() for x in d.illness.split('\n')]]
        context["matched_days"] = days

        if details:
            combos, foodcombos = util.calc(illness)
        else:
            combos, foodcombos = util.calc()
        context["matched_foods"] = []
        for food, illnesses in combos.items():
            if illness in illnesses and illnesses[illness][0] > 0:
                context["matched_foods"].append((food, *illnesses[illness]))
        context["matched_foods"] = sorted(context["matched_foods"], key=lambda x: x[1], reverse=True)
        context["foodcombos"] = foodcombos
        return context
