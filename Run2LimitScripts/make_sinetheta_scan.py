import ROOT
from plotting import *
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
import json
import os 
import glob
import pandas as pd
import argparse

m_a = '200'

def DrawLimitBand(pad, graph_dict, draw=['exp2', 'exp1', 'exp0'], draw_legend=None,
                  legend=None, legend_overwrite=None):
    legend_dict = {
        'obs' : { 'Label' : 'Observed', 'LegendStyle' : 'LP', 'DrawStyle' : 'PLSAME'},
        'exp0' : { 'Label' : 'Expected', 'LegendStyle' : 'L', 'DrawStyle' : 'LSAME'},
        'exp1' : { 'Label' : '95% Expected', 'LegendStyle' : 'F', 'DrawStyle' : '3SAME'},
        'exp2' : { 'Label' : '68% Expected', 'LegendStyle' : 'F', 'DrawStyle' : '3SAME'}
    }
    if legend_overwrite is not None:
        for key in legend_overwrite:
            if key in legend_dict:
                legend_dict[key].update(legend_overwrite[key])
            else:
                legend_dict[key] = legend_overwrite[key]
    pad.cd()
    for key in draw:
        if key in graph_dict:
            graph_dict[key].Draw(legend_dict[key]['DrawStyle'])
    if legend is not None:
        if draw_legend is None:
            draw_legend = reversed(draw)
        for key in draw_legend:
            if key in graph_dict: 
                legend.AddEntry(graph_dict[key],legend_dict[key]['Label'],legend_dict[key]['LegendStyle'])



mA_ticks = [200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1200.0, 1600.0]
ma_ticks = [100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0, 500.0]


def add_text(text="", lowX=0.5, lowY=0.5):
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


def get_json(channel, year, cat='gg'):
    if cat=='gg':
        _path = 'limits_2HDMa/limit_'+year+'_'+channel+'_Signal_2HDMa_gg_*_tanb_1p0_mXd_10_MH3_600_MH4_'+m_a+'.json'

    elif cat=='bbgg':
        _path = 'limits_bbgg/limits_cmb_2HDMa_bbgg_*_tanb_1p0_mXd_10_MH3_600_MH4_'+m_a+'.json' 
 
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
        sintheta = inFile[1 + inFile.index('sinp')].replace('p', '.')
        sintheta = float(sintheta)
        massA=str(mA)
        values = data[massA]
        values['mA'] = mA
        values['ma'] = ma

        values['exp0'] = values['exp0'] 
        values['exp+1'] = values['exp+1']
        values['exp-1'] = values['exp-1']
        values['exp+2'] = values['exp+2']
        values['exp-2'] = values['exp-2']
        values['obs'] = values['obs'] 
        print ("values from the files value:   ",values)
        out[ sintheta ] = values
        data_json = json.dumps(out)
        
        with open('sinetheta_scan_'+cat+'_'+year+'_'+channel+'_resolved.json', 'w+') as json_file:
            json.dump(out, json_file, indent=4, sort_keys=True)

def make_plotid(channel, year, cat='gg'): 
    # Style and pads
    ModTDRStyle()
    canv = ROOT.TCanvas('2hdma_limit_1d_sinetheta_scan_'+cat+'_'+year+'_'+channel+'_resolved', 'limit_1d'+'mA=600GeV ma=200GeV ')
    canv.SetCanvasSize(1000, 800)
    pads = OnePad()
    
    # Get limit TGraphs as a dictionary
    try:
        graphs = StandardLimitsFromJSONFile('sinetheta_scan_'+cat+'_'+year+'_'+channel+'_resolved.json')
    except:
        return
    # Create an empty TH1 from the first TGraph to serve as the pad axis and frame
    temp_grValues = list(graphs.values())
    axis = CreateAxisHist(temp_grValues[0])
    axis.SetTitle('Limit 1D scan '+' varying sin#theta')
    axis.GetXaxis().SetTitle('sin#theta')
    axis.GetXaxis().SetTitleOffset(0.9)
    axis.GetYaxis().SetTitle('#sigma_{95% CL}/#sigma_{theory}')
    axis.GetYaxis().SetTitleSize(0.06)
    axis.GetYaxis().SetTitleOffset(1.0)
    axis.GetYaxis().SetMoreLogLabels(True)
    
    pads[0].cd()
    axis.Draw('axis')
    
    # Create a legend in the top left
    #legend = PositionedLegend(0.3, 0.24, 1, 0.56, 0.5)
    legend = PositionedLegend(0.3, 0.24, 1, 0.18, 0.45)
    
    # Set the standard green and yellow colors and draw
    StyleLimitBand(graphs)
    DrawLimitBand(pads[0], graphs, legend=legend, draw=['exp2', 'exp1', 'exp0', 'obs'])
    legend.Draw()
    
    #title_text = add_text('2HDMa Limit 1D sin#theta scan', 0.35, 0.91)
    title_text = add_lumi(year)    
    title_text.Draw('SAME')

    tline = ROOT.TLine(0.1,1, 0.9, 1)
    tline.SetLineStyle(2)
    tline.Draw("SAME")

    text0 = add_text('2HDM + a', 0.20, 0.85)
    text0.SetTextFont(62)
    #text0.SetTextSize(0.1)
    text0.Draw('SAME')  
    text00 = add_text('h #rightarrow #tau#tau', 0.20, 0.8)                                                                 
    text00.SetTextFont(42)
    text00.Draw('SAME')

    text1 = add_text('m_{A} = 600 GeV;', 0.53, 0.85)
    text1.Draw('SAME')
    text2 = add_text('m_{a} = '+m_a+' GeV', 0.75, 0.85)
    text2.Draw('SAME')
    text3 = add_text('tan#beta = 1', 0.75, 0.79)
    text3.Draw('SAME')
    text4 = add_text('m_{#chi} = 10 GeV;', 0.53, 0.79)
    text4.Draw('SAME')

    # Re-draw the frame and tick marks
    pads[0].SetLogy()
    pads[0].RedrawAxis()
    pads[0].GetFrame().Draw()
    
    # Adjust the y-axis range such that the maximum graph value sits 25% below
    # the top of the frame. Fix the minimum to zero.
    FixBothRanges(pads[0], 0.4, 0.01, 13, 0.25)
    
    # Standard CMS logo
    DrawCMSLogo(pads[0], 'CMS', 'Preliminary', 0, 0.12, 0.035, 1.2, '', 0.9)
    
    canv.Print('limit_1D_2HDMa_sinetheta_scan_mA600_ma200_2017_2018.pdf')
    canv.Print('limit_1D_2HDMa_sinetheta_scan_mA600_ma200_2017_2018.png')

    
if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-ch","--channel",
                    help="name of channel 'etau', 'mutau', 'tautau' or 'cmb'. Default=ALL")
    parser.add_argument("-y","--year",
                    help="year, options '2017', '2018', 'cmb'")

    print ('python make_sinetheta_scan.py -ch et mt tt cmb -y 2017 2018 201718')
    args =  parser.parse_args()
    channels = []
    channel = str(args.channel)
    year  = str(args.year) 
    get_json(channel, year, 'gg')
    make_plotid(channel, year, 'gg')
