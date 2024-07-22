import ROOT
#from ROOM import TColor
from plotting import *
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
import json
import os 
import glob
import pandas as pd
import argparse

doLogY = True

mA_ticks = [200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1200.0, 1600.0]
ma_ticks = [100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0, 500.0]
#ma_ticks = [150.0]

def add_text(text="", lowX=0.9, lowY=0.5):
    lumi  = ROOT.TPaveText(lowX, lowY, lowX+0.1, lowY+0.1, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.04)
    lumi.SetTextFont (   42 )
    lumi.AddText(text)
    return lumi


def add_lumi( year_=""):
    lowX=0.70
    lowY=0.91
    #0.35, 0.91
    lumi  = ROOT.TPaveText(lowX, lowY, lowX+0.1, lowY+0.1, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.04)
    lumi.SetTextFont (   42 )
    if year_=="2017":
        lumiProcessed="41.5"
    if year_=="2018":
        lumiProcessed="59.7"
    elif year_=='2016':
        lumiProcessed="35.9"
    if year_=="201718":
        lumiProcessed="101.2"
    lumi.AddText(lumiProcessed+" fb^{-1} (13 TeV)")
    return lumi


def get_json(amass, channel, year, cat='gg'):
    if cat=='gg':
        _path = 'limits_2HDMa/limit_'+year+'_'+channel+'_Signal_2HDMa_gg_sinp_0p35_*_mXd_10_MH3_600_MH4_'+amass+'.json'

    elif cat=='bb':
        _path = 'limits_2HDMa/limit_'+year+'_'+channel+'_Signal_2HDMa_bb_sinp_0p35_*_mXd_10_MH3_600_MH4_'+amass+'.json'
    elif cat=='bbgg':
        _path = 'limits_2HDMa_bbgg/limits_cmb_2HDMa_bbgg_sinp_0p35_tanb_*_mXd_10_MH3_600_MH4_'+ma+'.json'

        

    
    files = glob.glob(_path)
    out = {}
    nPoint = 0
    if not files :
        return
    for inFile in files:
        print(inFile)
        with open(inFile) as f:
            data = json.load(f)
            
        inFile = inFile.split('/')[-1]
        inFile = inFile.replace('.json', '')
        inFile = inFile.split('_')
        mA = float(inFile[1 + inFile.index('MH3')])
        ma = float(inFile[1 + inFile.index('MH4')])
        tanbeta = inFile[1 + inFile.index('tanb')].replace('p', '.')
        tanbeta = float(tanbeta)
        massA=str(mA)
        values = data[massA]
        values['mA'] = mA
        values['ma'] = ma
        _name = '_'.join(inFile[inFile.index('2HDMa') : ])
        values['obs'] = values['obs'] 
        values['exp0'] = values['exp0'] 
        values['exp+1'] = values['exp+1']
        values['exp-1'] = values['exp-1']
        values['exp+2'] = values['exp+2']
        values['exp-2'] = values['exp-2']

        print(values)
        out[ tanbeta ] = values
        data_json = json.dumps(out)
        #_ma_ = float(ma)
        with open(cat+'_'+year+'_'+channel+'_resolved_tanbeta_scan_MH3_600_ma_'+amass+'tanrange_4p0.json', 'w+') as json_file:
            json.dump(out, json_file, indent=4, sort_keys=True)

