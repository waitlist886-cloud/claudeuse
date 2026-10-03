# -*- coding: utf-8 -*-
"""组卡：以用户 0930 导出为底，换主提示词、后缀、CSS，世界书＝新核心＋已重制时代（匹诺康尼、雅利洛、仙舟、哈托彼亚）＋其余时代的旧条目（索引）。
创作文本全部来自手写的 md；本脚本只做切分、钥匙拼接与装箱。"""
import json, re, glob, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # 工作包根目录
B = os.path.join(ROOT, '02_构建')            # 主提示词、后缀、CSS、各时代总览
ERA_DIR = os.path.join(ROOT, '03_时代')      # 各时代的档案批次（子目录随便分，按文件名找）
OUT_DIR = os.path.join(ROOT, '01_成品')
SRC = glob.glob(os.path.join(ROOT, '00_底稿', '*.json'))[0]   # 以你最近一次导出为底；换底就换这个文件
VER = 'v1.3'
OUT = os.path.join(OUT_DIR, f'银轨纪行_{VER}_匹诺康尼雅利洛仙舟哈托彼亚重制_以你0930导出为底.json')

def entry(group, key, value, depth, kr, sort):
    return {"group": group, "match_type": 3, "key": key, "key_region": kr, "value_type": 0,
            "value": value.strip() + "\n", "value_configs": [], "value_region": 1,
            "sort": sort, "depth": depth, "probability": 100, "enable": True}

def parse_meta_file(path):
    txt = open(path, encoding='utf-8').read()
    parts = re.split(r'\n?@@ENTRY ', '\n' + txt)
    out = []
    for p in parts[1:]:
        head, body = p.split('\n', 1)
        meta = dict(kv.strip().split('=', 1) for kv in head.split(' | '))
        out.append((meta, body))
    return out

def rx_escape(t):
    return re.sub(r'([.^$*+?{}\[\]\\|()])', r'\\\1', t)

ORDER = ['第一批', '第二批', '第三批', '第四批', '第五批', '第六批']

# ---------- 核心条目 ----------
core_entries = []
odd = iter(range(1, 400, 2))
for meta, body in parse_meta_file(os.path.join(B, 'wb_core.md')):
    core_entries.append(entry(meta['group'], meta['key'], body, int(meta['depth']), int(meta['kr']), next(odd)))

# ---------- 已重制的时代 ----------
# 匹诺康尼
PEN_STOP = set("""入梦 梦里 相位 公司 时刻 大典 开幕 忆者 繁育 神秘 假面愚者 虚无令使 太一 博识学会 领航员 测绘师 歌者 黑客
牛仔 星际和平公司 石心十人 基石 舰队 赌局 炸弹 剧透 烟花 寰宇蝗灾 动画 原型 齿轮 史学家 出勤 坑 盐 信使 内乱 迷失 空洞 禁航
公馆 苦痛 起义 暴动 独立 停火 粉笔 荒地 惊醒 账本 驻军 信号塔 起降坪 补给船 检查站 主舰 弹药库 水塔 路封 高热 铁骑 子夜 正午
哥哥 亲爱的 贪心 那把刀 幕布 锚 记号 年轻人 飞蛾扑火 Boom 巡海游侠 虫灾 工区 果园 回潮 大剧院""".split())
PEN_REMOVE = {
    '活事件：《谐乐大典》': ['十二时刻', '死灭之蛹'],
    '博雷克林·铁尔南': ['银轨'],
    '活事件：《银轨》': ['银轨'],
    '匹诺康尼 2158': ['2158'],
    '流梦礁与稚子的月光': ['黑狗'],
}
PEN_EXTRA = {
    '博雷克林·铁尔南': ['银轨尽头', '重开银轨'],
    '活事件：《银轨》': ['重开银轨', '开垦银轨', '银轨修复', '银轨尽头'],
    '其他来客': ['真理医生', '银枝', '希世难得号', '唐·怀亚特', '梅芙恩·伊里斯', '惠特克爵士', '其他来客'],
    '匹诺康尼大剧院': ['匹诺康尼大剧院', '谐乐颂', '中央监狱', '好梦剧场', '大剧院的幕布'],
    '活事件：《白色沙漠》': ['果园的水', '黑布林的果园'],
    '忆质泄口与球笼工区': ['球笼工区'],
    '活事件：《狼之死》': ['哈努努之死', '老狼上船'],
    '活事件：《虫鸣》': ['匹诺康尼的虫灾', '那年的虫灾'],
}

