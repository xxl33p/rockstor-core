"""
Copyright (c) 2012-2013 RockStor, Inc. <http://rockstor.com>
This file is part of RockStor.

RockStor is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published
by the Free Software Foundation; either version 2 of the License,
or (at your option) any later version.

RockStor is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from django.db import models
from storageadmin.models import Share
from smart_manager.models import ShareUsage

class Snapshot(models.Model):
    """share which this snapshot belongs to"""
    share = models.ForeignKey(Share)
    """display name of the snapshot"""
    name = models.CharField(max_length=4096)
    """real name of the snapshot"""
    real_name = models.CharField(max_length=4096, default='unknownsnap')
    """read-only by default"""
    writable = models.BooleanField(default=False)
    """size of the snapshot"""
    size = models.IntegerField(default=0)
    toc = models.DateTimeField(auto_now=True)
    qgroup = models.CharField(max_length=100)
    uvisible = models.BooleanField(default=False)
    """replication, admin etc.."""
    snap_type = models.CharField(max_length=64, default='admin')

    def cur_rusage(self, *args, **kwargs):
        try:
            su = ShareUsage.objects.filter(name=self.real_name).order_by('-ts')[0]
            return su.r_usage
        except:
            return -1

    def cur_eusage(self, *args, **kwargs):
        try:
            su = ShareUsage.objects.filter(name=self.real_name).order_by('-ts')[0]
            return su.e_usage
        except:
            return -1

    class Meta:
        unique_together = ('share', 'name',)
        app_label = 'storageadmin'
