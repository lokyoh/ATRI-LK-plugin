import random

from ATRI import driver, TEXT_DIR
from ATRI.log import log
from ATRI.service import Service

DATA_PATH = TEXT_DIR / "tiangou.txt"

tian_gou = Service("舔狗日记").document("爱你无需多言(doge)").type(Service.ServiceType.ENTERTAINMENT).version("1.1.0")

get_tiangou = tian_gou.on_command(cmd='舔狗日记', docs='爱你无需多言(doge)')


@get_tiangou.handle()
async def _():
    await get_tiangou.finish(random.choice(tiangou))


tiangou = []

with open(DATA_PATH, 'r', encoding='utf-8') as file:
    for line in file:
        tiangou.append(line)

driver().on_startup(lambda: log.success(f'舔狗日记共加载{len(tiangou)}个'))
