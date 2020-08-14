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
from django.urls import path

from essen.views.homeview import HomeView
from essen.views.dayview import DayView
from essen.views.essenview import EssenView
from essen.views.illnessview import IllnessView
from essen.views.calcview import CalcView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path(r'day/<int:day>/', DayView.as_view(), name='day'),
    path(r'essen/<str:essen>/', EssenView.as_view(), name='essen'),
    path(r'illness/<str:illness>/', IllnessView.as_view(), name='illness'),
    path(r'illness/<str:illness>/<str:details>/', IllnessView.as_view(), name='illness_detail'),
    path(r'auswertung/', CalcView.as_view(), name="calc"),
]