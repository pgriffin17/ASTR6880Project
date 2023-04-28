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
        exp_time = f[1].header['TSTOP'] - f[1].header['TSTART']
        exp_time_print = round(exp_time/1000,None) #converts to integer in kiloseconds
        obs_start = f[1].header['MJD-OBS']
    return(round(obs_start-t_0_mjd,0),exp_time)

def epoch_header_parse(epoch):
    #get exposure time and start time from an obsid fits header
    t_0 = '2017-08-17'
    t_0_mjd = 57982.00000000
    t_peak = t_0_mjd + 160

    infile = f'data/merge_test/epoch_{epoch_in}/merged_evt.fits'
    with fits.open(infile) as f:
        exp_time = f[1].header['TSTOP'] - f[1].header['TSTART']
        exp_time_print = round(exp_time/1000,None) #converts to integer in kiloseconds
        obs_start = f[1].header['MJD-OBS']
    return(round(obs_start-t_0_mjd,0),exp_time)

def epoch_list_tabulator (obsid_list):
    #write the list to a csv file with Epoch number
    start_epoch = 4
    with open('obsids.csv','w',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Group #','Representative T-T0 (days)','Exposure Time (ksec)','Obs IDs'])
        for obsid_row in obsid_list:
            epoch = start_epoch+obsid_list.index(obsid_row)
            exp_time_total = 0
            representative_t_t0_weighted = 0
            for obsid in obsid_row:
                [t_t0,exp_time]=obsid_header_parse(obsid)
                representative_t_t0_weighted = (representative_t_t0_weighted*exp_time_total + t_t0*exp_time)/(exp_time_total+exp_time)
                exp_time_total = exp_time_total+exp_time
            writer.writerow([epoch,representative_t_t0_weighted,exp_time_total,', '.join(obsid_row)])