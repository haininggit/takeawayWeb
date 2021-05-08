data = {}
ens = {
    "code": 200,
    "data": data,
    "msg": "success"
}


def successful(data):
    ens['data'] = data
    return ens

# def successful(**kwargs):
#     data = kwargs['data']
#     ens['data'] = data
#     return ens


def failed(msg):
    ens['msg'] = msg
    ens['code'] = 400
    return ens


if __name__ == '__main__':
    a = {"d": "d"}
    b = ['sa', 's']
    print(successful(a))
