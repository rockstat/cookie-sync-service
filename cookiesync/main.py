# Band service skeleton
# (c) Dmitry Rodin 2018
# ---------------------
import asyncio
from itertools import count
from prodict import Prodict as pdict
from band import expose, cleanup, worker, settings, logger, response, redis_factory


state=pdict()
partners=settings.partners


def gen_key(uid):
    key = str(uid).encode()
    return f'cs:{key}'


async def set_id(uid, partner, ext_id):
    with await state.redis_pool as conn:
        await conn.execute('hmset', gen_key(uid), partner, ext_id)


@expose.handler()
async def init(uid, data, **params):
    partner = data.get('partner', None)
    if partner and state.redis_pool:
        logger.info('init: partner given')
        partner_data = partners.get(partner, None)
        if partner_data and partner_data.init:
            logger.info('init: partner and init link found. redirecting')
            link = partner_data.init.format(partner_id=uid)
            return response.redirect(link)
    return response.pixel()


@expose.handler()
async def sync(uid, data, **params):
    partner = data.pop('partner', None)
    partner_id = data.pop('partner_id', None)
    if partner and partner_id and state.redis_pool:
        logger.info('sync: params given, rerdis connected')
        partner_data = partners.get(partner, None)
        if partner_data:
            logger.info('sync: partner found. saving match')
            await set_id(uid, partner, partner_id)
            if partner_data.sync:
                logger.info('sync: sync pixel found. redirecting')
                link = partner_data.sync.format(partner_id=uid, user_id=partner_id)
                return response.redirect(link)
    return response.pixel()


@expose.handler()
async def done(uid, data, **params):
    partner = data.pop('partner', None)
    partner_id = data.pop('partner_id', None)
    user_id = data.pop('user_id', None)
    if uid != user_id:
        logger.warn('user ids not equal')
        return response.pixel()
    if partner and partner_id and user_id:
        logger.info('done: params given', p=partner, pid=partner_id, u=user_id)
        if partner in partners:
            logger.info('done: partner found', p=partner)
            if state.redis_pool:
                logger.info('done: redis connected. saving')
                await set_id(uid, partner, partner_id)
    return response.pixel()


@worker()
async def service_worker():
    for num in count():
        try:
            if not state.redis_pool:
                state.redis_pool = await redis_factory.create_pool()
        except asyncio.CancelledError:
            break
        except Exception:
            logger.exception('exc')
        await asyncio.sleep(30)
