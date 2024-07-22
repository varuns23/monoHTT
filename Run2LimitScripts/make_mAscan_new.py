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

    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_200_MH4_100' : 3.628e-01 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_200_MH4_150' : 3.209e-01 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_300_MH4_100' : 2.892e+00 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_300_MH4_150' : 1.596e+00 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_400_MH4_100' : 1.352e+00 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_400_MH4_150' : 9.943e-01 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_400_MH4_200' : 5.997e-01 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_400_MH4_250' : 2.301e-01 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_500_MH4_150' : 5.070e-01 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_500_MH4_200' : 3.709e-01 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_500_MH4_250' : 2.375e-01 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_500_MH4_300' : 1.295e-01 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_600_MH4_100' : 3.778e-01 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_600_MH4_150' : 2.981e-01 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_600_MH4_200' : 2.313e-01 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_600_MH4_250' : 1.657e-01 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_600_MH4_300' : 1.160e-01 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_600_MH4_350' : 7.739e-02 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_600_MH4_400' : 4.035e-02 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_600_MH4_500' : 5.494e-03 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_700_MH4_250' : 1.084e-01 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_700_MH4_300' : 8.360e-02 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_700_MH4_350' : 6.513e-02 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_700_MH4_400' : 4.227e-02 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_800_MH4_250' : 7.091e-02 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_800_MH4_300' : 5.730e-02 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_800_MH4_350' : 4.830e-02 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_800_MH4_500' : 1.604e-02 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_900_MH4_300' : 3.757e-02 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_900_MH4_350' : 3.359e-02 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_900_MH4_400' : 2.559e-02 , 
    'Signal_2HDMa_gg_sinp_0p35_tanb_1p0_mXd_10_MH3_900_MH4_500' : 1.432e-02 ,

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
    if year_=="2017_cmb":
        lumiProcessed="41.5"
    if year_=="2018_cmb":
        lumiProcessed="59.7"
    elif year_=='2016':
        lumiProcessed="35.9"
    if year_=="201718_cmb":
        lumiProcessed="101.2"
    lumi.AddText(lumiProcessed+" fb^{-1} (13 TeV)")
    return lumi


def get_json(mchi = '', year=''):
    filename = 'limits_2HDMa/limit_'+year+'_Signal_2HDMa_gg_*tanb_1p0*_MH4_'+mchi+'.json'
    print("#################################################################################################")
    print(filename)
    files = glob.glob(filename)
    out = {}
    nPoint = 0
    if not files :
        print ("File " , filename,  ' NOT FOUND!!!!!!')
        return
    for inFile in files:
        print (inFile)
        with open(inFile) as f:
            data = json.load(f)
        
        inFile = inFile.replace('.json', '')
        mA = float(inFile.split('_')[-3])
        ma = float(inFile.split('_')[-1])
        massA=str(mA)
        values = data[massA]
        values['mA'] = mA
        values['ma'] = ma
        values['obs'] = values['obs']
        _name = 'MZp_'+str(int(values['mA']))+'_MChi_'+str(int(values['ma']))

        print (values)
        out[ str(mA) ] = values
        data_json = json.dumps(out)
        
        with open('mchi'+mchi+'_year_'+year+'.json', 'w+') as json_file:
            json.dump(out, json_file, indent=4, sort_keys=True)


def make_plot1d(mchi="", year=''):
    # Style and pads
    ModTDRStyle()
    canv = ROOT.TCanvas('2hdma_limit_1d_mChi_'+mchi, 'limit_1d'+' mChi '+mchi)
    canv.SetCanvasSize(1000, 800)
    pads = OnePad()
    
    # Get limit TGraphs as a dictionary
    if not os.path.exists('mchi'+mchi+'_year_'+year+'.json'):
        print ("File " , 'mchi'+mchi+'_year_'+year+'.json NOT FOUND!!!!!!')
        return 
    try:
        graphs = StandardLimitsFromJSONFile('mchi'+mchi+'_year_'+year+'.json')
    except:
        return
    # Create an empty TH1 from the first TGraph to serve as the pad axis and frame
    temp_grValues = list(graphs.values())
    axis = CreateAxisHist(temp_grValues[0])
    axis.SetTitle('Limit 1D scan '+'ma = '+mchi+' GeV')
    axis.GetXaxis().SetTitle('m_{A} [GeV]')
    axis.GetXaxis().SetTitleOffset(0.9)
    axis.GetYaxis().SetTitle('#sigma_{95% CL}/#sigma_{theory}')
    axis.GetYaxis().SetTitleSize(0.06)
    axis.GetYaxis().SetTitleOffset(1.0)
    axis.GetYaxis().SetMoreLogLabels(True)
    pads[0].cd()
    axis.Draw('axis')
    
    # Create a legend in the top left
    #legend = PositionedLegend(0.3, 0.2, 3, 0.015)
    #legend = PositionedLegend(0.3, 0.24, 1, 0.56, 0.5)
    legend = PositionedLegend(0.3, 0.22, 1, 0.59, 0.5)
    
    # Set the standard green and yellow colors and draw
    StyleLimitBand(graphs)
    DrawLimitBand(pads[0], graphs, legend=legend)
    legend.Draw()

    title_text = add_lumi(year)
    title_text.Draw('SAME')
   
    text0 = add_text('2HDM + a', 0.20, 0.85)
    text0.SetTextFont(62)
    #text0.SetTextSize(0.1)
    text0.Draw('SAME')
    text00 = add_text('h #rightarrow #tau#tau', 0.20, 0.8)
    text00.SetTextFont(42)
    text00.Draw('SAME')
 
    text1 = add_text('m_{a} = 150 GeV;', 0.53, 0.85)
    text1.Draw('SAME')
    text1a = add_text('m_{#chi} = 10 GeV', 0.75, 0.85)
    text1a.Draw('SAME')
    text2 = add_text('sin#theta = 0.35;', 0.53, 0.79)
    text2.Draw('SAME')
    text3 = add_text('tan#beta = 1.0', 0.75, 0.79)
    text3.Draw('SAME')


    # Re-draw the frame and tick marks
    pads[0].SetLogy()
  #  pads[0].SetLogx()
    pads[0].RedrawAxis()
    pads[0].GetFrame().Draw()
   
    if (mchi == '250'):
        tline = ROOT.TLine(400,1, 1600, 1)
    else:
        tline = ROOT.TLine(200,1, 1600, 1)
    tline.SetLineStyle(2)
    tline.Draw("SAME")
    

    
    # Adjust the y-axis range such that the maximum graph value sits 25% below
    # the top of the frame. Fix the minimum to zero.
    FixBothRanges(pads[0], 0.2, 0.02, 20, 0.25)
    
    # Standard CMS logo
    DrawCMSLogo(pads[0], 'CMS', 'Preliminary', 0, 0.12, 0.035, 1.2, '', 0.9)
    
    if (year == '201718_cmb'): 
        canv.Print('limit_1D_2HDMa_mAscan_ma150_2017_2018.pdf')
        canv.Print('limit_1D_2HDMa_mAscan_ma150_2017_2018.png')
    
if __name__=="__main__":
    
    for ma in ['150']:
        for year in ['201718_cmb']: #['2016', '2017', '2018', '201718', 'run2']:
            get_json(str(ma), year)
            make_plot1d(str(ma), year)