# 雅利洛：词义太宽、或会撞别的时代（星核、公司、列车组、假面愚者、仙舟、瞥视……）的钥匙都不要，靠专名触发
JAR_STOP = set("""公司 星核 奇迹 许愿 列车 星穹列车 列车组 开拓者 三月七 丹恒 姬子 瓦尔特 帕姆 无名客 景元 仙舟人 砂金 假面愚者 瞥视
反物质军团 万界之癌 星际和平公司 公司的人 公司员工 总监 投资人 旧世界 星港 远行 迁徙 避难所 安全屋 矿工 矿队 工头 流浪者
上层 下层 守护者 继承人 手记 历法 大学 伯爵 智者 配给 建制 议事 十二年 十余年 新世界 养母 实验室 面具 民兵 演算 概率 格式化
外来者 宝藏 冒险 小朋友 孤儿院 阿丽娜（孤儿院的） 小子 师父 大叔 头儿 老头子 亲爱的 那女人 大人 长官 哥 姐 拉钩 迷晕 迷药 换装 假发
抓捕 战后 债务 合同 手机 群聊 现行 眼下 大门封闭 放逐 残响 城外 禁区 悬崖 蝴蝶 塔 墙 钟 井 雪 冷 冰 钱 碑 门 船 枪 盾 拳 狼 蟹
日记 书信 信 照片 价 引擎 蜘蛛 铁锤 军医 守军 缺口 那一夜 烛火 炉子 重建 餐具 安东 试剂 愚者 米哈伊 傀儡 演武仪典 邀请函 封锁
星际和平公司（节点六） 景元（节点六） 无名客（节点六） 瓦尔特·杨 杨叔 求援""".split())
JAR_REMOVE = {'虎克与鼹鼠党': ['阿丽娜'], '其他来客': ['瓦尔特·杨', '杨叔']}
JAR_EXTRA = {
    '其他来客': ['其他来客', '列车上的另一位乘客', '仙舟的船'],
    '活事件：《愚者》': ['希莉儿案', '愚者希莉儿', '第八任之死'],
    '希莉儿、希莉雅与斯捷潘': ['愚者守护者', '第八任大守护者'],
    '历代大守护者': ['米哈伊·兰德', '卡特琳娜·兰德', '肖像墙', '十九任'],
    '伊戈尔·哈夫特': ['伊戈尔的远行', '罗浮的拳手', '七百年前的拳手'],
    '活事件：《断航》': ['罗浮的信', '六百年的静'],
    '托帕与公司': ['战略投资部的人', '公司的总监', '石心十人的电话'],
    '虎克与鼹鼠党': ['鼹鼠党的老大', '阿丽娜的爸爸妈妈'],
    '活事件：《封锁令》': ['封锁的那一年', '封锁十二年', '封锁十余年'],
    '活事件：《冬夜》': ['列车来了', '列车停靠', '外来者进城', '那三个外来者'],
}

