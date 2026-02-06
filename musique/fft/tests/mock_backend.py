import numpy as np
import musique.fft
import threading

class _MockFunction:
    def __init__(self, return_value = None):
        self.number_calls = threading.local()
        self.return_value = return_value
        self.last_args = threading.local()

    def __call__(self, *args, **kwargs):
        if not hasattr(self.number_calls, 'c'):
            self.number_calls.c = 0

        self.number_calls.c += 1
        self.last_args.l = (args, kwargs)
        return self.return_value


fft = _MockFunction(np.random.random(10))
fft2 = _MockFunction(np.random.random(10))
fftn = _MockFunction(np.random.random(10))

ifft = _MockFunction(np.random.random(10))
ifft2 = _MockFunction(np.random.random(10))
ifftn = _MockFunction(np.random.random(10))

rfft = _MockFunction(np.random.random(10))
rfft2 = _MockFunction(np.random.random(10))
rfftn = _MockFunction(np.random.random(10))

irfft = _MockFunction(np.random.random(10))
irfft2 = _MockFunction(np.random.random(10))
irfftn = _MockFunction(np.random.random(10))

hfft = _MockFunction(np.random.random(10))
hfft2 = _MockFunction(np.random.random(10))
hfftn = _MockFunction(np.random.random(10))

ihfft = _MockFunction(np.random.random(10))
ihfft2 = _MockFunction(np.random.random(10))
ihfftn = _MockFunction(np.random.random(10))

dct = _MockFunction(np.random.random(10))
idct = _MockFunction(np.random.random(10))
dctn = _MockFunction(np.random.random(10))
idctn = _MockFunction(np.random.random(10))

dst = _MockFunction(np.random.random(10))
idst = _MockFunction(np.random.random(10))
dstn = _MockFunction(np.random.random(10))
idstn = _MockFunction(np.random.random(10))

fht = _MockFunction(np.random.random(10))
ifht = _MockFunction(np.random.random(10))


__ua_domain__ = "numpy.musique.fft"


_implements = {
    musique.fft.fft: fft,
    musique.fft.fft2: fft2,
    musique.fft.fftn: fftn,
    musique.fft.ifft: ifft,
    musique.fft.ifft2: ifft2,
    musique.fft.ifftn: ifftn,
    musique.fft.rfft: rfft,
    musique.fft.rfft2: rfft2,
    musique.fft.rfftn: rfftn,
    musique.fft.irfft: irfft,
    musique.fft.irfft2: irfft2,
    musique.fft.irfftn: irfftn,
    musique.fft.hfft: hfft,
    musique.fft.hfft2: hfft2,
    musique.fft.hfftn: hfftn,
    musique.fft.ihfft: ihfft,
    musique.fft.ihfft2: ihfft2,
    musique.fft.ihfftn: ihfftn,
    musique.fft.dct: dct,
    musique.fft.idct: idct,
    musique.fft.dctn: dctn,
    musique.fft.idctn: idctn,
    musique.fft.dst: dst,
    musique.fft.idst: idst,
    musique.fft.dstn: dstn,
    musique.fft.idstn: idstn,
    musique.fft.fht: fht,
    musique.fft.ifht: ifht
}


def __ua_function__(method, args, kwargs):
    fn = _implements.get(method)
    return (fn(*args, **kwargs) if fn is not None
            else NotImplemented)
