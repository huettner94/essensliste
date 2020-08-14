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
from datetime import timedelta
from bitarray import bitarray
import itertools


def _count_matches(fooddate, illnessdate, offset):
    illnessdate = illnessdate[offset:]
    illnessdate.extend([False] * offset)

    match = (fooddate & illnessdate).count()
    matchfood = fooddate.count()
    matchillness = illnessdate.count()
    total = (fooddate | illnessdate).count()

    if total == 0:
        return (0, 0, 0, 0, offset)
    return ((match/total)*100, match, matchfood, matchillness, total, offset)


def _get_matches(fooddate, illnessdate):
    MAX_OFFSET = 2
    output_possible = [None] * MAX_OFFSET
    for i in range(0, MAX_OFFSET):
        output_possible[i] = _count_matches(fooddate, illnessdate, i)
    return sorted(output_possible, key=lambda x: x[1], reverse=True)[0]


def calc(foodcombosfor=None):
    days = {day.date:
            (
                [x.strip() for x in day.food.split('\n') if x],
                [x.strip() for x in day.illness.split('\n') if x]
            ) for day in Day.objects.all()}
    
    firstday = Day.objects.order_by("date").first().date
    lastday = Day.objects.order_by("date").last().date
    daycount = (lastday - firstday).days

    foods = {}
    illnesses = {}
    for i in range(daycount):
        currday = firstday + timedelta(days=i)
        if currday in days:
            dayfoods, dayillnesses = days[currday]
            for food in dayfoods:
                if food not in foods:
                    foods[food] = bitarray([False] * daycount)
                foods[food][i] = True
            for illness in dayillnesses:
                if illness not in illnesses:
                    illnesses[illness] = bitarray([False] * daycount)
                illnesses[illness][i] = True
    
    combos = {}
    for food, fooddate in foods.items():
        combos[food] = {}
        for illness, illnessdate in illnesses.items():
            combos[food][illness] = _get_matches(fooddate, illnessdate)

    foodcombos = None
    if foodcombosfor is not None:
        illnessdate = illnesses[foodcombosfor]
        matches = []
        for combocount in [2, 3, 4]:
            for data in itertools.combinations(foods.items(), combocount):
                food = ", ".join([x[0] for x in data])
                dates = bitarray([False] * daycount)
                for _, fooddate in data:
                    dates = dates | fooddate
                matches.append((food, *_get_matches(dates, illnessdate)))
        foodcombos = sorted(matches, key=lambda x: x[1], reverse=True)[:5]

    return combos, foodcombos