# 仙舟：词义太宽、或会撞别的时代（列车组、星核猎手、公司、匹诺康尼的来客、通用词）的钥匙都不要，靠专名触发
XZ_STOP = set("""公司 星核 列车 星穹列车 列车组 开拓者 三月七 丹恒 姬子 瓦尔特 帕姆 无名客 卡芙卡 刃 尾巴 老铁 将军 黑洞 红星 死士 大火
星际和平公司 博识学会 黄金年代 宣言 物价 群聊 其他来客 卢卡 桑博 托帕 波提欧 银枝 公司专员 流星 妾身 小女子 姐姐 小妹 长高 问责 劫后
战后 那个人 轮替 匣子 打扫卫生 金人 信仰危机 医士 复仇 阴谋 誓言 棺材 大人 恩公 老师 师父 徒弟 兄弟 家人 故乡 古国 启航 天艟
星核猎手 锁链 灵符 策士 熏香 补天 烽火 标准 不朽 位子 武库 折翼 王牌 摸鱼 星际海盗 叛徒 神使
枪 箭 船 门 碑 信 纸 牌 茶 酒 糖 香 药 梦 卵 月 星 光 血 泥 雪 冷 热""".split())
XZ_REMOVE = {
    '罗浮 8100': ['太卜司', '工造司', '丹鼎司', '鳞渊境', '幽囚狱', '罗浮'],
    '活事件：《九艟》': ['古国', '启航'],
    '帝弓（登神以前的那个人）': ['那个人'],
    '罗刹': ['匣子'],
    '貊泽与椒丘': ['巡镝'],
}
XZ_EXTRA = {
    '活事件：《九艟》': ['仙舟启航', '九舟出航', '仙舟的来历', '仙舟从哪儿来'],
    '帝弓（登神以前的那个人）': ['帝弓的故事', '帝弓是谁', '帝弓的真名'],
    '活事件：《建木》': ['仙舟人怎么不死的', '长生之始', '建木降临'],
    '活事件：《火劫》': ['帝弓之箭', '帝弓的那一箭'],
    '活事件：《云上五骁》': ['五骁的故事', '五骁是谁'],
    '活事件：《倏忽之乱与饮月之乱》': ['饮月之乱的真相', '丹枫做了什么', '五骁的结局'],
    '景元': ['景元将军', '神策府的主人', '白头发的将军'],
    '罗浮 8100': ['罗浮8100', '罗浮的物价', '罗浮的报纸', '罗浮的群聊', '罗浮的地方', '罗浮的洞天'],
    '活事件：《星核》': ['列车到罗浮', '星核在建木里', '罗浮的星核'],
    '活事件：《演武》': ['呼雷之乱', '演武仪典的那场仗', '演武仪典（8100）'],
    '活事件：《慰灵》': ['罗浮的慰灵', '劫后的罗浮'],
    '其他来客｜列车、公司、学会与一个贝洛伯格的孩子': ['罗浮的来客', '列车组在罗浮', '卢卡在罗浮', '卢卡来仙舟'],
    '藿藿与尾巴': ['藿藿的尾巴', '尾巴大爷'],
    '云璃与怀炎｜朱明的剑': ['云璃的老铁', '老铁（剑胚）'],
    '十王司与幽囚狱': ['十王司', '幽囚狱'],
    '魔阴身（尺子档案）｜与柳华、寒泉派': ['魔阴身的尺子'],
    '持明、龙尊与龙师': ['鳞渊境的持明'],
}

