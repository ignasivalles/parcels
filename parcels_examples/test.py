# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



from parcels import FieldSet, ParticleSet, JITParticle, AdvectionRK4, ErrorCode
from datetime import timedelta
import numpy as np

filenames = "GlobCurrent_example_data/20*.nc"
variables = {'U': 'eastward_eulerian_current_velocity',
             'V': 'northward_eulerian_current_velocity'}
dimensions = {'lat': 'lat',
              'lon': 'lon',
              'time': 'time'}
fieldset = FieldSet.from_netcdf(filenames, variables, dimensions)

lons, lats = np.meshgrid(range(15, 35), range(-40, -30))
pset = ParticleSet(fieldset=fieldset, pclass=JITParticle, lon=lons, lat=lats)

def DeleteParticle(particle, fieldset, time, dt):
    particle.delete()
    
for cnt in range(3):
    # First plot the particles
    pset.show(savefile='particles'+str(cnt).zfill(2), field='vector', land=True, vmax=2.0)
    
    # Then advect the particles for 6 hours
    pset.execute(AdvectionRK4,
                 runtime=timedelta(hours=6),  # runtime controls the interval of the plots
                 dt=timedelta(minutes=5),
                 recovery={ErrorCode.ErrorOutOfBounds: DeleteParticle})  # the recovery kernells