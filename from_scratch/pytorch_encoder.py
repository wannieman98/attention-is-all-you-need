from ... import util
from torch.nn import Dropout
from torch.nn import Module

class Encoder(Module):
    def __init__(self, layer, N):
        super(Encoder, self).__init__()
        self.layers = util.clones(layer, N)
        self.norm = util.LayerNorm(layer.size)

    def forward(self, x, mask):
        for layer in self.layers:
            x = layer(x, mask)
        return self.norm(x)

class EnocderLayer(Module):
    def __init__(self, size, self_attn, feed_forward, dropout):
        super(EnocderLayer, self).__init__()
        self.self_attn = self_attn
        self.feed_forward = feed_forward
        self.dropout = Dropout(dropout)
        self.sublayer = util.clones(util.SubLayer(size, dropout), 2)
        self.size = size

    def forward(self, x, mask):
        x = self.sublayer[0](x, lambda x: self.self_attn(x, x, x, mask.reshape((128, 22))))
        return self.sublayer[1](x, self.feed_forward)