# 哈托彼亚：词义太宽、或会撞别的时代（列车组、星核猎手、公司部门、匹诺康尼与仙舟的来客、通用词）的钥匙都不要，靠专名触发
HT_STOP = set("""三月七 丹恒 帕姆 瓦尔特 姬子 星期日 银狼 花火 火花 砂金 翡翠 知更鸟 桑博 刃 应星 停云 忘归人 怀炎 竟天 大丽花 康士坦丝 焚化工 铁尔南 零号
列车组 战略投资部 市场开拓部 技术研发部 石心十人 星际和平公司 一切献给琥珀王 寰宇蝗灾 流梦礁 古国时代 假面愚者 本座 建木 威灵 调律
面具 奇迹 相位 群聊 一分钟 酒馆 影子 剧本 骰子 钻石 临摹 大猫 雪球 随便 处决 逃离 布阵 塔顶 学院 校长 院长 前辈 部长 管家 养子 祖宗 闭嘴 张嘴 无言
舒翁 车票 法界 旁白 剧团 归途 启行 灰烬 曙光""".split())
HT_REMOVE = {
    '古弁才天国': ['古国时代'],
    '真隆介与假隆介': ['无言'],
}
HT_EXTRA = {
    '幻月游戏': ['谒者面具', '面具的能力', '欢愉假面', '幻月游戏怎么玩', '幻月游戏的刻度'],
    '二相乐园 1999': ['乐园的群聊', '二相乐园的群聊', '二相乐园的热搜'],
    '真隆介与假隆介': ['隆介校长', '绘世学院院长', '院长隆介', '隆介的无言', '闭嘴机器人', '机器人闭嘴', '隆介身边的机器人', '归途项目', '隆介的归途'],
    '活事件：《逃离》': ['逃离乐园', '逃出哈托彼亚', '逃离二相乐园', '逃离哈托彼亚'],
    '活事件：《十五年》': ['处决告死魔', '告死魔的处决', '处决那天'],
    '七人部长与在田': ['在田的一分钟', '千星城的管家', '在田的养子', '在田那一票'],
    '归寂／我见／未抵': ['归寂的骰子', '骰子头', '会说话的骰子', '骰子脑袋'],
    '「世界尽头」酒馆（哈托彼亚分店）': ['乐子神的酒馆', '愚者的酒馆', '酒馆的规矩', '哈托彼亚的酒馆'],
    '活事件：《游乐王》': ['埃尔温的随便', '说了句随便', '随便那一届'],
    '真珠': ['真珠的临摹', '真珠的推演'],
    '绯英': ['哈托彼亚的建木', '秘庭的建木', '秘庭的树'],
    '火花与花火': ['火花的直播', '花火在哈托彼亚', '火花在哈托彼亚'],
    '千星城': ['张嘴烤肠', '加钠烤肠机器人'],
    '悲悼伶人与假面愚者（在哈托彼亚）': ['哈托彼亚的愚者', '哈托彼亚的伶人', '愚者与伶人同台'],
    '列车组与仙舟来客（在二相乐园）': ['列车组在哈托彼亚', '列车组的人', '仙舟来客', '列车上的另一位乘客'],
    '姬子·启行': ['姬子的过去', '姬子的真相', '姬子回来了'],
    '银狼 LV.999': ['银狼在哈托彼亚', '银狼的面具'],
    '千冶·刃（在哈托彼亚）': ['刃在哈托彼亚', '刃的面具', '刃与倏忽'],
    '星期日（乌鸦面具）': ['星期日在哈托彼亚', '星期日的面具', '星期日的车票'],
    '爻光': ['爻光的锦囊', '爻光的卦', '仙舟来的将军'],
    '二维市的人': ['猴子老白', '会说话的猴子'],
    '幽灵与死后就业': ['千星城的死人', '死了还要上班'],
    '活事件：《血涂》': ['十五年前的幻月游戏', '上一届幻月游戏'],
    '破晓战队与灰烬': ['灰烬战士', '破晓的灰烬', '破晓的曙光', '破晓的赤焰'],
}

ERAS = [
    dict(tag='匹诺康尼', group='10｜匹诺康尼', core='wb_pen_core.md', archives='匹诺康尼_档案_第*批.md',
         sort_start=4541, sort_end=4977, STOP=PEN_STOP, REMOVE=PEN_REMOVE, EXTRA=PEN_EXTRA, old_prefix='10｜'),
    dict(tag='雅利洛', group='09｜雅利洛寒潮', core='wb_jar_core.md', archives='雅利洛_档案_第*批.md',
         sort_start=4031, sort_end=4541, STOP=JAR_STOP, REMOVE=JAR_REMOVE, EXTRA=JAR_EXTRA, old_prefix='09｜'),
    dict(tag='仙舟', group='08｜仙舟', core='wb_xz_core.md', archives='仙舟_档案_第*批.md',
         sort_start=3441, sort_end=4031, STOP=XZ_STOP, REMOVE=XZ_REMOVE, EXTRA=XZ_EXTRA, old_prefix='08｜'),
    dict(tag='哈托彼亚', group='11｜哈托彼亚', core='wb_ht_core.md', archives='哈托彼亚_档案_第*批.md',
         sort_start=4979, sort_end=5357, STOP=HT_STOP, REMOVE=HT_REMOVE, EXTRA=HT_EXTRA, old_prefix='11｜'),
]

