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


class EssenView(HomeView):
    template_name = "essen/essen.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        food = kwargs["essen"]
        context["food"] = food
        days = [d for d in Day.objects.filter(food__contains=food) if food in [x.strip() for x in d.food.split('\n')]]
        context["matched_days"] = days

        combos, _ = util.calc()
        context["matched_illness"] = []
        for illness, illnessvalues in combos.get(food, {}).items():
            if illnessvalues[0] > 0:
                context["matched_illness"].append((illness, *illnessvalues))
        context["matched_illness"] = sorted(context["matched_illness"], key=lambda x: x[1], reverse=True)
        return context
