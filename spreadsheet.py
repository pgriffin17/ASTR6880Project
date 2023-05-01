import os
import csv # for epoch_obsid_tabulator
from astropy.io import fits

epoch_obsid_list = [['20860','20861'],
 ['20936','20937','20938','20939','20945'],
 ['21080','21090'],
 ['21371'],
 ['21322','22157','22158'],
 ['21372','22736','22737'],
 ['21323','23183','23184','23185'],
 ['22677','24887','24888','24889'], # Maybe combine this with the next one too?
 ['23870','24923','24924'],
 ['23869','26223','24336','24337'],
 ['25733','25734','25527'],
 ['27088','27089','27090','27731','27091','25528','27752','27753','27754']]

def obsid_header_parse(obsid):
    #get exposure time and start time from an obsid fits header
    t_0 = '2017-08-17'
    t_0_mjd = 57982.00000000
    t_peak = t_0_mjd + 160

    infile = f'data/{obsid}/repro/acisf{obsid}_repro_evt2.fits'
    with fits.open(infile) as f:
        time_stop = f[1].header['TSTOP']/(24*3600) + f[1].header['MJDREF'] - t_0_mjd
        time_start = f[1].header['TSTART']/(24*3600) + f[1].header['MJDREF'] - t_0_mjd
        #exp_time_print = round(exp_time/1000,None) #converts to integer in kiloseconds
        obs_date = f[1].header['MJD-OBS']
    return(obs_date-t_0_mjd,time_start,time_stop)

def epoch_header_parse(epoch):
    '''
    get exposure time and start time from an obsid fits header
    '''
    t_0 = '2017-08-17'
    t_0_mjd = 57982.00000000
    t_peak = t_0_mjd + 160

    infile = f'data/merge_test/epoch_{epoch+4}/merged_evt.fits'
    with fits.open(infile) as f:
        obs_time = f[1].header['TSTOP'] - f[1].header['TSTART']
        obs_date = f[1].header['MJD-OBS']
    return(obs_date-t_0_mjd,obs_time)

def epoch_list_tabulator (obsid_list):
    #write the list to a csv file with Epoch number
    start_epoch = 4
    with open('obsids.csv','w',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Epoch','Observation Start *(days since GW170817)','Halfway Date T-T0 *','Obs End *','Exposure Time (ksec)','Obs IDs'])
        for obsid_row in obsid_list:
            epoch = start_epoch+obsid_list.index(obsid_row)
            exp_time_total = 0
            for obsid in obsid_row:
                [t_t0,t_start,t_stop]=obsid_header_parse(obsid)
                if exp_time_total == 0:
                    ## this is the beginning of the obs
                    epoch_start_time = t_start
                obs_duration = t_stop - t_start
                #representative_t_t0_weighted = (representative_t_t0_weighted*exp_time_total + t_t0*obs_time)/(exp_time_total+obs_time)
                exp_time_total = exp_time_total+obs_duration
            ## use the last obs end time
            epoch_end_time = t_stop
            halfway_date = epoch_start_time + (epoch_end_time-epoch_start_time)/(2)
            writer.writerow([epoch,epoch_start_time, halfway_date,epoch_end_time,exp_time_total*(24*3.6),', '.join(obsid_row)])