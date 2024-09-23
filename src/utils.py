# TODO come up with a better name for this package ('pkg' is not very descriptive)

# create a label function
def _label_func(f):
    import re
    return f[0].isupper()

# I think this function is showing a batch of images
# def _batch_ex(bs):
#     from fastai.vision.all import TensorImage
#     return TensorImage(timg[None].expand(bs, *timg.shape).clone())
