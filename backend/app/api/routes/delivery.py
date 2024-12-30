from fastapi import APIRouter, HTTPException, Query, Request
from sqlalchemy import and_

from app.api.deps import SessionDep
from app.api.pagination import PageNumberPagination, paginate_by_page_number
from app.dao import delivery_dao
from app.dto import DeliveryApiInDTO, DeliveryDTO


router = APIRouter(tags=["delivery"], prefix="/delivery")


# @router.post("", status_code=201, response_model=TronWalletDTO)
# async def update_or_create(wallet_in: TronWalletApiInDTO) -> TronWalletDTO:
#     is_ok, result = await update_or_create_tron_account_info_service(wallet_in.address)
#     if not is_ok:
#         raise HTTPException(status_code=400, detail=result)
#     return result  # type:ignore[return-value]


# @router.get("", response_model=PageNumberPagination)
# async def get_list(
#     request: Request,
#     session: SessionDep,
#     page: int = Query(default=1, ge=1),
#     per_page: int = Query(default=100, ge=1, le=1000),
#     order: str = Query(default="id"),
# ) -> PageNumberPagination:
#     total = await tron_wallet_dao.count(session)
#     if total:
#         items = await tron_wallet_dao.get_list(
#             session, skip=(page - 1) * per_page, limit=per_page, order=order
#         )
#     else:
#         items = []
#     return paginate_by_page_number(request, items, total, page, per_page)
#
#
# @router.get("/{address}", response_model=TronWalletDTO)
# async def get(
#     address: str,
#     session: SessionDep,
# ) -> TronWalletDTO | None:
#     tron_wallet_dto = await tron_wallet_dao.get(
#         session, filter_expr=and_(TronWallet.address == address)
#     )
#     if not tron_wallet_dto:
#         raise HTTPException(status_code=404, detail="Not found")
#     return tron_wallet_dto
#
#
# @router.delete("/{address}", status_code=204)
# async def delete(
#     address: str,
#     session: SessionDep,
# ) -> None:
#     await tron_wallet_dao.remove(
#         session, filter_expr=and_(TronWallet.address == address)
#     )
#     return
