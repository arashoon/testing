

import os
import shutil as sh
import numpy as np
import pandas as pd
from get_RD_info_v1 import *
from get_sequence_info_v1 import *

ToEncode='1'
TestDecodeAtEncoder="off"
ToDecode='0'
ToMeasure='1'

tagname='0406a'
testfolder='_test/0421'
#ReleaseOrDebug='RelWithDebInfo'

testrunbase='01'
codingcond = 'AI'
NumOfFramesToCode = "4"
NumOfPasses='2'
CpuUsed='0'
testfolder+= testrunbase
root_path ='/home/sehoon/work/av1-test/'
os.chdir(root_path)
pythonscript_dir= root_path +  testfolder



## Additional options
AdditionalOptions = {
    'SuperResOff':' --cpu-used=1 --threads=0 --profile=0 --lag-in-frames=19 --min-q=0 --max-q=63 --auto-alt-ref=1 --passes=2 ' + \
                  ' --kf-max-dist=0 --kf-min-dist=0 --drop-frame=0 --static-thresh=0 --bias-pct=50 --minsection-pct=5 --maxsection-pct=1000 ' + \
                  ' --arnr-maxframes=7 --arnr-strength=5 --sharpness=0 --undershoot-pct=100 --overshoot-pct=100  --frame-parallel=0 --tile-columns=0 ' + \
                  ' --limit=1 --end-usage=vbr --superres-mode=0',

   'SuperResOn':  ' --cpu-used=1 --threads=0 --profile=0 --lag-in-frames=19 --min-q=0 --max-q=63 --auto-alt-ref=1 --passes=2 ' + \
                  ' --kf-max-dist=0 --kf-min-dist=0 --drop-frame=0 --static-thresh=0 --bias-pct=50 --minsection-pct=5 --maxsection-pct=1000 ' + \
                  ' --arnr-maxframes=7 --arnr-strength=5 --sharpness=0 --undershoot-pct=100 --overshoot-pct=100 --frame-parallel=0 --tile-columns=0 ' + \
                  ' --limit=1 --end-usage=vbr --superres-mode=4'}
#tested_rates = ['56'] #,'40','48','56']
tested_rates = ['50','100'] #,'150','200']
RAIntraPeriodTable={20:16,24:32,30:32,50:48,60:64,100:96}


# Begin test

for seq_name in ["sunflower_720p25.y4m" ]:
    #seqname = AOMSequenceTable[seq_name][0]
    seqname = seq_name
    videopath='/home/sehoon/work/VideoData/AOM/'
    #Width=str(AOMSequenceTable[seq_name][2])
    #Height = str(AOMSequenceTable[seq_name][3])
    FrameRate= 25 #AOMSequenceTable[seq_name][4]
    FrameRateSetting= str(FrameRate)+'000'+'/1000'
    BitDepth = "8"

    if codingcond == 'AI':
        IntraPeriod = 1
    elif codingcond == 'RA':
        IntraPeriod = RAIntraPeriodTable[FrameRate]
    elif codingcond == 'LB':
        IntraPeriod=-1

    for method in ['test']: #,'anchor']: # 'aom-anchor',,'test']:#,'anchor-v8-C1A_S04-planaron-K4M0' ]: #,'anchor-v8-ford01-planaroff']: #,'anchor-v8-cat3fs-planaron']: #,'anchor-v7']: #'anchor-v7','test1']: # Change per test

        if method =='anchor': #
            exeroot_path = root_path + r'\build\\' + ReleaseOrDebug + '/' + 'anchor/'
            tag=''
            BINNAME=method + seqname
            executable_enc = 'aomenc_anchor-fixed-partition.exe'
            executable_dec = 'aomdec_anchor-fixed-partition.exe'
        elif method=='test': # Change per test
            tag=tagname + ''
            exeroot_path = root_path + 'aom/build/'
            BINNAME = method + seqname
            executable_enc = 'aomenc'
            executable_dec = 'aomdec'


        for Options in AdditionalOptions:
            data = np.empty([1, 6])
            seq_col = []
            testrun =   testrunbase + Options
            for rate in tested_rates:

              results_dir = pythonscript_dir + '/' + codingcond + '_' + 'passes' + NumOfPasses + '_' + 'Cpu' + CpuUsed + '_' +method +  tag  +'_' + testrun + '_' +  seqname + '_' +  rate + '/'
              csv_dir = pythonscript_dir + '/' + codingcond + '_' + 'passes' + NumOfPasses + '_' + 'Cpu' + CpuUsed + '_'  + method +  tag + '_' + testrun + '_' + seqname


              if not os.path.exists(results_dir):
                os.makedirs(results_dir)

              enc_log = results_dir + 'enc_log.log'
              dec_log = results_dir + 'dec_log'

              #" --width=" + Width + " --height=" + Height + \
              enc_cmd = exeroot_path + executable_enc + ' ' + videopath + seqname  + \
                        " --passes=2 --skip=0 --limit=" + NumOfFramesToCode + " --target-bitrate=" + rate + \
                        " -o " + results_dir + BINNAME + ".bin" + \
                        " --fpf=" + results_dir + BINNAME + ".fpf" + \
                        " --input-bit-depth=" + BitDepth + \
                        " --fps=" + FrameRateSetting + \
                        " --auto-alt-ref=1 --lag-in-frames=19 --end-usage=vbr " + \
                        " --threads=1  -v --i420 " + \
                        " --test-decode=" + TestDecodeAtEncoder +\
                        " --codec=av1 " + \
                        " --minsection-pct=0 --maxsection-pct=2000 " + \
                        " --static-thresh=0 --drop-frame=0 --tune=psnr " + \
                        " --q-hist=0 --rate-hist=0 --psnr --bit-depth=" + BitDepth + \
                        " --arnr-maxframes=7 --arnr-strength=3 --enable-fwd-kf=1  " + \
                        Options

              print(enc_cmd)
              enc_cmd += ' 2> ' + enc_log
              if ToEncode=='1':
               os.system(enc_cmd)

              if ToDecode=='1':
               dec_cmd = exeroot_path + executable_dec + ' ' + results_dir + BINNAME +".bin" + " "  + \
                         " --i420 " + \
                         " -o " + results_dir + BINNAME + ".yuv" + " --summary"
               dec_cmd += ' 2> ' + dec_log
               print(dec_cmd)
               #if ReadResultOnly != '1':
               os.system(dec_cmd)

              if ToMeasure=='1':
               remove_controlchar(enc_log)
               rate, psnr_y, psnr_u, psnr_v, enc_time = get_bitstream_psnr_libaom(enc_log)
               if ToDecode=='1':
                   dec_time = get_dec_time_libaom(dec_log)
               else :
                   dec_time = 0
               seq_col.append(seq_name)
               data = np.vstack((data, np.array(
                   [rate, psnr_y, psnr_u, psnr_v,enc_time, dec_time])))
               datatocsv = data[1:, :]
               df = pd.DataFrame()
               df['seq-name'] = seq_col
               df['rate'] = datatocsv[:, 0]
               df['psnr_y'] = datatocsv[:, 1]
               df['psnr_u'] = datatocsv[:, 2]
               df['psnr_v'] = datatocsv[:, 3]
               df['enc_time'] = datatocsv[:, 4]
               df['dec_time'] = datatocsv[:, 5]




              csv_path = csv_dir + '_' + '_BDnumbers' + '.csv'
              df.to_csv(csv_path, index=None)

