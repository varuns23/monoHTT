import ROOT
from plotting import *
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

import json
import os 
import glob
import pandas as pd
import argparse

mA_ticks = [100, 200, 300, 350, 500, 650, 800, 1000, 1500, 2000, 2500, 3000, 3500]
ma_ticks = [1, 50, 100, 150, 200, 400, 600, 800]

xsec_map  = {
    'MZp_200_MChi_1': 2.67, 
    'MZp_2500_MChi_600': 0.004033, 'MZp_1000_MChi_400': 0.09047, 'MZp_2000_MChi_800': 0.007706, 'MZp_300_MChi_150': 0.3163, 'MZp_2500_MChi_1': 0.004382, 'MZp_500_MChi_400': 0.0001253, 
    'MZp_500_MChi_100': 0.9952, 'MZp_3000_MChi_200': 0.001456, 
    'MZp_1500_MChi_600': 0.02549, 
    'MZp_1500_MChi_1': 0.0505, 
    'MZp_2000_MChi_100': 0.01422, 'MZp_2500_MChi_100': 0.004391, 'MZp_2500_MChi_800': 0.003516, 
    'MZp_1000_MChi_1': 0.2094, 'MZp_200_MChi_50': 2.184, 'MZp_3500_MChi_1': 0.0005255, 
    'MZp_1000_MChi_100': 0.2077, 'MZp_350_MChi_50': 1.858, 'MZp_2000_MChi_200': 0.01413, 
    'MZp_2500_MChi_400': 0.004283, 'MZp_1000_MChi_200': 0.1947, 'MZp_100_MChi_1': 3.322, 
    'MZp_500_MChi_1': 1.139, 'MZp_2000_MChi_1': 0.01425, 
    'MZp_1500_MChi_800': 0.0002038, 'MZp_200_MChi_150': 0.0033, 'MZp_100_MChi_50': 0.9046, 
    'MZp_3500_MChi_100': 0.0005227, 
    'MZp_2500_MChi_200': 0.00435, 
    'MZp_2000_MChi_600': 0.01176, 
    'MZp_1000_MChi_800': 5.138e-06, 'MZp_1500_MChi_200': 0.04976, 
    'MZp_650_MChi_50': 0.6549, 'MZp_500_MChi_200': 0.4235, 
    'MZp_2000_MChi_400': 0.01351, 'MZp_1500_MChi_100': 0.05066, 
    'MZp_1500_MChi_400': 0.04371, 'MZp_3000_MChi_100': 0.001463, 'MZp_3000_MChi_1': 0.001458, 
    'MZp_200_MChi_100': 0.5484, 'MZp_1000_MChi_600': 0.0001443, 'MZp_800_MChi_50': 0.3935,
    'MZp_200_MChi_400':  0.00000859 , 
    'MZp_300_MChi_1':  2.356 , 
    'MZp_300_MChi_50':  2.034 , 
    'MZp_300_MChi_100':  1.291 , 
    'MZp_300_MChi_200':  0.00292 , 
    'MZp_350_MChi_1':  2.012 , 
    'MZp_350_MChi_100':  1.171 , 
    'MZp_350_MChi_150':  0.7871 , 
    'MZp_350_MChi_200':  0.009408 , 
    'MZp_350_MChi_400':  0.0000354 , 
    'MZp_500_MChi_50':  1.114 , 
    'MZp_500_MChi_150':  0.7065 , 
    'MZp_650_MChi_1':  0.6634 , 
    'MZp_650_MChi_100':  0.6317 , 
    'MZp_650_MChi_150':  0.5663 , 
    'MZp_650_MChi_200':  0.4386 , 
    'MZp_800_MChi_1':  0.3942 , 
    'MZp_800_MChi_100':  0.3872 , 
    'MZp_800_MChi_150':  0.3676 , 
    'MZp_800_MChi_200':  0.3336 , 
    'MZp_800_MChi_400':  0.03092 , 
    'MZp_1000_MChi_50':  0.2088 , 
    'MZp_1000_MChi_150':  0.2035 , 
    'MZp_1500_MChi_50':  0.05047 ,
    

    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_200_MH4_100' : 3.628e-01 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_200_MH4_150' : 3.209e-01 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_300_MH4_100' : 2.892e+00 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_300_MH4_150' : 1.596e+00 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_400_MH4_100' : 1.352e+00 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_400_MH4_150' : 9.943e-01 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_400_MH4_200' : 5.997e-01 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_400_MH4_250' : 2.301e-01 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_500_MH4_150' : 5.070e-01 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_500_MH4_200' : 3.709e-01 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_500_MH4_250' : 2.375e-01 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_500_MH4_300' : 1.295e-01 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_600_MH4_100' : 3.778e-01 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_600_MH4_150' : 2.981e-01 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_600_MH4_200' : 2.313e-01 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_600_MH4_250' : 1.657e-01 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_600_MH4_300' : 1.160e-01 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_600_MH4_350' : 7.739e-02 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_600_MH4_400' : 4.035e-02 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_600_MH4_500' : 5.494e-03 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_700_MH4_250' : 1.084e-01 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_700_MH4_300' : 8.360e-02 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_700_MH4_350' : 6.513e-02 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_700_MH4_400' : 4.227e-02 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_800_MH4_250' : 7.091e-02 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_800_MH4_300' : 5.730e-02 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_800_MH4_350' : 4.830e-02 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_800_MH4_500' : 1.604e-02 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_900_MH4_300' : 3.757e-02 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_900_MH4_350' : 3.359e-02 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_900_MH4_400' : 2.559e-02 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_900_MH4_500' : 1.432e-02 ,
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_900_MH4_250':  0.04471 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_1000_MH4_100':  0.05403 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_500_MH4_100':  0.6449 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_600_MH4_500':  0.005563 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_700_MH4_100':  0.2369 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_700_MH4_150':  0.1853 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_700_MH4_200':  0.1447 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_800_MH4_100':  0.1519 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_800_MH4_200':  0.09187 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_900_MH4_100':  0.0942 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_900_MH4_150':  0.07257 , 
    '2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_900_MH4_200':  0.05673 , 
}
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
    elif year_=="201718":
        lumiProcessed="101.2"
    elif year_=="20161718_cmb":
        lumiProcessed="138"
    lumi.AddText(lumiProcessed+" fb^{-1} (13 TeV)")
    return lumi

