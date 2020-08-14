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
import itertools
import copy


# Erbsen gegessen 01.05., 25.05
# Verdauung gut am 02.05. und 03.05
# Verdauung schlecht am 26.05
# Fazit: Erbsen sind nicht verdächtig

# Erbsen gegessen 01.05., 25.05
# Verdauung gut am 02.05. und 03.05
# Verdauung schlecht am 01.05 und 26.05
# Fazit: Erbsen sind nicht verdächtig

# Erbsen gegessen 01.05., 25.05
# Verdauung schlecht am 30.04, 01.05, 02.05, 03.05
# Fazit: Erbsen werden in diesem Zeitraum nicht ausgewertet, sind somit grundsätzlich nicht verdächtig

# CONFIGURATION CONSTANTS
CONSECUTIVE_DAYS_AFTER_BAD_GOES_TO_UNKOWN = 1
MINIMUM_GOOD_DAY_FOR_FOOD_TO_BE_GOOD = 2
FOOD_TO_ILLNESS_OFFSET = 1  # in days

# State constants
GOOD = 1
MEDIUM = 2
BAD = 3
UNKOWN = 4


def state_number_to_string(state):
    if state == GOOD:
        return "good"
    elif state == MEDIUM:
        return "medium"
    elif state == BAD:
        return "bad"
    else:
        return "unknown"


class CalcView(HomeView):
    template_name = "essen/calc.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        days = [(
            day.date,
            [x.strip() for x in day.food.split('\n') if x],
            [x.strip() for x in day.illness.split('\n') if x]
        ) for day in Day.objects.order_by("date").all()]
        firstday = Day.objects.order_by("date").first().date
        lastday = Day.objects.order_by("date").last().date
        daycount = (lastday - firstday).days

        if daycount+1 != len(days):
            context["error"] = "The stored daterange is %s days (between %s and %s). However we only have data for %s days." % (daycount+1, firstday, lastday, len(days))
            return context

        # Prepare list of days regarding the illness state
        days_illness = list([GOOD] * daycount)
        for i in range(daycount):
            for symptom in days[i][2]:
                symptom = symptom.lower()
                if symptom.startswith("verdauung"):
                    if "mittel" in symptom:
                        days_illness[i] = MEDIUM
                    elif "schlecht" in symptom:
                        days_illness[i] = BAD
                    elif "keine-ahnung-mehr" in symptom:
                        days_illness[i] = UNKOWN

        # Remove >2 consecutive days with the illness
        days_illness_limited = copy.deepcopy(days_illness)
        for i in range(daycount):
            if days_illness_limited[i] in [MEDIUM, BAD]:
                breakout = False
                # We just filter out the days which need to be bad before it becomes unkown
                for j in range(i + 1, min(i + CONSECUTIVE_DAYS_AFTER_BAD_GOES_TO_UNKOWN, daycount)):
                    if days_illness_limited[j] not in [MEDIUM, BAD]:
                        breakout = True
                        break
                if not breakout:
                    for j in range(i+CONSECUTIVE_DAYS_AFTER_BAD_GOES_TO_UNKOWN, daycount):
                        if days_illness_limited[j] in [MEDIUM, BAD]:
                            days_illness_limited[j] = UNKOWN
                        else:
                            break

        context["day_states"] = [(days[i][0], state_number_to_string(days_illness_limited[i])) for i in range(daycount)]

        # now check if foods are fine
        foods = list({x for x in itertools.chain.from_iterable([day[1] for day in days])})
        food_good = []
        food_medium_or_bad = []
        food_bad = []
        food_unkown = []

        for food in foods:
            goodcount = 0
            medium_or_bad_days = []
            bad_days = []

            for i in range(daycount):
                if food in days[i][1]:
                    if i+FOOD_TO_ILLNESS_OFFSET < daycount:
                        if days_illness_limited[i+FOOD_TO_ILLNESS_OFFSET] == GOOD:
                            goodcount += 1
                        elif days_illness_limited[i+FOOD_TO_ILLNESS_OFFSET] in [BAD, MEDIUM]:
                            medium_or_bad_days.append(days[i][0])
                        if days_illness[i+FOOD_TO_ILLNESS_OFFSET] == BAD and days_illness[i] in [GOOD, MEDIUM]:
                            bad_days.append(days[i][0])
            if goodcount >= MINIMUM_GOOD_DAY_FOR_FOOD_TO_BE_GOOD:
                food_good.append(food)
            # triggering bad is more important than filtered medium or bad
            else:
                if len(bad_days) > 0:
                    food_bad.append((food, bad_days))
                elif len(medium_or_bad_days) > 0:
                    food_medium_or_bad.append((food, medium_or_bad_days))
                else:
                    food_unkown.append(food)

        context["food_good"] = sorted(food_good)
        context["food_medium_or_bad"] = sorted(food_medium_or_bad, key=lambda x: x[0])
        context["food_bad"] = sorted(food_bad, key=lambda x: x[0])
        context["food_unkown"] = sorted(food_unkown)

        return context