era_entries = {}   # tag -> (core_list, archive_list, keytable)
for era in ERAS:
    sorts = iter(range(era['sort_start'], era['sort_end'], 2))
    cores = []
    for meta, body in parse_meta_file(os.path.join(B, era['core'])):
        cores.append(entry(meta['group'], meta['key'], body, int(meta['depth']), int(meta['kr']), next(sorts)))
    archives, keytable = [], []
    files = glob.glob(os.path.join(ERA_DIR, '*', era['archives']))
    files = sorted(files, key=lambda f: next(i for i, o in enumerate(ORDER) if o in f))
    for f in files:
        s = open(f, encoding='utf-8').read()
        secs = re.split(r'\n(?=## \d+[a-z]?｜)', s)
        for sec in secs[1:]:
            head, body = sec.split('\n', 1)
            title = re.sub(r'^## \d+[a-z]?｜', '', head).strip()
            short = title.split('｜')[0].strip()
            m = re.search(r'^触发词：(.+)$', body, re.M)
            toks = []
            if m:
                toks = [re.sub(r'（[^）]*）', '', t).strip() for t in m.group(1).split('｜')]
                body = body.replace(m.group(0) + '\n', '', 1).replace(m.group(0), '', 1)
            toks += era['EXTRA'].get(short, []) + era['EXTRA'].get(title, [])
            rm = set(era['REMOVE'].get(short, []) + era['REMOVE'].get(title, []))
            toks = [t for t in toks if t and t not in era['STOP'] and t not in rm and len(t) >= 2]
            seen = []
            for t in toks:
                if t not in seen: seen.append(t)
            if not seen:
                print('!! no keys for', era['tag'], title); sys.exit(1)
            key = '|'.join(rx_escape(t) for t in seen)
            re.compile(key)
            value = '## ' + era['tag'] + '｜' + title + '\n' + body.strip()
            archives.append(entry(era['group'], key, value, 2, 6, next(sorts)))
            keytable.append((title, seen, len(value)))
    era_entries[era['tag']] = (cores, archives, keytable)

# ---------- 装箱 ----------
d = json.load(open(SRC, encoding='utf-8'))
old = d['world_bk']
drop_prefixes = ['00｜全局运行'] + [e['old_prefix'] for e in ERAS]
kept = [e for e in old if not any(e['group'].startswith(p) for p in drop_prefixes)]
removed = len(old) - len(kept)
new_all = list(core_entries)
for era in ERAS:
    cores, archives, _ = era_entries[era['tag']]
    new_all += cores + archives
d['world_bk'] = new_all + kept
d['pre_pt'] = open(os.path.join(B, 'pre_pt.md'), encoding='utf-8').read().strip()
d['ptx'] = open(os.path.join(B, 'ptx.txt'), encoding='utf-8').read().strip()
d['inner_css'] = open(os.path.join(B, 'inner_css.css'), encoding='utf-8').read().strip()
json.dump(d, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)

# ---------- 钥匙表 ----------
lines = [f'# 世界书钥匙表（{VER}）', '',
         f'核心条目 {len(core_entries)} 条；' + '；'.join(
             f"{t}总览与示范 {len(era_entries[t][0])} 条、档案 {len(era_entries[t][1])} 条" for t in era_entries) +
         f'；保留旧条目 {len(kept)} 条（共享资料与其余八个时代，当索引用）；删去旧条目 {removed} 条（旧全局运行、旧匹诺康尼包、旧雅利洛包、旧仙舟包、旧哈托彼亚包）。', '',
         '## 核心运行']
for e in core_entries:
    lines.append(f"- {e['value'].splitlines()[0].lstrip('# ')}｜深度{e['depth']}｜钥匙 `{e['key'][:60]}`｜{len(e['value'])}字")
for tag, (cores, archives, keytable) in era_entries.items():
    lines += ['', f'## {tag}']
    for e in cores:
        lines.append(f"- {e['value'].splitlines()[0].lstrip('# ')}｜深度{e['depth']}｜钥匙 `{e['key'][:80]}`｜{len(e['value'])}字")
    for t, ks, n in keytable:
        lines.append(f"- {t}｜深度2｜钥匙 {'、'.join(ks)}｜{n}字")
open(os.path.join(OUT_DIR, f'世界书钥匙表_{VER}.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

tot = sum(len(e['value']) for e in new_all)
print('core', len(core_entries), {t: (len(c), len(a)) for t, (c, a, _) in era_entries.items()}, 'kept', len(kept), 'removed', removed)
print('new text chars', tot, '| pre_pt', len(d['pre_pt']), '| css', len(d['inner_css']), '| ptx', len(d['ptx']))
print('OUT', OUT, os.path.getsize(OUT))