#limit_20161718_cmb_ZprimeBaryonic_mzp2000_mchi1.json
#limit_2016_tt_ZprimeBaryonic_mzp2500_mchi1.json
def get_json(mchi = " ", year=''):
    filename = 'limits_zprime/limit_'+year+'_ZprimeBaryonic_mzp*_mchi1.json'
    files = glob.glob(filename)
    out = {}
    nPoint = 0
    if not files :
        print("File " , filename,  ' NOT FOUND!!!!!!')
        return
    for inFile in files:
        print(inFile)
        with open(inFile) as f:
            data = json.load(f)
   
        inFile = inFile.replace('.json', '')
        inFile = inFile.replace('mzp', '')
        inFile = inFile.replace('mchi', '')
        #print 'infile name == ', inFile
        #print inFile.split('_')
        mA = float(inFile.split('_')[-2])
        ma = float(inFile.split('_')[-1])
        mzp = str(mA)
        #for mz in mA_ticks: 
        #    mzp = mz
        print(mzp)    
        values = data[mzp]
        values['mA'] = mA
        values['ma'] = ma
        #values = values.pop('obs')
        #values['obs'] = 0.0
        _name = 'MZp_'+str(int(values['mA']))+'_MChi_'+str(int(values['ma']))


        xsec = xsec_map[_name]
        #if year=='20161718_cmb' :
        #        if year=='' :
        values['exp+1'] = values['exp+1']/xsec
        values['exp-1'] = values['exp-1']/xsec
        values['exp+2'] = values['exp+2']/xsec
        values['exp-2'] = values['exp-2']/xsec
        exp0bef = values['exp0']
        obsbef = values['obs']
        print('obs is *******************************8 ',obsbef)
        values['exp0'] = values['exp0']/xsec
        values['obs'] = values['obs'] /xsec
        #print(_name)
        #print(xsec)
        exp0aft = values['exp0']
        obsaft=values['obs']
        print('obs is ******%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5*************************8 ',obsaft)
        #print('expafter : ',exp0aft)
        #print(values)
        out[ str(mA) ] = values
        data_json = json.dumps(out)

        
        with open('mchi'+mchi+'_year_'+year+'.json', 'w+') as json_file:
            json.dump(out, json_file, indent=4, sort_keys=True)
    print('coming here 2')

