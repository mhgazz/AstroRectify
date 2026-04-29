from utils import *
from datetime import date, timedelta
import math
import logging
import sys

class Rectifier:
    """ Rectifier  """
    native_dates = {}
    birth_y = 0
    birth_m = 0
    birth_d = 0
    MC_adjust=[]
    logger = None
    orbe_tolerance : float = 1.0
    objects = {}
    geograph_long = 0   #birth location geoghaphic longitude decimal
    HS_GMT = 0          #sideral hour greenwich midnight taken from ephemerides
    GMT_Hour =0         #time zone GMT 

    def __init__(self):
 
        self.logger = logging.getLogger("AstroRectify")
        self.logger.setLevel(level=logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File Handler
        file_handler = logging.FileHandler("AstroRectify.log")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def set_HS_GMT(self,HS_GMT:float):
        self.HS_GMT = HS_GMT

    def set_GMT_Hour(self,GMT_Hour:int):
        self.GMT_Hour = GMT_Hour

    def set_geograph_long(self,hemis:str,degrees:int,mins:int,secs:int):
        """set geographic location logingitude for west o east use W or E"""
        if hemis=="W":
            dec_longitude = -convert_angle_decimal(degrees,mins,secs)
        else:
            dec_longitude = convert_angle_decimal(degrees,mins,secs)

        self.logger.debug(f'longitud geografica {hemis} {dec_longitude}')
        self.geograph_long = dec_longitude
        

    def set_radix_bithdate(self,year:int,month:int,day:int):
        self.birth_y = year
        self.birth_m = month
        self.birth_d = day

    def add_event(self,event_title:str,event_year:int,event_month:int,event_day:int):
        delta_days = dateptrdiffs(self.birth_y, self.birth_m, self.birth_d, event_year, event_month,event_day)
        direction_arc = get_direction_arc(delta_days)
        self.native_dates[event_title]=direction_arc
        self.logger.debug(f'days {delta_days} direction arc: {direction_arc}')

    def add_object(self,object:natal_chart_object):
        self.objects[object.name] = object.ecliptic_longitude

    def calculate(self):
        """main logic for calculation"""
        
        MC_adjust=[]
        #colocar MC en long ecliptica absoluta
        RAMC_radix = get_RAMC(self.birth_y,self.birth_m,self.birth_d)

        #iterate on given events
        for cur_event in self.native_dates:
            cur_arc = self.native_dates[cur_event]
            self.logger.info(f'\n\n--- rectificando para arco {cur_arc} {cur_event} ----')

            # direccionar el arco sobre el MC
            direct = RAMC_radix + cur_arc
            converse = RAMC_radix - cur_arc
            self.logger.info(f'direct: {direct}')
            self.logger.info(f'converse: {converse}')

            for cur_object in self.objects.keys():
                object_ecliptic_long = self.objects.get(cur_object)
                self.logger.debug(f'processing {cur_object} {str(object_ecliptic_long)}')

                eclep_longitude_direct = get_ecliptic_longitude(direct)
                eclep_longitude_converse = get_ecliptic_longitude(converse)
                self.logger.debug(f'direct Ecliptic longitude: {eclep_longitude_direct}')
                self.logger.debug(f'converse Ecliptic longitude: {eclep_longitude_converse}')

                direct_diff = eclep_longitude_direct - object_ecliptic_long
                converse_diff = eclep_longitude_converse - object_ecliptic_long

                self.logger.debug(f'direct diff: {direct_diff}')
                self.logger.debug(f'converse diff: {converse_diff}')

                self.logger.debug(f'identificando aspectos con {cur_object} radical')
                aspects = identify_aspect(direct_diff)
                
                if len(aspects)>0:
                    self.logger.info(f'MC ecliptica {eclep_longitude_direct}')
                    self.logger.info(f'{cur_object} {object_ecliptic_long} 🎯 aspects: {aspects[0]} orbe')
                    adhj_eclep_longitude_dir = eclep_longitude_direct + aspects[0]
                    g,m,s = get_angle_sexag(adhj_eclep_longitude_dir)
                    temp_ramc = get_RAMC(g, m, s)
                    self.logger.info(f'MC RA directo ajustada {temp_ramc}')
                    adj_ramc =  temp_ramc - cur_arc
                    self.logger.info(f'--> RA directa ajustada: {adj_ramc} 🆗')
                    MC_adjust.append(adj_ramc)

                aspects = identify_aspect(converse_diff)
                if len(aspects) > 0:
                    self.logger.info(f'MC ecliptica {eclep_longitude_converse}')
                    self.logger.info(f'{cur_object} {object_ecliptic_long} 🎯 aspects: {aspects[0]} orbe')
                    adhj_eclep_longitude_converse = eclep_longitude_converse + aspects[0]
                    g,m,s = get_angle_sexag(adhj_eclep_longitude_converse)
                    temp_ramc = get_RAMC(g, m, s)
                    self.logger.info(f'--> RA conversa ajustada: {temp_ramc}')
                    adj_ramc =  temp_ramc + cur_arc
                    self.logger.info(f'--> MC radix ajustado: {adj_ramc} 🆗')
                    MC_adjust.append(adj_ramc)

        #results computing
        self.logger.info("\n\n\nresultados finales:")
        self.logger.info("--------------------------------")
        x = 0
        t = 0
        for cur_ARMC in MC_adjust:
            x = x + 1
            t = t + cur_ARMC
            self.logger.info(f'MC radix ajustado: {cur_ARMC}')
        new_ARMC = t/x
        if x > 0:
            self.logger.info("--------------------------")
            self.logger.info(f'nueva ARMC {new_ARMC}')
            new_eceliptic_long = get_ecliptic_longitude(new_ARMC)
            self.logger.info(f'ARMC radical original {RAMC_radix}')
            self.logger.info(f'nueva longitud ecliptica {new_eceliptic_long}')
            HL = ((new_ARMC/15 + self.geograph_long - self.HS_GMT)*.99727) + self.GMT_Hour
            h,m,s = get_angle_sexag(HL)
            self.logger.info(f'nueva hora local {h} {m} {s}')
            return f'{h}hs {m}ms {s}scs'
        else:
            return None