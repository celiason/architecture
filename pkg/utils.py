# create a label function
def label_func(f):
    return f[0].isupper()

# TODO figure out what this function is doing!
def _batch_ex(bs):
    return TensorImage(timg[None].expand(bs, *timg.shape).clone())