def make_plot1d(mchi="", year=''):
    # Style and pads
    ModTDRStyle()
    canv = ROOT.TCanvas('zprimeb_limit_1d_mChi_'+mchi, 'limit_1d'+' mChi '+mchi)
    canv.SetCanvasSize(1000, 800)
    pads = OnePad()
    
    # Get limit TGraphs as a dictionary
    if not os.path.exists('mchi'+mchi+'_year_'+year+'.json'):
        print("File " , 'mchi'+mchi+'_year_'+year+'.json NOT FOUND!!!!!!')
        return 
    try:
        graphs = StandardLimitsFromJSONFile('mchi'+mchi+'_year_'+year+'.json')
    except:
        return
    # Create an empty TH1 from the first TGraph to serve as the pad axis and frame
    temp_grValues = list(graphs.values())                                   
    axis = CreateAxisHist(temp_grValues[0]) 
    axis.SetTitle('Limit 1D scan '+' mChi ='+mchi+'GeV')
    axis.GetXaxis().SetTitle("m_{Z'} [GeV]")
    axis.GetXaxis().SetTitleOffset(0.9)
    axis.GetYaxis().SetTitle('95% CL limit on #mu')
    axis.GetYaxis().SetTitleSize(0.052)
    axis.GetYaxis().SetTitleOffset(0.95)
    axis.GetYaxis().SetMoreLogLabels(True)
    pads[0].cd()
    axis.Draw('axis')
    
    # Create a legend in the top left
    legend = PositionedLegend(0.3, 0.22, 1, 0.59, 0.5)
    
    # Set the standard green and yellow colors and draw
    StyleLimitBand(graphs)
    DrawLimitBand(pads[0], graphs, legend=legend)
    legend.Draw()

    #title_text = add_text('Zprime Baryonic Limit 1D scan '+' mChi ='+mchi+'GeV', 0.35, 0.91)
    title_text = add_lumi(year)
    title_text.Draw('SAME')

    line = ROOT.TLine(100, 1.0, 2500, 1.0)
    line.SetLineColor(1)
    line.SetLineStyle(7)
    line.Draw('same')

    text0 = add_text("Baryonic-Z'", 0.20, 0.85)
    text0.SetTextFont(62)
    #text0.SetTextSize(0.1)
    text0.Draw('SAME')
    text00 = add_text("Z' #rightarrow DM + h(#tau#tau)", 0.20, 0.8)
    text00.SetTextFont(42)
    text00.Draw('SAME')

    text1 = add_text('g_{q} = 0.25;', 0.59, 0.85)
    text1.Draw('SAME')    
    text2 = add_text('g_{DM} = 1.0', 0.75, 0.85)
    text2.Draw('SAME')    
    text3 = add_text('m_{#chi} = '+mchi+'GeV', 0.59, 0.79)
    text3.Draw('SAME')    
    if year=='201718':
        year='2017+2018'
    if year=='run2':
        year = 'Full RunII'
    
    # Re-draw the frame and tick marks
    pads[0].SetLogy()
    pads[0].RedrawAxis()
    pads[0].GetFrame().Draw()

    # Adjust the y-axis range such that the maximum graph value sits 25% below
    # the top of the frame. Fix the minimum to zero.
    FixBothRanges(pads[0], 0.15, 0.01, 10, 0.25)
    
    # Standard CMS logo
    DrawCMSLogo(pads[0], 'CMS', 'Preliminary', 0, 0.12, 0.035, 1.2, '', 0.9)
    
    canv.Print('limit_1D_zprime_mchi1_runII.pdf')
    canv.Print('limit_1D_zprime_mchi1_runII.png')
    print('end done')
if __name__=="__main__":
    for mchi in ['1']:
        for year in [ '20161718_cmb' ]: 
            get_json(str(mchi), year)
            make_plot1d(str(mchi), year)
                
