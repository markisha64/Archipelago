
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Item, ItemClassification, Region
from .items import ALL_ITEMS_TABLE,DMW2003Item
from .locations import get_location, ALL_LOCATIONS_TABLE
from .rules import items_owned_rule_gen

class DMW2003WebWorld(WebWorld):
    option_groups = []
    rich_text_options_doc = True
    theme = "grass"
    tutorials = []

class DMW2003World(World):
    game = "Digimon World 2003"
    web = DMW2003WebWorld()
    item_name_to_id = {k: v.id for k, v in ALL_ITEMS_TABLE.items()}
    filler_list = [k for k, v in ALL_ITEMS_TABLE.items() if v.classification & ItemClassification.filler != 0]

    topology_present = True

    def create_items(self):
        self.multiworld.itempool += [self.create_item(name) for name in ALL_ITEMS_TABLE.keys()]

    def create_item(self, name: str) -> Item:
        item = ALL_ITEMS_TABLE[name]

        return DMW2003Item(name, item.classification, item.id, self.player)

    def get_filler_item_name(self):
        return self.random.choice(self.filler_list)

    def create_regions(self):
        menu_region = Region("Menu Region", self.player, self.multiworld)

        menu_region.locations.append(get_location("Old Claw". self.player))
        menu_region.locations.append(get_location("TNT Ball", self.player))

        for location_data, location_name in ALL_LOCATIONS_TABLE.items():
            if not location_data.classification & ItemClassification.progression:
                menu_region.locations.append(get_location(location_name))

        items_owned_rule = items_owned_rule_gen(self.player)

        beat_seiryu = Region("Beat Seiryu Leader", self.player, self.multiworld)
        beat_seiryu.connect(menu_region, "Old Claw", items_owned_rule(["Old Claw"]))
        beat_seiryu.locations.append(get_location("Seiryu Badge"))

        get_fake_blue_card = Region("Get Fake Blue Card", self.player)
        get_fake_blue_card.connect(beat_seiryu, "Seiryu Badge", items_owned_rule(["Seiryu Badge"]))
        get_fake_blue_card.locations.append(get_location("8lue Card"))
        
        get_blue_card = Region("Get Blue Card", self.player)
        get_blue_card.connect(get_fake_blue_card, "8lue Card", items_owned_rule(["8lue Card"]))
        get_blue_card.locations.append(get_location("Blue Card"))

        get_sepik_mask = Region("Get Sepik Mask", self.player)
        get_sepik_mask.connect(get_blue_card, "Blue Card", items_owned_rule(["Blue Card"]))
        get_sepik_mask.locations.append(get_location("Sepik Mask"))
        
        get_smelly_herb = Region("Get Smelly Herb", self.player)
        get_smelly_herb.connect(get_blue_card, "Sepik Mask", items_owned_rule(["Sepik Mask"]))
        get_smelly_herb.locations.append(get_location("Smelly Herb"))
        
        beat_suzaku = Region("Beat Suzaku Leader", self.player)
        beat_suzaku.connect(get_smelly_herb, "Smelly Herb", items_owned_rule(["Smelly Herb"]))
        beat_suzaku.locations.append(get_location("Suzaku Badge"))
        
        get_agumon_suit = Region("Get Agumon Suit", self.player)
        get_agumon_suit.connect(beat_suzaku, "Suzaku Badge", items_owned_rule(["Suzaku Badge"]))
        get_agumon_suit.locations.append(get_location("Agumon Suit"))

        get_tnt_chip = Region("Get TNT Chip", self.player)
        get_tnt_chip.connect(beat_suzaku, "TNT Ball", items_owned_rule(["TNT Ball", "Agumon Suit"]))
        get_tnt_chip.locations.append(get_location("TNT Chip"))

        get_digiegg_sincerity = Region("Get Digiegg Sincerity", self.player)
        get_digiegg_sincerity.connect(get_tnt_chip, "TNT Chip", items_owned_rule(["TNT Chip"]))
        get_digiegg_sincerity.locations.append(get_location("DE Sincerity"))
        
        beat_datamon = Region("Beat Datamon", self.player)
        beat_datamon.connect(get_digiegg_sincerity, "DE Sincerity", items_owned_rule(["DE Sincerity"]))
        beat_datamon.locations.append(get_location("Rusty Glove"))

        beat_byakko_leader = Region("Beat Byakko Leader", self.player)
        beat_byakko_leader.connect(get_digiegg_sincerity, "DE Sincerity", items_owned_rule(["DE Sincerity"]))
        beat_byakko_leader.locations.append(get_location("Byakko Badge"))
        
        beat_hiandromon = Region("Beat Hi-Andromon", self.player)
        beat_hiandromon.connect(get_digiegg_sincerity, "Byakko Badge", items_owned_rule(["Byakko Badge"]))
        beat_hiandromon.locations.append(get_location("Rusty Rifle"))
        
        get_staff_pass = Region("Get Staff Pass", self.player, "You need to talk to Datamon again :)")
        get_staff_pass.connect(beat_hiandromon, "Beat Hi-Andromon & Datamon", items_owned_rule(["Rusty Rifle", "Rusty Glove"]))
        get_staff_pass.locations.append(get_location("Staff Pass"))
       
        beat_qing_long = Region("Beat Qing Long Chief", self.player)
        beat_qing_long.connect(get_staff_pass, "Staff Pass", items_owned_rule(["Staff Pass"]))
        beat_qing_long.locations.append(get_location("Blue ID Pass"))
        
        beat_zhu_que = Region("Beat Zhu Que Chief", self.player)
        beat_zhu_que.connect(beat_qing_long, "Blue ID Pass", items_owned_rule(["Blue ID Pass"]))
        beat_zhu_que.locations.append(get_location("Red ID Pass"))

        get_digiegg_knowledge = Region("Get Digiegg Knowledge", self.player)
        get_digiegg_knowledge.connect(beat_zhu_que, "Red ID Pass", items_owned_rule(["Red ID Pass"]))
        get_digiegg_knowledge.locations.append(get_location("DE Knowledge"))
        
        beat_genbu = Region("Beat Genbu Leader", self.player)
        beat_genbu.connect(get_digiegg_knowledge, "DE Knowledge", items_owned_rule(["DE Knowledge"]))
        beat_genbu.locations.append(get_location("Genbu Badge"))

        beat_bai_hu = Region("Beat Bai Hu Chief", self.player)
        beat_bai_hu.connect(beat_genbu, "Genbu Badge", items_owned_rule(["Genbu Badge"]))
        beat_bai_hu.locations.append(get_location("Red ID Pass"))
        
        beat_xuen_wu = Region("Beat Xuen Wu Chief", self.player)
        beat_xuen_wu.connect(beat_genbu, "Red ID Pass", items_owned_rule(["Red ID Pass"]))
        beat_xuen_wu.locations.append(get_location("Black ID Pass"))
        
        self.multiworld.regions += [
            menu_region,
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
        ]
        
    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Black ID Pass", self.player)
