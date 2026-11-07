"""Additional controls, without modifying the frozen earlier model factories."""
import math
import torch
from torch import nn
from torch.nn import functional as F
from src.models.simple_quantile_risk import TCNQuantileRisk,QuantileRiskBase,make_model

class TCNLast(TCNQuantileRisk):
    def encode(self,x):return self.tcn(x.transpose(1,2))[:,:,-1]

class TransformerRisk(QuantileRiskBase):
    def __init__(self):
        super().__init__();self.input=nn.Linear(18,64)
        layer=nn.TransformerEncoderLayer(64,4,128,.1,batch_first=True)
        self.encoder=nn.TransformerEncoder(layer,2,enable_nested_tensor=False)
        for p in self.encoder.parameters():
            if p.ndim>1:nn.init.xavier_uniform_(p)
        pos=torch.arange(30).float().unsqueeze(1);rates=torch.exp(torch.arange(0,64,2)*(-math.log(10000)/64));pe=torch.zeros(30,64);pe[:,0::2]=torch.sin(pos*rates);pe[:,1::2]=torch.cos(pos*rates);self.register_buffer('position',pe)
    def encode(self,x):return self.encoder(self.input(x)+self.position[:x.shape[1]])[:,-1,:]

class GaussianGRU(nn.Module):
    def __init__(self):
        super().__init__();self.gru=nn.GRU(18,64,batch_first=True);self.fusion=nn.Sequential(nn.Linear(64,64),nn.ReLU(),nn.Dropout(.2));self.mean=nn.Sequential(nn.Linear(64,32),nn.ReLU(),nn.Linear(32,1));self.scale=nn.Sequential(nn.Linear(64,32),nn.ReLU(),nn.Linear(32,1))
    def mean_scale(self,x):
        h=self.fusion(self.gru(x)[0][:,-1,:]);return 125*self.mean(h),125*(F.softplus(self.scale(h))+.001)
    def forward(self,x):
        mu,sd=self.mean_scale(x);z=(30-mu)/sd;eta=torch.special.log_ndtr(z)-torch.special.log_ndtr(-z);return mu-1.6448536269514722*sd,mu,mu+1.6448536269514722*sd,eta

def factory(arm):
    if arm=='tcn_last':return TCNLast()
    if arm=='transformer':return TransformerRisk()
    if arm=='gaussian':return GaussianGRU()
    return make_model(arm)
