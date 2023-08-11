from Router import Router


router = Router()

# def _sort_order_book(self, symbol):
#     for side in ["asks", "bids"]:
#         orders = self._order_book[symbol][side]
#         prices = sorted(orders.keys(), reverse=True)
#         self._order_book[symbol][side] = {key: orders[key] for key in prices}


@router.depth_update()
def processing_1(depth):
    pass
    print("bids:", depth["bids"])


@router.depth_update()
def processing_2(depth):
    pass
    # print("asks:", depth["asks"][:10])
