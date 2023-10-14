from DepthProcessing.filter import get_order_book

from CryptoDataCollector.Router import Router
from CryptoDataCollector.Storage import Storage


router = Router()


@router.depth_update()
def processing_1(depth: dict, storage: Storage):
    storage.storage["depth"] = depth
    storage.storage["filtered_depth"] = get_order_book(depth, pct_chang=0.016)


@router.analysis_update()
def processing_2(analysis: dict, storage: Storage):
    storage.storage["analysis"] = analysis


@router.save_data()
def processing_3(storage: Storage):
    print(storage.storage["filtered_depth"])

