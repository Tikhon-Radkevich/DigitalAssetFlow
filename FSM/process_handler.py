from Router import Router


router = Router()


@router.depth_update()
def processing_1(depth: dict, storage: dict):
    print(depth)
#
#
# @router.analysis_update()
# def processing_2(analysis, storage):
#     sleep(5)
#     print("analysis update")

