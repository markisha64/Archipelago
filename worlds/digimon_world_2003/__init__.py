
from typing import Dict
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Item, ItemClassification, Region
from .items import ALL_ITEMS_TABLE,DMW2003Item
from .locations import get_location, ALL_LOCATIONS_TABLE, ALL_LOCATIONS_BY_ID 
from .rules import items_owned_rule_gen
from .client import DMW2003Client
from .options import DMW2003Options

class DMW2003WebWorld(WebWorld):
    option_groups = []
    rich_text_options_doc = True
    theme = "grass"
    tutorials = []

class DMW2003World(World):
    origin_region_name = "Beat Master Tyrannomon"
    game = "Digimon World 2003"
    web = DMW2003WebWorld()
    item_name_to_id = {k: v.id for k, v in ALL_ITEMS_TABLE.items()}
    location_name_to_id = {k: v.id for k, v in ALL_LOCATIONS_TABLE.items()}
    filler_list = [k for k, v in ALL_ITEMS_TABLE.items() if v.classification & ItemClassification.filler != 0]
    region_cache: Dict[int, Region] = {}

    options = DMW2003Options
    options_dataclass = DMW2003Options

    topology_present = True

    def create_items(self):
        self.multiworld.itempool += [self.create_item(name) for name in ALL_ITEMS_TABLE.keys()]

    def create_item(self, name: str) -> Item:
        item = ALL_ITEMS_TABLE[name]

        return DMW2003Item(name, item.classification, item.id, self.player)

    def get_filler_item_name(self):
        return self.random.choice(self.filler_list)

    def get_location_region(self, name: str) -> Region:
        location = ALL_LOCATIONS_TABLE[name]

        if location.id in self.region_cache:
            return self.region_cache[location.id]

        region = Region(name, self.player, self.multiworld)
        region.locations.append(get_location(name, self.player, region))        
        self.region_cache[location.id] = region
        
        return region

    def get_location_region_by_id(self, id: int) -> Region:
        if id in self.region_cache:
            return self.region_cache[id]
        
        name, location = ALL_LOCATIONS_BY_ID[id]

        region = Region(name, self.player, self.multiworld)
        region.locations.append(get_location(name, self.player, region))        
        self.region_cache[id] = region
        
        return region
    
    def create_regions(self):
        # item_boxes = self.options.item_boxes.merged()
        shops = self.options.shops.merged()
        
        beat_mt = Region("Beat Master Tyrannomon", self.player, self.multiworld)

        beat_mt.locations.append(get_location("Old Claw", self.player, beat_mt))
        beat_mt.connect(self.get_location_region("TNT Ball"))

        already_got = set([90])
        for shop_idx in range(0, 7):
            for item in set(shops[shop_idx]).difference(already_got):
                beat_mt.connect(self.get_location_region_by_id(item))

            already_got = already_got.union(shops[shop_idx])

        items_owned_rule = items_owned_rule_gen(self.player)

        beat_seiryu = Region("Beat Seiryu Leader", self.player, self.multiworld)
        beat_mt.connect(beat_seiryu, "Old Claw", items_owned_rule(["Old Claw"]))
        beat_seiryu.locations.append(get_location("Seiryu Badge", self.player, beat_seiryu ))

        get_fake_blue_card = Region("Get Fake Blue Card", self.player, self.multiworld)
        beat_seiryu.connect(get_fake_blue_card, "Seiryu Badge", items_owned_rule(["Seiryu Badge"]))
        get_fake_blue_card.locations.append(get_location("8lue Card", self.player, get_fake_blue_card ))

        get_blue_card = Region("Get Blue Card", self.player, self.multiworld)
        get_fake_blue_card.connect(get_blue_card, "8lue Card", items_owned_rule(["8lue Card"]))
        get_blue_card.locations.append(get_location("Blue Card", self.player, get_blue_card ))

        get_sepik_mask = Region("Get Sepik Mask", self.player, self.multiworld)
        get_blue_card.connect(get_sepik_mask, "Blue Card", items_owned_rule(["Blue Card"]))
        get_sepik_mask.locations.append(get_location("Sepik Mask", self.player, get_sepik_mask ))

        get_smelly_herb = Region("Get Smelly Herb", self.player, self.multiworld)
        get_blue_card.connect(get_smelly_herb, "Sepik Mask", items_owned_rule(["Sepik Mask"]))
        get_smelly_herb.locations.append(get_location("Smelly Herb", self.player, get_smelly_herb ))

        beat_suzaku = Region("Beat Suzaku Leader", self.player, self.multiworld)
        get_smelly_herb.connect(beat_suzaku, "Smelly Herb", items_owned_rule(["Smelly Herb"]))

        already_got = set()
        for shop_idx in [7, 8, 9]:
            for item in set(shops[shop_idx]).difference(already_got):
                beat_suzaku.connect(self.get_location_region_by_id(item))

            already_got = already_got.union(shops[shop_idx])

        beat_suzaku.locations.append(get_location("Suzaku Badge", self.player, beat_suzaku ))

        get_agumon_suit = Region("Get Agumon Suit", self.player, self.multiworld)
        beat_suzaku.connect(get_agumon_suit, "Suzaku Badge", items_owned_rule(["Suzaku Badge"]))
        get_agumon_suit.locations.append(get_location("Agumon Suit", self.player, get_agumon_suit ))

        get_tnt_chip = Region("Get TNT Chip", self.player, self.multiworld)
        beat_suzaku.connect(get_tnt_chip, "TNT Ball", items_owned_rule(["TNT Ball", "Agumon Suit"]))
        get_tnt_chip.locations.append(get_location("TNT Chip", self.player, get_tnt_chip ))

        get_digiegg_sincerity = Region("Get Digiegg Sincerity", self.player, self.multiworld)
        get_tnt_chip.connect(get_digiegg_sincerity, "TNT Chip", items_owned_rule(["TNT Chip"]))
        get_digiegg_sincerity.locations.append(get_location("DE Sincerity", self.player, get_digiegg_sincerity ))

        beat_datamon = Region("Beat Datamon", self.player, self.multiworld)
        get_digiegg_sincerity.connect(beat_datamon, "DE Sincerity", items_owned_rule(["DE Sincerity"]))
        beat_datamon.locations.append(get_location("Rusty Glove", self.player, beat_datamon ))

        beat_byakko_leader = Region("Beat Byakko Leader", self.player, self.multiworld)
        get_digiegg_sincerity.connect(beat_byakko_leader, "DE Sincerity ", items_owned_rule(["DE Sincerity"]))

        for item in shops[10]:
            beat_byakko_leader.connect(self.get_location_region_by_id(item))

        beat_byakko_leader.locations.append(get_location("Byakko Badge", self.player, beat_byakko_leader ))

        beat_hiandromon = Region("Beat Hi-Andromon", self.player, self.multiworld)
        beat_byakko_leader.connect(beat_hiandromon, "Byakko Badge", items_owned_rule(["Byakko Badge"]))
        beat_hiandromon.locations.append(get_location("Rusty Rifle", self.player, beat_hiandromon ))

        get_staff_pass = Region("Get Staff Pass", self.player, self.multiworld)
        beat_hiandromon.connect(get_staff_pass, "Beat Hi-Andromon & Datamon", items_owned_rule(["Rusty Rifle", "Rusty Glove"]))
        get_staff_pass.locations.append(get_location("Staff Pass", self.player, get_staff_pass ))

        beat_qing_long = Region("Beat Qing Long Chief", self.player, self.multiworld)
        get_staff_pass.connect(beat_qing_long, "Staff Pass", items_owned_rule(["Staff Pass"]))

        already_got = set()
        for shop_idx in [11, 12, 20, 21]:
            for item in set(shops[shop_idx]).difference(already_got):
                beat_qing_long.connect(self.get_location_region_by_id(item))

            already_got = already_got.union(shops[shop_idx])


        beat_qing_long.locations.append(get_location("Blue ID Pass", self.player, beat_qing_long ))

        beat_zhu_que = Region("Beat Zhu Que Chief", self.player, self.multiworld)
        beat_qing_long.connect(beat_zhu_que, "Blue ID Pass", items_owned_rule(["Blue ID Pass"]))

        already_got = set()
        for shop_idx in [22, 23, 24]:
            for item in set(shops[shop_idx]).difference(already_got):
                beat_zhu_que.connect(self.get_location_region_by_id(item))

            already_got = already_got.union(shops[shop_idx])

        beat_zhu_que.locations.append(get_location("Red ID Pass", self.player, beat_zhu_que ))

        get_digiegg_knowledge = Region("Get Digiegg Knowledge", self.player, self.multiworld)
        beat_zhu_que.connect(get_digiegg_knowledge, "Red ID Pass", items_owned_rule(["Red ID Pass"]))
        get_digiegg_knowledge.locations.append(get_location("DE Knowledge", self.player, get_digiegg_knowledge ))

        beat_genbu = Region("Beat Genbu Leader", self.player, self.multiworld)
        get_digiegg_knowledge.connect(beat_genbu, "DE Knowledge", items_owned_rule(["DE Knowledge"]))

        already_got = set()
        for shop_idx in [13, 14, 25]:
            for item in set(shops[shop_idx]).difference(already_got):
                beat_genbu.connect(self.get_location_region_by_id(item))

            already_got = already_got.union(shops[shop_idx])

        beat_genbu.locations.append(get_location("Genbu Badge", self.player, beat_genbu ))

        beat_bai_hu = Region("Beat Bai Hu Chief", self.player, self.multiworld)
        beat_genbu.connect(beat_bai_hu, "Genbu Badge", items_owned_rule(["Genbu Badge"]))

        already_got = set()
        for shop_idx in [26, 27]:
            for item in set(shops[shop_idx]).difference(already_got):
                beat_bai_hu.connect(self.get_location_region_by_id(item))

            already_got = already_got.union(shops[shop_idx])
        
        beat_bai_hu.locations.append(get_location("White ID Pass", self.player, beat_bai_hu ))

        beat_xuen_wu = Region("Beat Xuen Wu Chief", self.player, self.multiworld)
        beat_bai_hu.connect(beat_xuen_wu, "White ID Pass", items_owned_rule(["White ID Pass"]))

        already_got = set()
        for shop_idx in [28, 29]:
            for item in set(shops[shop_idx]).difference(already_got):
                beat_xuen_wu.connect(self.get_location_region_by_id(item))

            already_got = already_got.union(shops[shop_idx])
        
        beat_xuen_wu.locations.append(get_location("Black ID Pass", self.player, beat_xuen_wu ))

        beat_galacticmon = Region("Beat Galacticmon", self.player, self.multiworld) 
        beat_xuen_wu.connect(beat_galacticmon, "Black ID Pass", items_owned_rule(["Black ID Pass"]))

        already_got = set()
        for shop_idx in [15, 16, 17, 18, 19]:
            for item in set(shops[shop_idx]).difference(already_got):
                beat_galacticmon.connect(self.get_location_region_by_id(item))

            already_got = already_got.union(shops[shop_idx])
        
        self.region_cache.clear()
        
        self.multiworld.regions += [
            beat_mt,
            beat_seiryu,
            get_fake_blue_card,
            get_blue_card,
            get_sepik_mask,
            get_smelly_herb,
            beat_suzaku,
            get_agumon_suit,
            get_tnt_chip,
            get_digiegg_sincerity,
            beat_datamon,
            beat_byakko_leader,
            beat_hiandromon,
            get_staff_pass,
            beat_qing_long,
            beat_zhu_que,
            get_digiegg_knowledge,
            beat_genbu,
            beat_bai_hu,
            beat_xuen_wu,
            beat_galacticmon
        ]
        
    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Black ID Pass", self.player)
