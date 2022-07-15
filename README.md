# Traffic Flow Prediction(TFP) on Taipei metro with daily COVID-19 cases

## **��ƨӷ�**<br/>
- �x�W�C��T�E�H�Ƹ�T: �úֳ��e�޸p(CDC)
- �O�_���B�C�p�ɦU���i�X�H�y: �F���}���ƥ��x

## **�ѦҤ��m**<br/>
- **DCRNN**: Diffusion Convolutional Recurrent Neural Network: data-driven traffic forecasting, 2018
- **ST-GCN**: Predicting Station-Level Short-Term Passenger Flow in a Citywide Metro Network Using Spatiotemporal Graph Convolutional Neural Networks, 2019
- **ASTGCN**: Attention Based Spatial-Temporal Graph Convolutional Networks for Traffic Flow Forecasting, 2019<br/>

## **����**<br/>
�H���Y���S��ǬV�ʪͪ��]Coronavirus disease 2019�A�Y�g�GCOVID-19�^���̱����N�A�b�j���B��W���F�w�����r�B�j������f�n�H���U�ɤj���ɥi�઺�O������Z���~�A�b�T�E�Ӯ׷f���L���y��W�]�����ƾǧL�i��������r�C���קK���S��T�E�����I���A�\�h���q�Ұʤ��դu�@�Φb�a�u�@���Ҧ��A�H�קK���u�P�V�F�U�žǮդ]�H���Ҥ����ǡA���U��ǥͻ��Z�W�ҡA��X�\�h�]���ϱo���B�f���y�q��֡A�y�q���Ͷլۤ�H���]�󬰤��P�C

<p align="center">
<img src="image/routemap2020.png" width="200" height="200"/><br/>
�O�_���B���u��(source: �O�_�j�����B�ѥ��������q)
</p>

���g�����s�������ʽ�A�N���B���������@�㦳��V�ʡB�ɶ��ʪ��ϡ]Graph�^�A�C�ӱ��B���K�O�Ϥ����`�I�]Node�^�A�⯸�����O�_�۳s�i��F�K�O��]Edge�^�A���ձN�`�׾ǲߡB���s��������k���Φܥx�_���B����q�y�q�w���A�øչϦb�T����k�W�ǤJ�C�骺�T�E�H�Ƹ�T�Ϲw�����ȧ�[�ǽT�C<br/>

<p align="center">
<img src="image/taiwan_cases.png" width="300" height="200"/><br/>
�x�W�C��s�W�T�E�H��(2020-01-01 to 2021-04-30)
</p>

## **�ҫ�**<br/>
�����s�����b��q�y�q�w������k�A���g�ھ�ASTGCN����k�A�ھڷ�e��ƪ��S�ʰ��X�վ�C�b��J�W<img src="https://render.githubusercontent.com/render/math?math=x_h, x_d, x_w">���O�N��eh�p�ɶi�X�y�q�B�ed��b�S�w�ɬq���i�X�y�q�Ϋew��§���b�S�w�ɬq���i�X�y�q�C<br/>

����y�{�W���S��b��N���B�y�q���O��Ŷ��P�ɶ��i��F�`�N�O����]Attention�^�ASAtt�]Spatial Attention�^�PTAtt�]Temporal Attention�^���O���w��Ŷ��B�ɶ����`�N�O����FGCN�N��Ϩ��n�]Graph Convolution�^�FConv�N����n�]Convolution�^�FFC�N����s���h�]Fully-connected�^�FST block�N�� Spatial-Temporal block�A�H���]block�^���覡��ܸӵ��c�H�ۦ����覡�i��걵�F�̫�LSTM block�N��LSTM�ҫ��A�D�n�N�C��COVID-19�T�E�H�ƪ���T�i��S�x�����C

<p align="center">
<img src="image/model_strc.png" width="350" height="210"/><br/>
���g��s���ҫ��[�c
</p>

<p align="center">
<img src="image/ASTGCN.png" width="325" height="260"/><br/>
ASTGCN(source: ASTGCN, Guo etal., 2019)
</p>

## **���絲�G**<br/>
������A��ƨ̾ڱ��B��ƪ��ɶ����פ��e90%�@���V�m��ơA��10%�H5%�B5%���@���Ҹ�ƻP���ո�ơA���N�ƬҬ�150��epochs�C�U���������窺���G�A�b�o�����w�����ȤW�D�n�e�{MAE�BRMSE��MAPE�T�ث��СA�b�ҫ��s��1�P�s��2���t�O�b��O�_���Q��LSTM�ǤJCOVID-19��ơA�Ӹӵ��G�D�n��ܤF�Ҽ{COVID-19��Ư�Ϲw�����ȧ�[�ǽT�A�S�O�bMAE�PMAPE�Ҥ�쥻��<img src="https://render.githubusercontent.com/render/math?math=\frac{1}{3}\sim\frac{1}{4}">�C<br/>
�Ӽҫ��s��3�A�D�n�O�H��L���Φ��Ҽ{COVID-19��ơA�C�ӯ��I���|�Ҽ{�ӯ�����F��(ex.�x�_����/�����ϡB��s/���s�Ϥj�P�ϥ��)�A���e7�ѽT�E�H�ơA�Y�����F�ϥ���I�h�������@���N��C�ӳo�˪��ҫ��V�m�ĪG�ä��ΡA�q����]�D�n����ءG(1) �b2021�~5��e�A�x�W�����g�T�E�Ʒ��C�A���h�ƪ��ѼƽT�E�Ƭ��Ӧ�ơA�Y�b�e����H��F�ϰϤ��h�|�ϱo�j�h�ƪ���Ƭ�0�A�]���ҫ������Ǥ���S�x�B�h�ϥΤF�B�~���ѼơA��V�äF��L�S�x�������E�X�F(2) ���B��ƻPCOVID-19��Ƭ���ؤ��P�ɶ��B������ơA�@�ج��p�ɤ@�ج��ѡA�]����COVID-19��Ʈھڮɶ��걵�����B��Ʈɷ|�Ϸ�Ѫ����B�i�X���H�Ʀ걵��P�˪�COVID-19�S�x�A�o�]�ϼҫ��S��k�n�n�i��E�X�C


<div align="center">

|  Model<br/>No.  |  (hourly, Daily, Weekly)  |  With COVID-19<br/>features  |    <br/>MAE    |  Metrics<br/>RMSE  |    <br/>MAPE    |
|  :----:  | :----:  |  :----:  |  :----:  |  :----:  |  :----:  |
|  1  | (2,2,1)  |  No  |  95.09  |  177.98  |  100.71  |
|  2  | (2,2,1)  |  Yes  |  **78.47**  |  **164.71**  |  **76.88**  |
|  3  | (2,2,1)  |  x  |  870.64  |  1392.36  |  2313.79  |

</div>


Maily use `Train_ASTGCN_LSTM.py` <br/>
Otherwise: <br/>
- Data reformat and visualization: `data preprocess.ipynb`
- Get matro location: `preprocess/GetMetroDistrict.py`
- Test of model function: `train_ASTGCN_LSTM.ipynb`