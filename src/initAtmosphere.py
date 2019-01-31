from scipy import interpolate
import numpy as np
import settings as s
import pdb
from matplotlib import pyplot as pp
import inputs

def log_interp1d(xx, yy, kind='linear',fill_value=''):
    logy = np.log10(yy)
    lin_interp = interpolate.interp1d(xx, logy,\
        kind=kind,fill_value=fill_value)
    log_interp = lambda zz: np.power(10.0, lin_interp(zz))

    return log_interp

def getOHComposition(altitude):
    #NO2 and OH profiles taken from Cunnold et al. 1975
    OHDensity = [1.2e6,1.1e7]
    OHAltitudes = [i*1e5 for i in [70,41.5]]
    tempden = [0]*len(altitude)

    func1 = log_interp1d(OHAltitudes[0:2], \
        OHDensity[0:2],fill_value="extrapolate")
    tempden = func1(altitude)

    return tempden

def getNOComposition(altitude):
    #NO2 and OH profiles taken from Cunnold et al. 1975

    NO2Density = [1e5,2e8,3e9,1.45e9,1.1e9,1.25e9,1e10]
    NO2Altitudes = [i*1.e5 for i in [58,42,26,18,12,11,5]]

    #linear between 0,1; parabolic between 1-3; linear 3-4
    tempden = [0]*len(altitude)
    funchigh = log_interp1d(NO2Altitudes[0:2],
        NO2Density[0:2],fill_value="extrapolate")
    funclow = log_interp1d(NO2Altitudes[5:7],
        NO2Density[5:7],fill_value="extrapolate")
    funcmiddle1 = \
        log_interp1d(NO2Altitudes[1:4],\
            NO2Density[1:4],kind='quadratic')
    funcmiddle2 = \
        log_interp1d(NO2Altitudes[3:6],\
            NO2Density[3:6],kind='quadratic')



    for iAlt in range(len(altitude)):

        if altitude[iAlt] >= NO2Altitudes[1]:
            tempden[iAlt] = funchigh(altitude[iAlt])

        elif altitude[iAlt] < NO2Altitudes[1] and \
            altitude[iAlt] >= NO2Altitudes[3]:
            tempden[iAlt] = float(funcmiddle1(altitude[iAlt]))

        elif altitude[iAlt] < NO2Altitudes[3] and \
            altitude[iAlt] >= NO2Altitudes[5]:
            tempden[iAlt] = float(funcmiddle2(altitude[iAlt]))

        elif altitude[iAlt] < NO2Altitudes[5]:
            tempden[iAlt] = funclow(altitude[iAlt])


    return tempden

def initializeAtmosphere(f):
    input_data = inputs.readInputData(f)

    Pressure=[0*i for i in s.Temperature]
    nDensity=[0*i for i in s.Temperature]
    #Build up background atmosphere
    Pressure[-1]=inputs.pressure*1013250 #Barye
    #1 KPa = 1e5 Barye

    nDensity[-1]=(Pressure[-1]/s.consts['k_B']/s.Temperature[-1])
    #assume only O2 and N2

    mu=(32.*inputs.O2mixingratio+28.*(1.-inputs.O2mixingratio))
    s.R_star= inputs.rStar*s.consts['R_sun']
    s.D_pl=inputs.distancePlanet*s.consts['au']
    s.R_pl=inputs.rPlanet*s.consts['R_earth']
    s.M_pl=inputs.massPlanet*s.consts['M_earth']
    s.tstar=inputs.tStar
    s.tEnd = inputs.tEnd*86400.
    s.g=s.consts['G']*s.M_pl/s.R_pl/s.R_pl #cm s-2
    Hsca=(s.consts['k_B']*np.mean(s.Temperature)/(mu*  \
        s.consts['protonmass']*s.g))#cm

    # valori planetari e stellari

    s.P=[Pressure[-1]*np.exp(-z/Hsca) for z in s.Altitude]
    s.N=[(nDensity[-1]*np.exp(-z/Hsca)) for z in s.Altitude]

    s.O2=[inputs.O2mixingratio*i for i in s.N]
    s.N2=[(1.-inputs.O2mixingratio)*i for i in s.N]
    s.O3=[1e6]*len(s.Altitude)
    s.O=[1e9]*len(s.Altitude)
    s.NO2 = getNOComposition(s.Altitude)
    s.NO =[1e9]*len(s.Altitude)
    s.OH = getOHComposition(s.Altitude)

    # s.density = np.zeros((nlayers,nMajorSpecies))
    # for ispecies in range(len(s.nMajorSpecies)):
    #     for ialt = in range(nlayers):
    #         s.density[ialt,ispecies] =


    return 0