def make_plotid(amass, channel, year, cat='gg'):
    # Style and pads
    ModTDRStyle()
    canv = ROOT.TCanvas('2hdma_limit_1d_'+cat+'_'+year+'_'+channel+'_resolved_tanbeta_scan_ma_'+amass+'tanrange_4p0', 'limit_1d'+'mA=600GeV  ma='+amass)
    canv.SetCanvasSize(1000, 800)
    canv.GetFrame().SetLineWidth(4)
    pads = OnePad()
    print("coming in makeplotid")    
    # Get limit TGraphs as a dictionary
    try:
        graphs = StandardLimitsFromJSONFile(cat+'_'+year+'_'+channel+'_resolved_tanbeta_scan_MH3_600_ma_'+amass+'tanrange_4p0.json')
    except:
        return 
    # Create an empty TH1 from the first TGraph to serve as the pad axis and frame
    print("coming in makeplotid 1")
    temp_grValues = list(graphs.values())
    axis = CreateAxisHist(temp_grValues[0])
    axis.SetTitle('Limit 1D scan '+' varying tan#beta')
    axis.GetXaxis().SetTitle('tan#beta')
    axis.GetXaxis().SetTitleOffset(0.9)
    axis.GetXaxis().SetLimits(0.5,4.0)
    axis.GetYaxis().SetTitle('#sigma_{95% CL}/#sigma_{theory}')
    axis.GetYaxis().SetTitleSize(0.06)
    axis.GetYaxis().SetTitleOffset(1.0)
    axis.GetYaxis().SetMoreLogLabels(True)
    pads[0].cd()
    axis.Draw('axis')
  
    # Create a legend in the top left
    #legend = PositionedLegend(0.3, 0.2, 3, 0.015)
    legend = PositionedLegend(0.3, 0.24, 1, 0.56, 0.5)
    
    # Set the standard green and yellow colors and draw
    StyleLimitBand(graphs)
    DrawLimitBand(pads[0], graphs, legend=legend, draw=['exp2', 'exp1', 'exp0', 'obs'])
    legend.Draw()
    
    title_text = add_lumi(year)
    title_text.Draw('SAME')
    print("coming in makeplotid")    

    text0 = add_text('2HDM + a', 0.20, 0.85)
    text0.SetTextFont(62)
    #text0.SetTextSize(0.1)
    text0.Draw('SAME')  
    text00 = add_text('h #rightarrow #tau#tau', 0.20, 0.8)                                                                 
    text00.SetTextFont(42)
    text00.Draw('SAME') 

    #text = add_text('95% CL limit on #mu',0.7, 0.45)
    #text.Draw('SAME')
    text1 = add_text('m_{A} = 600 GeV;', 0.53, 0.85)
    text1.Draw('SAME')
    text1a = add_text('m_{a} = 150 GeV', 0.75, 0.85)
    text1a.Draw('SAME')
    text2 = add_text('sin#theta = 0.35', 0.75, 0.79)
    text2.Draw('SAME')
    text3 = add_text('m_{#chi} = 10 GeV;', 0.53, 0.79)
    text3.Draw('SAME')

    tline = ROOT.TLine(0.5,1, 4, 1)
    tline.SetLineStyle(2)
    tline.Draw("SAME")


    # Re-draw the frame and tick marks
    if(doLogY):
       pads[0].SetLogy()
    pads[0].RedrawAxis()
    pads[0].GetFrame().Draw()
    print("coming in makeplotid")    
    # Adjust the y-axis range such that the maximum graph value sits 25% below
    # the top of the frame. Fix the minimum to zero.
    FixBothRanges(pads[0], 0.3, 0.01, 5, 0.25)
    # Standard CMS logo
    DrawCMSLogo(pads[0], 'CMS', 'Preliminary', 0, 0.12, 0.035, 1.2, '', 0.9)
    
    canv.Print('limit_1D_2HDMa_tanBeta_scan_mA600_ma150_2017_2018.pdf')
    canv.Print('limit_1D_2HDMa_tanBeta_scan_mA600_ma150_2017_2018.png')
if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-ch","--channel",
                    help="name of channel 'etau', 'mutau', 'tautau' or 'cmb'. Default=ALL")
    parser.add_argument("-ma","--amass",
                    help="amass, options '150', '250'")
    parser.add_argument("-y","--year",
                    help="year, options '2017', '2018', 'cmb'")

    print('python make_sinetheta_scan.py -ch et mt tt cmb -ma 150 250 -y 2017 2018 201718')
    args =  parser.parse_args()
    channels = []
    channel = str(args.channel)
    amass = str(args.amass)
    year  = str(args.year) 
    print(amass)
    print(channel)
    print(year)
    get_json(amass, channel, year, 'gg')
    make_plotid(amass, channel, year, 'gg')
