from time import sleep

from Router import Router


router = Router()


# def _sort_order_book(self, symbol):
#     for side in ["asks", "bids"]:
#         orders = self._order_book[symbol][side]
#         prices = sorted(orders.keys(), reverse=True)
#         self._order_book[symbol][side] = {key: orders[key] for key in prices}


@router.depth_update()
def processing_1(depth: dict, storage: dict):
    print(depth)


@router.analysis_update()
def processing_2(analysis, storage):
    sleep(5)
    print("analysis update")

